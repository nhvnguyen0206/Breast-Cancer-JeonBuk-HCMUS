# A15 warm-up5 — fold-0 first 10 epochs

Job905_0 remains RUNNING on RTX5090. All scalar train losses are finite.
History proves epochs1--5 frozen and epochs6--10 unfrozen as registered.

A15 selected within epochs1--10: epoch6, Macro-F1 0.5668603551539351,
accuracy 0.849009900990099, QWK 0.6907439012147375, class F1
[0, 0.6451612903225806, 0.9022801302931596, 0.72], no severe errors.
Matched A5 first10 best: epoch7, Macro-F1 0.5452488631717199,
accuracy 0.8217821782178217, QWK 0.6538131962296487, class F1
[0, 0.6086956521739131, 0.8826446280991735, 0.6896551724137931].
A15/A5 AMP-skipped updates: 6/7.

A15 is +0.02161 Macro-F1 with higher B/C/D F1, accuracy and QWK, but both
miss the fold0 A case and A15 remains far below the .75 gate. Continue the
registered full50 without confirmation folds; next report at epoch20.
