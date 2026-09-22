# A47 folds2/3: matched first10

Both job1061 tasks remain RUNNING on `slurm-b20a-master-0` RTX5090. Each
history contains complete epochs1--10 with finite losses. Every value below
is independently selected by best DEV Macro-F1 within the same first-ten-
epoch horizon on the frozen cache/split and seed42.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs |
|---|---:|---:|---:|---:|---|---:|---:|
| A42/f2 | 8 | .606175 | .774194 | .606120 | .4/.641026/.850340/.533333 | .674900 | 1/10 |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/10 |
| A47/f2 | 3 | .653592 | .823821 | .644387 | .5/.636364/.888530/.589474 | .704789 | 1/10 |
| A47/f3 | 5 | .702931 | .846535 | .644497 | .666667/.692308/.905132/.547619 | .715020 | 4/10 |

| Aggregate | A42 | A47 | Delta A47-A42 |
|---|---:|---:|---:|
| Macro-F1 mean | .672370 | .678262 | +.005892 |
| Macro-F1 sample SD | .093614 | .034888 | -.058726 |
| Minimum Macro-F1 | .606175 | .653592 | +.047417 |
| B/C/D mean across folds | .718716 | .709904 | -.008811 |
| QWK mean | .657775 | .644442 | -.013332 |

The dual-endpoint head improves fold2 D F1 and substantially narrows the
early two-fold gap, but fold3 D/B and QWK regress. At first10 both fold Macro
scores remain below .72, sample SD .034888 is above .03, B/C/D mean is below
the registered .721698 floor and QWK mean is below .657234. Therefore the
expansion gate is not met. Fold2/fold3 positive-A epoch counts and longest
streaks are 1/1 and 4/3 respectively; this is diagnostic only.

Continue both registered runs unchanged to20/40/50. Do not tune on either
screen fold and do not launch folds0/1/4. These are selected DEV results, not
independent evaluation.

W&B:

- fold2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/109017w9
- fold3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zja66x7p
