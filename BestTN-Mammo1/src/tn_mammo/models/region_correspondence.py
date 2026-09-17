import math
import torch
import torch.nn as nn
import torch.nn.functional as F

LEFT_VIEWS = {"L_CC", "L_MLO"}
VIEW_KEYS = ("L_CC", "L_MLO", "R_CC", "R_MLO")
VIEW_INDEX = {"L_CC": 0, "L_MLO": 1, "R_CC": 2, "R_MLO": 3}

def maybe_reduce_spatial_size(fmap, mask, max_tokens):
    B, C, H, W = fmap.shape
    if H * W <= max_tokens:
        return fmap, mask
        
    target_h = 16
    target_w = 16
    assert target_h * target_w <= max_tokens
    
    fmap = F.adaptive_avg_pool2d(fmap, output_size=(target_h, target_w))
    
    if mask is not None:
        mask = F.interpolate(mask.float(), size=(target_h, target_w), mode="nearest").bool()
        
    return fmap, mask

def make_xy_grid(H, W, device):
    ys = torch.linspace(0, 1, H, device=device)
    xs = torch.linspace(0, 1, W, device=device)
    yy, xx = torch.meshgrid(ys, xs, indexing="ij")
    xy = torch.stack([xx, yy], dim=-1)
    return xy.reshape(H * W, 2)

def canonicalize_xy(xy, view_name):
    # This assumes images are NOT flipped during preprocessing to canonical orientation
    # We must flip the X coordinate for left views so left/right match anatomically.
    xy = xy.clone()
    if view_name in LEFT_VIEWS:
        xy[:, 0] = 1.0 - xy[:, 0]
    return xy

class RegionTokenizer(nn.Module):
    def __init__(self, in_channels: int, region_dim: int = 256, max_tokens: int = 256, use_positional_encoding: bool = True):
        super().__init__()
        self.in_channels = in_channels
        self.region_dim = region_dim
        self.max_tokens = max_tokens
        
        self.proj = nn.Conv2d(in_channels, region_dim, kernel_size=1, bias=False)
        self.norm = nn.LayerNorm(region_dim)
        self.use_positional_encoding = use_positional_encoding
        
        if use_positional_encoding:
            self.pos_proj = nn.Linear(2, region_dim, bias=False)
            
    def forward(self, fmap, spatial_mask=None, view_name=None):
        fmap, spatial_mask = maybe_reduce_spatial_size(fmap, spatial_mask, self.max_tokens)
        x = self.proj(fmap)
        
        B, D, H, W = x.shape
        tokens = x.flatten(2).transpose(1, 2)
        tokens = self.norm(tokens)
        
        if self.use_positional_encoding:
            xy = make_xy_grid(H, W, tokens.device)
            xy = canonicalize_xy(xy, view_name)
            pos = self.pos_proj(xy)
            tokens = tokens + pos.unsqueeze(0)
            
        if spatial_mask is None:
            token_valid = torch.ones(B, H * W, dtype=torch.bool, device=tokens.device)
        else:
            token_valid = spatial_mask.flatten(1).bool()
            
        return tokens, token_valid

def make_safe_key_padding_mask(source_valid):
    kpm = ~source_valid
    all_masked = kpm.all(dim=1)
    safe_kpm = kpm.clone()
    if all_masked.any():
        safe_kpm[all_masked, 0] = False
    return safe_kpm, all_masked

class RegionCrossAttention(nn.Module):
    def __init__(self, region_dim=256, num_heads=8, dropout=0.0):
        super().__init__()
        assert region_dim % num_heads == 0
        self.attn = nn.MultiheadAttention(embed_dim=region_dim, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.norm = nn.LayerNorm(region_dim)
        
    def forward(self, query_tokens, source_tokens, query_valid, source_valid, relation_valid, need_weights=False):
        key_padding_mask, all_source_masked = make_safe_key_padding_mask(source_valid)
        
        context, weights = self.attn(
            query=query_tokens,
            key=source_tokens,
            value=source_tokens,
            key_padding_mask=key_padding_mask,
            need_weights=need_weights,
            average_attn_weights=False if need_weights else True,
        )
        
        context = context * query_valid.unsqueeze(-1)
        valid = relation_valid & (~all_source_masked)
        context = context * valid[:, None, None]
        context = self.norm(context)
        context = context * valid[:, None, None]
        
        return context, weights

class RegionContextAggregator(nn.Module):
    def __init__(self, region_dim, output_dim):
        super().__init__()
        self.out_proj = nn.Linear(region_dim, output_dim, bias=False)
        self.norm = nn.LayerNorm(output_dim)
        
    def forward(self, context_tokens, query_valid, relation_valid):
        weights = query_valid.float()
        denom = weights.sum(dim=1, keepdim=True).clamp_min(1.0)
        
        pooled = (context_tokens * weights.unsqueeze(-1)).sum(dim=1) / denom
        region_context = self.out_proj(pooled)
        region_context = self.norm(region_context)
        region_context = region_context * relation_valid[:, None]
        
        return region_context

class RegionGatedUpdate(nn.Module):
    def __init__(self, feature_dim, alpha_init=0.0):
        super().__init__()
        self.gate = nn.Sequential(
            nn.Linear(feature_dim * 2, feature_dim),
            nn.Sigmoid(),
        )
        self.alpha = nn.Parameter(torch.tensor(float(alpha_init)))
        
    def forward(self, original_feature, region_context, relation_valid):
        gate = self.gate(torch.cat([original_feature, region_context], dim=-1))
        delta = self.alpha * gate * region_context
        delta = delta * relation_valid[:, None]
        updated = original_feature + delta
        return updated, gate

def relation_valid(view_mask, target_view, source_view):
    if view_mask is None:
        # fallback if view_mask is not provided, though it's a hard requirement usually
        # To handle view_mask being completely omitted
        return None
    target_valid = view_mask[:, VIEW_INDEX[target_view]]
    source_valid = view_mask[:, VIEW_INDEX[source_view]]
    return target_valid & source_valid

class CrossViewRegionModule(nn.Module):
    def __init__(self, in_channels: int, backbone_feature_dim: int, region_dim=256, max_tokens=256, num_heads=8, enabled=False, contralateral=True, ipsilateral=False, alpha_init=0.0):
        super().__init__()
        self.enabled = enabled
        self.contralateral = contralateral
        self.ipsilateral = ipsilateral
        
        if not enabled:
            return
            
        self.tokenizer = RegionTokenizer(in_channels=in_channels, region_dim=region_dim, max_tokens=max_tokens)
        
        self.cc_attn = RegionCrossAttention(region_dim, num_heads)
        self.mlo_attn = RegionCrossAttention(region_dim, num_heads)
        
        self.aggregator = RegionContextAggregator(region_dim, backbone_feature_dim)
        self.updater = RegionGatedUpdate(backbone_feature_dim, alpha_init=alpha_init)
        
    def _update_one_direction(self, target_view, source_view, attn_module, tokens, token_valid, global_features, view_mask, return_attention):
        rel_valid = relation_valid(view_mask, target_view, source_view)
        if rel_valid is None:
            # fallback: all true
            rel_valid = torch.ones(global_features[target_view].shape[0], dtype=torch.bool, device=global_features[target_view].device)
            
        context_tokens, attn_weights = attn_module(
            query_tokens=tokens[target_view],
            source_tokens=tokens[source_view],
            query_valid=token_valid[target_view],
            source_valid=token_valid[source_view],
            relation_valid=rel_valid,
            need_weights=return_attention,
        )
        
        region_context = self.aggregator(context_tokens, token_valid[target_view], rel_valid)
        updated, gate = self.updater(global_features[target_view], region_context, rel_valid)
        
        return updated, gate, attn_weights

    def forward(self, feature_maps, global_features, spatial_masks, view_mask, return_attention=False):
        if not self.enabled:
            return global_features, {"region_enabled": False}
            
        tokens = {}
        token_valid = {}
        for view in VIEW_KEYS:
            s_mask = spatial_masks.get(view) if spatial_masks else None
            tokens[view], token_valid[view] = self.tokenizer(feature_maps[view], s_mask, view_name=view)
            
        updated = dict(global_features)
        gate_means = {}
        attention = {}
        
        if self.contralateral:
            for tgt, src, attn_mod in [
                ("L_CC", "R_CC", self.cc_attn),
                ("R_CC", "L_CC", self.cc_attn),
                ("L_MLO", "R_MLO", self.mlo_attn),
                ("R_MLO", "L_MLO", self.mlo_attn),
            ]:
                upd, gate, a_w = self._update_one_direction(tgt, src, attn_mod, tokens, token_valid, global_features, view_mask, return_attention)
                updated[tgt] = upd
                gate_means[f"gate_mean_{tgt}"] = gate.mean()
                if return_attention:
                    attention[f"{tgt}_{src}"] = a_w
                    
        aux = {
            "region_enabled": True,
            "alpha": self.updater.alpha.detach(),
        }
        for k, v in gate_means.items():
            aux[k] = v
            
        if return_attention:
            aux["attention"] = attention
            
        return updated, aux
