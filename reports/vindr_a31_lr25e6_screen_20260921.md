# A31 completed fold-0 screen: global LR 2.5e-5

A31 changes only global learning rate from 5e-5 to 2.5e-5 relative to A6.
Architecture, sampling, augmentation, losses, cache, seed 42, and frozen
grouped split are unchanged. There is no ensemble.

Job `986_0` completed all 50 epochs on `slurm-b20a-master-0` with RTX 5090,
exit code 0:0, no restart/requeue, and worker2/Vesta excluded. The read-only
screen audit passed; the W&B source run is `finished`; split digest remains
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.

Selected epoch 6: Macro-F1 **0.6851250647**, accuracy **0.7871287129**,
QWK **0.6311990489**, class F1 A/B/C/D
**0.666667 / 0.596491 / 0.854701 / 0.622642**, with zero severe errors.
The score is below the amended 0.70 expansion gate. Reject A31 and do not
submit folds 1–4. These are selected DEV results, not an independent test.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/9v7h7cr0

