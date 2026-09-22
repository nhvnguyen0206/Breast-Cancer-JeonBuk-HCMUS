# A50 preregistration: projection-specific feature adapters

Registered after A49 first20 and before A49 final results, A50 implementation
or training. A49's controlled RNG repair restores A42-like rare-A behavior but
does not improve the two weak folds through epoch20. Across A40--A49, global
and spatial attention, local/global token fusion, per-view auxiliary loss,
MixStyle, output-head factorization and a fine-scale D expert have all failed
to meet the stability screen. The remaining untested structural hypothesis in
the registered search policy is negative transfer from sharing the complete
image encoder between CC and MLO projections.

## Controlled structural change

Use audited A42 as the control. Preserve its ImageNet-pretrained ConvNeXt-Tiny
backbone, global hierarchical relational fusion, residual spatial attention,
A-vs-rest plus conditional B/C/D head, ordinal/binary auxiliary heads, losses,
augmentation, sampling, optimizer and schedule.

At the 384-channel ConvNeXt feature stage, before the final downsampling/stage,
add two projection-specific residual adapters:

- one adapter shared by L-CC and R-CC;
- one adapter shared by L-MLO and R-MLO;
- each adapter is a low-capacity spatial 1x1 bottleneck with normalization and
  a zero-initialized output projection;
- left and right breasts continue sharing the same projection adapter, so the
  treatment adds projection specialization without side-specific memorization;
- the adapted maps continue through the existing shared upper ConvNeXt stage
  and the unchanged A42 fusion/head.

This is partial encoder unsharing at the feature-map interface, not another
token-fusion or scalar-loss tweak. The inference graph is one end-to-end model
and produces one normalized four-class distribution; no ensemble, threshold,
calibration or test-time averaging is introduced.

## Initialization and implementation requirements

Register architecture
`convnext_tiny_hybrid_spatial_a_gate_projection_adapters_v17`. Construct the
adapter modules after all A42 modules while restoring CPU RNG, and keep adapter
forward deterministic. Zero initialization must make A42/A50 shared state,
initial train/eval outputs, construction RNG and post-forward RNG bit-exact
under matched seeds. The adapter output projection must receive a finite
non-zero gradient on the first update; its upstream bottleneck must receive a
finite non-zero gradient after that projection becomes non-zero. Reject the
implementation before training if any invariant fails.

## Fixed screen and gates

Do not launch A50 until A49 completes its registered epoch50 audits and is
accepted or rejected. Then screen only frozen folds2/3 for 50 epochs on RTX5090
with worker2/Vesta excluded, assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
the registered cache and seed42. Keep W&B offline until external aggregate
upload permission is explicit.

Expand to folds0/1/4 only if both local audits PASS and all gates hold:

- each fold Macro-F1 >= `.72`;
- two-fold Macro-F1 sample SD <= `.03`;
- B/C/D mean >= `.7216976152`, minimum >= `.6808637798`;
- QWK mean >= `.6572337361`, minimum >= `.6050383049`.

The two weak folds must improve together: holding A42 folds0/1/4 fixed, changing
fold2 alone cannot reduce final CV5 sample SD below `.03` (its numerical lower
bound is approximately `.03255`). For orientation, fold2 and fold3 near `.76`
would yield CV5 mean about `.78008` and SD `.02881` if the other A42 folds were
preserved. This arithmetic is a design constraint, not a predicted result.

Report per-class F1, accuracy, QWK, confusion matrices, positive-A epochs and
adapter norms. Scores remain selected DEV, not an independent test. Final CV5
acceptance remains mean Macro-F1 >= `.72`, sample SD <= `.03` and minimum
fold >= `.65`.

Status: preregistered; implementation and real-cache RTX5090 preflight passed.
The registered folds2/3 screen is unlocked; folds0/1/4 remain locked until all
screening gates pass.
