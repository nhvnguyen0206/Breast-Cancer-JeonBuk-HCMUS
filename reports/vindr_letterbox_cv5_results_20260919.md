# Letterbox CV5: completed 2026-09-19

All five folds completed 50 epochs on RTX 5090, excluding Vesta.
Frozen density/group split and seed 42 unchanged. Only resize geometry changed
against B0. Results are DEV-selected, not an independent final test.

| Metric | Baseline B0 | Letterbox L1 |
|---|---:|---:|
| Mean best four-class Macro-F1 | 60.12% | 61.91% |
| Sample SD across folds | 5.62 pp | 8.08 pp |
| Mean best-checkpoint accuracy | 81.86% | 81.11% |
| Mean best-checkpoint QWK | 0.6204 | 0.6126 |
| Mean epoch-50 Macro-F1 | 51.86% | 49.91% |

| Fold | Best epoch | L1 Macro-F1 | Change vs B0 |
|---|---:|---:|---:|
| 0 | 16 | 75.72% | +7.44 pp |
| 1 | 3 | 55.89% | -0.37 pp |
| 2 | 31 | 58.84% | +0.94 pp |
| 3 | 23 | 56.97% | +2.21 pp |
| 4 | 20 | 62.12% | -1.32 pp |

The +1.78 pp mean gain does not demonstrate robust improvement: dispersion
increased, B/C/D descriptive mean at selected checkpoints declined in four
of five folds, and mean accuracy/QWK declined. Fold 0's peak depends strongly
on its single class-A DEV case. Pooled Macro-F1 is 60.88%, versus B0 61.56%.
Do not substitute pooled scores for the requested mean per-fold score.

Pooled class F1: A 38.10%, B 60.05%, C 88.11%, D 57.26%.
True-class supports A/B/C/D = 6/196/1556/259. Confusion (true rows):

```text
          predicted A B    C    D
true A              4 2    0    0
true B             10 127 59    0
true C              1 97  1363 95
true D              0 1   116  142
```

Verified: complete epoch histories; W&B finished with no early stop;
best checkpoint matches history maximum; prediction CSV metrics match
checkpoint; probabilities finite, normalized and argmax-consistent; DEV
membership/labels match frozen manifests; exactly 2,017 unique pooled cases.

W&B IDs in fold order: 4lbfmjyc, pcruvhxl, wqxdgc1u, 3epkvxx9, rx2441bh.
Raw metrics: [JSON](vindr_letterbox_cv5_results_20260919.json).

Decision: target 75% mean not achieved. Do not launch multi-seed confirmation
for letterbox alone as a successful candidate. Continue controlled sampling
and learning-rate screens; preserve this completed, mixed-result experiment.
