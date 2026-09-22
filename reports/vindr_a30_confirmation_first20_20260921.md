# A30 common first20-epoch review

Array982 tasks1–4 RUNNING at29:05; actual epochs [50,20,20,21,21]
including original981 fold0. Restrict every fold to first20 for comparison.
Selected DEV values, not final audit or independent test.

|Fold|Selected epoch|Macro-F1|A F1|
|---|---:|---:|---:|
|0|11|.7025951908901428|.6666666667|
|1|20|.7584943371085943|1|
|2|4|.6310390439700785|.4|
|3|2|.6864294857992337|.5|
|4|16|.6149715028078115|.5|

Mean .6787059121151722; sampleSD .05772943192664435;
minimum .6149715028078115. All three final numerical criteria currently
unmet; training incomplete. Fold1 improvement partly reflects its one A
case becoming perfectly classified without false positives; selected D F1
.4810126582 remains weak (32/51 D predicted C). Do not interpret rare-A
improvement alone as reliable generalization. Keep unchanged full50.
Next review common30 epochs; no added training jobs or tuning on weak folds.
