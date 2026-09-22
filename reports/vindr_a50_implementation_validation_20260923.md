# A50 implementation validation

A50 passed every registered implementation invariant and the real-cache
RTX5090 preflight before training was launched. No A50 training metric was
available or inspected during these checks.

## Implemented treatment

Architecture
`convnext_tiny_hybrid_spatial_a_gate_projection_adapters_v17` preserves A42
and adds two 384-to-96-to-384 residual feature adapters after ConvNeXt feature
block 5. L-CC/R-CC share one adapter and L-MLO/R-MLO share the other. Each
adapter uses GroupNorm, two 1x1 projections and GELU; the output projection is
zero initialized. The model remains a single end-to-end predictor.

## Validation evidence

- Local syntax checks passed.
- Focused A42/A47/A48/A49/A50 tests passed 20/20.
- The complete test suite passed 82/82.
- At 512x512 with the production configuration, all outputs were finite and
  shaped 4/3/2 for primary/ordinal/binary logits.
- A42 has 32,367,980 parameters; A50 has 32,517,932, an increase of 149,952.
- Under matched seeds, shared state, construction CPU RNG, train-mode outputs,
  post-forward CPU RNG and post-forward CUDA RNG are bit-exact.
- The adapter output projection received finite non-zero first-step gradient;
  its bottleneck received finite non-zero gradient after the output projection
  became non-zero.
- Local and Atlas hashes match for every deployed A50 source/config/test file.
- Atlas focused tests passed 20/20.
- CUDA parity job1076 passed on NVIDIA GeForce RTX 5090. The first submission,
  job1075, exited before model construction because its launcher omitted
  `src` from `PYTHONPATH`; job1076 corrected only the launcher environment.
- Real VinDR cache preflight job1077 passed on RTX5090 with input shape
  2x4x3x512x512, finite loss 1.4355605, finite gradient norm 18.8586 and peak
  allocated memory 2.7185 GiB. AMP skipped one initial update and recovered on
  the next real batch within the registered eight-batch bound.

## Deployment identity

Immutable snapshot:
`/slurmshared/Ngoc/code/hcmus-density-projection-adapters-20260923-v1`

- model: `c3e8e763ef9791576f2c6ffbe1fccd0cf165f233558568ddf0eed1f57639f9c0`
- engine: `2d778b34b0718501643ff8b509624cc3fa591665e18a9b6d4717cfe46fb724fe`
- config: `c751dc8dd4665d948fc16b5b89f3a770a3f5b461e9226ed593caccd73bfc92f4`
- A50 tests: `df8d2fd980930a90f592982289694fbc291a8142c428e04c25e21bcd48cc756c`
- CUDA verifier: `c0e3905ef904d3c57b932ba70b1a1a9b9502477b9eefc89ca793c407b34e8977`

The registered fold2/fold3 screen is therefore unlocked. Folds0/1/4 remain
locked until both weak folds pass all preregistered gates.
