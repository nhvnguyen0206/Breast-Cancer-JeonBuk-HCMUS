# A27 first20 — incomplete screen

Job964_0 verified RUNNING on master;20 epochs completed. Training scalar
losses finite,10 AMP skipped updates. No change to registered experiment.

Selected epoch16: Macro-F1 .6751496226906062, accuracy .7995049504950495,
QWK .6115753489697084; class F1 [.6666666666666666,.6095238095238096,
.8688524590163934,.5555555555555556]. Confusion rows A/B/C/D:
[[1,0,0,0],[1,32,7,0],[0,33,265,13],[0,0,27,25]], severe errors0.
Epoch20 Macro-F1 .57455525606469, accuracy .8118811881188119,
QWK .600624349635796.

Matched A5 first20 selected Macro-F1 .7654421854687274 at epoch20,
F1 [1,.6086956521739131,.8637873754152824,.5892857142857143].
A27 has slightly higher B/C but lower A/D; no evidence yet that increased
rotation improves the primary metric or stability. A has only one DEV case.
Still below .75 screen gate. Continue full50 unchanged; no folds1–4.
Next milestone30. Selected DEV, not independent test or final CV5 evidence.
W&B https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/wjz7dz8t.
