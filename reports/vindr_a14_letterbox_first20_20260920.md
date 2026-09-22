# A14 letterbox — fold-0 first 20 epochs

Job878_0 remains RUNNING on RTX5090. All recorded scalar train losses are
finite. A14 and A5 both accumulated eleven AMP-skipped updates through20.

A14 selected within epochs1--20 remains epoch10: Macro-F1
0.5588157368155812, accuracy 0.7896039603960396, QWK 0.6110809096674821,
class F1 [0.2857142857142857, 0.45569620253164556,
0.8688524590163934, 0.625]. Epoch20 Macro-F1 is 0.5021215677905819.

Matched A5 selected within epochs1--20 is epoch20: Macro-F1
0.7654421854687274, accuracy 0.7970297029702971, QWK 0.6126648582920213,
class F1 [1, 0.6086956521739131, 0.8637873754152824,
0.5892857142857143].

A14 trails matched A5 by 0.20663 Macro-F1. It has not reached the .75 screen
gate; the single fold0 A case continues to dominate Macro-F1 changes. Continue
registered full50 for a valid screen, with no confirmation folds submitted.
