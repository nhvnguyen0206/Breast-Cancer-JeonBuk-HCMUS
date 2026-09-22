# A9 fold-1 diagnostic

This is a read-only diagnosis of the completed A9 fold1 run
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-791-fold1`, compared with the
same frozen fold in substantive parent A5
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-771-fold1`.

## The split is not density-count imbalanced

Fold1 DEV support is A/B/C/D = 1/39/312/51, the same total and essentially
the same density distribution as folds2 and4. The assignment hash and exact
membership passed the completed CV5 audit. Numerically inspected cache views
for the six A cases and nine false-A B cases were present, finite and
nonconstant. These checks do not establish anatomical crop quality or label
correctness, and do not rule out issues in uninspected cache records. No
density-count or manifest-membership split error was identified.

Fold1 is systematically low across completed arms: its Macro-F1 lies between
approximately 0.55 and 0.62 in all 13 audited CV5 variants. This is mainly a
protocol/data limitation: one missed A case fixes A-F1 at zero and contributes
one quarter of four-class Macro-F1. In A5, fold1 has Macro-F1 0.5792 but B/C/D
mean F1 0.7723, so the apparent gap greatly overstates the ordinary-density
degradation.

## A9 adds a real A/B boundary failure

A5 selected epoch8 confusion matrix:
`[[0,1,0,0],[0,35,4,0],[0,19,283,10],[0,0,21,30]]`.
It misses the one A case, but predicts no non-A case as A. Its class F1 is
`[0,.7447,.9129,.6593]`, accuracy .8635 and QWK .7101.

A9 selected epoch28 confusion matrix:
`[[1,0,0,0],[9,20,10,0],[0,13,285,14],[0,0,24,27]]`.
It recognizes the one A case but sends nine B cases to A. Its class F1 is
`[.1818,.5556,.9033,.5870]`, accuracy .8263 and QWK .6644. Eight of those
nine false-A B cases have p(A) above .995; the ninth has p(A)=.655. A5
classified all nine as B, generally with p(B) above .81. This is a strongly
overconfident boundary shift, not a threshold-level tie.

Paired best-checkpoint predictions show 16 A9 corrections versus 31 A9
regressions relative to A5. A9's Macro-F1-selected checkpoint has B/C/D mean
F1 .6820. Even selecting A9's best B/C/D epoch (epoch8) reaches only .7364,
still below A5's .7723. Thus the observed degradation is not solely a
Macro-F1 checkpoint-selection artifact. It is associated with dropout .5 in
this seed; a general causal conclusion requires replication.

## Mechanism supported by the configuration

A9 changes only dropout .3 -> .5. That dropout is applied inside both the
shared CC/MLO relational fusion and bilateral relational fusion. At the same
time, fold1 FIT has only five unique A cases. With beta=.999, effective-number
focal weights for fold1 are approximately `[3.7457,.1286,.0263,.0995]` for
A/B/C/D: one A example is weighted about 29x a B example and 143x a C
example. These are per-example weight ratios, not measured aggregate gradient
contributions. Increased dropout destabilizing a scarce-class boundary is a
hypothesis, not an isolated mechanism demonstrated by this experiment.
Recognition of the sole DEV-A case accompanies high-confidence B->A false
positives.

The fold1 A cache case passes the numerical checks but has asymmetric
intensity statistics between left and right views. This does not establish
that it is anatomically atypical or wrongly labelled; visual review remains
outstanding. Six total A cases provide very limited rare-class evidence.

## Decision

Do not change the split, discard fold1, tune on its single A case, or use an
ensemble. Reject A9 and return to A5. A5 remains the substantive best CV5
model. Future one-factor screens should target calibration/adjacent B-C-D
boundaries and report A-F1 separately; no conclusion should be driven by one
A case. A3 tested beta=.99 on A1, not on A5. Its failure to beat A5 does not
rule out a controlled beta change on the A5 parent.

## Current A10 corroboration (interim, fold1 epoch42)

A10 fold1 best remains epoch2: Macro-F1 .5605285498, class F1
[0,.7123287671,.9161490683,.6136363636], BCD mean .7473713997,
accuracy .8635235732. All 42 evaluated epochs miss the single DEV A case;
A5 missed it in all50. Selected confusion matrix is
`[[0,1,0,0],[0,26,13,0],[0,7,295,10],[0,0,24,27]]`.
Fold2 selected class F1 is [1,.6582278481,.8903020668,.5625]: fold1
outperforms it in B/C/D despite much lower four-class Macro-F1. This
isolates the metric contribution of scarce A support, not the cause of the
A-case prediction failure. A10 is still running; do not treat interim
selection as a completed comparison or change the frozen split.
