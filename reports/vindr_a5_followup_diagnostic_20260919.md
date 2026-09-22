# A5 paired errors and training dynamics

Read-only analysis of audited A1/A5 selected-DEV reports and completed
A5 histories, all five frozen folds. No retraining, selection-rule change,
ensemble, or independent-test claim. Companion JSON records history values.

## Paired class changes

Mean class F1 change A5 minus A1: A -0.0133333, B +0.0411516,
C +0.0027485, D +0.0608445. BCD mean rises from 0.7021895 to
0.7371044. D improves on four folds, B on three (one unchanged),
C on three. Fold0 deteriorates on all B/C/D, so the gain is not universal.

Pooled confusion counts (descriptive, not an ensemble):

| Error | A1 | A5 |
|---|---:|---:|
| A to B | 2 | 3 |
| B to A | 3 | 0 |
| B to C | 55 | 45 |
| C to B | 93 | 92 |
| C to D | 66 | 92 |
| D to C | 127 | 96 |

A5 recovers 31 additional D cases at the cost of 26 additional C-to-D
errors. Correct B cases increase 138 to 151. Correct A cases decrease
4 to 3. The mean gain is therefore not an improvement in a few A cases,
but A scarcity still drives very large variability in the four-class score.

## Training dynamics

| Fold | Selected epoch | Selected F1 | Epoch50 F1 | Last10 mean F1 | Epochs >= .75 |
|---|---:|---:|---:|---:|---:|
| 0 | 30 | .789650 | .514793 | .498406 | 5 |
| 1 | 8 | .579231 | .511904 | .510217 | 0 |
| 2 | 5 | .799100 | .510282 | .494195 | 1 |
| 3 | 3 | .570186 | .509464 | .517960 | 0 |
| 4 | 27 | .775974 | .752730 | .734042 | 6 |

Epoch50 A F1 is zero on folds0--3 and one on fold4. Training focal,
binary and neighbor losses become small, yet DEV B/D remain imperfect.
This is consistent with a generalization gap but not proof of its cause:
training loss is measured under augmentation/dropout and is not a clean
FIT-versus-DEV inference comparison. Ordinal loss remains around .514;
its scalar size does not prove gradient domination (see prior CORAL floor
diagnostic). No gradient-conflict measurement was made here.

AMP skipped updates total 16/18/16/17/15 across folds0--4. They are sparse
and occur beyond initialization too, not only epoch1. Histories alone do
not establish them as the cause of F1 deterioration. Finite scalar losses
must not be described as proof that all optimizer updates occurred.

## Next controlled question

Test whether modest minority exposure improves B/D and preserves A without
changing inference: A6 candidate uses sampling_power=0.25 relative to A5,
keeping dropout .3, augmentation, LR, losses and all protocol settings.
Sampling changes training class exposure, so improvement is a hypothesis,
not assured. Prior O2 used this power on a different low-LR baseline and
did not improve its parent CV5; do not present that prior result as support.
Only fixed fold0 may be screened first, fresh initialization, full50 and
audit; expand remaining folds only if selected four-class DEV F1 >= .75.
No configuration or cluster job for A6 has been created yet.
