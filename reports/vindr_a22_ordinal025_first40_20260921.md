# A22 fold0 — first 40 epochs

Job `950_0` remains healthy on the master RTX 5090 with no requeue or restart.
All recorded losses are finite. The selected checkpoint remains epoch 22:

- Macro-F1: **0.771853**
- Accuracy: **0.801980**
- QWK: **0.625822**
- F1 A/B/C/D: **1.000000 / 0.595745 / 0.866667 / 0.625000**
- Severe errors: **0**
- Cumulative AMP skipped updates: **16**

No epoch from 31 through 40 improved the selected checkpoint. Exactly one
checkpoint has crossed the `0.75` fold0 gate. Continue through epoch 50 and
audit the selected checkpoint before deciding whether to launch folds 1--4.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gdne1bkg)
