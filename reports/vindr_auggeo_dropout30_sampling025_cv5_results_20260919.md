# A6: augmentation + dropout 0.3 + sampling power 0.25, completed CV5

Only FIT sampling changed from A5: natural sampling became inverse-frequency
power 0.25 with replacement and the same number of draws per epoch. Shared
DenseNet121, hierarchical fusion, augmentation, dropout 0.3, losses, seed 42,
frozen density split and single-checkpoint inference remained unchanged. No
ensemble was used.

All five folds completed 50 epochs. Fold 0 was retained from screened job 775;
folds 1--4 came from array 776. Confirmation tasks independently verified
`COMPLETED` with `ExitCode=0:0`; folds 1/2 ran on master and folds 3/4 on
worker1, with worker2 excluded. RTX 5090 startup was verified for every task.

Read-only audit **PASS**: checkpoint/history selection, architecture and common
config, frozen manifests and assignment hash, exact DEV membership and labels,
normalized probabilities and argmax, recomputed metrics, and all five W&B runs
finished at 50 epochs. The union contains 2,017 unique cases with support
A/B/C/D = 6/196/1,556/259.

| Fold | Best epoch | DEV Macro-F1 |
|---|---:|---:|
| 0 | 4 | 0.7829792575 |
| 1 | 25 | 0.6194960833 |
| 2 | 12 | 0.6868304061 |
| 3 | 3 | 0.6552764923 |
| 4 | 8 | 0.6381746803 |

Mean Macro-F1 **0.6765513839**, sample SD **0.0644461991**. Mean accuracy is
0.8205365698 ± 0.0140202412 and mean QWK is 0.6528158653 ± 0.0235832965.
Mean class F1 A/B/C/D is 0.5600000000 / 0.6417969022 / 0.8837216711 /
0.6206869623; B/C/D mean is 0.7154018452. Epoch-50 mean Macro-F1 is
0.5297036255 ± 0.0174355678.

Compared with A5, A6 decreases mean Macro-F1 by 0.0262768962, accuracy by
0.0168390536, QWK by 0.0179404904 and B/C/D mean by 0.0217025282. Mean F1
decreases for every class (A/B/C/D deltas: -0.0400000000 / -0.0400294036 /
-0.0100475268 / -0.0150306542). Fold dispersion is lower, but this does not
compensate for the lower mean. Therefore tempered sampling on the A5 parent is
rejected; A5 remains the best completed CV5 arm at 0.7028282801.

These are per-fold best DEV-selected results, not an independent test. The
0.75 target is not met, and no multi-seed success claim is made. The six total
A cases remain too few for a stable A-class conclusion. No additional
experiment is submitted by this report.

Audited JSON: `vindr_auggeo_dropout30_sampling025_cv5_results_20260919.json`.
[W&B summary](https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/nixhkmas)
was independently verified `finished` with the exact mean/SD, 2,017 cases,
fold table, audit artifact, and `independent_test=false`,
`target_met_single_seed=false`, `multi_seed_verified=false`.
