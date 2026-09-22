# A17 sampling power 0.10 — first 40 epochs

Job907_0 remains RUNNING on `slurm-b20a-master-0`. All scalar training losses
are finite. Aggregate sampled counts are `[326,7194,47530,9470]`; total
AMP-skipped updates are 16.

The selected checkpoint remains epoch17: DEV Macro-F1
0.7914694342156339, accuracy 0.8267326732673267, QWK 0.6559945504087192,
class F1 `[1.0,0.6285714285714286,0.8856209150326797,0.651685393258427]`,
no severe errors. Twelve of the first 40 checkpoints reach Macro-F1 0.75 or
higher, compared with five for A5 and one for A6 at the matched horizon.

Epoch40 Macro-F1 is 0.6788652025429585, accuracy 0.8217821782178217 and QWK
0.6109981812346208. It recovers partial class-A F1 but does not improve the
selected checkpoint. The repeated threshold crossings are encouraging, while
the single fold0 A case still makes four-class Macro-F1 volatile.

Continue unchanged to epoch50 and the full screen audit. Do not submit
folds1--4 before the audit passes the preregistered gate.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/djz4e32c
