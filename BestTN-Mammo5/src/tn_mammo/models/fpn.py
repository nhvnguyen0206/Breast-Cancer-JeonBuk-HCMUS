import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models.feature_extraction import create_feature_extractor

class MultiScaleExtractor(nn.Module):
    """
    Extracts multi-scale features from DenseNet121 and aggregates them globally.
    Replaces the standard feature extractor in density_model.py.
    """
    def __init__(self, backbone_features_module, out_dim=1024):
        super().__init__()
        # We extract at the end of each dense block (before pooling in transition, or at norm5)
        self.extractor = create_feature_extractor(
            backbone_features_module,
            return_nodes={
                'transition1.relu': 'scale1',  # channels: 128
                'transition2.relu': 'scale2',  # channels: 256
                'transition3.relu': 'scale3',  # channels: 512
                'norm5': 'scale4'              # channels: 1024
            }
        )
        
        # transition1.relu is 256, transition2.relu is 512, transition3.relu is 1024, norm5 is 1024
        # Total: 256 + 512 + 1024 + 1024 = 2816
        in_channels = 256 + 512 + 1024 + 1024
        
        self.aggregator = nn.Sequential(
            nn.Linear(in_channels, out_dim),
            nn.BatchNorm1d(out_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2)
        )

    def forward(self, x):
        features = self.extractor(x)
        
        pooled_features = []
        for key in ['scale1', 'scale2', 'scale3', 'scale4']:
            feat = features[key]
            # DenseNet requires ReLU before pooling, which is already done for scale1-3, 
            # but norm5 is just batchnorm, so we apply ReLU manually to it just in case,
            # or rely on the extractor. Actually densenet121 features ends with norm5 (BatchNorm2d).
            # We apply ReLU to norm5 output:
            if key == 'scale4':
                feat = F.relu(feat, inplace=True)
            
            # Global Average Pooling
            pooled = F.adaptive_avg_pool2d(feat, output_size=(1, 1))
            pooled = torch.flatten(pooled, start_dim=1)
            pooled_features.append(pooled)
            
        concat = torch.cat(pooled_features, dim=1)
        out = self.aggregator(concat)
        return out
