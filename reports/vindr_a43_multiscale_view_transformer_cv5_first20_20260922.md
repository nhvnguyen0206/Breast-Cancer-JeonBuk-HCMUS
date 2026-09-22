# A43 multi-scale four-view Transformer CV5 — common first 20 epochs

Expansion job `1046` remains RUNNING on worker1 RTX 5090. The common first-20
selection is unchanged from first10.

| Fold | Selected epoch <=20 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 6 | 0.816001 | 0.841584 | 0.694806 | 1.0000 / 0.7033 / 0.8940 / 0.6667 |
| 1 | 4 | 0.585024 | 0.811414 | 0.693671 | 0.2000 / 0.5778 / 0.8844 / 0.6780 |
| 2 | 7 | 0.799443 | 0.836228 | 0.668040 | 1.0000 / 0.7158 / 0.8925 / 0.5895 |
| 3 | 7 | 0.678563 | 0.806931 | 0.611126 | 0.6667 / 0.6882 / 0.8752 / 0.4842 |
| 4 | 6 | 0.583589 | 0.794045 | 0.618219 | 0.3333 / 0.5660 / 0.8703 / 0.5647 |

CV5 mean remains `0.6925240`, sample SD `0.1121339`, minimum `0.5835890`,
mean accuracy `0.8180404`, mean QWK `0.6571724`, and B/C/D F1 mean
`0.7100320`. No gate passes and folds 1/4 have not improved, but the completed
screen demonstrates that later gains can occur at epoch 35. Continue full50
unchanged; do not tune on the expansion folds.
