# A45 preregistration: local summaries with per-view auxiliary supervision

Registered before implementation or training results. A44 showed that
local/global fusion can produce a high selected Macro-F1 on fold1, but only
when its single A exam is correct; B/C/D and QWK regress and A recovery occurs
in only one of 50 epochs. The next hypothesis is that the local view summaries
are insufficiently constrained by the exam-level objective.

## Controlled change

Retain A44's ConvNeXt-Tiny two-scale encoder, shared within-view Transformer,
CC/MLO and left/right residual adapters, global four-view Transformer,
A-gate conditional B/C/D exam head, auxiliary ordinal/binary exam heads,
augmentation, optimizer, sampling, seed and 50-epoch schedule.

Add one shared four-class linear head to the four local view-summary tokens.
During training only, apply the exam density label to each view and average a
class-balanced focal loss across the four views. Add it to the existing loss
with fixed coefficient `0.25`. The sole deployed inference output remains the
normalized exam-level four-class distribution; no ensemble or averaging of
view predictions is allowed.

This arm changes one hypothesis group: supervision of the local representation.
Four view losses do not create four independent labels; they provide four
view-specific gradients for the same exam label. Claims must therefore remain
at exam level.

## Protocol and gates

Use the frozen VinDR cache/grouped split, seed42, fold1, assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Run 50 epochs on RTX5090 only and exclude worker2/Vesta. Log to W&B project
`HCMUS-paper1` from an immutable snapshot after tests and a real-cache AMP
preflight.

Expand only if the completed fold1 audit PASSes and the selected checkpoint
meets all three gates: Macro-F1 >= 0.72, B/C/D mean F1 >= 0.7133658737, and
QWK >= 0.6936709874. Also report the number and longest consecutive run of
epochs with positive A F1; this is diagnostic and cannot replace the gates.
If any gate fails, reject A45 without expanding or retuning on fold1.

Final CV5 acceptance remains mean Macro-F1 >= 0.72, sample SD <= 0.03 and
minimum fold >= 0.65, with all class F1/accuracy/QWK/confusion matrices and
one registered inference path. All values are selected DEV unless a genuinely
independent evaluation is later introduced.

Status: preregistered; implementation and launch pending.
