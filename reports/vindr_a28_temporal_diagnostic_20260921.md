# A6 versus A28: matched temporal diagnostic

Read original remote histories775/776 (A6) and965/966 (A28), all five
folds. Compare mean per-epoch B/C/D F1 over epochs1–10 and41–50;
diagnostic only, not an alternative checkpoint selection or target metric.

|Fold|A6 early BCD|A6 late BCD|A28 early BCD|A28 late BCD|
|---|---:|---:|---:|---:|
|0|.688720|.733758|.654865|.717116|
|1|.658389|.667476|.657469|.662288|
|2|.663286|.718868|.660785|.626435|
|3|.685040|.701855|.691105|.622436|
|4|.679464|.689354|.659974|.676596|

Both arms' mean training objectives drop from roughly .65–.73 to .26–.27
on every fold. A6 BCD improves in every fold across these windows;
A28 BCD declines notably in folds2/3 and remains below A6 late in all folds.
Thus an early best four-class checkpoint alone does not establish general
overfitting of B/C/D. Do not infer gradient dominance from loss magnitudes.
The failed decay change has broader effects than rare-A classification.

Existing A19 already tested weaker beta.995 on A6 and failed; do not repeat
it as an untested remedy. Next intervention requires checking actual gradient
contributions or other FIT-only evidence, not assuming that stronger decay
or weaker class weights must help. No new training job launched by this audit.
