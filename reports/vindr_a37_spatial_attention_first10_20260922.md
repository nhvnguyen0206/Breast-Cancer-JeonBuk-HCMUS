# A37 spatial-token attention common first-10 review

Both fixed stress folds reached epoch 10 normally. Selection uses the best
DEV Macro-F1 within the common first-10 window.

| Fold | Best epoch | Macro-F1 | Accuracy | F1 A/B/C/D | QWK |
|---|---:|---:|---:|---|---:|
| 1 | 1 | 0.570846 | 0.863524 | 0.0000 / 0.6667 / 0.9140 / 0.7027 | 0.693358 |
| 3 | 3 | 0.619532 | 0.811881 | 0.3636 / 0.6154 / 0.8837 / 0.6154 | 0.670562 |

The two-fold mean is 0.595189, sample SD 0.034426 and minimum 0.570846.
Dispersion is initially much lower than A36, and fold 1 is slightly higher,
but the mean is substantially worse because fold 3 has not reproduced A36's
early gain. Both expansion gates fail.

Continue unchanged to common epoch 20 to distinguish slower optimization of
64 spatial tokens from a genuinely inferior architecture. Do not expand to
folds 0/2/4.

