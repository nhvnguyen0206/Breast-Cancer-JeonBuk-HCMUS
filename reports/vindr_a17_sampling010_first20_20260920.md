# A17 sampling power 0.10 — first 20 epochs

Job907_0 remains RUNNING on `slurm-b20a-master-0`. All scalar training losses
are finite. Aggregate sampled counts are `[175,3616,23775,4694]`; total
AMP-skipped updates are 10. Five of the first 20 checkpoints reach Macro-F1
0.75 or higher.

A17's selected checkpoint is now epoch17: DEV Macro-F1
0.7914694342156339, accuracy 0.8267326732673267, QWK 0.6559945504087192,
class F1 `[1.0,0.6285714285714286,0.8856209150326797,0.651685393258427]`,
no severe errors. Confusion matrix:
`[[1,0,0,0],[0,33,7,0],[0,32,271,8],[0,0,23,29]]`.

At the matched first-20 horizon, A5's selected Macro-F1 is
0.7654421854687274 and A6's is 0.782979257528481. A17 also improves its
selected B/C/D mean F1 to 0.7219592456208451, rather than relying only on the
single A case. It is already 0.0018195780619777 above A5's eventual completed
fold0 best (0.7896498561536562), with higher accuracy and QWK. This is a
promising fold0 signal, but not five-fold stability evidence.

Epoch20 itself drops to Macro-F1 0.5092051745761185, showing substantial
checkpoint variability; selection remains DEV-based. Continue the
preregistered run unchanged to epoch50. No folds1--4 are authorized before the
completed screen audit.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/djz4e32c
