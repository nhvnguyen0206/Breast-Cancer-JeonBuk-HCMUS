# A41 preregistration: ConvNeXt hybrid relational-spatial fusion

## Evidence and hypothesis

A40 proves that ConvNeXt-Tiny can raise selected-DEV CV5 mean Macro-F1 to
0.7196907017, but it fails stability with sample SD 0.1124297521 and minimum
0.5439920998. Fold 0 remains strong late in training while fold 2 never
improves after epoch 3. Replacing only the backbone therefore raises capacity
without producing a fold-stable exam representation.

A36/A37 previously replaced the relational representation with view/spatial
attention and failed. A41 tests a different structural hypothesis: keep A40's
proven global hierarchical relational path intact and add learned regional
cross-view information as a **residual correction**, rather than replacing
the global path.

## Registered change

Relative to A40, A41 changes only fusion:

- the four ConvNeXt feature maps are pooled to a 4x4 grid per view;
- 64 tokens receive explicit CC/MLO, left/right and spatial embeddings;
- a two-layer, eight-head Transformer produces a spatial exam vector;
- the original A40 relational exam vector remains present;
- final pre-normalization exam representation is
  `global_relational + sigmoid(alpha) * spatial_attention`;
- `sigmoid(alpha)` initializes to 0.1, preserving a dominant global path while
  allowing gradients through the new spatial branch from the first step.

Backbone, flat/ordinal/binary heads, losses, optimizer, sampling, augmentation,
cache, grouped split, assignment digest, seed 42 and 50-epoch contract remain
unchanged. The model is a single inference path, not an ensemble.

Architecture ID:
`convnext_tiny_hybrid_relational_spatial_multitask_v7`.
Trainable parameters: 32,367,980 versus A40's 30,387,819.

## Verification before GPU preflight

- 37/37 repository tests PASS in the deployed runtime.
- The new test verifies finite forward/backward and nonzero gradients through
  relational fusion, spatial token projection, residual weight and flat head.
- Strict state-dict roundtrip reproduces every output bit-for-bit.
- The unchanged A40 configuration is backward compatible: matched-seed state
  SHA256 `822523d003dcc89bfb6c2f1b51b5bf0a617f7f5f4733c56b253e5fcd5df6fcd8`
  and output SHA256
  `1dbca5be618c01e3ff128bd591a889c9813f36839b1ede2141ba6235ef018935`
  are identical in the A40 and A41 snapshots.
- The generalized optimizer path is test-proven bit-exact to legacy AdamW
  under this config; optional optimizer/BatchNorm controls are not activated.

Immutable snapshot:
`/slurmshared/Ngoc/code/hcmus-density-convnext-hybrid-spatial-20260922-v1`.

Relevant SHA256 values:

- config: `6d7a1628eccd15bf064a32274ca20a75a6bc639c1a27b6237ec9bcb09e2df9a3`
- model: `f9eb126235aa3ef3b388e77f056fea0cefda74ee03f550c1a7cc3c78ce27ac90`
- engine: `1d8e4f9383f61bb7bfbc6d87dbabd2acbdc2aac909288bfad5652f3fed1e3e84`
- launcher: `01e5c7689f4ba0fed29ca0ebfffee6b47f7619c394d8f80dea8d81212107ea06`

## Execution and decision rule

First require a real cached `[2,4,3,512,512]` RTX 5090 forward/backward/update
preflight. If it passes, run only the fixed historically weak folds 1 and 3
for 50 epochs. Use no Vesta/worker2. Expand to folds 0/2/4 only if both audits
PASS, two-fold mean Macro-F1 >=0.70 and minimum >=0.65. Final acceptance still
requires CV5 mean >=0.70, sample SD <=0.05 and minimum >=0.65.
