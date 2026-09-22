# A34 completed fold-0 screen

Job 997 completed 50/50 epochs with exit code 0 on
`slurm-b20a-master-0` (RTX 5090), without restart/requeue and without using
worker2/Vesta. The read-only screen audit passed for all five frozen
manifests, split digest, experiment provenance, architecture, saved best
checkpoint, predictions, probability sums, recomputed metrics, and finished
W&B run `6bhg258e`.

The selected checkpoint is epoch 33: Macro-F1 **0.7779130831**, accuracy
0.8391089109, QWK 0.6138535927, class F1 A/B/C/D
[1.000000, 0.589744, 0.899687, 0.622222], with one severe error. Epoch-50
Macro-F1 is 0.5298463894. One of 50 checkpoints reached 0.75; 15 AMP updates
were skipped over the full run.

A34 passes the preregistered fold-0 expansion gate of 0.70. This is only a
selected DEV screen and its perfect A F1 is based on one class-A case. Retain
job 997 fold 0 and run fresh folds 1–4 from the identical immutable snapshot;
do not rerun or replace fold 0. Final acceptance still requires CV5 mean
>=0.70, sample SD <=0.05, and minimum fold >=0.65.

W&B:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6bhg258e
