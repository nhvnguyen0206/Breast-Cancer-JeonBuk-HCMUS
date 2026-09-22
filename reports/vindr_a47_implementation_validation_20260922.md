# A47 implementation and local validation

Implemented architecture
`convnext_tiny_hybrid_spatial_dual_endpoint_gate_multitask_v14`.
A47 retains A42's complete ConvNeXt hybrid relational/spatial representation,
A gate and auxiliary heads. The existing three-output `bcd_head` projection is
reinterpreted as one conditional D-vs-(B/C) logit and two conditional B/C
logits. The final positive normalized A/B/C/D distribution follows the
preregistered product factorization.

No module, parameter, threshold, inference branch or ensemble was added. A42
and A47 have identical state-dict keys, bit-exact initial values under seed42
and the same 32,367,980 parameters. The configuration differs from A42 only
in `experiment.arm` and `model.primary_head`.

Local validation in `/home/tyler/miniconda3/envs/paper_1`:

- All 70 discovered repository tests PASS.
- Ten focused A41/A42/A47 tests PASS.
- Five new tests cover normalized finite probabilities, all four controllable
  argmax regions, nonzero finite gradients through A gate, D/B-C projection
  rows and spatial attention, exact A42 initialization/parameter parity,
  strict v14 checkpoint roundtrip and invalid representation rejection.
- Production-shape synthetic inference `[1,4,3,512,512]` PASS with probability
  sum exactly 1.0 and unchanged output shapes `[1,4]`, `[1,3]`, `[1,2]`.
- Syntax compilation and whitespace checks PASS.

Source SHA256:

- `model.py`: 7f7dfd0f05178c7bd781506cfbd7a894b10d3dbbee8081c2beb9152dc9c3d1c9
- `engine.py`: 4708ced2cbeba6d217943137e3934e7075453b639e9072957ab18109d4b07a63
- A47 config: 1a4e62c43610cf85b60d19176d60451ede5d28f0ba4f5a117d23e96a2805282d
- A47 tests: ac92aaf0e65c3074ee42705ace81f8a064dfcc789fa7907252a61d90b06d7577
- screen auditor: 1cb3e27ceeeeebbfeecba6c6c55ba1ebf86344dbdb3bf216ec359179e4487608
- CV5 auditor: 6baff17664ab19e33696c615d8451b3630c0c0762793880c673e28a97c9bdd87

Deployment and real-cache RTX5090 AMP preflight remain pending at the time of
this report.
