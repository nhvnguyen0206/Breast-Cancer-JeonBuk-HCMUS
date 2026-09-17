from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn
from torch.nn import functional as F
from torchvision.models import (
    DenseNet121_Weights,
    densenet121,
)

from tn_mammo.constants import (
    FEATURE_DIM,
    NUM_CLASSES,
    VIEW_ORDER,
)
from coral_pytorch.layers import CoralLayer


class SpatialViT(nn.Module):
    """
    Applies a Transformer Encoder to the spatial features of a CNN.
    """
    def __init__(self, feature_dim=1024, num_layers=4, nhead=8, max_seq_len=1025):
        super().__init__()
        self.cls_token = nn.Parameter(torch.zeros(1, 1, feature_dim))
        self.pos_embed = nn.Parameter(torch.randn(1, max_seq_len, feature_dim) * 0.02)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=feature_dim, 
            nhead=nhead, 
            dim_feedforward=feature_dim * 4,
            dropout=0.1,
            activation='gelu',
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
    def forward(self, x):
        # x: [B, C, H, W]
        B, C, H, W = x.shape
        x = x.flatten(2).transpose(1, 2) # [B, H*W, C]
        
        cls_tokens = self.cls_token.expand(B, -1, -1) # [B, 1, C]
        x = torch.cat((cls_tokens, x), dim=1) # [B, H*W + 1, C]
        
        seq_len = x.shape[1]
        x = x + self.pos_embed[:, :seq_len, :]
        
        x = self.transformer(x) # [B, seq_len, C]
        
        return x[:, 0] # Return the CLS token feature: [B, C]


class ViewViT(nn.Module):
    """
    Applies a Transformer Encoder across the 4 view features.
    """
    def __init__(self, feature_dim=1024, num_layers=4, nhead=8):
        super().__init__()
        self.cls_token = nn.Parameter(torch.zeros(1, 1, feature_dim))
        self.pos_embed = nn.Parameter(torch.randn(1, 5, feature_dim) * 0.02) # 4 views + 1 CLS
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=feature_dim, 
            nhead=nhead, 
            dim_feedforward=feature_dim * 4,
            dropout=0.1,
            activation='gelu',
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
    def forward(self, x):
        # x: [B, 4, C]
        B = x.shape[0]
        
        cls_tokens = self.cls_token.expand(B, -1, -1) # [B, 1, C]
        x = torch.cat((cls_tokens, x), dim=1) # [B, 5, C]
        
        x = x + self.pos_embed
        
        x = self.transformer(x) # [B, 5, C]
        
        return x[:, 0] # Return the CLS token feature: [B, C]


class CatBeoDensityModel(nn.Module):
    """
    CatBeo architecture:
    1. DenseNet121 spatial features + Spatial ViT -> 4 independent features
    2. View ViT across the 4 features -> 1 combined feature
    3. Concat all 5 features -> classifier
    """
    def __init__(self, options) -> None:
        super().__init__()
        self.options = options
        
        weights = (
            DenseNet121_Weights.IMAGENET1K_V1
            if options.imagenet_init
            else None
        )
        self.backbone = densenet121(weights=weights)
        
        in_features = int(self.backbone.classifier.in_features)
        if in_features != FEATURE_DIM:
            raise RuntimeError(f"Unexpected DenseNet121 feature dimension: {in_features}")
            
        # "Heavier" Transformers
        self.spatial_vit = SpatialViT(feature_dim=FEATURE_DIM, num_layers=4, nhead=8)
        self.view_vit = ViewViT(feature_dim=FEATURE_DIM, num_layers=4, nhead=8)
        
        self.fusion_dim = FEATURE_DIM * 5
        
        self.flat_head = nn.Linear(self.fusion_dim, NUM_CLASSES)
        
        if options.use_ordinal_head:
            self.ordinal_head = CoralLayer(self.fusion_dim, NUM_CLASSES)
        else:
            self.ordinal_head = None
            
        if options.use_binary_head:
            self.binary_head = nn.Linear(self.fusion_dim, 2)
        else:
            self.binary_head = None
            
        if options.use_cd_head:
            self.cd_head = nn.Linear(self.fusion_dim, 2)
        else:
            self.cd_head = None

    def encode_spatial_images(self, images: torch.Tensor) -> torch.Tensor:
        if self.options.freeze_early_layers:
            frozen_layers = [
                "conv0", "norm0", "relu0", "pool0",
                "denseblock1", "transition1",
                "denseblock2"
            ]
            for name, child in self.backbone.features.named_children():
                if name in frozen_layers:
                    for param in child.parameters():
                        param.requires_grad = False
                        
        features = self.backbone.features(images)
        features = F.relu(features, inplace=False)
        return features

    def encode_views(self, views: torch.Tensor) -> torch.Tensor:
        if views.ndim != 5:
            raise ValueError("views must have shape [B, 4, 3, H, W].")
            
        batch_size, num_views = views.shape[:2]
        
        if num_views != len(VIEW_ORDER):
            raise ValueError(f"Expected {len(VIEW_ORDER)} views, received {num_views}.")
            
        flattened = views.reshape(batch_size * num_views, *views.shape[2:])
        
        spatial_features = self.encode_spatial_images(flattened) # [B*4, 1024, H, W]
        
        # Apply Spatial ViT
        view_features = self.spatial_vit(spatial_features) # [B*4, 1024]
        
        return view_features.reshape(batch_size, num_views, FEATURE_DIM)

    def forward(self, views: torch.Tensor) -> dict[str, torch.Tensor | None]:
        # 1. CNN + ViT chạy độc lập 4 view để trích xuất features 4 view (1 view -> 1 features)
        view_features = self.encode_views(views) # [B, 4, 1024]
        
        # 2. Xong cho 1 cái ViT chạy 4 ảnh gộp thành 1 features
        combined_feature = self.view_vit(view_features) # [B, 1024]
        
        # 3. Gộp 5 th đó lại, concat làm features
        # Concatenate 4 view features and 1 combined feature
        concat_features = torch.cat([view_features.flatten(1), combined_feature], dim=1) # [B, 5120]
        
        flat_logits = self.flat_head(concat_features)
        
        ordinal_logits = self.ordinal_head(concat_features) if self.ordinal_head is not None else None
        binary_logits = self.binary_head(concat_features) if self.binary_head is not None else None
        cd_logits = self.cd_head(concat_features) if self.cd_head is not None else None
        
        return {
            "flat_logits": flat_logits,
            "ordinal_logits": ordinal_logits,
            "binary_logits": binary_logits,
            "cd_logits": cd_logits,
            "exam_features": concat_features,
            "view_features": view_features,
            "left_features": view_features[:, 0:2].mean(dim=1), # Dummy for compatibility
            "right_features": view_features[:, 2:4].mean(dim=1), # Dummy for compatibility
            "left_gate_weights": torch.ones(views.shape[0], 2, device=views.device) * 0.5, # Dummy
            "right_gate_weights": torch.ones(views.shape[0], 2, device=views.device) * 0.5, # Dummy
            "bilateral_gate_weights": None,
        }
