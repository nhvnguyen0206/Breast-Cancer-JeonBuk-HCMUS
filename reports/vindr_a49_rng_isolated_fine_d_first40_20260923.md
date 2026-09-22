# A49 folds2/3: matched first40

Both Slurm job1069 tasks remain RUNNING on `slurm-b20a-master-0` RTX5090.
Histories contain complete, finite epochs1--40 with no runtime error markers.
The values below use independent best-DEV selection restricted to the common
first-40 horizon; fold3 epochs41--42 are excluded.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Macro >=.72 epochs | D-head norm |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A42/f2 | 25 | .677315 | .823821 | .605038 | .666667/.658537/.889937/.494118 | .680864 | 2/40 | n/a | n/a |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/40 | n/a | n/a |
| A48/f2 | 3 | .540083 | .831266 | .627450 | 0/.685714/.892800/.581818 | .720111 | 0/40 | 0 | .015358 |
| A48/f3 | 6 | .738368 | .858911 | .701292 | .666667/.750000/.910543/.626263 | .762269 | 15/40 | n/a | .022067 |
| A49/f2 | 5 | .606284 | .799007 | .640927 | .333333/.649351/.871022/.571429 | .697267 | 1/40 | 0 | .017473 |
| A49/f3 | 7 | .711244 | .787129 | .649892 | .666667/.761905/.850615/.565789 | .726103 | 5/40 | 0 | .024728 |

| Aggregate | A42 | A48 | A49 | Delta A49-A42 | Delta A49-A48 |
|---|---:|---:|---:|---:|---:|
| Macro-F1 mean | .707940 | .639226 | .658764 | -.049176 | +.019538 |
| Macro-F1 sample SD | .043311 | .140209 | .074218 | +.030907 | -.065991 |
| Minimum Macro-F1 | .677315 | .540083 | .606284 | -.071031 | +.066201 |
| B/C/D mean across folds | .721698 | .741190 | .711685 | -.010013 | -.029505 |
| B/C/D minimum | .680864 | .720111 | .697267 | +.016403 | -.022844 |
| QWK mean | .657234 | .664371 | .645409 | -.011824 | -.018962 |
| QWK minimum | .605038 | .627450 | .640927 | +.035888 | +.013476 |

A49 remains unchanged from first10/20 and has no epoch reaching Macro-F1
`.72` on either fold. It repairs much of A48's RNG-induced imbalance and
improves both B/C/D and QWK minima relative to A42, but fails both per-fold
Macro gates, the SD gate, the B/C/D mean gate and the QWK mean gate. A42 itself
improves after epoch20 on fold2, so A49 now trails the matched A42 mean by
`.049176` and minimum by `.071031`.

Finish epoch50 and execute queued audits1073/1074. The numerical screen is
already unsupported at first40, but no final rejection is recorded before the
registered completion/audit. Folds0/1/4 remain locked. These are selected DEV
metrics, not an independent test. W&B remains offline under IDs `7msbizh4`
and `7mch95l6`.
