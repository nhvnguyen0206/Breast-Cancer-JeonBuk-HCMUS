# A40 preregistration: ConvNeXt-Tiny backbone with A30 relational fusion

A40 is a conditional major-architecture successor and must not launch before
A39 completes/audits. The campaign has now isolated handcrafted fusion,
view-token attention, spatial-token attention and monotonic ordinal-primary
heads without solving the historically hard fold 1. A40 tests whether the
ImageNet feature extractor, rather than fusion or output parameterization, is
the remaining representational bottleneck.

A40 returns every downstream choice to strongest audited A30: hierarchical
relational fusion, flat primary head, CORAL/binary auxiliaries, dropout 0.40,
sampling power 0.25, augmentation, loss weights, optimizer, seed and the same
four-view cache/split. It changes only DenseNet121 to ImageNet-pretrained
ConvNeXt-Tiny. Standard ConvNeXt pooled LayerNorm is retained before the
unchanged relational fusion. This is one model and one inference path, not an
ensemble.

The model has 30,387,819 trainable parameters versus A30's 11,163,787, so
overfitting and slower training are explicit risks. The hypothesis is that
ConvNeXt's modern convolutional blocks learn global parenchymal texture more
effectively than DenseNet121 under identical supervision.

## Prepared snapshot

Prepared but not launched:
`/slurmshared/Ngoc/code/hcmus-density-convnext-relational-20260922-v1`.
The isolated snapshot passes 18/18 tests, including ConvNeXt relational
forward/backward, all three heads, finite gradients and invalid-combination
guards. Strict checkpoint save/load is bit-exact. Matched-seed state and
output hashes prove the default DenseNet/A30 path remains bit-exact after the
source extension. Official ConvNeXt-Tiny ImageNet weights are downloaded and
load successfully from the shared Torch cache.

- Config SHA256: `1c5ac46b77213f7ab7a5956e237369d50ebdf13f5a703563a9c337a5e00ca80e`
- Model SHA256: `867c93a29e5023d3ab6fe6de9904ad99a16fe5a8a2f12a92685a90d4aa6e70a4`
- Minimal engine SHA256: `0eb1d0688b56bb4d8afd7a82d770c18d5985f8bc6016e4287e6ae52e198127f3`
- Launcher SHA256: `dacaae0afe657135e845dc4f7a1fbcd917f09d2761ea892c99396308cb2cdefd`
- Frozen assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

Real 512x512 cached-batch RTX 5090 preflight remains pending while A39 uses
both permitted GPUs. If A39 fails and A40 preflight passes, screen only fixed
folds 1 and 3 under the existing gates.

