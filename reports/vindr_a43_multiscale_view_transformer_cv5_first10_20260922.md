# A43 multi-scale four-view Transformer CV5 — common first 10 epochs

Expansion job `1046` remains RUNNING on worker1 RTX 5090. Combining preserved
folds 2/3 with expansion folds 0/1/4 at the common first-10 horizon gives:

| Fold | Selected epoch <=10 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 6 | 0.816001 | 0.841584 | 0.694806 | 1.0000 / 0.7033 / 0.8940 / 0.6667 |
| 1 | 4 | 0.585024 | 0.811414 | 0.693671 | 0.2000 / 0.5778 / 0.8844 / 0.6780 |
| 2 | 7 | 0.799443 | 0.836228 | 0.668040 | 1.0000 / 0.7158 / 0.8925 / 0.5895 |
| 3 | 7 | 0.678563 | 0.806931 | 0.611126 | 0.6667 / 0.6882 / 0.8752 / 0.4842 |
| 4 | 6 | 0.583589 | 0.794045 | 0.618219 | 0.3333 / 0.5660 / 0.8703 / 0.5647 |

CV5 mean is `0.6925240`, sample SD `0.1121339`, minimum `0.5835890`, mean
accuracy `0.8180404`, mean QWK `0.6571724`, and B/C/D F1 mean `0.7100320`.
All three final gates fail at this early horizon.

Folds 1 and 4 are the current bottlenecks. This is not yet grounds for
rejection: the preserved fold 3 improved only at epoch 35 in the completed
screen. Continue common20 and full50 without modifying the arm.
