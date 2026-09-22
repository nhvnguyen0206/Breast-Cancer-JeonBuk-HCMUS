# A12 completed CV5: focal gamma1 on A5

Audit PASS: exact50 epochs, common configuration, frozen manifests,
checkpoint selection, prediction-derived metrics and finished W&B source runs.
All848 tasks completed ExitCode0:0, no restarts/requeue, master/worker1;
RTX5090 startup verified, worker2 excluded. All scalar training losses finite.

Selected-DEV mean Macro-F1 .6214802421275368, sample SD .09823553898728177.
Accuracy .8363781539444267, QWK .6381084466002989.
Class F1 means [.36,.6605213336551757,.8985955965112578,.5668040383437138].
BCD mean .7086403228367157; epoch50 Macro-F1 mean .540344778192545.
Fold scores [.7946366892484166,.5753719449613244,.5955795592068516,
.5521248178727538,.5896881993483378], selected epochs [27,9,38,34,24].

Reject relative to A5 mean .7028282800839902 and BCD .7371043734453203.
C slightly improves but A/B/D regress; the deficit is not solely rare A.
Retain A5 as parent. No ensemble, independent test or multi-seed success.
Visual crop/label review and fresh forward inference are not covered by audit.

W&B summary nwuuq6k9 independently verified finished: aggregate scalars,
source IDs, 2017 cases, false independent-test/multi-seed flags, fold table
and cv5-audit artifact.
https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/nwuuq6k9
