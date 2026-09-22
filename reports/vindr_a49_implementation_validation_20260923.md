# A49 implementation validation

Status: local and Atlas implementation validation plus real-cache RTX5090
preflight complete. No A49 training result was inspected during implementation
or preflight validation.

## Registered treatment

Architecture
`convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_rngisolated_v16` is
topologically identical to A48. It retains the complete A42 path and adds one
fine-scale four-view attention expert whose zero-initialized scalar residual
changes only the conditional D logit. A49 changes only incidental RNG handling:

- CPU RNG is forked and restored around construction of the fine-D modules;
- CPU and active CUDA RNG are forked and restored around the fine-D forward;
- stochastic operations on the original A42 path remain untouched.

It remains one end-to-end model with one four-class distribution. There is no
ensemble, threshold, post-hoc calibration or test-time averaging.

## Local validation

- Python syntax: PASS.
- Focused fine-D/A-gate/dual-endpoint suite: 15/15 PASS.
- Complete repository suite: 77/77 PASS.
- `git diff --check`: PASS.
- Config comparison against A48 offline: only the comment, registered arm name
  and `model.isolate_fine_d_rng: true` differ.
- Synthetic production-shape train-mode inference `[1,4,3,512,512]`: PASS;
  finite outputs of shapes `[1,4]`, `[1,3]`, `[1,2]`, probability-sum error
  `0.0`.
- Under identical seeds, A42/A49 shared state is bit-exact, construction RNG is
  bit-exact, complete initial train-mode outputs are bit-exact, and post-forward
  RNG is bit-exact.
- The treatment head receives a finite non-zero gradient; its upstream
  fine-feature attention receives gradient after the zero-initialized head's
  first update.
- A42 parameters: 32,367,980; A49 parameters: 34,152,301; treatment adds
  1,784,321 parameters (5.51%).

Critical local SHA256 values:

- `src/tn_mammo/model.py`: `5892159d342696ce51da5c6396bd3e2ff9e6983597b4014ab9e123037dd798a2`
- `src/tn_mammo/engine.py`: `3bf6190c95bb937feb5b11d6ef775e8fc747629d86d1b0d374726bd9932248a7`
- A49 config: `3e894552522c949acd71ba8180f7de3b05bc68143cc4135b87c3036d866086f7`
- A49 tests: `7cd322d77c7394aef78f990d8bb51760aebf9b134b444e5a8aceb1308861c11e`
- screen auditor: `51b9f595eb2712de4d76c92d7a0c5fd6cfac4e31fa41852edc11cd0fa23ef71f`
- CV5 auditor: `206702893af50129383ce0bd25d3bcb5f48239bd7436b0774568291c0af3d77c`

The frozen cache, split assignment, seed42, two-fold screen and expansion gates
remain exactly as preregistered. W&B remains offline pending explicit informed
permission for an external payload.

## Atlas snapshot and real-cache preflight

Immutable snapshot:
`/slurmshared/Ngoc/code/hcmus-density-rngisolated-fine-d-20260923-v1`.
Local and remote SHA256 values match for all treatment-critical files, and the
focused suite passes 15/15 inside the deployed snapshot. The snapshot was then
made recursively read-only.

Preflight job 1068 ran on `NVIDIA GeForce RTX 5090` using fold2 FIT cache
tensors with production batch shape `[2,4,3,512,512]`. Forward, backward,
gradient clipping and optimizer update completed under AMP. Loss and outputs
were finite; AMP recovered after three skipped scale updates, peak allocated
memory was 2.719 GiB, and the preflight result was PASS.
