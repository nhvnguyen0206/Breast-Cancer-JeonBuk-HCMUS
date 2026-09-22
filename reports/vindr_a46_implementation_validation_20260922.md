# A46 implementation and local validation

Implemented architecture
`convnext_tiny_local_global_view_transformer_perview_aux_mixstyle_v13`.
A46 retains A45's complete single-model inference path and adds one
parameter-free, training-only ExamMixStyle operation after ConvNeXt's fine
stage. It mixes channel-wise feature mean/standard deviation with a different
exam while preserving corresponding L-CC/L-MLO/R-CC/R-MLO view identity.
One Beta(.1,.1) coefficient is shared across all views and channels of each
exam; application probability is .5. Batch size two always swaps exams, so
the pairing cannot be an identity permutation.

Evaluation disables the operation before any random draw and is bit-exact to
A45 under identical initialization/state. A46 therefore adds no parameters,
inference branch, threshold, test-time augmentation, averaging or ensemble.
The parameter count remains 31,554,797.

The A46 configuration differs from A45 only in `experiment.arm`,
`model.mixstyle_probability=.5`, and `model.mixstyle_alpha=.1`.

Local validation in `/home/tyler/miniconda3/envs/paper_1`:

- All 65 discovered repository tests PASS.
- Six new MixStyle tests and ten A44/A45 compatibility tests PASS (16/16).
- Tests cover forced non-identity pairing, one coefficient across four views,
  validation, exact evaluation bypass, full forward/backward gradients,
  registered v13 architecture, bit-exact A45 shared initialization/evaluation,
  and strict checkpoint roundtrip.
- Production-shape synthetic inference `[1,4,3,512,512]` PASS with finite
  normalized exam probabilities summing to 1.0.
- Output shapes remain exam logits `[1,4]`, ordinal `[1,3]`, binary `[1,2]`,
  and training-only auxiliary view logits `[1,4,4]`.
- Syntax compilation and whitespace checks PASS.

Source SHA256:

- `model.py`: 409208362dfc73db59cc4bdc613abd94936ccbeced862aa6588a0309f58192ae
- `engine.py`: b4ceefc0fa20d4c293940a1cf249342a75528f8b924f9f281784cf1d8bb9aeae
- A46 config: 082b146a6eea8d4fbb662c232af3cf55c9a2fde0b9ae74ed4cdfcde604641681
- A46 tests: 54b558a32e14d499260d05296126b674dd0ac10cec8a927f86c5c16f94f1c8f9
- screen auditor: 2982b8a528959931e87deb4710174f1610fa08637a9cd5a097dd3d4ae9397f82
- CV5 auditor: 78ce06e19d3d99aad5c4a52ce36035976d6bccb75f2ad1add2034bf122786f8f

Deployment and real-cache RTX5090 AMP preflight remain pending at the time of
this report.
