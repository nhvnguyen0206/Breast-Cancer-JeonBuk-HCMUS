# A22 CV5 confirmation — first 30 epochs

All confirmation tasks remain healthy on RTX 5090 nodes with no requeue or
restart. Best selected DEV checkpoints through epoch 30 are:

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 22 | 0.771853 | 0.801980 | 0.625822 | 1.000000 / 0.595745 / 0.866667 / 0.625000 |
| 1 | 10 | 0.566206 | 0.848635 | 0.672144 | 0.000000 / 0.763158 / 0.903537 / 0.598131 |
| 2 | 9 | 0.681848 | 0.821340 | 0.615531 | 0.666667 / 0.673267 / 0.887460 / 0.500000 |
| 3 | 15 | 0.593283 | 0.821782 | 0.628439 | 0.333333 / 0.555556 / 0.892405 / 0.591837 |
| 4 | 29 | 0.562611 | 0.791563 | 0.629839 | 0.250000 / 0.521739 / 0.870861 / 0.607843 |

Temporary mean Macro-F1 is **0.635160**, sample SD **0.090328**, minimum
**0.562611**, mean accuracy **0.817060**, and mean QWK **0.634355**. Mean class
F1 A/B/C/D is `0.450000 / 0.621893 / 0.884186 / 0.584562`. Mean performance
improved again, but dispersion also increased. Continue unchanged through
epoch 50; next review is epoch 40.
