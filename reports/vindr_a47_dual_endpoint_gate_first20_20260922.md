# A47 folds2/3: matched first20

Both job1061 tasks remain RUNNING on master RTX5090 with complete, finite
epochs1--20. Best DEV Macro-F1 selection within this common horizon is
unchanged from first10 for both A42 and A47.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs |
|---|---:|---:|---:|---:|---|---:|---:|
| A42/f2 | 8 | .606175 | .774194 | .606120 | .4/.641026/.850340/.533333 | .674900 | 1/20 |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/20 |
| A47/f2 | 3 | .653592 | .823821 | .644387 | .5/.636364/.888530/.589474 | .704789 | 1/20 |
| A47/f3 | 5 | .702931 | .846535 | .644497 | .666667/.692308/.905132/.547619 | .715020 | 5/20 |

A47 two-fold Macro-F1 mean/sample-SD/minimum remain
`.6782616/.0348884/.6535918`, compared with A42
`.6723700/.0936142/.6061748`. B/C/D mean/minimum are
`.7099044/.7047891`, and QWK mean/minimum are `.6444421/.6443867`.

Fold3 gains one additional positive-A epoch at epoch13, but neither selected
checkpoint improves after first10. Both fold Macro scores remain below .72,
sample SD exceeds .03, and B/C/D/QWK means remain below their registered
parent floors. Expansion remains prohibited. Continue unchanged to40/50,
then audit both completed screens. These are selected DEV results and are not
independent evaluation.

W&B:

- fold2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/109017w9
- fold3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zja66x7p
