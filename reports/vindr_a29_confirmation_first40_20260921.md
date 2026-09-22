# A29 confirmation first40 — selected DEV only

Job977 folds1–4 verified RUNNING at elapsed57:59–58:00.
Histories [40,40,42,43]; comparison restricted to first40.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | A F1 |
|---|---:|---:|---:|---:|---:|
| 1 | 26 | .5669240438 | .8511166253 | .6896100228 | 0 |
| 2 | 24 | .6340591474 | .8486352357 | .6572699262 | .4 |
| 3 | 13 | .5573547226 | .8564356436 | .6737489906 | 0 |
| 4 | 38 | .6628648704 | .8163771712 | .5791538483 | .6666666667 |

Folds1–3 best checkpoints unchanged since first30. Fold4 per-class F1:
[.6666666667,.5555555556,.8857589984,.5434782609].
Fold4 selected confusion matrix true rows A/B/C/D:
[[1,0,0,0],[1,20,18,0],[0,13,283,15],[0,0,27,25]].
Its Macro-F1 gain is not broad: A/C improve but B/D F1 and QWK decline
relative to its first30 selected checkpoint. No stable high-CV5 claim.
Continue all four unchanged to50, retain original976fold0; final audit after
all finish. Next score report at completion, no mixed-budget final summary.
