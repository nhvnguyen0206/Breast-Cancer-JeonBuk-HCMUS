# A29 confirmation first30 — selected DEV only

Job977 folds1–4 verified RUNNING at elapsed43:21–43:22.
Histories [30,30,31,32], comparison restricted to first30 epochs.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | A F1 |
|---|---:|---:|---:|---:|---:|
| 1 | 26 | .5669240438 | .8511166253 | .6896100228 | 0 |
| 2 | 24 | .6340591474 | .8486352357 | .6572699262 | .4 |
| 3 | 13 | .5573547226 | .8564356436 | .6737489906 | 0 |
| 4 | 15 | .6378461565 | .8014888337 | .6191466238 | .5 |

Per-class F1 A/B/C/D:
- Fold1 [0,.7368421053,.9082125604,.6226415094]
- Fold2 [.4,.7012987013,.9099378882,.525]
- Fold3 [0,.6578947368,.9119496855,.6595744681]
- Fold4 [.5,.6136363636,.8717105263,.5660377358]

Fold1 B/C/D all improve at its selected checkpoint relative to first20,
but its A remains missed. Fold2 gain is mostly A recognition; D F1 drops
from .5858586 to .525. Folds3/4 selected bests unchanged since first20.
This is not evidence of stable high performance across folds.
Continue unchanged to50. Do not combine partial confirmation results with
completed fold0 into a final CV5 claim. Next score review at40 epochs.
