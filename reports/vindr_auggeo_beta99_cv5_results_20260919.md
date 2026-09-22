# A3: augmentation + beta 0.99, completed CV5

Only loss.beta changes from .999 to .99 relative to A1. This changes class
weight ratios and effective loss scale for focal and binary terms.
Same architecture, split, seed 42, fresh ImageNet and 50 epochs per fold.
No ensemble; flat-head single-checkpoint predictions.

| Fold | Best DEV epoch | Macro-F1 |
|---|---:|---:|
| 0 | 14 | 0.7752373149 |
| 1 | 13 | 0.5725595526 |
| 2 | 18 | 0.7978324071 |
| 3 | 19 | 0.5509285166 |
| 4 | 31 | 0.6740580848 |

Mean Macro-F1 **0.6741231752**, sample SD **0.1129381921**.
Mean accuracy 0.8319399061, QWK 0.6419252803.
Mean class F1 A/B/C/D: 0.5833333333, 0.6325155465, 0.8941654782, 0.5864783427.
Mean B/C/D F1 0.7043864558.
Epoch-50 mean Macro-F1 0.5529984318.

A3 does not meet .75 and is 0.585 percentage points below A1 (.6799754745),
with larger fold dispersion. B/C/D mean is only slightly above A1 (.7021895215).
Do not advance A3 to multi-seed confirmation as a successful candidate.

Full audit PASS: exact epochs 1–50; checkpoint/history selection; frozen
assignment hash and FIT/DEV manifests; exact unique prediction IDs and labels;
finite normalized probabilities and argmax; recomputed metrics; finished W&B.
2017 unique cases, support [6,196,1556,259]. Slurm 756_0 and 761_1–4 completed
exit 0, RTX5090 startup verified, worker-2/Vesta excluded.
Selected DEV results are not independent-test estimates. Rare A has only six
cases; neither multi-seed stability nor target achievement is established.

W&B source runs:
- Fold 0: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/gvcsv9lm
- Fold 1: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/sfdz24yr
- Fold 2: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/m8s2uyk6
- Fold 3: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/mo99kw4x
- Fold 4: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/jud6l8uz
