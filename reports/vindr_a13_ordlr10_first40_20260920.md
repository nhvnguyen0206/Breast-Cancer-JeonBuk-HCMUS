# A13 first40 matched-horizon observation

Job852_0 verified RUNNING on slurm-b20a-master-0,40 completed epochs;
all recorded scalar training losses finite. Configuration and split unchanged.

A13 selected epoch20 remains best: Macro-F1 .7580533506398416,
accuracy .7970297029702971, QWK .5906446690825864,
class F1 [1,.5656565656565656,.8665568369028006,.6].
Confusion matrix [[1,0,0,0],[0,28,12,0],[0,30,263,18],[0,1,21,30]];
one severe D->B error.

A5 matched first40 selects epoch30: Macro-F1 .7896498561536562,
accuracy .8267326732673267, QWK .6486083499005965,
class F1 [1,.6419753086419753,.8859934853420195,.6306306306306306],
zero severe errors. A13 remains lower on each B/C/D F1, accuracy and QWK.
No new best since epoch20; provisional .75 crossing is not CV5 success.

Continue registered50 unchanged and audit completed screen before any
fresh folds1--4. No confirmation submitted. Next report completion.
Selected DEV, not independent test; multi-seed stability unverified.
