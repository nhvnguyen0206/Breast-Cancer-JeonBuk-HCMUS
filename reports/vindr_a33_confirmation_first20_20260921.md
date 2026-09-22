# A33 common first-20 CV5 review

Array job 993 tasks 1–4 remained RUNNING on permitted RTX 5090 nodes. Actual
epochs were [50, 20, 20, 21, 21], with fold 0 retained from job 992. All
reported training losses are finite. Selection is restricted to common first
20 epochs and is selected DEV, not independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 2 | 0.815975 | 0.834158 | 0.691212 | 1.000000 / 0.678899 / 0.887755 / 0.697248 |
| 1 | 2 | 0.545568 | 0.784119 | 0.657378 | 0.142857 / 0.509091 / 0.870748 / 0.659574 |
| 2 | 3 | 0.582166 | 0.754342 | 0.578166 | 0.400000 / 0.534483 / 0.836489 / 0.557692 |
| 3 | 1 | 0.604775 | 0.814356 | 0.613007 | 0.400000 / 0.604651 / 0.885714 / 0.528736 |
| 4 | 20 | 0.632226 | 0.789082 | 0.614241 | 0.500000 / 0.574713 / 0.860972 / 0.593220 |

Provisional mean Macro-F1 is **0.6361421088**, sample SD **0.1054234302**,
and minimum **0.5455677048**. Mean accuracy is 0.7952116552 and mean QWK is
0.6308009356. Mean class F1 A/B/C/D is
0.488571/0.580367/0.868336/0.607294.

Only fold 4 improved after first10. Mean, SD, and minimum all remain outside
their acceptance limits, and the strong fold0 result has not generalized.
Continue all tasks unchanged to common first40; no acceptance or early stop.
