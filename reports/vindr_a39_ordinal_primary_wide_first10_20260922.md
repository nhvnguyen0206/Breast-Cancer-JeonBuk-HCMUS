# A39 corrected ordinal-primary common first-10 review

Both folds reached epoch 10 normally. The spacing-2 correction removes A38's
initial extreme-class collapse.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK |
|---|---:|---:|---:|---|---:|
| 1 | 5 | 0.541072 | 0.828784 | 0.0000 / 0.6250 / 0.8936 / 0.6457 | 0.663031 |
| 3 | 1 | 0.594343 | 0.732673 | 0.4000 / 0.6304 / 0.8094 / 0.5375 | 0.599728 |

The two-fold mean is 0.567707, sample SD 0.037669 and minimum 0.541072.
This is a large controlled improvement over A38 first10 mean 0.116009 and
validates the threshold-initialization diagnosis. It does not yet meet either
expansion gate; fold 1 still has F1_A=0.

Continue unchanged to common epoch 20. Do not expand to folds 0/2/4.

