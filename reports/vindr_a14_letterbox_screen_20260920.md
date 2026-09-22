# A14 letterbox — completed fold-0 screen

Screen audit PASS against the frozen grouped split and live W&B run. All 50
epochs completed; scalar train losses finite; checkpoint, predictions,
manifests, labels, probabilities and W&B selection agree. Architecture remains
DenseNet121 hierarchical bilateral multitask; selected DEV is not an
independent test.

Selected epoch10: Macro-F1 0.5588157368155812, accuracy
0.7896039603960396, QWK 0.6110809096674821, class F1
[0.2857142857142857, 0.45569620253164556, 0.8688524590163934, 0.625].
Epoch50 Macro-F1 0.5171638803336838. Zero of 50 epochs reached .75;
18 AMP-skipped updates total.

A14 fails the preregistered expansion gate and is rejected. Do not submit
folds1--4. A5 fold0 selected Macro-F1 0.7896498561536562, so aspect-preserving
letterbox plus centered zero padding is substantially worse in this pipeline.
This tests the complete preprocessing change, not whether aspect preservation
would work with a tighter crop or higher occupied resolution.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/p5m57omo
