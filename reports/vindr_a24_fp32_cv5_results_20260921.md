# A24 completed CV5: rejected against acceptance criteria

All five50-epoch source runs audited PASS including live W&B finished,
saved predictions/checkpoint/history agreement, frozen manifests and unique
2017-case DEV union. Audit does not rerun inference. Full evidence in the
adjacent JSON. Original screen957 fold0 preserved; confirmation958 folds1--4.

Macro-F1 folds0--4: .8016882344 / .5697976627 / .6717936881 /
.7056476091 / .6556473298. Selected epochs43/2/48/21/19.
Mean .6809149048144196; sample SD .08406335743255076;
minimum .5697976626548055. Fails mean>=.70, SD<=.05 and minimum>=.65.
Accuracy mean .8492776945188315; QWK mean .6628753154986771.
Mean F1 A/B/C/D [.5333333333,.6740475399,.9059315930,.6103471530].

Compared with A5, FP32 reduces fold dispersion but lowers mean Macro-F1
(.702828 -> .680915); it does not solve the stability requirement.
Fold1 has A F1=0 despite B/C/D F1 .717949/.916797/.644444.
Pooled confusion matrix [[4,2,0,0],[4,129,63,0],[0,56,1439,61],
[0,0,118,141]] highlights persistent D->C confusion as well as scarce A.
Only six A studies; selected DEV is not independent test evidence.

No additional training submitted by this final audit. Next step: review
completed controlled arms and loss/class-weight evidence before registering
a new single-factor fold0 screen; do not combine changes or reuse weak-fold
outcomes as a substitute for the fixed screen gate.

Published audited W&B summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/oik71g9h
