# A13: ordinal-bias LR multiplier 10, completed CV5

Audit PASS: all five source W&B runs finished 50 epochs; checkpoint selection,
stored predictions and frozen manifests agree, unique DEV union 2017.
Confirmation jobs 860_1--4 COMPLETED, ExitCode 0:0, Restarts 0, Requeue 0;
master/worker1 only, worker2 excluded. Recorded scalar train losses finite.
Retained screened fold0 job852; no ensemble or independent test.

Selected-DEV Macro-F1 mean 0.6083934605957435, sample SD 0.08403430838315352,
minimum 0.5632771274097002. Accuracy 0.8319337640960126; QWK 0.6395174220721775.
Class mean F1 A/B/C/D: 0.316667 / 0.626794 / 0.896327 / 0.593786.
Fold scores: 0.758053 / 0.567588 / 0.563277 / 0.568871 / 0.584177;
selected epochs: 20 / 33 / 36 / 2 / 21.
Epoch50 mean Macro-F1 0.5245928851595144.

A5 remains better: mean 0.7028282800839902, SD 0.1172888127211152,
minimum 0.5701863354037267. A13 reduces SD by lowering overall performance;
it fails all joint thresholds (mean >=.70, SD <=.05, minimum >=.65).
Reject A13 as an improvement; do not use it as the next baseline.
Only six A cases; pooled predictions have 3 A correct, 3 A->B and 10 B->A.
Lower ordinal training loss did not translate into improved classification.
Audit verifies saved outputs, not fresh forward inference or visual cache quality.

W&B summary: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/5lipxk3w
