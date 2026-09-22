# A28: first 40 epochs (provisional DEV)

Live job965_0 verified RUNNING on slurm-b20a-master-0 at43:32;
history contains40 completed epochs. No confirmation jobs submitted.
Run: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/zzcsyjs3

Selected best remains epoch11: Macro-F1 .764525162671938,
accuracy .8292079207920792, QWK .6047078842881453.
Class F1 A/B/C/D: [1,.5555555555555556,.892018779342723,.6105263157894737].
Confusion matrix: [[1,0,0,0],[0,20,20,0],[0,12,285,14],[0,0,23,29]].

Epoch40 Macro-F1 .5454439108806068, accuracy .8415841584158416,
QWK .6187446074201899; class F1
[0,.6486486486486487,.9004739336492891,.6326530612244898].
Confusion matrix: [[0,1,0,0],[0,24,16,0],[2,9,285,15],[0,0,21,31]].
Training objective .26410844833852304; accumulated AMP skipped updates14.

No improvement in selected best since epoch11. The sole DEV A case and
false-positive A predictions substantially affect the four-class score;
accuracy alone conceals this weakness. Single-fold selected DEV does not
establish stability or independent generalization. Continue registered50
epochs, audit completed artifacts, then expand folds1–4 only if gate passes.
