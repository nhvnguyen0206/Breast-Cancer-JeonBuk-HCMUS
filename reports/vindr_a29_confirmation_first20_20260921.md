# A29 confirmation first20 — selected DEV only

Job977 folds1–4 verified RUNNING at elapsed28:53–28:54.
Histories contained [20,20,21,21] epochs; comparison restricted to first20.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | A F1 |
|---|---:|---:|---:|---:|---:|
| 1 | 8 | .5533777778 | .8461538462 | .6641305517 | 0 |
| 2 | 15 | .5418186657 | .8312655087 | .6422080635 | 0 |
| 3 | 13 | .5573547226 | .8564356436 | .6737489906 | 0 |
| 4 | 15 | .6378461565 | .8014888337 | .6191466238 | .5 |

Per-class F1 A/B/C/D:
- Fold1 [0,.7111111111,.9024,.6]
- Fold2 [0,.6896551724,.8917609047,.5858585859]
- Fold3 [0,.6578947368,.9119496855,.6595744681]
- Fold4 [.5,.6136363636,.8717105263,.5660377358]

Fold1 has not improved its best since epoch8. Folds2/3 improve only slightly
over first10. Fold4 gain is driven by recognition of its one A: B/C/D F1,
accuracy and QWK at the selected checkpoint are lower than its first10 best.
Do not interpret that gain alone as broad improvement. All selected A cases
in folds1–3 remain misclassified as B. Continue all four unchanged to50;
no fold replacement, early stopping, split change or ensemble.
No final CV5 summary by mixing completed fold0 with partial confirmations.
Next review at30 epochs. These are tuning DEV results, not independent test.
