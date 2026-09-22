# A22 fold0 — first 30 epochs

Job `950_0` remains healthy on the master RTX 5090 with no requeue or restart.
All recorded losses are finite. The selected checkpoint through epoch 30 is
epoch 22:

- Macro-F1: **0.771853**
- Accuracy: **0.801980**
- QWK: **0.625822**
- F1 A/B/C/D: **1.000000 / 0.595745 / 0.866667 / 0.625000**
- Severe errors: **0**
- Cumulative AMP skipped updates: **13**

One checkpoint has crossed the preregistered fold0 gate of `0.75`. The score
is still `0.017797` below A5's final selected fold0 score (`0.789650`), and
class A contains only one DEV study. Continue the unchanged registered run
through epoch 50, audit the saved checkpoint and only then decide whether to
launch folds 1--4. Next review is epoch 40.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gdne1bkg)
