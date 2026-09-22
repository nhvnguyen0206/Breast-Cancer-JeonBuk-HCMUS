# A33 common first-10 CV5 review

Array job 993 tasks 1–4 remained RUNNING on permitted RTX 5090 nodes. Actual
epochs were [50, 10, 10, 10, 10], with fold 0 retained from job 992. All
reported training losses are finite. Selection is restricted to the common
first ten epochs and is selected DEV, not independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 2 | 0.815975 | 0.834158 | 0.691212 | 1.000000 / 0.678899 / 0.887755 / 0.697248 |
| 1 | 2 | 0.545568 | 0.784119 | 0.657378 | 0.142857 / 0.509091 / 0.870748 / 0.659574 |
| 2 | 3 | 0.582166 | 0.754342 | 0.578166 | 0.400000 / 0.534483 / 0.836489 / 0.557692 |
| 3 | 1 | 0.604775 | 0.814356 | 0.613007 | 0.400000 / 0.604651 / 0.885714 / 0.528736 |
| 4 | 9 | 0.587042 | 0.826303 | 0.619226 | 0.333333 / 0.537313 / 0.896875 / 0.580645 |

Provisional mean Macro-F1 is **0.6271052299**, sample SD **0.1077538685**,
and minimum **0.5455677048**. Mean accuracy is 0.8026558239 and mean QWK is
0.6317979663. Mean class F1 A/B/C/D is
0.455238/0.572887/0.875516/0.604779.

All acceptance gates currently fail. Fold 0 is not representative of the
other folds at this early horizon. Continue all tasks unchanged to common
first-20; do not accept, stop, or alter the experiment based on first ten.
