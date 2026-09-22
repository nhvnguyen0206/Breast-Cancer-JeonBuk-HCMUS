# A44 preregistration: local-global four-view fusion

Registered before implementation or training results. A43 completed50 and
passed the CV5 artifact audit, but mean .7392163, sample SD .0935366 and
minimum .5850244 fail the active goal. Its weakest folds are1 and3.
The latest goal requests one screening fold first; choose fold1 by this
fixed ranking. Do not select a favorable fold or alter the frozen split.

## Hypothesis and architecture

A43 lets all80 regional tokens interact immediately. A44 will first build
one summary for each view through shared within-view attention, then learn
exam-level relationships between the four summaries. This may preserve
within-view composition and reduce unstable cross-view interactions; it is
a hypothesis, not an established cause of the A43 failure.

- Keep ConvNeXt-Tiny, its384/768-channel feature scales and4x4/2x2 pooling.
- Encode20 regional tokens plus a learned view-summary token separately for
  each view using a shared two-layer Transformer, dimension256,8 heads.
- Apply residual bottleneck adapters (256 ->32 ->256, GELU) keyed by CC/MLO
  and left/right to the four summaries; zero-initialize output projections.
- Fuse an exam token and four view summaries with a two-layer global
  Transformer, dimension256,8 heads. Keep explicit view/side embeddings.
- Retain A43's A-gate/conditional-BCD and auxiliary heads, normalization,
  losses, augmentation, optimizer, sampling and50-epoch schedule.
- No extra per-view loss or encoder unsharing in this arm. The changed
  experimental factor is the fusion architecture family. An improvement
  would not isolate adapters from local/global attention without ablations.
- One normalized four-class output, one model per fold, no ensemble.

## Protocol and decision gates

Use the existing VinDR window16 cache and grouped split, seed42, assignment
SHA256 43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.
Run only on RTX5090; exclude worker2/Vesta. Log to HCMUS-paper1.
Freeze the code/config snapshot after tests and a real-cache AMP smoke step.

Screen fold1 for50 epochs. Expand only after audit PASS and best-DEV
Macro-F1>=.72, B/C/D mean F1 at least A43 fold1's matched selected-checkpoint
value (mean of .5777777778,.8843537415,.6779661017), and QWK>=.6936709874.
These secondary gates prevent passing through A-only recovery with degraded
common-class discrimination. Reject the candidate if screening fails; do
not loosen gates or tune fold-specific thresholds. If passed, preserve fold1
and train remaining0/2/3/4 unchanged, then audit and assess final CV5.

Final acceptance: mean Macro-F1>=.72, sample SD<=.03, min fold>=.65, all
class F1/accuracy/QWK/confusion matrices, one seed42 and one inference path.
Report selected-DEV separately from independent evaluation; no independent
test estimate is claimed. Report results every10--20 epochs or completion.

## Required implementation checks

Check aligned fine/coarse shapes, output normalization, finite nonzero
gradients through both scales/local/global/adapters, deterministic eval and
strict checkpoint roundtrip. Verify local summaries are independent across
views before global fusion, and masked views cannot affect exam output when
the fusion's mask interface is used. Full images use the current four-view
loader; do not claim missing-view training support merely from a unit test.
Check architecture IDs in training/inference and both auditors. Complete a
real-cache512x512 AMP forward/backward preflight before the50-epoch screen.

Status: implemented and locally validated (50 tests PASS); user explicitly
approved the Atlas destination after the initial review rejection. Remote
tests and real-cache RTX5090 preflight1049 PASS. Fold1 training1050_1 is
RUNNING; see `vindr_a44_local_global_launch_20260922.md`.
