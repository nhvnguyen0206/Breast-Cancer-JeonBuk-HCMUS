# A17 sampling power 0.10 — first 30 epochs

Job907_0 remains RUNNING on `slurm-b20a-master-0`. All scalar training losses
are finite. Aggregate sampled counts are `[246,5401,35681,7062]`; total
AMP-skipped updates are 13.

The selected checkpoint remains epoch17: DEV Macro-F1
0.7914694342156339, accuracy 0.8267326732673267, QWK 0.6559945504087192,
class F1 `[1.0,0.6285714285714286,0.8856209150326797,0.651685393258427]`,
no severe errors. Nine of the first 30 checkpoints reach Macro-F1 0.75 or
higher, compared with three for A5 and one for A6 at the matched horizon.

The best value has not increased after epoch17, and epoch30 is only
0.5383710440432582 because class-A F1 is zero. This confirms large per-epoch
four-class Macro-F1 movement caused partly by the single fold0 A case, despite
more frequent threshold crossings. The selected B/C/D mean remains
0.7219592456208451 and is not dependent on A alone.

Continue unchanged to the completed 50-epoch audit. No folds1--4 are
authorized yet; the current numbers are selected DEV results, not independent
test evidence.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/djz4e32c
