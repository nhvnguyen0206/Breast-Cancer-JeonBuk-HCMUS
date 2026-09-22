# A27 first30 — incomplete screen

Job964_0 verified RUNNING on master;30 completed epochs, finite training
scalar losses,14 cumulative AMP skipped updates. Registered setup unchanged.

Best remains epoch16: Macro-F1 .6751496226906062, accuracy
.7995049504950495,QWK .6115753489697084; classF1
[.6666666666666666,.6095238095238096,.8688524590163934,.5555555555555556].
No improvement in selected metric during epochs21–30.

Epoch30: Macro-F1 .5363996245556187, accuracy .8168316831683168,
QWK .6348140495867769; classF1 [0,.6451612903225806,.8822553897180763,
.6181818181818182]. Confusion rows A/B/C/D:
[[0,1,0,0],[1,30,9,0],[0,21,266,24],[0,1,17,34]],severe errors1.

Matched A5 first30 selected Macro-F1 .7896498561536562 exceeds A27.
Below .75 expansion gate; continue unchanged full50, no confirmation folds.
Next review40. These are selected DEV estimates, not independent test or
evidence of cross-fold stability; one A case in this DEV fold.
W&B https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/wjz7dz8t.
