# A19 fold0 — first 10 epochs

Job936 remains RUNNING on master RTX5090. All recorded scalar training losses
are finite. Selected through epoch10 is epoch5:

- Macro-F1: 0.750652421402925
- Accuracy: 0.7846534653465347
- QWK: 0.5914543425702065
- F1 A/B/C/D: `[1.0,0.5473684211,0.8552412646,0.6]`
- Severe errors: 0
- Epoch10 Macro-F1: 0.6720768042618684
- Checkpoints at or above .75: 1/10
- AMP-skipped updates: 7
- Aggregate sampled A/B/C/D: `[194,2288,10815,2833]`

At the matched horizon, A6 selects epoch4 at Macro-F1 0.7829792575 with
accuracy 0.8143564356, QWK 0.6444663475 and F1
`[1.0,0.5957446809,0.8756218905,0.6605504587]`. A19 therefore trails its A6
parent by 0.0323268361 and is lower in each B/C/D class. Identical sampled
counts and AMP-skip totals confirm that the beta treatment, rather than a
sampling difference, is active.

A19 narrowly crosses the provisional numeric screen threshold, but the gain
includes the single fold0 A case and common-class evidence is weaker than A6.
Continue the preregistered fold0 unchanged through 50 epochs. Do not expand
folds1--4 before completed audit.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6wtyzm62
