# A47 folds2/3: matched first40

Both job1061 tasks remain RUNNING on master RTX5090 with complete, finite
epochs1--40. A47's selected checkpoints remain unchanged from first10, while
A42 fold2's matched-horizon baseline has reached its final selected epoch25.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs |
|---|---:|---:|---:|---:|---|---:|---:|
| A42/f2 | 25 | .677315 | .823821 | .605038 | .666667/.658537/.889937/.494118 | .680864 | 2/40 |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/40 |
| A47/f2 | 3 | .653592 | .823821 | .644387 | .5/.636364/.888530/.589474 | .704789 | 1/40 |
| A47/f3 | 5 | .702931 | .846535 | .644497 | .666667/.692308/.905132/.547619 | .715020 | 5/40 |

A47 two-fold Macro mean/sample-SD/minimum are
`.6782616/.0348884/.6535918`, versus A42
`.7079399/.0433108/.6773145`. A47 improves the spread and raises the minimum
B/C/D and minimum QWK, but its Macro mean/minimum, B/C/D mean and QWK mean are
all lower than A42. Both A47 fold Macro scores are below .72 and SD remains
above .03. No A47 selected checkpoint has improved since epoch5; the latest
positive-A epoch remains fold3 epoch13.

At epoch40 Macro-F1 is .5170289 on fold2 and .5425992 on fold3, with A F1 zero
on both. This late behavior does not indicate recovery. Finish the registered
50 epochs unchanged, then audit both runs and apply every gate. Do not launch
folds0/1/4 or tune on these DEV folds.

W&B:

- fold2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/109017w9
- fold3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zja66x7p
