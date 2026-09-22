# Selected-DEV fold variance decomposition

Read-only calculation from completed audited A5, A6 and A22 CV5 reports.
For each fold, M = A + B where A = F1_A / 4 and
B = (F1_B + F1_C + F1_D) / 4. Sample variance satisfies
Var(M) = Var(A) + Var(B) + 2 Cov(A,B). The identity was checked numerically.

| Arm | Macro SD | SD of A contribution | SD of BCD contribution | Cov(A,B) | BCD mean | BCD SD |
|---|---:|---:|---:|---:|---:|---:|
| A5 | 0.117289 | 0.136931 | 0.021835 | -0.00273506 | 0.737104 | 0.029114 |
| A6 | 0.064446 | 0.062750 | 0.015690 | -0.00001518 | 0.715402 | 0.020920 |
| A22 | 0.090328 | 0.097272 | 0.025607 | -0.00097921 | 0.696880 | 0.034143 |

The A contribution varies much more than the combined BCD contribution.
Negative covariance means these variances cannot be presented as additive
percentages without the covariance term. A6 reduces both contributions but
also reduces BCD mean. A22 reduces A variability versus A5 while degrading
BCD mean and increasing BCD variability.

This explains the arithmetic of fold dispersion; it does not identify the
cause of rare-A errors. There are only six unique A studies. Repeated DEV
selection remains an additional limitation. The four-class acceptance metric,
fixed folds, and seed stay unchanged; BCD is diagnostic only.

For ongoing A23, the selected checkpoint through epoch30 has weaker BCD than
its parent A6. That observation alone does not prove sampling power 0.35
causes generally worse BCD learning: selection depends on the rare A case,
and later checkpoints have different BCD performance. Complete the registered
screen before choosing the next experiment.
