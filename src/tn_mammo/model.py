"""Architecture matching the original hierarchical relational fusion diagram."""
import math

import torch
from torch import nn
from torch.nn import functional as F
from torchvision.models import (convnext_tiny, ConvNeXt_Tiny_Weights,
                                densenet121, DenseNet121_Weights)


RELATIONAL_ARCHITECTURE = "densenet121_hierarchical_bilateral_multitask_v1"
ATTENTION_ARCHITECTURE = "densenet121_view_token_attention_multitask_v2"
SPATIAL_ATTENTION_ARCHITECTURE = "densenet121_spatial_view_attention_multitask_v3"
ORDINAL_PRIMARY_ARCHITECTURE = "densenet121_hierarchical_bilateral_ordinalprimary_v4"
ORDINAL_PRIMARY_WIDE_ARCHITECTURE = "densenet121_hierarchical_bilateral_ordinalprimary_wide_v5"
CONVNEXT_RELATIONAL_ARCHITECTURE = "convnext_tiny_hierarchical_bilateral_multitask_v6"
CONVNEXT_HYBRID_SPATIAL_ARCHITECTURE = "convnext_tiny_hybrid_relational_spatial_multitask_v7"
CONVNEXT_HYBRID_A_GATE_ARCHITECTURE = "convnext_tiny_hybrid_spatial_a_gate_multitask_v8"
CONVNEXT_MULTISCALE_ARCHITECTURE = "convnext_tiny_multiscale_view_transformer_multitask_v9"
CONVNEXT_MULTISCALE_A_GATE_ARCHITECTURE = "convnext_tiny_multiscale_view_transformer_a_gate_v10"
CONVNEXT_LOCAL_GLOBAL_A_GATE_ARCHITECTURE = "convnext_tiny_local_global_view_transformer_a_gate_v11"
CONVNEXT_LOCAL_GLOBAL_PERVIEW_AUX_ARCHITECTURE = "convnext_tiny_local_global_view_transformer_perview_aux_v12"
CONVNEXT_LOCAL_GLOBAL_PERVIEW_AUX_MIXSTYLE_ARCHITECTURE = "convnext_tiny_local_global_view_transformer_perview_aux_mixstyle_v13"
CONVNEXT_DUAL_ENDPOINT_GATE_ARCHITECTURE = "convnext_tiny_hybrid_spatial_dual_endpoint_gate_multitask_v14"
CONVNEXT_FINE_D_EXPERT_ARCHITECTURE = "convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_v15"
CONVNEXT_RNG_ISOLATED_FINE_D_EXPERT_ARCHITECTURE = "convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_rngisolated_v16"


class ExamMixStyle(nn.Module):
    """Mix feature statistics between exams while preserving four-view identity."""

    def __init__(self, probability=0.0, alpha=0.1, eps=1e-6):
        super().__init__()
        if (isinstance(probability, bool)
                or not isinstance(probability, (int, float))
                or not math.isfinite(float(probability))
                or not 0 <= float(probability) <= 1):
            raise ValueError("mixstyle_probability must be finite and in [0,1]")
        if (isinstance(alpha, bool) or not isinstance(alpha, (int, float))
                or not math.isfinite(float(alpha)) or float(alpha) <= 0):
            raise ValueError("mixstyle_alpha must be finite and positive")
        self.probability = float(probability)
        self.alpha = float(alpha)
        self.eps = float(eps)

    def forward(self, feature_maps):
        if feature_maps.ndim != 5 or feature_maps.shape[1] != 4:
            raise ValueError("ExamMixStyle expects [B,4,C,H,W]")
        batch = feature_maps.shape[0]
        if (not self.training or self.probability == 0 or batch < 2
                or torch.rand((), device=feature_maps.device) >= self.probability):
            return feature_maps

        # Compute style statistics in float32 for stable AMP behavior. They are
        # detached so MixStyle changes acquisition style without providing a
        # shortcut through another exam's statistics.
        working = feature_maps.float()
        mean = working.mean(dim=(-2, -1), keepdim=True)
        variance = working.var(dim=(-2, -1), keepdim=True, unbiased=False)
        std = (variance + self.eps).sqrt()
        normalized = (working - mean) / std
        mean, std = mean.detach(), std.detach()

        # A non-zero cyclic shift guarantees a different paired exam, including
        # the batch-size-two production setting. Canonical views stay aligned.
        if batch == 2:
            shift = 1
        else:
            shift = int(torch.randint(1, batch, (), device=feature_maps.device))
        paired_mean = mean.roll(shifts=shift, dims=0)
        paired_std = std.roll(shifts=shift, dims=0)
        concentration = torch.full(
            (batch,), self.alpha, device=feature_maps.device, dtype=torch.float32
        )
        mixing = torch.distributions.Beta(concentration, concentration).sample()
        mixing = mixing.reshape(batch, 1, 1, 1, 1)
        mixed_mean = mixing * mean + (1 - mixing) * paired_mean
        mixed_std = mixing * std + (1 - mixing) * paired_std
        return (normalized * mixed_std + mixed_mean).to(feature_maps.dtype)


class PairFusion(nn.Module):
    def __init__(self, dim=1024, dropout=0.1):
        super().__init__()
        self.gate = nn.Linear(dim, 1)
        self.relation = nn.Sequential(nn.Linear(dim * 3, dim), nn.GELU(), nn.Dropout(dropout))
        self.norm = nn.LayerNorm(dim)

    def forward(self, cc, mlo):
        pair = torch.stack((cc, mlo), dim=1)
        weights = self.gate(pair).softmax(dim=1)
        pooled = (pair * weights).sum(dim=1)
        relation = torch.cat((pooled, (cc - mlo).abs(), cc * mlo), dim=1)
        return self.norm(pooled + self.relation(relation))


class ViewTokenAttentionFusion(nn.Module):
    """Fuse four view vectors using explicit view/laterality-aware tokens."""

    def __init__(self, input_dim=1024, token_dim=256, heads=8, layers=2,
                 attention_dropout=0.1, output_dropout=0.1):
        super().__init__()
        if token_dim <= 0 or heads <= 0 or layers <= 0 or token_dim % heads:
            raise ValueError("Attention dimensions/layers must be positive and divisible")
        if not 0 <= attention_dropout < 1:
            raise ValueError("attention_dropout must be in [0,1)")
        self.token_projection = nn.Sequential(
            nn.Linear(input_dim, token_dim), nn.GELU(), nn.LayerNorm(token_dim)
        )
        # Factorized embeddings express CC/MLO and left/right identity without
        # treating the four canonical views as unrelated positions.
        self.view_type_embedding = nn.Parameter(torch.empty(2, token_dim))
        self.laterality_embedding = nn.Parameter(torch.empty(2, token_dim))
        self.exam_token = nn.Parameter(torch.empty(1, 1, token_dim))
        layer = nn.TransformerEncoderLayer(
            d_model=token_dim, nhead=heads, dim_feedforward=token_dim * 4,
            dropout=attention_dropout, activation="gelu", batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(
            layer, num_layers=layers, norm=nn.LayerNorm(token_dim)
        )
        self.to_exam = nn.Sequential(
            nn.Linear(token_dim, input_dim), nn.GELU(), nn.Dropout(output_dropout)
        )
        nn.init.trunc_normal_(self.view_type_embedding, std=0.02)
        nn.init.trunc_normal_(self.laterality_embedding, std=0.02)
        nn.init.trunc_normal_(self.exam_token, std=0.02)

    def forward(self, features):
        if features.ndim != 3 or features.shape[1:] != (4, 1024):
            raise ValueError("Expected four 1024-dimensional view vectors")
        tokens = self.token_projection(features)
        view_type = torch.tensor([0, 1, 0, 1], device=features.device)
        laterality = torch.tensor([0, 0, 1, 1], device=features.device)
        tokens = (tokens + self.view_type_embedding[view_type]
                  + self.laterality_embedding[laterality])
        exam = self.exam_token.expand(features.shape[0], -1, -1)
        encoded = self.encoder(torch.cat((exam, tokens), dim=1))
        return self.to_exam(encoded[:, 0])


class SpatialTokenAttentionFusion(nn.Module):
    """Fuse a small spatial grid from every view without global pooling first."""

    def __init__(self, input_dim=1024, token_dim=256, heads=8, layers=2,
                 grid_size=4, attention_dropout=0.1, output_dropout=0.1):
        super().__init__()
        if token_dim <= 0 or heads <= 0 or layers <= 0 or token_dim % heads:
            raise ValueError("Attention dimensions/layers must be positive and divisible")
        if not isinstance(grid_size, int) or grid_size <= 0:
            raise ValueError("grid_size must be a positive integer")
        if not 0 <= attention_dropout < 1:
            raise ValueError("attention_dropout must be in [0,1)")
        self.input_dim = input_dim
        self.grid_size = grid_size
        self.token_projection = nn.Sequential(
            nn.Linear(input_dim, token_dim), nn.GELU(), nn.LayerNorm(token_dim)
        )
        self.view_type_embedding = nn.Parameter(torch.empty(2, token_dim))
        self.laterality_embedding = nn.Parameter(torch.empty(2, token_dim))
        self.spatial_embedding = nn.Parameter(torch.empty(grid_size * grid_size, token_dim))
        self.exam_token = nn.Parameter(torch.empty(1, 1, token_dim))
        layer = nn.TransformerEncoderLayer(
            d_model=token_dim, nhead=heads, dim_feedforward=token_dim * 4,
            dropout=attention_dropout, activation="gelu", batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(
            layer, num_layers=layers, norm=nn.LayerNorm(token_dim)
        )
        self.to_exam = nn.Sequential(
            nn.Linear(token_dim, input_dim), nn.GELU(), nn.Dropout(output_dropout)
        )
        for parameter in (self.view_type_embedding, self.laterality_embedding,
                          self.spatial_embedding, self.exam_token):
            nn.init.trunc_normal_(parameter, std=0.02)

    def forward(self, feature_maps):
        if (feature_maps.ndim != 5 or feature_maps.shape[1] != 4
                or feature_maps.shape[2] != self.input_dim):
            raise ValueError(f"Expected four {self.input_dim}-channel feature maps")
        batch = feature_maps.shape[0]
        pooled = F.adaptive_avg_pool2d(
            feature_maps.flatten(0, 1), self.grid_size
        ).reshape(batch, 4, self.input_dim, self.grid_size * self.grid_size)
        tokens = self.token_projection(pooled.permute(0, 1, 3, 2))
        view_type = torch.tensor([0, 1, 0, 1], device=feature_maps.device)
        laterality = torch.tensor([0, 0, 1, 1], device=feature_maps.device)
        tokens = (tokens + self.view_type_embedding[view_type][None, :, None, :]
                  + self.laterality_embedding[laterality][None, :, None, :]
                  + self.spatial_embedding[None, None, :, :])
        tokens = tokens.flatten(1, 2)
        exam = self.exam_token.expand(batch, -1, -1)
        encoded = self.encoder(torch.cat((exam, tokens), dim=1))
        return self.to_exam(encoded[:, 0])


class MultiScaleViewTokenFusion(nn.Module):
    """Replace handcrafted pair fusion with learned multi-scale four-view fusion."""

    def __init__(self, fine_dim=384, coarse_dim=768, token_dim=256, heads=8,
                 layers=2, fine_grid_size=4, coarse_grid_size=2,
                 attention_dropout=0.1, output_dropout=0.1):
        super().__init__()
        if token_dim <= 0 or heads <= 0 or layers <= 0 or token_dim % heads:
            raise ValueError("Attention dimensions/layers must be positive and divisible")
        if (not isinstance(fine_grid_size, int) or fine_grid_size <= 0
                or not isinstance(coarse_grid_size, int) or coarse_grid_size <= 0):
            raise ValueError("Multi-scale grid sizes must be positive integers")
        if not 0 <= attention_dropout < 1:
            raise ValueError("attention_dropout must be in [0,1)")
        self.fine_dim = fine_dim
        self.coarse_dim = coarse_dim
        self.fine_grid_size = fine_grid_size
        self.coarse_grid_size = coarse_grid_size
        self.fine_projection = nn.Conv2d(fine_dim, token_dim, kernel_size=1)
        self.coarse_projection = nn.Conv2d(coarse_dim, token_dim, kernel_size=1)
        self.view_type_embedding = nn.Parameter(torch.empty(2, token_dim))
        self.laterality_embedding = nn.Parameter(torch.empty(2, token_dim))
        self.scale_embedding = nn.Parameter(torch.empty(2, token_dim))
        self.fine_spatial_embedding = nn.Parameter(
            torch.empty(fine_grid_size * fine_grid_size, token_dim)
        )
        self.coarse_spatial_embedding = nn.Parameter(
            torch.empty(coarse_grid_size * coarse_grid_size, token_dim)
        )
        self.exam_token = nn.Parameter(torch.empty(1, 1, token_dim))
        layer = nn.TransformerEncoderLayer(
            d_model=token_dim, nhead=heads, dim_feedforward=token_dim * 4,
            dropout=attention_dropout, activation="gelu", batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(
            layer, num_layers=layers, norm=nn.LayerNorm(token_dim)
        )
        self.to_exam = nn.Sequential(
            nn.Linear(token_dim, coarse_dim), nn.GELU(), nn.Dropout(output_dropout)
        )
        for parameter in (self.view_type_embedding, self.laterality_embedding,
                          self.scale_embedding, self.fine_spatial_embedding,
                          self.coarse_spatial_embedding, self.exam_token):
            nn.init.trunc_normal_(parameter, std=0.02)

    def _tokens(self, maps, projection, grid_size, spatial_embedding, scale):
        batch = maps.shape[0]
        projected = projection(maps.flatten(0, 1))
        pooled = F.adaptive_avg_pool2d(projected, grid_size)
        tokens = pooled.flatten(2).transpose(1, 2).reshape(batch, 4, -1,
                                                            projected.shape[1])
        view_type = torch.tensor([0, 1, 0, 1], device=maps.device)
        laterality = torch.tensor([0, 0, 1, 1], device=maps.device)
        return (tokens + self.view_type_embedding[view_type][None, :, None, :]
                + self.laterality_embedding[laterality][None, :, None, :]
                + self.scale_embedding[scale][None, None, None, :]
                + spatial_embedding[None, None, :, :])

    def forward(self, fine_maps, coarse_maps, view_mask=None):
        if (fine_maps.ndim != 5 or fine_maps.shape[1:3] != (4, self.fine_dim)
                or coarse_maps.ndim != 5
                or coarse_maps.shape[1:3] != (4, self.coarse_dim)
                or fine_maps.shape[0] != coarse_maps.shape[0]):
            raise ValueError("Expected aligned four-view fine and coarse feature maps")
        batch = fine_maps.shape[0]
        fine = self._tokens(fine_maps, self.fine_projection,
                            self.fine_grid_size, self.fine_spatial_embedding, 0)
        coarse = self._tokens(coarse_maps, self.coarse_projection,
                              self.coarse_grid_size,
                              self.coarse_spatial_embedding, 1)
        tokens = torch.cat((fine.flatten(1, 2), coarse.flatten(1, 2)), dim=1)
        padding_mask = None
        if view_mask is not None:
            if view_mask.shape != (batch, 4):
                raise ValueError("view_mask must have shape [B,4]")
            present = view_mask.to(device=tokens.device, dtype=torch.bool)
            if not present.any(dim=1).all():
                raise ValueError("Every exam must contain at least one view")
            fine_mask = (~present).repeat_interleave(
                self.fine_grid_size ** 2, dim=1
            )
            coarse_mask = (~present).repeat_interleave(
                self.coarse_grid_size ** 2, dim=1
            )
            padding_mask = torch.cat((
                torch.zeros(batch, 1, device=tokens.device, dtype=torch.bool),
                fine_mask, coarse_mask,
            ), dim=1)
        exam = self.exam_token.expand(batch, -1, -1)
        encoded = self.encoder(torch.cat((exam, tokens), dim=1),
                               src_key_padding_mask=padding_mask)
        return self.to_exam(encoded[:, 0])


class LocalGlobalViewTokenFusion(MultiScaleViewTokenFusion):
    """Summarize each view independently before attending across four views."""

    def __init__(self, fine_dim=384, coarse_dim=768, token_dim=256, heads=8,
                 layers=2, fine_grid_size=4, coarse_grid_size=2,
                 attention_dropout=0.1, output_dropout=0.1):
        super().__init__(fine_dim, coarse_dim, token_dim, heads, layers,
                         fine_grid_size, coarse_grid_size,
                         attention_dropout, output_dropout)
        self.view_token = nn.Parameter(torch.empty(1, 1, token_dim))
        nn.init.trunc_normal_(self.view_token, std=0.02)
        layer = nn.TransformerEncoderLayer(
            d_model=token_dim, nhead=heads, dim_feedforward=token_dim * 4,
            dropout=attention_dropout, activation="gelu", batch_first=True,
            norm_first=True,
        )
        self.local_encoder = nn.TransformerEncoder(
            layer, num_layers=layers, norm=nn.LayerNorm(token_dim)
        )
        self.type_adapters = nn.ModuleList([self._adapter(token_dim) for _ in range(2)])
        self.side_adapters = nn.ModuleList([self._adapter(token_dim) for _ in range(2)])

    @staticmethod
    def _adapter(dim):
        adapter = nn.Sequential(nn.Linear(dim, 32), nn.GELU(), nn.Linear(32, dim))
        nn.init.zeros_(adapter[-1].weight)
        nn.init.zeros_(adapter[-1].bias)
        return adapter

    def summarize_views(self, fine_maps, coarse_maps):
        if (fine_maps.ndim != 5 or fine_maps.shape[1:3] != (4, self.fine_dim)
                or coarse_maps.ndim != 5
                or coarse_maps.shape[1:3] != (4, self.coarse_dim)
                or fine_maps.shape[0] != coarse_maps.shape[0]):
            raise ValueError("Expected aligned four-view fine and coarse feature maps")
        batch = fine_maps.shape[0]
        fine = self._tokens(fine_maps, self.fine_projection,
                            self.fine_grid_size, self.fine_spatial_embedding, 0)
        coarse = self._tokens(coarse_maps, self.coarse_projection,
                              self.coarse_grid_size, self.coarse_spatial_embedding, 1)
        # Views stay in the batch axis during local attention; tokens never
        # cross a view boundary until the global encoder below.
        tokens = torch.cat((fine, coarse), dim=2).flatten(0, 1)
        local = self.local_encoder(torch.cat((
            self.view_token.expand(batch * 4, -1, -1), tokens), dim=1))[:, 0]
        local = local.reshape(batch, 4, -1)
        return torch.stack([
            local[:, v] + self.type_adapters[v % 2](local[:, v])
            + self.side_adapters[v // 2](local[:, v]) for v in range(4)
        ], dim=1)

    def forward(self, fine_maps, coarse_maps, view_mask=None,
                return_view_summaries=False):
        batch = fine_maps.shape[0]
        padding_mask = None
        if view_mask is not None:
            if view_mask.shape != (batch, 4):
                raise ValueError("view_mask must have shape [B,4]")
            present = view_mask.to(device=fine_maps.device, dtype=torch.bool)
            if not present.any(dim=1).all():
                raise ValueError("Every exam must contain at least one view")
            absent = ~present[:, :, None, None, None]
            fine_maps = fine_maps.masked_fill(absent, 0)
            coarse_maps = coarse_maps.masked_fill(absent, 0)
            padding_mask = torch.cat((
                torch.zeros(batch, 1, device=fine_maps.device, dtype=torch.bool),
                ~present), dim=1)
        summaries = self.summarize_views(fine_maps, coarse_maps)
        exam = self.exam_token.expand(batch, -1, -1)
        encoded = self.encoder(torch.cat((exam, summaries), dim=1),
                               src_key_padding_mask=padding_mask)
        exam = self.to_exam(encoded[:, 0])
        if return_view_summaries:
            return exam, summaries
        return exam


class MonotonicOrdinalHead(nn.Module):
    """Produce ordered cumulative logits and a valid four-class distribution."""

    def __init__(self, input_dim=1024, initial_gap=1.0):
        super().__init__()
        if float(initial_gap) not in {1.0, 2.0}:
            raise ValueError("ordinal_initial_gap must be 1.0 or 2.0")
        initial_gap = float(initial_gap)
        self.score = nn.Linear(input_dim, 1, bias=False)
        self.threshold_start = nn.Parameter(torch.tensor(-initial_gap))
        inverse_softplus = torch.log(torch.expm1(torch.tensor(initial_gap)))
        self.threshold_deltas = nn.Parameter(inverse_softplus.repeat(2))

    def forward(self, features):
        increments = F.softplus(self.threshold_deltas)
        thresholds = torch.cat((
            self.threshold_start.reshape(1),
            self.threshold_start + increments.cumsum(0),
        ))
        ordinal_logits = self.score(features).float() - thresholds.float()
        cumulative = ordinal_logits.sigmoid()
        probabilities = torch.stack((
            1 - cumulative[:, 0],
            cumulative[:, 0] - cumulative[:, 1],
            cumulative[:, 1] - cumulative[:, 2],
            cumulative[:, 2],
        ), dim=1)
        probabilities = probabilities.clamp_min(torch.finfo(torch.float32).tiny)
        probabilities = probabilities / probabilities.sum(dim=1, keepdim=True)
        return probabilities.log(), ordinal_logits


class DensityModel(nn.Module):
    def __init__(self, pretrained=False, dropout=0.1, bottleneck=256,
                 fusion="hierarchical_relational", attention_dim=256,
                 attention_heads=8, attention_layers=2, attention_dropout=0.1,
                 spatial_grid_size=4, primary_head="flat",
                 ordinal_initial_gap=1.0, backbone="densenet121",
                 view_auxiliary=False, mixstyle_probability=0.0,
                 mixstyle_alpha=0.1, fine_d_expert=False,
                 isolate_fine_d_rng=False):
        super().__init__()
        if not isinstance(view_auxiliary, bool):
            raise ValueError("view_auxiliary must be boolean")
        if not isinstance(fine_d_expert, bool):
            raise ValueError("fine_d_expert must be boolean")
        if not isinstance(isolate_fine_d_rng, bool):
            raise ValueError("isolate_fine_d_rng must be boolean")
        if backbone not in {"densenet121", "convnext_tiny"}:
            raise ValueError("Unknown backbone")
        if fusion not in {"hierarchical_relational", "view_token_attention",
                          "spatial_token_attention",
                          "hybrid_relational_spatial_attention",
                          "multiscale_view_token_attention", "local_global_view_attention"}:
            raise ValueError("Unknown fusion architecture")
        if primary_head not in {"flat", "monotonic_ordinal",
                                "a_gate_hierarchical",
                                "dual_endpoint_hierarchical"}:
            raise ValueError("Unknown primary head")
        if primary_head == "monotonic_ordinal" and fusion != "hierarchical_relational":
            raise ValueError("Ordinal-primary arm requires hierarchical relational fusion")
        if (backbone == "convnext_tiny"
                and (fusion not in {"hierarchical_relational",
                                    "hybrid_relational_spatial_attention",
                                    "multiscale_view_token_attention", "local_global_view_attention"}
                     or primary_head not in {"flat", "a_gate_hierarchical",
                                             "dual_endpoint_hierarchical"})):
            raise ValueError("ConvNeXt arm requires relational/hybrid fusion and a supported head")
        if fusion == "hybrid_relational_spatial_attention" and backbone != "convnext_tiny":
            raise ValueError("Hybrid spatial fusion requires ConvNeXt-Tiny")
        if fusion == "multiscale_view_token_attention" and backbone != "convnext_tiny":
            raise ValueError("Multi-scale view-token fusion requires ConvNeXt-Tiny")
        if fusion == "local_global_view_attention" and (
                backbone != "convnext_tiny" or primary_head != "a_gate_hierarchical"):
            raise ValueError("Local-global fusion requires ConvNeXt-Tiny and A-gate head")
        if view_auxiliary and fusion != "local_global_view_attention":
            raise ValueError("Per-view auxiliary head requires local-global fusion")
        mixstyle = ExamMixStyle(mixstyle_probability, mixstyle_alpha)
        if mixstyle.probability and not (
                view_auxiliary and fusion == "local_global_view_attention"
                and backbone == "convnext_tiny"
                and primary_head == "a_gate_hierarchical"):
            raise ValueError(
                "Feature MixStyle requires the ConvNeXt local-global per-view auxiliary arm"
            )
        if (primary_head == "a_gate_hierarchical"
                and (backbone != "convnext_tiny"
                     or fusion not in {"hybrid_relational_spatial_attention",
                                       "multiscale_view_token_attention", "local_global_view_attention"})):
            raise ValueError("A-gate head requires a registered ConvNeXt fusion")
        if (primary_head == "dual_endpoint_hierarchical"
                and (backbone != "convnext_tiny"
                     or fusion != "hybrid_relational_spatial_attention")):
            raise ValueError(
                "Dual-endpoint head requires ConvNeXt hybrid spatial fusion"
            )
        if fine_d_expert and not (
                backbone == "convnext_tiny"
                and fusion == "hybrid_relational_spatial_attention"
                and primary_head == "a_gate_hierarchical"):
            raise ValueError(
                "Fine-scale D expert requires the ConvNeXt hybrid spatial A-gate arm"
            )
        if isolate_fine_d_rng and not fine_d_expert:
            raise ValueError("Fine-D RNG isolation requires fine_d_expert")
        self.backbone = backbone
        self.fusion = fusion
        self.primary_head = primary_head
        self.view_auxiliary = bool(view_auxiliary)
        self.fine_d_expert = bool(fine_d_expert)
        self.isolate_fine_d_rng = bool(isolate_fine_d_rng)
        self.exam_mixstyle = mixstyle
        if fusion == "local_global_view_attention":
            if self.exam_mixstyle.probability:
                self.architecture = CONVNEXT_LOCAL_GLOBAL_PERVIEW_AUX_MIXSTYLE_ARCHITECTURE
            elif self.view_auxiliary:
                self.architecture = CONVNEXT_LOCAL_GLOBAL_PERVIEW_AUX_ARCHITECTURE
            else:
                self.architecture = CONVNEXT_LOCAL_GLOBAL_A_GATE_ARCHITECTURE
        elif (fusion == "multiscale_view_token_attention"
                and primary_head == "a_gate_hierarchical"):
            self.architecture = CONVNEXT_MULTISCALE_A_GATE_ARCHITECTURE
        elif fusion == "multiscale_view_token_attention":
            self.architecture = CONVNEXT_MULTISCALE_ARCHITECTURE
        elif self.isolate_fine_d_rng:
            self.architecture = CONVNEXT_RNG_ISOLATED_FINE_D_EXPERT_ARCHITECTURE
        elif self.fine_d_expert:
            self.architecture = CONVNEXT_FINE_D_EXPERT_ARCHITECTURE
        elif primary_head == "dual_endpoint_hierarchical":
            self.architecture = CONVNEXT_DUAL_ENDPOINT_GATE_ARCHITECTURE
        elif primary_head == "a_gate_hierarchical":
            self.architecture = CONVNEXT_HYBRID_A_GATE_ARCHITECTURE
        elif backbone == "convnext_tiny" and fusion == "hybrid_relational_spatial_attention":
            self.architecture = CONVNEXT_HYBRID_SPATIAL_ARCHITECTURE
        elif backbone == "convnext_tiny":
            self.architecture = CONVNEXT_RELATIONAL_ARCHITECTURE
        elif primary_head == "monotonic_ordinal":
            if float(ordinal_initial_gap) == 1.0:
                self.architecture = ORDINAL_PRIMARY_ARCHITECTURE
            elif float(ordinal_initial_gap) == 2.0:
                self.architecture = ORDINAL_PRIMARY_WIDE_ARCHITECTURE
            else:
                raise ValueError("ordinal_initial_gap must be 1.0 or 2.0")
        else:
            self.architecture = {
                                 "hierarchical_relational": RELATIONAL_ARCHITECTURE,
                                 "view_token_attention": ATTENTION_ARCHITECTURE,
                                 "spatial_token_attention": SPATIAL_ATTENTION_ARCHITECTURE,
                             }[fusion]
        if backbone == "densenet121":
            self.features = densenet121(
                weights=DenseNet121_Weights.IMAGENET1K_V1 if pretrained else None
            ).features
            self.feature_dim = 1024
            self.backbone_pool_norm = nn.Identity()
        else:
            convnext = convnext_tiny(
                weights=ConvNeXt_Tiny_Weights.IMAGENET1K_V1 if pretrained else None
            )
            self.features = convnext.features
            self.feature_dim = 768
            self.backbone_pool_norm = convnext.classifier[0]
        if fusion in {"hierarchical_relational", "hybrid_relational_spatial_attention"}:
            self.pair_fusion = PairFusion(dim=self.feature_dim, dropout=dropout)
            self.side_gate = nn.Linear(self.feature_dim, 1)
            self.bilateral = nn.Sequential(
                nn.Linear(self.feature_dim * 3, bottleneck), nn.GELU(), nn.Dropout(dropout),
                nn.Linear(bottleneck, self.feature_dim),
            )
            if fusion == "hybrid_relational_spatial_attention":
                self.spatial_attention_fusion = SpatialTokenAttentionFusion(
                    input_dim=self.feature_dim, token_dim=attention_dim,
                    heads=attention_heads, layers=attention_layers,
                    grid_size=spatial_grid_size,
                    attention_dropout=attention_dropout,
                    output_dropout=dropout,
                )
                # Start as a small correction to the proven global relational
                # path, while retaining gradient flow through the spatial arm.
                self.spatial_residual_logit = nn.Parameter(torch.tensor(-2.1972246))
        elif fusion in {"multiscale_view_token_attention", "local_global_view_attention"}:
            fusion_class = (LocalGlobalViewTokenFusion if fusion == "local_global_view_attention"
                            else MultiScaleViewTokenFusion)
            self.multiscale_attention_fusion = fusion_class(
                fine_dim=384, coarse_dim=self.feature_dim,
                token_dim=attention_dim, heads=attention_heads,
                layers=attention_layers, fine_grid_size=spatial_grid_size,
                coarse_grid_size=max(1, spatial_grid_size // 2),
                attention_dropout=attention_dropout, output_dropout=dropout,
            )
        elif fusion == "view_token_attention":
            self.attention_fusion = ViewTokenAttentionFusion(
                token_dim=attention_dim, heads=attention_heads,
                layers=attention_layers, attention_dropout=attention_dropout,
                output_dropout=dropout,
            )
        else:
            self.spatial_attention_fusion = SpatialTokenAttentionFusion(
                input_dim=self.feature_dim, token_dim=attention_dim,
                heads=attention_heads,
                layers=attention_layers, grid_size=spatial_grid_size,
                attention_dropout=attention_dropout, output_dropout=dropout,
            )
        self.exam_norm = nn.LayerNorm(self.feature_dim)
        if primary_head in {"flat", "a_gate_hierarchical",
                            "dual_endpoint_hierarchical"}:
            if primary_head == "flat":
                self.flat_head = nn.Linear(self.feature_dim, 4)
            else:
                self.a_gate = nn.Linear(self.feature_dim, 1)
                # A42 interprets all three outputs as a conditional B/C/D
                # softmax. A47 keeps the identical initialized projection but
                # interprets output 0 as D-vs-(B/C) and outputs 1:3 as B/C.
                self.bcd_head = nn.Linear(self.feature_dim, 3)
            # CORAL: one shared weight vector and three threshold-specific biases.
            self.ordinal_score = nn.Linear(self.feature_dim, 1, bias=False)
            self.ordinal_bias = nn.Parameter(torch.tensor([1.0, 0.0, -1.0]))
        else:
            self.ordinal_head = MonotonicOrdinalHead(
                input_dim=self.feature_dim, initial_gap=ordinal_initial_gap
            )
        self.binary_head = nn.Linear(self.feature_dim, 2)
        if self.view_auxiliary:
            # Initialize this after every existing A44 module so the shared
            # parameters remain identical under the same random seed.
            self.view_aux_head = nn.Linear(attention_dim, 4)
        if self.fine_d_expert:
            # Construct the treatment after every A42 module so all shared
            # parameters remain bit-exact under the same seed. A49 also
            # restores the CPU RNG after treatment initialization so the
            # original A42 stochastic training stream starts identically.
            with torch.random.fork_rng(
                    devices=[], enabled=self.isolate_fine_d_rng):
                self.d_fine_fusion = SpatialTokenAttentionFusion(
                    input_dim=384, token_dim=attention_dim,
                    heads=attention_heads, layers=attention_layers,
                    grid_size=spatial_grid_size,
                    attention_dropout=attention_dropout,
                    output_dropout=dropout,
                )
                self.d_fine_norm = nn.LayerNorm(384)
                self.d_fine_head = nn.Linear(384, 1)
                nn.init.zeros_(self.d_fine_head.weight)
                nn.init.zeros_(self.d_fine_head.bias)

    def forward(self, views):
        if views.ndim != 5 or tuple(views.shape[1:3]) != (4, 3):
            raise ValueError("Expected [B,4,3,H,W] in L_CC,L_MLO,R_CC,R_MLO order")
        batch = views.shape[0]
        flattened_views = views.flatten(0, 1)
        fine_maps = None
        if (self.fusion in {"multiscale_view_token_attention",
                            "local_global_view_attention"}
                or self.fine_d_expert):
            maps = flattened_views
            for index, block in enumerate(self.features):
                maps = block(maps)
                if index == 5:
                    fine_maps = maps.reshape(
                        batch, 4, 384, maps.shape[-2], maps.shape[-1]
                    )
                    if self.fusion in {"multiscale_view_token_attention",
                                       "local_global_view_attention"}:
                        fine_maps = self.exam_mixstyle(fine_maps)
                        maps = fine_maps.flatten(0, 1)
            if fine_maps is None:
                raise RuntimeError("ConvNeXt fine-scale feature stage was not found")
        else:
            maps = self.features(flattened_views)
        if self.backbone == "densenet121":
            maps = F.relu(maps, inplace=False)
        view_summaries = None
        if self.fusion in {"multiscale_view_token_attention", "local_global_view_attention"}:
            fusion_inputs = (
                fine_maps,
                maps.reshape(batch, 4, self.feature_dim,
                             maps.shape[-2], maps.shape[-1]),
            )
            if self.view_auxiliary:
                exam, view_summaries = self.multiscale_attention_fusion(
                    *fusion_inputs, return_view_summaries=True)
            else:
                exam = self.multiscale_attention_fusion(*fusion_inputs)
            features = None
        elif self.fusion == "spatial_token_attention":
            exam = self.spatial_attention_fusion(
                maps.reshape(batch, 4, self.feature_dim, maps.shape[-2], maps.shape[-1])
            )
            features = None
        else:
            pooled = F.adaptive_avg_pool2d(maps, 1)
            pooled = self.backbone_pool_norm(pooled)
            features = pooled.flatten(1).reshape(batch, 4, self.feature_dim)
        if self.fusion in {"hierarchical_relational",
                           "hybrid_relational_spatial_attention"}:
            left = self.pair_fusion(features[:, 0], features[:, 1])
            right = self.pair_fusion(features[:, 2], features[:, 3])
            sides = torch.stack((left, right), dim=1)
            pooled = (sides * self.side_gate(sides).softmax(dim=1)).sum(dim=1)
            relation = torch.cat(((left + right) / 2, (left - right).abs(),
                                  left * right), dim=1)
            exam = pooled + self.bilateral(relation)
            if self.fusion == "hybrid_relational_spatial_attention":
                spatial = self.spatial_attention_fusion(
                    maps.reshape(batch, 4, self.feature_dim,
                                 maps.shape[-2], maps.shape[-1])
                )
                exam = exam + self.spatial_residual_logit.sigmoid() * spatial
        elif self.fusion == "view_token_attention":
            exam = self.attention_fusion(features)
        exam = self.exam_norm(exam)
        if self.primary_head == "flat":
            flat_logits = self.flat_head(exam)
            ordinal_logits = self.ordinal_score(exam) + self.ordinal_bias
        elif self.primary_head == "a_gate_hierarchical":
            a_logit = self.a_gate(exam).float()
            bcd_logits = self.bcd_head(exam).float()
            if self.fine_d_expert:
                devices = ([torch.cuda.current_device()]
                           if fine_maps.is_cuda else [])
                # A49 restores the CPU/CUDA RNG after the treatment branch,
                # preventing its attention/dropout draws from shifting the
                # next A42-path dropout and stochastic-depth masks.
                with torch.random.fork_rng(
                        devices=devices, enabled=self.isolate_fine_d_rng):
                    fine_exam = self.d_fine_fusion(fine_maps)
                    d_residual = self.d_fine_head(
                        self.d_fine_norm(fine_exam)
                    ).float()
                bcd_logits = torch.cat((
                    bcd_logits[:, :2], bcd_logits[:, 2:] + d_residual,
                ), dim=1)
            bcd_log_prob = F.log_softmax(bcd_logits, dim=1)
            flat_logits = torch.cat((
                F.logsigmoid(a_logit),
                F.logsigmoid(-a_logit) + bcd_log_prob,
            ), dim=1)
            ordinal_logits = self.ordinal_score(exam) + self.ordinal_bias
        elif self.primary_head == "dual_endpoint_hierarchical":
            a_logit = self.a_gate(exam).float()
            endpoint_logits = self.bcd_head(exam).float()
            d_logit = endpoint_logits[:, :1]
            bc_log_prob = F.log_softmax(endpoint_logits[:, 1:], dim=1)
            not_a = F.logsigmoid(-a_logit)
            not_d = F.logsigmoid(-d_logit)
            flat_logits = torch.cat((
                F.logsigmoid(a_logit),
                not_a + not_d + bc_log_prob,
                not_a + F.logsigmoid(d_logit),
            ), dim=1)
            ordinal_logits = self.ordinal_score(exam) + self.ordinal_bias
        else:
            flat_logits, ordinal_logits = self.ordinal_head(exam)
        outputs = {"flat_logits": flat_logits, "ordinal_logits": ordinal_logits,
                   "binary_logits": self.binary_head(exam)}
        if view_summaries is not None:
            outputs["view_logits"] = self.view_aux_head(view_summaries)
        return outputs
