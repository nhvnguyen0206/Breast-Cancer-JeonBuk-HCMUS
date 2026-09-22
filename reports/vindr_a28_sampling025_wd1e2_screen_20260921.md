# A28 completed fixed-fold screen

Job965_0 COMPLETED, exit0, runtime54:18, no restart/requeue; master5090.
Completed50 epochs. Read-only audit PASS: checkpoint selection, prediction
metrics/probabilities, all five frozen manifests and finished live W&B agree.
Audit uses stored predictions, not fresh inference.
Assignment SHA256: 43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.
Config SHA256: d4506d47c8482be44aa4b7f2d301b113529a9d9e3001421309b9d22b0ee2ac75.

Selected epoch11: Macro-F1 .764525162671938, accuracy .8292079207920792,
QWK .6047078842881453. Class F1 A/B/C/D:
[1,.5555555555555556,.892018779342723,.6105263157894737].
CM [[1,0,0,0],[0,20,20,0],[0,12,285,14],[0,0,23,29]].
Epoch50 Macro-F1 .5384407206173768;3 epochs met .75;18 AMP skipped updates.
Maximum prediction probability-sum error1.168783114735561e-7.
W&B finished: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zzcsyjs3.

Screen gate passes, not campaign success. Selected DEV is not independent
test; only one A case in this fold. Retain original965-fold0 and run fresh
folds1–4 with identical immutable snapshot/config,50epochs,seed42,5090 only.
Joint CV5 acceptance remains mean>=.70, sampleSD<=.05,min>=.65;
mean>=.75 aspirational. Do not replace any weak fold.

Confirmation submitted once as array966 tasks1–4. All four verified RUNNING
on master/worker1, not Vesta or excluded worker2. Retain965-fold0.

Startup verification: all four logs confirm NVIDIA GeForce RTX5090;
all four histories completed first epoch with finite training metrics.
W&B runs: fold1 smp9n05h, fold2 5r21dr58, fold3 dgjpbw2y,
fold4 9r1fv0bm, under TN_Mammo_BreastDensity/HCMUS-paper1.
No intermediate score review before the10–20epoch milestone.
