# A11 completed fold0 screen

Job830_0 COMPLETED ExitCode0:0 on master, no restart/requeue, worker2
excluded. Full50 audit PASS: frozen manifests, checkpoint/prediction metrics,
architecture/protocol and finished W&B xls5diws. Does not redo inference or
visually establish crop/label correctness.

Best epoch43 Macro-F1 .819363312392079, accuracy .8638613861386139,
QWK .697374155589453. Class F1 [1,.6666666667,.9131121643,.6976744186],
zero severe errors. Epoch50 .811754225568901; 22/50 epochs >=.75.
16 total AMP skipped updates; scalar training losses finite.

Passes expansion gate. Improvement over A5 fold0 is2.97135pp; B/C/D
also improve, but this is selected DEV with one A case, not CV5 or
multi-seed success. Retain fold0 and run fresh folds1--4 unchanged.

https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/xls5diws
