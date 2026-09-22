# A33 common first-40 CV5 review

Array job 993 tasks 1–4 remained RUNNING on permitted RTX 5090 nodes. Actual
epochs were [50, 41, 41, 43, 43], with fold 0 retained from job 992. Selection
is restricted to the common first 40 epochs and is selected DEV, not
independent evaluation.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 2 | 0.815975 | 0.834158 | 0.691212 | 1.000000 / 0.678899 / 0.887755 / 0.697248 |
| 1 | 2 | 0.545568 | 0.784119 | 0.657378 | 0.142857 / 0.509091 / 0.870748 / 0.659574 |
| 2 | 22 | 0.619445 | 0.806452 | 0.586667 | 0.500000 / 0.626506 / 0.879365 / 0.471910 |
| 3 | 33 | 0.670448 | 0.829208 | 0.586164 | 0.666667 / 0.597015 / 0.895385 / 0.522727 |
| 4 | 22 | 0.650992 | 0.799007 | 0.550316 | 0.666667 / 0.588235 / 0.873817 / 0.475248 |

Provisional mean Macro-F1 is **0.660485696**, sample SD **0.099066797**,
and minimum **0.545567705**. Mean accuracy is 0.810588900 and mean QWK is
0.614347365. Mean class F1 A/B/C/D is
0.595238/0.599949/0.881414/0.565341.

The mean improved from the first-20 review, but all three acceptance gates
remain unmet (mean >= 0.70, sample SD <= 0.05, minimum fold >= 0.65). Continue
unchanged to epoch 50 for the preregistered final audit.
