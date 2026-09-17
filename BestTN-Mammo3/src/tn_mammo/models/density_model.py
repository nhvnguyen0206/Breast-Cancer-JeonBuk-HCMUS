from __future__ import annotations

from dataclasses import dataclass

import torch
from coral_pytorch.layers import CoralLayer
from torch import nn
from torch.nn import functional as F
from torchvision.models import (
    DenseNet121_Weights,
    densenet121,
    convnext_tiny,
    ConvNeXt_Tiny_Weights,
)

from tn_mammo.constants import (
    FEATURE_DIM,
    NUM_CLASSES,
    VIEW_ORDER,
)
from tn_mammo.models.fusion import (
    build_four_view_fusion,
)
from tn_mammo.models.cbam import CBAM
from tn_mammo.models.fpn import MultiScaleExtractor
from tn_mammo.models.region_correspondence import CrossViewRegionModule


@dataclass(frozen=True)
class ModelOptions:
    use_ordinal_head: bool = False
    use_binary_head: bool = False
    imagenet_init: bool = False
    fusion: str = "mean"
    fusion_dropout: float = 0.1
    control_hidden_dim: int = 608
    bilateral_bottleneck_dim: int = 256
    use_cbam: bool = False
    use_fpn: bool = False
    freeze_early_layers: bool = False
    backbone: str = "densenet121"
    use_cd_head: bool = False
    image_size: int = 512
    
    # Region Correspondence Options
    region_enabled: bool = False
    region_dim: int = 256
    region_max_tokens: int = 256
    region_num_heads: int = 8
    region_contralateral: bool = True
    region_ipsilateral: bool = False
    region_alpha_init: float = 0.0
    
    # Class B/C Diagnostic Options
    bc_aux_enabled: bool = False


class FourViewDensityModel(nn.Module):
    """Shared DenseNet121 four-view breast-density model.

    E0: Mean fusion and flat A/B/C/D head.
    E1: E0 plus CORAL ordinal head.
    E2: E1 plus A/B-versus-C/D auxiliary head.
    """

    def __init__(
        self,
        options: ModelOptions,
    ) -> None:
        super().__init__()
        self.options = options

        backbone_name = getattr(options, "backbone", "densenet121")
        if backbone_name == "convnext_tiny":
            weights = (
                ConvNeXt_Tiny_Weights.IMAGENET1K_V1
                if options.imagenet_init
                else None
            )
            self.backbone = convnext_tiny(weights=weights)
            in_features = self.backbone.classifier[2].in_features
            self.proj = nn.Linear(in_features, FEATURE_DIM)
        elif backbone_name == "densenet121":
            weights = (
                DenseNet121_Weights.IMAGENET1K_V1
                if options.imagenet_init
                else None
            )
            self.backbone = densenet121(weights=weights)
            in_features = int(self.backbone.classifier.in_features)
            if in_features != FEATURE_DIM:
                raise RuntimeError(
                    f"Unexpected DenseNet121 feature dimension: {in_features}"
                )
            self.proj = nn.Identity()
        else:
            import timm
            img_sz = getattr(options, "image_size", 512)
            try:
                self.backbone = timm.create_model(backbone_name, pretrained=options.imagenet_init, num_classes=0, img_size=img_sz)
            except TypeError:
                self.backbone = timm.create_model(backbone_name, pretrained=options.imagenet_init, num_classes=0)
            in_features = self.backbone.num_features
            self.proj = nn.Linear(in_features, FEATURE_DIM) if in_features != FEATURE_DIM else nn.Identity()

        self.backbone_feature_dim = in_features
        
        self.region_module = CrossViewRegionModule(
            in_channels=self.backbone_feature_dim,
            backbone_feature_dim=self.backbone_feature_dim,
            region_dim=getattr(options, "region_dim", 256),
            max_tokens=getattr(options, "region_max_tokens", 256),
            num_heads=getattr(options, "region_num_heads", 8),
            enabled=getattr(options, "region_enabled", False),
            contralateral=getattr(options, "region_contralateral", True),
            ipsilateral=getattr(options, "region_ipsilateral", False),
            alpha_init=getattr(options, "region_alpha_init", 0.0),
        )

        self.flat_head = nn.Linear(
            FEATURE_DIM,
            NUM_CLASSES,
        )

        self.fusion_module = (
            build_four_view_fusion(
                name=options.fusion,
                feature_dim=FEATURE_DIM,
                dropout=options.fusion_dropout,
                control_hidden_dim=(
                    options.control_hidden_dim
                ),
                bilateral_bottleneck_dim=(
                    options.bilateral_bottleneck_dim
                ),
            )
        )

        if options.use_ordinal_head:
            self.ordinal_head: nn.Module | None = (
                CoralLayer(
                    FEATURE_DIM,
                    NUM_CLASSES,
                )
            )
        else:
            self.ordinal_head = None

        if options.use_binary_head:
            self.binary_head: nn.Module | None = (
                nn.Linear(
                    FEATURE_DIM,
                    2,
                )
            )
        else:
            self.binary_head = None
            
        if getattr(options, "bc_aux_enabled", False):
            self.bc_aux_head: nn.Module | None = nn.Linear(FEATURE_DIM, 2)
        else:
            self.bc_aux_head = None

        if options.use_cbam:
            self.cbam = CBAM(in_planes=1024)
        else:
            self.cbam = None
            
        if options.use_fpn:
            self.fpn = MultiScaleExtractor(self.backbone.features, out_dim=FEATURE_DIM)
        else:
            self.fpn = None

        if options.use_cd_head:
            self.cd_head: nn.Module | None = (
                nn.Linear(FEATURE_DIM, 2)
            )
        else:
            self.cd_head = None

    def extract_view_features_pre_gap(
        self,
        images: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
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

        if getattr(self.options, "use_fpn", False) and self.fpn is not None:
            features = self.fpn(images)
            return features.unsqueeze(-1).unsqueeze(-1), features
            
        backbone_name = getattr(self.options, "backbone", "densenet121")
        if backbone_name == "convnext_tiny":
            fmap = self.backbone.features(images)
            pooled = self.backbone.avgpool(fmap)
            pooled = torch.flatten(pooled, start_dim=1)
            return fmap, pooled
        elif backbone_name != "densenet121":
            if hasattr(self.backbone, 'forward_features'):
                fmap = self.backbone.forward_features(images)
                pooled = self.backbone.global_pool(fmap) if hasattr(self.backbone, 'global_pool') else fmap.mean([-2, -1])
                pooled = torch.flatten(pooled, start_dim=1)
                return fmap, pooled
            else:
                features = self.backbone(images)
                return features.unsqueeze(-1).unsqueeze(-1), features
                
        fmap = self.backbone.features(images)

        if getattr(self.options, "use_cbam", False) and self.cbam is not None:
            fmap = self.cbam(fmap)

        fmap = F.relu(fmap, inplace=False)

        pooled = F.adaptive_avg_pool2d(fmap, output_size=(1, 1))
        pooled = torch.flatten(pooled, start_dim=1)

        return fmap, pooled

    def encode_images(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        # Legacy method for backward compatibility if needed, but not used in forward now.
        _, pooled = self.extract_view_features_pre_gap(images)
        return self.proj(pooled)

    def encode_views(
        self,
        views: torch.Tensor,
    ) -> torch.Tensor:
        # Legacy method
        batch_size, num_views = views.shape[:2]
        flattened = views.reshape(batch_size * num_views, *views.shape[2:])
        encoded = self.encode_images(flattened)
        return encoded.reshape(batch_size, num_views, FEATURE_DIM)

    def forward(
        self,
        views: torch.Tensor,
        spatial_masks: torch.Tensor | None = None,
        view_mask: torch.Tensor | None = None,
        return_region_attention: bool = False,
    ) -> dict[str, torch.Tensor | None]:
        if views.ndim != 5:
            raise ValueError("views must have shape [B, 4, 3, H, W].")
            
        B, num_views = views.shape[:2]
        if num_views != len(VIEW_ORDER):
            raise ValueError(f"Expected {len(VIEW_ORDER)} views, received {num_views}.")
            
        view_keys = ("L_CC", "L_MLO", "R_CC", "R_MLO")
        
        feature_maps = {}
        global_features = {}
        s_masks_dict = {}
        
        # Derive view_mask if not provided (sum of absolute pixel values > 0)
        if view_mask is None:
            view_mask = (views.view(B, 4, -1).abs().sum(dim=-1) > 1e-5)
            
        for i, view in enumerate(view_keys):
            view_tensor = views[:, i]
            fmap, pooled = self.extract_view_features_pre_gap(view_tensor)
            feature_maps[view] = fmap
            global_features[view] = pooled
            if spatial_masks is not None:
                s_masks_dict[view] = spatial_masks[:, i]
                
        if self.region_module.enabled:
            global_features, region_aux = self.region_module(
                feature_maps=feature_maps,
                global_features=global_features,
                spatial_masks=s_masks_dict if spatial_masks is not None else None,
                view_mask=view_mask,
                return_attention=return_region_attention,
            )
        else:
            region_aux = {"region_enabled": False}
            
        # Apply projection and reconstruct into [B, 4, FEATURE_DIM]
        view_features = []
        for view in view_keys:
            feat = global_features[view]
            feat = self.proj(feat)
            view_features.append(feat)
            
        view_features = torch.stack(view_features, dim=1)

        fusion_result = self.fusion_module(view_features)
        exam_features = fusion_result.exam_features

        flat_logits = self.flat_head(exam_features)
        ordinal_logits = self.ordinal_head(exam_features) if self.ordinal_head is not None else None
        binary_logits = self.binary_head(exam_features) if self.binary_head is not None else None
        bc_logits = self.bc_aux_head(exam_features) if self.bc_aux_head is not None else None
        cd_logits = self.cd_head(exam_features) if self.cd_head is not None else None

        outputs = {
            "flat_logits": flat_logits,
            "ordinal_logits": ordinal_logits,
            "binary_logits": binary_logits,
            "bc_logits": bc_logits,
            "cd_logits": cd_logits,
            "exam_features": exam_features,
            "view_features": view_features,
            "left_features": fusion_result.left_features,
            "right_features": fusion_result.right_features,
            "region_aux": region_aux,
        }
        
        return outputs
