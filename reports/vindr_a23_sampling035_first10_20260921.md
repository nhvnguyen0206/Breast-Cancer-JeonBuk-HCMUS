# A23 fold0 — first 10 epochs

Job `955_0` remains healthy on the master RTX 5090 with no requeue or restart.
Losses are finite. The selected checkpoint through epoch 10 is epoch 4:

- Macro-F1: **0.650500**
- Accuracy: **0.722772**
- QWK: **0.589580**
- F1 A/B/C/D: **0.666667 / 0.534351 / 0.796330 / 0.604651**
- B/C/D mean: **0.645111**
- Severe errors: **0**
- Sampled A/B/C/D counts: **286 / 2626 / 10108 / 3110**

A23 is above A5's matched first-10 Macro-F1 (`0.545249`) but below direct
parent A6 (`0.782979`), with weaker B/C/D performance. No checkpoint has
crossed the `0.75` expansion gate. Continue the unchanged registered fold0
through epoch 50; next review is epoch 20.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hk1ukax3)
