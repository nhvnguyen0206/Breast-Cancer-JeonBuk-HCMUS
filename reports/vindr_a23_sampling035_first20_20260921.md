# A23 fold0 — first 20 epochs

Job `955_0` remains healthy on the master RTX 5090 with no requeue or restart.
The selected checkpoint remains epoch 4:

- Macro-F1: **0.650500**
- Accuracy: **0.722772**
- QWK: **0.589580**
- F1 A/B/C/D: **0.666667 / 0.534351 / 0.796330 / 0.604651**
- B/C/D mean: **0.645111**
- Cumulative sampled A/B/C/D: **563 / 5144 / 20303 / 6250**

No epoch from 11--20 improved the selected checkpoint and no checkpoint has
crossed `0.75`. A23 trails both A5 (`0.765442`) and direct parent A6
(`0.782979`) at the matched horizon. Continue the preregistered full-50 screen;
next review is epoch 30.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hk1ukax3)
