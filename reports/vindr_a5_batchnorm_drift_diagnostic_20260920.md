# A5 DenseNet BatchNorm drift diagnostic

This read-only diagnostic compares the 121 DenseNet121 BatchNorm running-stat
buffers in each selected A5 checkpoint with the ImageNet initialization. It
does not alter predictions or establish that BatchNorm drift causes the CV
dispersion.

| Fold | Selected epoch | Mean standardized running-mean drift | Mean absolute log running-variance ratio |
|---:|---:|---:|---:|
| 0 | 30 | 0.227054 | 0.418065 |
| 1 | 8 | 0.177374 | 0.356957 |
| 2 | 5 | 0.148428 | 0.346639 |
| 3 | 3 | 0.126159 | 0.317155 |
| 4 | 27 | 0.228714 | 0.396144 |

The mean drift statistic is the average across layers of
`mean(abs(trained_mean - initial_mean) / sqrt(initial_variance))`. The
variance statistic averages `abs(log(trained_variance / initial_variance))`.

All selected checkpoints materially modify pretrained BatchNorm statistics,
and the amount varies with training horizon. The evidence is sufficient to
motivate a controlled BN-statistics-freeze screen, especially because the
training batch contains only two exams and four correlated views per exam.
It is not evidence that freezing will improve DEV Macro-F1. A valid test must
keep A5 fixed and change only the BatchNorm running-statistics policy.
