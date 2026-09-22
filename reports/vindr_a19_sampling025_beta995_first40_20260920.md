# A19 fold0 — first 40 epochs

Job936 remains RUNNING on master RTX5090. Scalar losses remain finite. The
selected checkpoint is unchanged from epoch11:

- Macro-F1: 0.7623856925078064
- Accuracy: 0.7772277227722773
- QWK: 0.6014556296036478
- F1 A/B/C/D: `[1.0,0.6419753086,0.8464163823,0.5611510791]`
- Severe errors: 0
- Epoch40 Macro-F1: 0.54480534400056
- Checkpoints at or above .75: 3/40
- AMP-skipped updates: 14
- Aggregate sampled A/B/C/D: `[718,9090,43308,11404]`

No selected improvement occurred from epochs12--40. At the matched horizon,
A6 remains 0.7829792575 and A5 remains 0.7896498562. A19 trails A5 by
0.0272641636, matches its B F1, and is lower in C and D. The lower-beta
treatment has not surpassed either parent comparator.

Continue through the registered epoch50 and perform the completed screen
audit. Do not launch folds1--4 before that audit.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6wtyzm62
