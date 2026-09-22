# A43 multi-scale four-view Transformer — common first 30 epochs

Both job-1041 tasks remain RUNNING on worker1 RTX 5090 and completed epoch 30.
Fold 3 improves at the horizon endpoint while fold 2 retains epoch 7.

| Fold | Selected epoch <=30 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 2 | 7 | 0.799443 | 0.836228 | 0.668040 | 1.0000 / 0.7158 / 0.8925 / 0.5895 |
| 3 | 30 | 0.715252 | 0.841584 | 0.654839 | 0.6667 / 0.7397 / 0.9002 / 0.5545 |

Aggregate mean is `0.7573472`, sample SD `0.0595321`, minimum `0.7152517`,
accuracy `0.8389062`, QWK `0.6614393`, and B/C/D F1 mean `0.7320185`. Both
registered mean/minimum screen gates pass. Relative to first20, fold 3 and the
B/C/D mean improve materially; B/C/D is now close to A41's `0.7391713` on
the same folds, while A43 preserves its recovery of fold-2 A.

This is the strongest evidence so far for the major redesign: it no longer
looks like an A-only gain. Nevertheless, its two-fold SD `0.0595` remains just
above the final CV5 stability threshold, fold 2 has not improved after epoch
7, and fold-2 epoch30 again has A F1 zero. Finish full50 and audit both folds
before any expansion.
