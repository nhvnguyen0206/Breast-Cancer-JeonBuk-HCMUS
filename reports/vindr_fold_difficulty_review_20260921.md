# Fold difficulty review

This review separates the current early A34 ranking from persistent behavior
across completed experiments. It does not alter the frozen split.

## Current A34 at the common first-10 horizon

| Rank (worst first) | Fold | Macro-F1 | Main weakness |
|---:|---:|---:|---|
| 1 | 4 | 0.526866 | A F1 0.000; B 0.630; D 0.621 |
| 2 | 2 | 0.610368 | D F1 0.515 |
| 3 | 3 | 0.616801 | A F1 0.400; D 0.523 |
| 4 | 0 | 0.629048 | A F1 0.400 |
| 5 | 1 | 0.729744 | strongest at this early horizon |

Fold 4 is currently worst, but this is only a ten-epoch result. Its one A
case was predicted as B. Fold 2 misclassified 27/52 D cases as C, and fold 3
misclassified 24/52 D cases as C. Supports are otherwise nearly identical:
folds 0/1/2/4 contain one A case and fold 3 contains two; B/C/D counts differ
by at most one.

## Persistent pattern across 25 completed CV5 result files

| Fold | Mean selected Macro-F1 | Median | Mean F1 A/B/C/D |
|---:|---:|---:|---:|
| 0 | 0.780463 | 0.789650 | 0.973333 / 0.631872 / 0.881876 / 0.634769 |
| 1 | 0.573657 | 0.563956 | 0.078987 / 0.689588 / 0.903921 / 0.622133 |
| 2 | 0.666565 | 0.671794 | 0.578924 / 0.656077 / 0.894264 / 0.536994 |
| 3 | 0.619210 | 0.606002 | 0.327556 / 0.651635 / 0.898865 / 0.598782 |
| 4 | 0.653209 | 0.635454 | 0.572667 / 0.605106 / 0.877299 / 0.557763 |

Fold 1 is historically the hardest, overwhelmingly because its single A case
is rarely recognized. Fold 3 is the second-hardest and also has unstable A
recognition. Fold 2's persistent weakness is D; fold 4 is relatively weak on
both B and D. The current fold-1 first-10 score is therefore not sufficient to
declare that historical problem resolved.

No split should be changed or fold dropped: the six total A cases make any
fold-specific A estimate discrete and high variance. Continue A34 to 50 and
judge only the audited CV5 mean/SD/minimum gates, while using these class-wise
patterns to choose a later controlled intervention if A34 fails.

## Case-level evidence across available saved fold predictions

Across 30–44 available saved runs per fold, the sole fold-1 A case
`695d09e0fdad29a27dff29500d352008` was correctly classified only 7/30 times.
Fold 3 contains two A cases: `a9b660b8266fab27e192128667f3828d`
was correct 19/31 times, while `b2de1bf8d49ecabeef05b60b2c4a8a0b` was
never correct (0/31). These cases explain much of the persistent fold-1 and
fold-3 difficulty.

By contrast, fold 4's A case `c488d7ef379be78343fd91eefa9cc477`
was correct in 25/31 saved runs. Its A34 first-20 failure is therefore more
consistent with configuration/training variability than an intrinsically
unrecognized case. Fold 0's A case was correct 40/44 times and fold 2's was
correct 27/31 times. Counts summarize saved selected-checkpoint predictions;
they are descriptive, not independent repeated trials.
