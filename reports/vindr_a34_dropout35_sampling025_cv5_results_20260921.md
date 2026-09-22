# A34 completed CV5: dropout 0.35 with sampling power 0.25

A34 changes only dropout 0.30 -> 0.35 relative to A6. Fold 0 comes from job
997 and folds 1–4 from job 998. Every fold completed 50 epochs with exit code
0 on permitted RTX 5090 nodes; worker2/Vesta was not used.

The read-only audit passed for the frozen split, all 2,017 unique studies,
configuration and architecture provenance, saved checkpoints, predictions,
probability sums, recomputed metrics, and five finished W&B runs.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 0 | 33 | 0.777913 | 0.839109 | 0.613854 | 1.000000 / 0.589744 / 0.899687 / 0.622222 |
| 1 | 4 | 0.729744 | 0.851117 | 0.690563 | 0.666667 / 0.707317 / 0.904992 / 0.640000 |
| 2 | 35 | 0.658355 | 0.831266 | 0.565168 | 0.666667 / 0.626866 / 0.898331 / 0.441558 |
| 3 | 8 | 0.616801 | 0.816832 | 0.616708 | 0.400000 / 0.656716 / 0.887122 / 0.523364 |
| 4 | 18 | 0.551079 | 0.846154 | 0.656351 | 0.000000 / 0.647059 / 0.902711 / 0.654545 |

Selected-fold mean Macro-F1 is **0.6667784264**, sample SD
**0.0898201723**, and minimum **0.5510789005**. Mean accuracy is
0.8368953148, mean QWK is 0.6285288398, and mean class F1 A/B/C/D is
0.546667/0.645540/0.898569/0.576338.

A34 fails all registered gates: mean >=0.70, sample SD <=0.05, and minimum
>=0.65. It is rejected. The dropout midpoint did not interpolate smoothly
between A6 and A30 and did not stabilize the hard folds. These are selected
DEV estimates, not independent-test results.

Audited W&B summary:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/yv44es8x
