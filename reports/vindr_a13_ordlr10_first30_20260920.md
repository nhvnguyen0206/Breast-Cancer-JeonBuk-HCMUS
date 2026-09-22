# A13 first30 matched-horizon observation

Job852_0 verified RUNNING on slurm-b20a-master-0 with30 completed epochs.
All recorded scalar training losses finite. No split/configuration changes.

A13 selected epoch20 remains unchanged: Macro-F1 .7580533506398416,
accuracy .7970297029702971, QWK .5906446690825864,
class F1 [1,.5656565656565656,.8665568369028006,.6].
Confusion matrix [[1,0,0,0],[0,28,12,0],[0,30,263,18],[0,1,21,30]];
one severe D->B error.

A5 at matched first30 selects epoch30: Macro-F1 .7896498561536562,
accuracy .8267326732673267, QWK .6486083499005965,
class F1 [1,.6419753086419753,.8859934853420195,.6306306306306306].
Zero severe errors. A13 is below A5 on B/C/D, accuracy and QWK;
no improvement or stability claim is supported by the provisional .75 crossing.

Continue registered50 unchanged, then full screen audit before any fresh
folds1--4. No expansion submitted. Next metrics40. Selected DEV, not test.
