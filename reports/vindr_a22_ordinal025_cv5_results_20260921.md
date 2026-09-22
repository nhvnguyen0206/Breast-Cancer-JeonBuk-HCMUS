# A22 ordinal-0.25 — audited CV5 result

The five-fold audit passed checkpoint, prediction, probability, split,
provenance and W&B consistency checks. All jobs completed 50 epochs on RTX
5090 with no restart or requeue.

| Fold | Best epoch | Macro-F1 | Accuracy | QWK |
|---:|---:|---:|---:|---:|
| 0 | 22 | 0.771853 | 0.801980 | 0.625822 |
| 1 | 10 | 0.566206 | 0.848635 | 0.672144 |
| 2 | 9 | 0.681848 | 0.821340 | 0.615531 |
| 3 | 15 | 0.593283 | 0.821782 | 0.628439 |
| 4 | 29 | 0.562611 | 0.791563 | 0.629839 |

- Mean Macro-F1: **0.635160**
- Sample SD: **0.090328**
- Minimum fold: **0.562611**
- Mean accuracy: **0.817060**
- Mean QWK: **0.634355**
- Mean F1 A/B/C/D: **0.450000 / 0.621893 / 0.884186 / 0.584562**
- Pooled descriptive Macro-F1: **0.623571**

A22 fails the agreed mean `>=0.70`, sample SD `<=0.05`, and minimum-fold
`>=0.65` criteria. Reducing the ordinal coefficient from 0.5 to 0.25 harms
the A5 mean by `0.067668` and does not solve fold instability. Reject A22 and
retain A5 as the strongest completed mean-CV5 reference. These are selected
DEV results, not an independent test; class A has only six cases in total.

[Audited W&B CV5 summary](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/uytf37nh)
