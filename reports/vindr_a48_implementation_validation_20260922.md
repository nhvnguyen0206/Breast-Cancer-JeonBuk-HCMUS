# A48 implementation validation

Status: implementation and real-cache RTX5090 preflight complete. No training
result was inspected while implementing or validating this treatment.

## Registered treatment

Architecture `convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_v15` retains
the complete A42 path and its A-vs-rest plus conditional B/C/D probability
head. It captures the 384-channel ConvNeXt stage-5 feature maps, fuses the four
canonical views through one spatial-token attention module, and adds one
zero-initialized scalar residual only to the conditional D logit. It remains a
single end-to-end model with one four-class distribution; no ensemble,
threshold, post-hoc calibration or test-time averaging is introduced.

The treatment modules are constructed after every A42 module. Under seed42,
all shared state tensors are bit-exact and the complete initial A42/A48 outputs
are bit-exact in evaluation mode. The zero-initialized final projection gets a
non-zero finite gradient on the first backward pass; after one optimizer step,
the upstream fine-feature attention also receives a non-zero finite gradient.

## Local validation

- Python syntax: PASS.
- Focused A42/A47/A48 suite: 14/14 PASS.
- Complete repository suite: 76/76 PASS.
- `git diff --check`: PASS.
- Synthetic production-shape inference `[1,4,3,512,512]`: PASS; finite outputs
  of shapes `[1,4]`, `[1,3]`, `[1,2]`, probability-sum error `0.0`.
- Initial A42/A48 output equality at 512x512: bit-exact PASS.
- A42 parameters: 32,367,980; A48 parameters: 34,152,301; treatment adds
  1,784,321 parameters (5.51%).
- Config comparison: only the comment, registered arm name and
  `model.fine_d_expert: true` differ from A42.

## Atlas snapshot validation

Snapshot:
`/slurmshared/Ngoc/code/hcmus-density-fine-d-expert-20260922-v1`.
It was copied from the immutable A42 snapshot and only the registered A48
implementation, config, auditors, launch/preflight scripts, tests and reports
were overlaid. Local and remote SHA256 values match for every treatment-critical
file. With the snapshot's registered `.deps` path active, the focused
A42/A47/A48 suite passes 14/14 on Atlas. The first verification invocation did
not include `.deps` and therefore stopped during import because the base Python
environment does not contain OpenCV; this was an invocation-environment issue,
not a model/test failure.

Critical SHA256 values:

- `src/tn_mammo/model.py`: `5b5f23bde1e5955943c23186556617cda32f52e1f879c76aec194c8650100a64`
- `src/tn_mammo/engine.py`: `85fe44b72c8092e02e93c34ca2300b5f72fec0143b16ee22bb0dcc9ad1960524`
- A48 config: `17a883798b1e2a736edec573276d75d5ed0963afe062a9f4a0d034794aac1eff`
- A48 tests: `40e47189f7864166d2e6cf51dbf5b470a995ba5b416548b020ca821e74985529`
- screen auditor: `29cce04f7882e256f1be4f82370dab3c9c63c70a89aaf93ba7d9cf665f45a216`
- CV5 auditor: `c52c7c1f2c31f23ee0cc1a16fa148c7544f54073877245436ce18a9c00fd22b9`

The preregistered fold2/fold3 gates and the frozen split/cache/seed remain
unchanged. Scores from these folds are selected DEV and not an independent
test.

## Real-cache RTX5090 preflight

Slurm job 1065 ran on `NVIDIA GeForce RTX 5090` using fold2 FIT cache tensors
with production batch shape `[2,4,3,512,512]`. Forward, backward, gradient
clipping and optimizer update completed under AMP. The loss and all output
tensors were finite; AMP recovered after three skipped scale updates, peak
allocated memory was 2.719 GiB, and the preflight result was PASS. The
two-fold training launch remains pending explicit approval for the narrowly
defined aggregate-only W&B payload.
