# A28 completed CV5: rejected

All five runs completed50, live W&B finished, audit PASS (saved predictions,
checkpoint metadata and frozen manifests; not fresh inference).
Original965-fold0 retained,966-fold1–4. Full audit JSON alongside this file.
Macro-F1 mean .6329272758361971, sampleSD .08947073219536511,
minimum .5543703053360648. Accuracy .8115851411443874,
QWK .6145756233959224. ClassF1 means A/B/C/D:
[.5111111111111111,.5700628167667968,.8830494155047893,.5674857599620915].
All three joint acceptance conditions fail. No campaign completion.

Compared to A6 parent mean .676551383913, SD .064446199071,
minimum .619496083313: increased weight decay worsened all three.
BCD mean .6735326640778926 also below parent approximately .7154;
therefore regression is not only a rare-A effect. Reject this decay change.
Best epochs [11,6,7,1,4]; no late selected-best recovery.

Selected DEV is not independent test. Six A cases limit certainty.
Pooled confusion matrix [[5,1,0,0],[15,117,64,0],[0,93,1378,85],[0,0,122,137]]:
15 B->A false positives,122 D->C errors remain substantial.
Do not alter splits, replace folds or switch evaluation definitions.
Next action: review prior tested arms and investigate remaining training
imbalance/generalization mechanisms before registering a new single-fold arm.

Published audited summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/lv6gx0or
