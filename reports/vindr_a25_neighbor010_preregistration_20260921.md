# A25: reduced neighbor penalty, registered before launch

Parent is immutable A5, not A24. Only loss.neighbor changes .2 -> .1
(plus arm metadata). Preserve architecture, heads, seed42, split/cache,
augmentation, natural sampling, optimizer, AMP, and full50 schedule.

The neighbor term minimizes expected cost under an asymmetric-in-distance
cost matrix: C/D errors cost3, B/C errors1.5. It is not class balanced and
can compete with the class-balanced focal objective under dominant C support.
Reducing its weight tests that interaction, not a demonstrated root cause.
All inspected previous candidate configs retain neighbor=.2. Retain the
term and all heads; single flat-head inference, no ensemble.

First validate semantic delta, source parity, all frozen manifests and tests.
Run fixed fold0 full50 on RTX5090, excluding worker2 and Vesta, no requeue.
Only completed audited selected DEV Macro-F1>=.75 permits fresh folds1–4;
retain screen fold0. Accept CV5 only at mean>=.70, sample SD<=.05, min>=.65;
aspirational mean>=.75. Report per-class F1, accuracy and QWK; six A studies
limit certainty. Selected DEV is not an independent test. Review at 10–20
epoch intervals, not every epoch. Do not alter selection based on outcomes.

## Deployment

Cloned immutable A5 into
`/slurmshared/Ngoc/code/hcmus-density-auggeo-dropout30-neighbor010-20260921-v1`.
Source/scripts/split byte parity verified, all five manifests validated with
frozen assignment hash, and parsed config differs only in neighbor and arm.
Config SHA256: `3c230881a20d0bb3eb2fb4364c44069e93d00d07f6c7cb8c87d24d1cf575619e`.
Remote regression suite:16/16 PASS. Submitted fold0 only as job962.
No confirmation submitted; no result claimed at submission.
Job962_0 verified RUNNING on master, Requeue0/Restarts0, worker2 excluded.
W&B run: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/vjgvwnx6
