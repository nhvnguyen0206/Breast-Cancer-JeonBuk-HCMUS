# A19 fold0 — first 20 epochs

Job936 remains RUNNING on master RTX5090. All recorded scalar training losses
are finite. Selected through epoch20 improves to epoch11:

- Macro-F1: 0.7623856925078064
- Accuracy: 0.7772277227722773
- QWK: 0.6014556296036478
- F1 A/B/C/D: `[1.0,0.6419753086,0.8464163823,0.5611510791]`
- Confusion matrix: `[[1,0,0,0],[0,26,14,0],[0,15,248,48],[0,0,13,39]]`
- Severe errors: 0
- Epoch20 Macro-F1: 0.5061134169344099
- Checkpoints at or above .75: 3/20
- AMP-skipped updates: 10
- Aggregate sampled A/B/C/D: `[376,4537,21638,5709]`

At the same horizon, A6 remains 0.7829792575 and A5 reaches 0.7654421855.
A19 trails A6 by 0.0205935650 and A5 by 0.0030564930. Relative to A6, A19
raises B F1 by 0.0462306278 but lowers C by 0.0292055083 and D by
0.0993993796. Its three gate crossings are more frequent than A5/A6 (one
each), but each selected result still includes the single fold0 A case.

The beta treatment has altered the B/C/D tradeoff but has not yet improved
the substantive parent result. Continue the preregistered fold0 unchanged to
50 epochs; no folds1--4 confirmation before completed audit.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6wtyzm62
