# A52 preregistration: multiscale rare-A expert

Registered after A51 first20 and before inspecting its first40/final results.
A52 is conditional and must not train unless A51 completes, both read-only
audits pass, and A51 fails at least one registered expansion gate.

## Evidence and hypothesis

A42 remains the strongest audited mean model, but its A-gate built on the
hybrid relational/spatial exam vector is unstable on fold2. A43's full
multi-scale four-view Transformer produced a materially persistent A decision
region on fold2 and selected Macro-F1 `.7994428`, but replacing the complete
A42 representation destabilized fold1 and increased CV5 SD to `.0935366`.
A51 first20 retains the stronger A42 base and adds bilateral spatial evidence,
yet fold2 has only one isolated positive-A epoch and no epoch at or above
`.72`.

The registered hypothesis is therefore narrower than another fusion
replacement: A43's multi-scale representation is useful specifically for the
rare A-vs-rest boundary, while A42's hybrid representation should remain the
sole source for conditional B/C/D, ordinal and binary predictions.

## Structural change

Use A42 as the unchanged base. In parallel, extract the 384-channel
intermediate and 768-channel final ConvNeXt maps for all four canonical views.
Feed them to the already tested A43 `MultiScaleViewTokenFusion` with registered
4x4/2x2 grids, 256-dimensional tokens, eight heads and two Transformer layers.
Normalize its 768-dimensional exam vector and map it to one A-vs-rest residual
logit through a zero-initialized linear projection.

The final A logit is `A42_A_logit + multiscale_A_residual`. A42's conditional
B/C/D logits, ordinal logits, binary logits and all existing losses remain
unchanged. The expert is trained end-to-end through the same normalized
four-class distribution; there is no auxiliary checkpoint, probability
averaging, TTA, calibration or ensemble. Inference has one shared backbone,
one graph and one four-class output.

Register architecture
`convnext_tiny_hybrid_spatial_a_gate_multiscale_a_expert_v19`. Construct the
expert after every A42 module inside a CPU RNG fork and run its stochastic
forward inside CPU/CUDA RNG forks. Under matched seeds, A42/A52 shared state,
construction RNG, initial train outputs and post-forward RNG must be bit-exact.
The zero-initialized residual projection must get finite non-zero gradient on
the first update; upstream expert projections/attention must get finite
non-zero gradients after that projection becomes non-zero.

## Frozen protocol and gates

Keep the exact A42/A51 cache, five-fold assignments, seed42, augmentation,
sampling power `.25`, optimizer, schedule, losses, 512x512 input and 50-epoch
selection rule. W&B remains offline; run only on RTX5090 with worker2/Vesta
excluded. Screen folds2/3 first, never folds0/1/4 unless both audits PASS and:

- each fold Macro-F1 >= `.72`;
- two-fold Macro-F1 sample SD <= `.03`;
- B/C/D mean >= `.7216976152`, minimum >= `.6808637798`;
- QWK mean >= `.6572337361`, minimum >= `.6050383049`.

Report accuracy, QWK, per-class F1, confusion matrices, A-positive epoch count
and streak, epochs at/above `.72`, and the expert output-projection norm. These
are selected DEV estimates, not an independent test. Final CV5 acceptance
remains mean Macro-F1 >= `.72`, sample SD <= `.03`, and minimum fold >= `.65`.

Status: preregistered and locally validated. Audited A51 rejection satisfies
the dependency, so Atlas hash/tests, CUDA parity and real-cache RTX5090
preflight are unlocked. Training remains locked until every validation passes.
