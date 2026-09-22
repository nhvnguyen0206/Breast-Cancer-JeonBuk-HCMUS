# A22 CV5 confirmation — first 20 epochs

All confirmation tasks remain healthy on RTX 5090 nodes with no requeue or
restart. Best selected DEV checkpoints through epoch 20 are:

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 18 | 0.688852 | 0.809406 | 0.625421 | 0.666667 / 0.613333 / 0.875410 / 0.600000 |
| 1 | 10 | 0.566206 | 0.848635 | 0.672144 | 0.000000 / 0.763158 / 0.903537 / 0.598131 |
| 2 | 9 | 0.681848 | 0.821340 | 0.615531 | 0.666667 / 0.673267 / 0.887460 / 0.500000 |
| 3 | 15 | 0.593283 | 0.821782 | 0.628439 | 0.333333 / 0.555556 / 0.892405 / 0.591837 |
| 4 | 8 | 0.524670 | 0.794045 | 0.623131 | 0.000000 / 0.631579 / 0.860544 / 0.606557 |

Temporary mean Macro-F1 is **0.610972**, sample SD **0.072204**, and minimum
**0.524670**. Mean class F1 A/B/C/D is
`0.333333 / 0.647379 / 0.883871 / 0.579305`. The mean improved from the
first-10 horizon, but dispersion increased and no fold has crossed `0.75`
within its first 20 epochs. Continue unchanged; next review is epoch 30.
