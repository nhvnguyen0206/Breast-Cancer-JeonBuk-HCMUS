# A45 implementation and local validation

Implemented architecture
convnext_tiny_local_global_view_transformer_perview_aux_v12.
A45 retains A44's complete exam-level inference path and adds one shared
four-class linear classifier over the four local view summaries. Its
class-balanced focal loss is averaged over views and enters the training
objective at the preregistered coefficient 0.25. Inference continues to use
only the normalized exam-level flat_logits; view logits are neither averaged
nor ensembled.

The A45 configuration differs from A44 only in the experiment arm,
model.view_auxiliary=true, and loss.view_auxiliary=0.25.

Local validation in /home/tyler/miniconda3/envs/paper_1:

- All 59 repository tests PASS in 30.498 seconds.
- Ten focused A44/A45 tests PASS, covering auxiliary gradients, local encoder
  gradients, loss/shape validation, v11 backward compatibility, strict v12
  checkpoint roundtrip, and bit-exact initialization of every shared
  parameter under the same seed.
- Production configuration forward on synthetic [1,4,3,512,512] PASS with
  finite normalized exam probabilities summing to 1.0.
- Output shapes are exam logits [1,4], ordinal [1,3], binary [1,2], and
  training-only view logits [1,4,4].
- Parameter count is 31,554,797.
- Syntax compilation and whitespace checks PASS.

Source SHA256:

- model.py: a392080188884344554f39bad936df4553eaa984d81cc44e5c1370acf3f5c49d
- loss.py: a26ceebe584032614e9d22d4de3b0fe6acf3e2d9c46dcce74446020bbe4d6f37
- engine.py: 598f3296bb10a188a23109be4d2dc4a076e82dd19f9c9fff7d109ff8de79a9a9
- A45 config: a273ad22c8b7e57d79990d3912f584269991b76217b9177cdd3605d30203398c
- A45 tests: bc4582c827a9f4454933de566784e845e9cf953a9b20b5bb60f195dd55e7c0b4

## Deployment status

The earlier deployment block was resolved by the user's explicit authorization.
The exact tested files were deployed to the intended immutable snapshot,
remote hashes and ten focused tests match, real-cache RTX5090 AMP preflight
1052 PASS, and fold1 job 1053_1 was observed RUNNING. Worker2/Vesta is
excluded. See vindr_a45_per_view_auxiliary_launch_20260922.md.
