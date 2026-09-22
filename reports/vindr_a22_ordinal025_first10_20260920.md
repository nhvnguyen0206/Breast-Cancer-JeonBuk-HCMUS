# A22 fold0 — first 10 epochs

Job `950_0` remains healthy on the master RTX 5090 with no requeue or restart.
Losses are finite. The selected checkpoint through epoch 10 is epoch 10:

- Macro-F1: **0.560716**
- Accuracy: **0.834158**
- QWK: **0.656362**
- F1 A/B/C/D: **0.200000 / 0.437500 / 0.905363 / 0.700000**
- Severe errors: **1**
- Cumulative AMP skipped updates: **7**

This is `+0.015467` versus A5 at the matched first-10 horizon
(`0.545249`), but no checkpoint has reached the preregistered `0.75` gate.
Continue the unchanged fold0 run through epoch 50; next review is epoch 20.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gdne1bkg)
