# A36 preregistration: view-token attention fusion

A36 is the first substantive architecture arm under the revised goal. It
retains the DenseNet121 ImageNet feature extractor, four-view input, A30 data/
augmentation/sampling/loss/optimizer settings and three prediction heads, but
replaces the complete handcrafted fusion path (CC/MLO scalar gates,
absolute-difference/product relations, side gate and bilateral MLP) with a
learnable attention encoder over the four view vectors.

Each 1024-dimensional view vector is projected to 256 dimensions. Factorized
learned embeddings identify CC versus MLO and left versus right. A learned
exam token and two pre-norm Transformer encoder layers (8 heads, feed-forward
dimension 1024, attention dropout 0.10) model all four views jointly. The exam
token is projected back to 1024 dimensions for the unchanged flat, CORAL and
binary heads. Output dropout remains 0.40. This is a single model and a single
flat-head inference path, not an ensemble.

Hypothesis: joint attention can learn view-dependent and bilateral relations
that the fixed average/absolute-difference/product representation cannot,
particularly for the historically difficult folds 1 and 3. This is a major
fusion change, not a claim that attention is inherently superior.

The architecture has 9,070,473 trainable parameters versus 11,163,787 for the
A30 relational model. Default relational construction in the new source is
state-dict identical and produces bit-exact outputs to immutable A30 under a
matched seed, protecting backward compatibility.

Use the fixed two-fold stress screen: folds 1 and 3, 50 epochs, seed 42, RTX
5090, worker2/Vesta excluded. Launch only after A35 completes and is audited.
Expand to folds 0/2/4 only if both screen audits PASS, two-fold mean Macro-F1
>=0.70 and minimum >=0.65. Final CV5 gates remain mean >=0.70, sample SD
<=0.05 and minimum >=0.65. Selected DEV is not independent-test evidence.

## Prepared immutable snapshot

Prepared, but not launched:
`/slurmshared/Ngoc/code/hcmus-density-viewtoken-attention-20260921-v1`.
Frozen assignment SHA256 remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Config SHA256 is
`a248ba636a1ebea59ed16abe6d97a996a5ac84e4ee3d9c02d6d6fe1a55c75cf3`;
model source SHA256 is
`c3ec7148847801f0bfe27c63f1ee5ef1936a99ff60294516221204b46b010b20`;
minimal engine SHA256 is
`3eb8214a7bdb2a04a695f3f7ed6661e8df895064b86cc19454c99fecf494fca4`.
Snapshot tests pass 17/17, including attention shape, finite-gradient,
identity-embedding and invalid-configuration checks. A real RTX 5090 cache
batch preflight is still required after A35 and before submission.

The production checkpoint path was also exercised directly in the immutable
snapshot: an attention model was saved with its architecture/config metadata,
reloaded through `engine.load_model` with strict state-dict loading, and all
three output tensors were bit-exact on the same input. Result:
`ATTENTION_CHECKPOINT_ROUNDTRIP_PASS`.

After A35's final audits passed and its screen was rejected, the real cached-
batch preflight ran on `NVIDIA GeForce RTX 5090` with input shape
`[2,4,3,512,512]`. Forward/loss/backward/gradient clipping and an AdamW update
all completed with finite values under AMP. GradScaler skipped the first two
overflowing warm-up updates and recovered on the third, matching the training
engine's intended recovery behavior. Peak allocated memory was 2.686 GiB.
Preflight result: PASS.
