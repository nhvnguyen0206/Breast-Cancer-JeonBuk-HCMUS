# A23 fold0 — first 30 epochs

Job `955_0` remains healthy on the master RTX 5090 with no requeue or restart.
The selected checkpoint remains epoch 4 with Macro-F1 **0.650500**, accuracy
**0.722772**, QWK **0.589580**, and F1 A/B/C/D
`0.666667 / 0.534351 / 0.796330 / 0.604651`.

No epoch from 11--30 improved the selection. Epoch 30 Macro-F1 is `0.538025`;
zero of 30 checkpoints reached `0.75`. Cumulative sampled A/B/C/D counts are
`837 / 7742 / 30424 / 9387`. Continue unchanged to epoch 50; next review is
epoch 40.

[W&B run](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/hk1ukax3)
