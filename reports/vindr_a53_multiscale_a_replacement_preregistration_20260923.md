# A53 preregistration: multiscale A-gate replacement

Registered after A52 first20 and before inspecting its first40/final results.
A53 is conditional and cannot train unless A52 completes, both audits pass,
and at least one registered expansion gate fails.

## Evidence and hypothesis

A43's full multi-scale four-view representation uniquely repaired fold2's rare
A region and reached Macro-F1 `.7994428`, but using it for every task weakened
other folds. A42 retains the strongest audited overall representation for
B/C/D. A52 attempted to combine these strengths by adding a zero-initialized
multi-scale residual to A42's existing A logit. Through epoch20, however,
fold2 remains `.6034620` with one isolated positive-A epoch, while improvement
and expert-norm growth occur only on fold3.

The registered hypothesis is that A42's established A logit dominates a small
corrective residual and prevents the A43 decision geometry from forming. The
next structural test therefore assigns the A decision exclusively to the
multi-scale representation, while retaining A42 exclusively for the remaining
tasks.

## Structural change

Use one shared ConvNeXt-Tiny backbone and compute two exam representations:

- the unchanged A42 hierarchical relational plus spatial-residual exam vector;
- the tested A43 `MultiScaleViewTokenFusion` over all four 384/768-channel
  feature-map scales using 4x4/2x2 grids, 256-dimensional tokens, eight heads
  and two Transformer layers.

Apply A42's existing single `a_gate` linear layer to the normalized multi-scale
exam vector, not the A42 exam vector. Apply A42's conditional B/C/D head,
ordinal head and binary head only to the A42 exam vector. The final four-class
distribution remains the normalized hierarchical composition of this one A
logit and one conditional B/C/D distribution.

There is no residual mixing coefficient, duplicate classifier, auxiliary
checkpoint, probability averaging, TTA or calibration. This is a single
shared-backbone computation graph and not an ensemble. Register architecture
`convnext_tiny_hybrid_bcd_multiscale_a_gate_v20`.

Construct the new fusion after every A42 module inside a CPU RNG fork so all
shared parameters and construction RNG remain bit-exact. Run its stochastic
forward inside CPU/CUDA RNG forks. Initial outputs are intentionally not
required to equal A42 because the registered treatment replaces the A-gate
input from update zero. Strict roundtrip, finite normalized output, non-zero
gradient through the A gate/fine/coarse projections/attention, production
512x512 forward/backward, CUDA RNG parity and real-cache RTX5090 update are
mandatory.

## Frozen protocol and gates

Keep the exact cache, assignments SHA256, seed42, augmentation, sampling
power `.25`, losses, optimizer, schedule, 512x512 input and 50-epoch selection
rule. Keep W&B offline and use RTX5090 only, excluding worker2/Vesta. Screen
folds2/3 first and expand only if both audits PASS and:

- each fold Macro-F1 >= `.72`;
- two-fold Macro-F1 sample SD <= `.03`;
- B/C/D mean >= `.7216976152`, minimum >= `.6808637798`;
- QWK mean >= `.6572337361`, minimum >= `.6050383049`.

Report per-class metrics/confusions, A-positive count/streak and epochs at or
above `.72`. These are selected DEV estimates, not independent test results.
Final CV5 acceptance remains mean Macro-F1 >= `.72`, sample SD <= `.03`, and
minimum fold >= `.65`.

Status: preregistered and locally validated. Audited A52 rejection satisfies
the dependency, so Atlas hash/tests, CUDA parity and real-cache RTX5090
preflight are unlocked. Training remains locked until every validation passes.
