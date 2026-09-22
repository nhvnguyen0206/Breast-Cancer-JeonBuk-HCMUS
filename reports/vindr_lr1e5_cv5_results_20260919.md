# Lower-LR O1 CV5: completed 2026-09-19

All five folds completed 50 epochs on RTX 5090, excluding Vesta. Frozen
density/group split and seed 42 were unchanged. Relative to B0, only learning
rate changed from 5e-5 to 1e-5 (zero validation workers is a previously
verified runtime-only mitigation). Results are DEV-selected, not an independent
test.

| Metric | Baseline B0 | Lower-LR O1 |
|---|---:|---:|
| Mean best four-class Macro-F1 | 60.12% | 63.52% |
| Sample SD across folds | 5.62 pp | 10.23 pp |
| Mean best-checkpoint accuracy | 81.86% | 84.43% |
| Mean best-checkpoint QWK | 0.6204 | 0.6633 |
| Mean epoch-50 Macro-F1 | 51.86% | 50.25% |
| Mean selected B/C/D F1 | 69.37% | 73.58% |

| Fold | Best epoch | O1 Macro-F1 | Change vs B0 | B/C/D change |
|---|---:|---:|---:|---:|
| 0 | 13 | 79.68% | +11.40 pp | +4.09 pp |
| 1 | 4 | 56.81% | +0.55 pp | +0.74 pp |
| 2 | 15 | 67.77% | +9.87 pp | +0.46 pp |
| 3 | 7 | 56.44% | +1.69 pp | +2.25 pp |
| 4 | 5 | 56.90% | -6.54 pp | +13.50 pp |

The requested mean four-class target was not achieved. O1 improved mean
Macro-F1 by 3.39 pp, mean accuracy by 2.58 pp and mean QWK by 0.043, but fold
dispersion almost doubled. Only folds 0 and 2 recognized their single A case;
folds 1/3/4 had A F1 zero. In contrast, descriptive B/C/D mean increased in
every fold. This supports retaining low LR as a component to test with a mild
imbalance treatment, but does not justify multi-seed confirmation of O1 alone.

Epoch-50 mean Macro-F1 was only 50.25%, below B0's 51.86%; selected epochs were
4--15. The large peak-to-final gap shows material temporal instability despite
the lower LR.

Pooled selected-checkpoint metrics (descriptive only): Macro-F1 66.35%,
accuracy 84.43%, QWK 0.6630. Pooled class F1 A/B/C/D =
44.44%/70.73%/90.12%/60.08%. True-class supports are 6/196/1556/259.
Do not substitute the pooled metric for the requested mean per-fold metric.

```text
          predicted A  B    C    D
true A              2  4    0    0
true B              1 145  50    0
true C              0  65 1410   81
true D              0  0  113  146
```

Verified: Slurm COMPLETED exit 0 for all folds; exact 50-epoch histories; W&B
`finished`, 50 epochs and no early stop; checkpoint equals history maximum;
prediction metrics equal checkpoint; probabilities finite, normalized and
argmax-consistent; membership/labels match frozen manifests; exactly 2,017
unique pooled cases.

W&B IDs in fold order: a7d4bt0w, 77eq4ie2, tjwdppss, vsh65hkq, 8rvtdj1d.

Decision: target 75% mean not achieved. Do not run additional seeds for O1
alone. A controlled follow-up may add only mild sampling to O1, screening fixed
fold 0 first; retain the same architecture, split and seed.
