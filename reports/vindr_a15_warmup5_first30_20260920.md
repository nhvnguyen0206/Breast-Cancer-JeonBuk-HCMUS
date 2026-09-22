# A15 warm-up5 — fold-0 first 30 epochs

Job905_0 remains RUNNING on RTX5090. All scalar train losses are finite.
History proves epochs1--5 frozen and epochs6--30 unfrozen as preregistered.

A15 selected within epochs1--30: epoch26, Macro-F1 0.7145881415028787,
accuracy 0.8539603960396039, QWK 0.6663867428059568, class F1
[0.6666666666666666, 0.6301369863013698, 0.909375,
0.6521739130434783], no severe errors. Its confusion matrix is
[[1,0,0,0],[1,23,16,0],[0,10,291,10],[0,0,22,30]]. Epoch30 Macro-F1 is
0.53526142087893.

Matched A5 first30 selected epoch30: Macro-F1 0.7896498561536562,
accuracy 0.8267326732673267, QWK 0.6486083499005965, class F1
[1.0, 0.6419753086419753, 0.8859934853420195, 0.6306306306306306], no
severe errors. A15/A5 AMP-skipped updates are 12/12.

A15 improves accuracy, QWK, C and D F1 over A5, but trails by
0.0750617146507775 Macro-F1 due primarily to the unstable contribution of the
single fold-0 class-A case and slightly lower B F1. Its selected DEV Macro-F1
exceeds 0.70 but not the preregistered 0.75 expansion gate. Continue the
preregistered full50 unchanged; do not submit folds1--4. Next report at
epoch40.
