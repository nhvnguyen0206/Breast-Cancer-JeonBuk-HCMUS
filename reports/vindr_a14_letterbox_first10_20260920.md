# A14 letterbox — fold-0 first 10 epochs

Job 878_0 remains RUNNING on RTX5090. All recorded scalar train losses are
finite. A14 and A5 both accumulated seven AMP-skipped updates through epoch10.

A14 selected within epochs1--10: epoch10, Macro-F1 0.5588157368155812,
accuracy 0.7896039603960396, QWK 0.6110809096674821, class F1
[0.2857142857142857, 0.45569620253164556, 0.8688524590163934, 0.625].
Confusion matrix: [[1,0,0,0],[5,18,17,0],[0,21,265,25],[0,0,17,35]].

Matched A5 selected within epochs1--10: epoch7, Macro-F1
0.5452488631717199, accuracy 0.8217821782178217, QWK 0.6538131962296487,
class F1 [0, 0.6086956521739131, 0.8826446280991735, 0.6896551724137931].

A14 is +0.01357 Macro-F1 at this early horizon, but lower accuracy/QWK and
lower B/C/D F1; its Macro-F1 advantage is driven by the single fold-0 A case.
That is explicitly insufficient evidence. Continue the registered full50;
do not submit confirmation folds before completed screen audit and >=.75 gate.
