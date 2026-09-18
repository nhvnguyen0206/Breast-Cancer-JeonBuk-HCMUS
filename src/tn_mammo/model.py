"""Architecture matching the original hierarchical relational fusion diagram."""
import torch
from torch import nn
from torch.nn import functional as F
from torchvision.models import densenet121, DenseNet121_Weights


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


class DensityModel(nn.Module):
    def __init__(self, pretrained=False, dropout=0.1, bottleneck=256):
        super().__init__()
        self.features = densenet121(
            weights=DenseNet121_Weights.IMAGENET1K_V1 if pretrained else None
        ).features
        self.pair_fusion = PairFusion(dropout=dropout)  # shared across breasts
        self.side_gate = nn.Linear(1024, 1)
        self.bilateral = nn.Sequential(
            nn.Linear(3072, bottleneck), nn.GELU(), nn.Dropout(dropout),
            nn.Linear(bottleneck, 1024),
        )
        self.exam_norm = nn.LayerNorm(1024)
        self.flat_head = nn.Linear(1024, 4)
        # CORAL: one shared weight vector and three threshold-specific biases.
        self.ordinal_score = nn.Linear(1024, 1, bias=False)
        self.ordinal_bias = nn.Parameter(torch.tensor([1.0, 0.0, -1.0]))
        self.binary_head = nn.Linear(1024, 2)

    def forward(self, views):
        if views.ndim != 5 or tuple(views.shape[1:3]) != (4, 3):
            raise ValueError("Expected [B,4,3,H,W] in L_CC,L_MLO,R_CC,R_MLO order")
        batch = views.shape[0]
        maps = F.relu(self.features(views.flatten(0, 1)), inplace=False)
        features = F.adaptive_avg_pool2d(maps, 1).flatten(1).reshape(batch, 4, 1024)
        left = self.pair_fusion(features[:, 0], features[:, 1])
        right = self.pair_fusion(features[:, 2], features[:, 3])
        sides = torch.stack((left, right), dim=1)
        pooled = (sides * self.side_gate(sides).softmax(dim=1)).sum(dim=1)
        relation = torch.cat(((left + right) / 2, (left - right).abs(), left * right), dim=1)
        exam = self.exam_norm(pooled + self.bilateral(relation))
        return {"flat_logits": self.flat_head(exam),
                "ordinal_logits": self.ordinal_score(exam) + self.ordinal_bias,
                "binary_logits": self.binary_head(exam)}
