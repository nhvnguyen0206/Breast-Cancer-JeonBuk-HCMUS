# A22 fold0 — first 20 epochs

Job `950_0` remains healthy on the master RTX 5090 with no requeue or restart.
All recorded losses are finite. The selected checkpoint through epoch 20 is
epoch 18:

- Macro-F1: **0.688852**
- Accuracy: **0.809406**
- QWK: **0.625421**
- F1 A/B/C/D: **0.666667 / 0.613333 / 0.875410 / 0.600000**
- Severe errors: **0**
- Cumulative AMP skipped updates: **10**

The selected score is below A5 at the matched first-20 horizon by `0.076590`
(`0.688852` versus `0.765442`). No checkpoint has reached the preregistered
`0.75` gate. Continue the unchanged fold0 run through epoch 50; next review is
epoch 30.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gdne1bkg)
