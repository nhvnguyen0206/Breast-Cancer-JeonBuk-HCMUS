# A25 first10: screen remains below expansion gate

Job962_0 verified RUNNING on master at runtime11:49. Ten completed epochs;
no intervention or confirmation submitted. Six cumulative AMP skipped updates.

Best selected DEV checkpoint so far: epoch4, Macro-F1 .706347382145964,
accuracy .801980198019802, QWK .6636976608673937, severe errors0.
F1 A/B/C/D: [.6666666666666666,.6016260162601627,.8640275387263339,
.693069306930693]. Confusion matrix:
[[1,0,0,0],[1,37,2,0],[0,46,251,14],[0,0,17,35]].

A5 matched first10 selected epoch7 Macro .5452488631717199 and class F1
[0,.6086956521739131,.8826446280991735,.6896551724137931].
A25 gain .1610985189742441 is almost entirely attributable to class A:
BCD mean is .7195742873057299 versus A5 .7269984842289266.
Therefore this is not evidence of broad improvement or stable CV5 performance.

Epoch10 Macro .5103324198943933, accuracy .7772277227722773,
QWK .6102451573849879, severe errors4. Predicting A too often includes
11 B and4 C cases at this epoch; avoid concluding rare-A learning is stable.
Continue unchanged full50, next milestone20. Completed audited fold0>=.75
still required before folds1–4. Selected DEV is not independent test.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/vjgvwnx6
