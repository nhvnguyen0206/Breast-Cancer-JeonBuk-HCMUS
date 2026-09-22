# A27 first40 — incomplete screen

Job964_0 verified RUNNING on master;40 completed epochs, training scalar
losses finite,15 cumulative AMP skipped updates. Registered setup unchanged.

Best remains epoch16: Macro-F1 .6751496226906062, accuracy
.7995049504950495,QWK .6115753489697084; classF1
[.6666666666666666,.6095238095238096,.8688524590163934,.5555555555555556].
No selected-metric improvement during epochs31–40.

Epoch40: Macro-F1 .5306800394718932, accuracy .8316831683168316,
QWK .6165240641711229; classF1 [0,.625,.8955696202531646,.6021505376344086].
Confusion rows A/B/C/D:
[[0,1,0,0],[1,25,14,0],[1,14,283,13],[0,0,24,28]],severe errors1.

Below A5 matched selected Macro-F1 .7896498561536562 and .75 gate.
Continue unchanged full50 then audit; no confirmation folds. Selected DEV,
not independent test or cross-fold stability evidence; one A case in DEV.
W&B https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/wjz7dz8t.
