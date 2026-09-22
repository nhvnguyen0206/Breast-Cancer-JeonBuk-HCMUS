# A5: augmentation + dropout 0.3, completed CV5

Only dropout changed from A1 (0.1 to 0.3). Shared DenseNet121,
hierarchical fusion, seed42 and frozen density split unchanged. No ensemble.
All five runs completed 50 epochs. Fold0 job770; folds1--4 array771.
Confirmation tasks independently verified COMPLETED ExitCode=0:0;
folds1/2 on master, folds3/4 on worker1, worker2 excluded.
End times (2026-09-19): f1 11:23:01, f2 11:23:04,
f3 11:20:22, f4 11:19:52. RTX5090 startup was verified previously.

Read-only audit PASS: checkpoint/history selection, architecture and common
config, frozen manifests/hash, unique DEV membership/labels, normalized
probabilities and argmax, recomputed metrics, all W&B runs finished50.
Union 2017 cases, support A/B/C/D = 6/196/1556/259.

| Fold | Best epoch | DEV Macro-F1 |
|---|---:|---:|
| 0 | 30 | 0.7896498562 |
| 1 | 8 | 0.5792311841 |
| 2 | 5 | 0.7991001000 |
| 3 | 3 | 0.5701863354 |
| 4 | 27 | 0.7759739248 |

Mean Macro-F1 **0.7028282801**, sample SD **0.1172888127**.
Accuracy 0.8373756234 ± 0.0258578896; QWK 0.6707563558 ± 0.0326389085.
Mean class F1 A/B/C/D: 0.6000000000 / 0.6818263058 /
0.8937691979 / 0.6357176166. BCD mean 0.7371043734.
Epoch50 mean Macro-F1 0.5598344538 ± 0.1078510234.

A5 improves on A1 mean 0.6799754745 by 2.2853 percentage points,
but dispersion increases from 0.0971587423. Mean A F1 decreases slightly
(0.613333 to 0.600000), while mean B/C/D improve; this mean gain is not
solely an A-class gain. Nevertheless A F1 is zero on folds1/3 and one on
the other folds, with only six A cases total. This prevents strong stability
claims. The large selected-versus-final gap also persists.

These are selected DEV results, not an independent test; no multi-seed
confirmation and target 0.75 not met. A5 is the best completed CV5 mean
in this campaign so far. Next decision should examine paired class errors
and training dynamics before preregistering another single-factor screen
on fixed fold0. No new experiment submitted by this report.

Audited JSON: `vindr_auggeo_dropout30_cv5_results_20260919.json`.
[W&B summary](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/bj99x9ia)
verified finished, exact mean, 2017 cases, fold table and audit artifact;
independent_test=false, multi_seed_verified=false.
