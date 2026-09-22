# A28 first30 — incomplete screen

Job965_0 verified RUNNING on master;30 completed epochs, finite training
scalar losses,13 cumulative AMP skipped updates. Registered setup unchanged.

Selected remains epoch11: Macro-F1 .764525162671938, accuracy
.8292079207920792,QWK .6047078842881453; classF1
[1,.5555555555555556,.892018779342723,.6105263157894737].
No selected-metric improvement during epochs21–30; still below A6 parent
.782979257528481. One A DEV study limits interpretation.

Epoch30 Macro-F1 .5412416089909962,accuracy .8193069306930693,
QWK .6263813448211275; classF1 [0,.6041666666666666,.8811881188118812,
.6796116504854369]. Confusion rows A/B/C/D:
[[0,1,0,0],[0,29,11,0],[2,26,267,16],[0,0,17,35]],severe errors2.
Sampled counts [14,222,1120,257].

Continue unchanged full50 then audit before fresh folds1–4; none submitted.
Numeric gate has been crossed but is not evidence of cross-fold stability.
Next review40. Selected DEV, not independent test.
W&B https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zzcsyjs3.
