# A30 preregistration: moderate dropout on A6

Parent A6, not A29. Only learning change: dropout .3->.4. Retain sampling
power .25, original brightness .9–1.1, all losses, optimizer/LR/weight decay,
AMP, batch2, cache, preprocessing, seed42 and frozen grouped split.
Config: configs/vindr_density_auggeo_dropout40_sampling025.yaml.

Rationale: A6 remains the stronger stability reference (.6765514 mean,
.0644462 sampleSD, .6194961 minimum). Test whether moderate activation
dropout with repeated minority exposure improves generalization. This is an
untested interaction hypothesis, not evidence that A6 is overfitting or that
scores will improve. A9 dropout .5 on natural-sampling A5 harmed B/D and
CV5 mean; A28 stronger weight decay on A6 also failed. Neither result
supports indiscriminately increasing regularization. The .4 change is a
bounded intermediate test on a different, explicitly fixed sampling parent.
Do not adopt it unless the complete unchanged protocol supports it.

Before submission: clone immutable A6; only add this config, verify exact
parsed delta (dropout and arm metadata), source/script/split byte parity,
run snapshot tests and validate sampler/config. Do not deploy dirty local
source edits. Run fixed fold0 full50 on RTX5090 only, exclude worker2,
never Vesta. No other training submitted before this preflight.

Expand fresh folds1–4 only after completed screen audit PASS and selected
DEV Macro-F1>=.75, retain original fold0. Final joint acceptance:
mean>=.70, sampleSD<=.05, minimum>=.65, seed42; aspiration mean>=.75.
No ensemble or changed checkpoint selection. Selected DEV is not independent
test; six A cases limit claims. Report B/C/D as well as all four classes.
Review scores every10–20 epochs. No job submitted at preregistration.

## Deployment

Cloned immutable A6 to
/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout40-sampling025-20260921-v1.
Parsed config delta exactly dropout and arm metadata PASS; source/scripts/
split byte parity PASS; assignment digest unchanged. Snapshot unittest
discovery exited0. Sampling implementation/config identical to parent A6.
Config SHA256 a9a96fd9e28dbfa8a34d187376e416d191bb6605bb5d5f9bb0ab7cb2806c112d.
Submitted fixed fold0 only as job981_0. No confirmation folds submitted.
Verified RUNNING on master; launch log explicitly reports NVIDIA GeForce
RTX5090. W&B run metadata created:
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/u5g2ni5n
At initial29-second check no epoch completed yet; no score claim.
