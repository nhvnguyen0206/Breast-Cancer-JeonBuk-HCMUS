# A19 fold0 — first 30 epochs

Job936 remains RUNNING on master RTX5090. All scalar training losses are
finite. The selected checkpoint remains epoch11:

- Macro-F1: 0.7623856925078064
- Accuracy: 0.7772277227722773
- QWK: 0.6014556296036478
- F1 A/B/C/D: `[1.0,0.6419753086,0.8464163823,0.5611510791]`
- Severe errors: 0
- Epoch30 Macro-F1: 0.5474753243710277
- Checkpoints at or above .75: 3/30
- AMP-skipped updates: 11
- Aggregate sampled A/B/C/D: `[552,6809,32501,8528]`

No selected improvement occurred during epochs21--30. At the matched horizon,
A6 remains 0.7829792575 and A5 improves to 0.7896498562. A19 trails A5 by
0.0272641636 and has lower C and D F1 while matching B. Its epoch30 value is
also far below its selected value, retaining the large checkpoint-to-late
gap seen throughout this campaign.

Continue the registered fold0 unchanged to 50 epochs. Do not launch folds1--4
before the completed screen audit.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6wtyzm62
