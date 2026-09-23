# A53 folds2/3: matched first40

Array job1096 remains active on RTX5090 with worker2/Vesta excluded. Both runs
use the immutable v20 snapshot, frozen split/cache/seed42 and offline W&B
receipts `6irwuqqa`/`82som6u1`. This selected-DEV interim analysis is not an
independent test or final gate decision.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Longest A streak | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A53/f2 | 19 | .556355 | .856079 | .658714 | .000000/.736842/.910798/.577778 | .741806 | 0/40 | 0 | 0 |
| A53/f3 | 16 | .720535 | .836634 | .676824 | .666667/.747253/.893964/.574257 | .738491 | 10/40 | 7 | 1 |

The selected checkpoints and every aggregate remain unchanged from first20:
Macro-F1 mean `.6384449`, sample SD `.1160933`, minimum `.5563545`; accuracy
mean `.8463565`; QWK mean/minimum `.6677687/.6587139`; B/C/D mean/minimum
`.7401487/.7384914`.

Fold2 has not produced one positive-A epoch in forty attempts. Fold3 adds only
one positive-A epoch after first20 and does not improve its selected
checkpoint. B/C/D and QWK gates pass, while fold2 Macro-F1 and two-fold SD fail
decisively. This is evidence against delayed convergence and strengthens the
registered A54 hypothesis that the multiscale representation needs dense
multi-task supervision, not only A-vs-rest supervision.

Finish epoch50 and queued read-only audits1098/1099 without retuning. Do not
expand A53 to folds0/1/4. A54 was preregistered before this first40 inspection
and remains Atlas/training-locked until audited A53 rejection.

