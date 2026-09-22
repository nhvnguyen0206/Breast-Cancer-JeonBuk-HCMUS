# A29 confirmation first10 — selected DEV only

Job977 folds1–4 all reached10 completed epochs. No configuration changes.
Best checkpoints within first10, not final50 selections:

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | A F1 |
|---|---:|---:|---:|---:|---:|
| 1 | 8 | .5533777778 | .8461538462 | .6641305517 | 0 |
| 2 | 7 | .5406332196 | .8387096774 | .6320875293 | 0 |
| 3 | 9 | .5520062796 | .8564356436 | .6590915704 | 0 |
| 4 | 5 | .5445265081 | .8138957816 | .6398913419 | 0 |

Per-class F1 A/B/C/D:
- Fold1 [0,.7111111111,.9024,.6]
- Fold2 [0,.7012987013,.8987341772,.5625]
- Fold3 [0,.7368421053,.9130434783,.5581395349]
- Fold4 [0,.6944444444,.8762541806,.6074074074]

All rare A DEV examples are predicted B at these selected checkpoints.
This explains part of low four-class Macro-F1 but does not justify dropping A,
changing split, or selecting folds. B/D remain weaker than C.
No final CV5 mean/SD is reported by mixing these partial runs with completed
fold0. Continue all four unchanged through50; next review at20 epochs.
