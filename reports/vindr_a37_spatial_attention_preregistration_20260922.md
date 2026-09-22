# A37 preregistration: spatial cross-view attention

A37 is a conditional successor to A36 and must not launch before A36 finishes
and passes its final audit. A36's first-20 evidence shows that attention over
four globally pooled view vectors can improve fold 3 but has not recovered
fold 1. The new hypothesis is that global average pooling discards regional
density patterns before cross-view fusion.

A37 retains the same DenseNet121 ImageNet backbone, four-view cache,
augmentation, sampling, losses, optimizer, three heads, seed and 50-epoch
protocol as A36/A30. The only architectural hypothesis changes tokenization:
each view's final DenseNet feature map is pooled to a 4x4 grid, producing 16
regional tokens per view and 64 tokens per exam. Tokens receive learned 2-D
spatial, CC/MLO and left/right embeddings. A learned exam token and the same
two-layer, eight-head 256-dimensional pre-norm Transformer perform joint
spatial and cross-view fusion. Inference remains one model and one flat head,
not an ensemble.

This is materially different from both the handcrafted relational model and
A36's one-token-per-view model while still isolating one interpretable change.
It has 9,074,569 trainable parameters, only 4,096 more than A36, so any change
is not explained by a large capacity increase.

## Verification and frozen snapshot

Prepared but not launched:
`/slurmshared/Ngoc/code/hcmus-density-spatial-attention-20260921-v1`.
The final isolated snapshot passes 19/19 tests. The spatial embeddings and all
prediction heads receive finite, nonzero gradients. Strict checkpoint
save/load produces bit-exact outputs. Matched-seed state hashes for the old
relational and A36 view-token modes are identical between the A36 and A37
sources, proving backward compatibility.

- Config SHA256: `0d29908520d682b58280c14485c5630fe1ace03f4d24f1e54413517687181b0f`
- Model SHA256: `01a9dddded1a52e4dd9b854078948d502f39d5eadb9038e0a36bd6179de1a59f`
- Minimal engine SHA256: `8f355b544078a4aebe39a6af8bc461a54469fface0b84836fa0356587645459e`
- Launcher SHA256: `dacaae0afe657135e845dc4f7a1fbcd917f09d2761ea892c99396308cb2cdefd`
- Frozen assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

After A36 completed and released its GPUs, the real 512x512 cached-batch
preflight PASSed on `NVIDIA GeForce RTX 5090`. Forward, multitask loss,
backward, gradient clipping and AdamW update were finite under AMP. GradScaler
recovered after one initial skipped update, and peak allocated memory was
2.686 GiB. A37 is cleared for its fixed folds 1/3 screen.

If preflight passes and final A36 fails, screen only fixed folds 1 and 3.
Expand only if both audits PASS, mean Macro-F1 >=0.70 and minimum >=0.65.
