# A43 multi-scale four-view Transformer — common first 20 epochs

Both job-1041 tasks remain RUNNING on worker1 RTX 5090 and completed epoch 20.
The reproducible horizon summary is unchanged from first10.

| Fold | Selected epoch <=20 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 2 | 7 | 0.799443 | 0.836228 | 0.668040 | 1.0000 / 0.7158 / 0.8925 / 0.5895 |
| 3 | 7 | 0.678563 | 0.806931 | 0.611126 | 0.6667 / 0.6882 / 0.8752 / 0.4842 |

Aggregate mean is `0.7390029`, sample SD `0.0854750`, minimum `0.6785630`,
accuracy `0.8215795`, QWK `0.6395829`, and B/C/D F1 mean `0.7075594`. The
registered mean and minimum screen gates remain provisionally met, but there
was no checkpoint improvement between epochs 11 and 20.

At epoch 20 itself, fold-2/fold-3 Macro-F1 is `0.5243444/0.5365968` and both
have A F1 `0`. The selected gain therefore depends on transient recovery of
rare A at epoch 7, while substantive B/C/D performance remains below A41.
Continue full50 and audit without expansion or tuning.
