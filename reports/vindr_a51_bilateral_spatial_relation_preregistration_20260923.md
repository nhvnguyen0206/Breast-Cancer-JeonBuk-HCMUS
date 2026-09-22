# A51 preregistration: orientation-aligned bilateral spatial relation

Registered after A50 first10 and before its first20/final results, A51
implementation or training. A42 remains the strongest audited parent (CV5
mean `.7592604`) but fails stability (sample SD `.0561945`), with fold2/3
Macro-F1 `.6773145/.7385653`. A43--A50 show that generic multi-scale tokens,
local/global attention, view auxiliary loss, MixStyle, endpoint/fine-D heads
and projection-specific adapters do not reliably repair the weak folds.

The untested structural hypothesis is that generic four-view attention lacks
the mammography-specific bilateral correspondence needed for stable density
features. A cache-geometry audit performed without labels on the first 100
frozen assignments found all L-CC tissue centroids left of image center and
all R-CC centroids right of center (mean normalized x `.4003/.5975`). Thus a
horizontal flip of right feature maps is required before spatial comparison.

## Controlled structural change

Use audited A42 as the control and preserve its ImageNet ConvNeXt-Tiny
backbone, hierarchical CC/MLO then left/right relational path, generic spatial
residual, A-gate primary head, ordinal/binary heads, losses, sampling,
augmentation, optimizer and schedule.

Add one parallel bilateral spatial-relation residual at the final 768-channel
feature-map stage:

- horizontally flip R-CC and R-MLO feature maps to align chest-wall direction;
- pool every map to the registered 4x4 grid;
- independently form symmetric CC and MLO relation maps as
  `[mean(left,right), abs(left-right), left*right]`;
- pass both relation maps through one shared 1x1 2304-to-256 projection,
  GELU, GroupNorm and a depthwise 3x3 spatial block;
- spatially pool the CC and MLO relation vectors, concatenate them in fixed
  CC/MLO order and project the 512-vector to the 768-dimensional exam space;
- zero-initialize the final projection and add the result residually to A42's
  existing exam feature before all heads.

The symmetric relation statistics prevent side-specific memorization, while
fixed CC/MLO ordering preserves projection identity. The generic A42 paths
remain intact. This is one end-to-end inference model with one four-class
distribution; it is not an ensemble, TTA or checkpoint averaging method.

## Initialization and implementation requirements

Register architecture
`convnext_tiny_hybrid_spatial_a_gate_bilateral_relation_v18`. Construct the
new module inside an RNG fork after every A42 module. Under identical seeds,
A42/A51 shared state, construction CPU RNG, train/eval initial outputs and
post-forward CPU/CUDA RNG must be bit-exact. The zero-initialized output
projection must receive finite non-zero gradient on update one; the shared
relation projection and depthwise block must receive finite non-zero gradient
after the output projection becomes non-zero. Strict state roundtrip, 512x512
finite forward/backward and real-cache RTX5090 update are mandatory.

## Fixed screen and gates

A51 remains locked until A50 completes 50 epochs and both read-only audits,
then is formally accepted or rejected. If unlocked, screen only frozen folds
2/3 for 50 epochs on RTX5090, excluding worker2/Vesta, with seed42, cache and
assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Keep W&B offline until external upload permission explicitly covers research
metrics/checkpoints.

Expand to folds0/1/4 only if both audits PASS and all gates hold:

- each fold Macro-F1 >= `.72`;
- two-fold Macro-F1 sample SD <= `.03`;
- B/C/D mean >= `.7216976152`, minimum >= `.6808637798`;
- QWK mean >= `.6572337361`, minimum >= `.6050383049`.

Report per-class F1, accuracy, QWK, confusion matrices, A-positive epochs and
bilateral-branch norms. Results are selected DEV, not independent-test
estimates. Final CV5 acceptance remains mean Macro-F1 >= `.72`, sample SD <=
`.03` and minimum fold >= `.65`.

Status: preregistered; implementation unlocked after audited A50 rejection.
Training remains locked pending every registered validation and real-cache
RTX5090 preflight.
