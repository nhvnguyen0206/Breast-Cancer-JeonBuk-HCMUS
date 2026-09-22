# A28 first20 — incomplete screen

Job965_0 verified RUNNING on master;20 completed epochs, finite training
scalar losses,11 cumulative AMP skipped updates. Registered setup unchanged.

Selected epoch11: Macro-F1 .764525162671938, accuracy .8292079207920792,
QWK .6047078842881453; classF1 [1,.5555555555555556,.892018779342723,
.6105263157894737]. Confusion rows A/B/C/D:
[[1,0,0,0],[0,20,20,0],[0,12,285,14],[0,0,23,29]],severe errors0.
Epoch20 Macro-F1 .6860569985569985,accuracy .8193069306930693,
QWK .6342032149235959; sampled class counts [17,217,1082,297].

Selected score improves over first10 .7579900045494687 but still trails A6
parent .782979257528481 (epoch4). B/D remain lower, C higher. Only one A
DEV study; numerical screening success is not cross-fold stability evidence.
Continue unchanged full50 then audit before fresh folds1–4; none submitted.
Next review30. Selected DEV, not independent test.
W&B https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zzcsyjs3.
