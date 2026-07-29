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
        else:
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

    def encode_images(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        if self.options.freeze_early_layers:
            # Freeze features from conv0 to denseblock2
            # DenseNet121 features: conv0, norm0, relu0, pool0, denseblock1, transition1, denseblock2, transition2, denseblock3, transition3, denseblock4, norm5
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
            # FPN completely replaces the default sequential execution
            features = self.fpn(images)
            
            if getattr(self.options, "use_cbam", False) and self.cbam is not None:
                # Need spatial features for CBAM, but FPN outputs pooled features.
                # CBAM should ideally be applied BEFORE FPN pooling, but since we use
                # global pooling in FPN, we can't easily apply CBAM here. 
                # So if FPN is used, CBAM is bypassed for simplicity.
                pass
                
            return features
            
        backbone_name = getattr(self.options, "backbone", "densenet121")
        if backbone_name == "convnext_tiny":
            features = self.backbone.features(images)
            features = self.backbone.avgpool(features)
            features = torch.flatten(features, start_dim=1)
            features = self.proj(features)
            return features
            
        features = self.backbone.features(
            images
        )

        if getattr(self.options, "use_cbam", False) and self.cbam is not None:
            features = self.cbam(features)

        # Required to match torchvision DenseNet forward.
        features = F.relu(
            features,
            inplace=False,
        )

        features = F.adaptive_avg_pool2d(
            features,
            output_size=(1, 1),
        )

        return torch.flatten(
            features,
            start_dim=1,
        )

    def encode_views(
        self,
        views: torch.Tensor,
    ) -> torch.Tensor:
        if views.ndim != 5:
            raise ValueError(
                "views must have shape "
                "[B, 4, 3, H, W]."
            )

        batch_size, num_views = views.shape[:2]

        if num_views != len(VIEW_ORDER):
            raise ValueError(
                f"Expected {len(VIEW_ORDER)} views, "
                f"received {num_views}."
            )

        flattened = views.reshape(
            batch_size * num_views,
            *views.shape[2:],
        )

        encoded = self.encode_images(
            flattened
        )

        return encoded.reshape(
            batch_size,
            num_views,
            FEATURE_DIM,
        )

    def forward(
        self,
        views: torch.Tensor,
    ) -> dict[
        str,
        torch.Tensor | None,
    ]:
        view_features = self.encode_views(
            views
        )

        fusion_result = self.fusion_module(
            view_features
        )

        exam_features = (
            fusion_result.exam_features
        )

        flat_logits = (
            self.flat_head(
                exam_features
            )
        )

        ordinal_logits = (
            self.ordinal_head(exam_features)
            if self.ordinal_head is not None
            else None
        )

        binary_logits = (
            self.binary_head(exam_features)
            if self.binary_head is not None
            else None
        )

        cd_logits = (
            self.cd_head(exam_features)
            if self.cd_head is not None
            else None
        )

        return {
            "flat_logits": flat_logits,
            "ordinal_logits": ordinal_logits,
            "binary_logits": binary_logits,
            "cd_logits": cd_logits,
            "exam_features": exam_features,
            "view_features": view_features,
            "left_features": (
                fusion_result.left_features
            ),
            "right_features": (
                fusion_result.right_features
            ),
            "left_gate_weights": (
                fusion_result.left_gate_weights
            ),
            "right_gate_weights": (
                fusion_result.right_gate_weights
            ),
            "bilateral_gate_weights": (
                fusion_result.bilateral_gate_weights
            ),
        }
