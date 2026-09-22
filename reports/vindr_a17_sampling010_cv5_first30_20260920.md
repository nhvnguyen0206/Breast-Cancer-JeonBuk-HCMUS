# A17 CV5 confirmation — matched first 30 epochs

Retained fold0 plus confirmation folds1--4 each have at least 30 epochs. All
four confirmation tasks remain RUNNING on RTX5090 nodes, scalar training
losses are finite, and total AMP-skipped updates across the five folds are 66.

Selected first-30 DEV results:

| Fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | Epoch-30 Macro-F1 | >=0.75 |
|---:|---:|---:|---:|---:|---|---:|---:|
| 0 | 17 | 0.791469 | 0.826733 | 0.655995 | 1.0000 / 0.6286 / 0.8856 / 0.6517 | 0.538371 | 9 |
| 1 | 5 | 0.553133 | 0.851117 | 0.682527 | 0.0000 / 0.6897 / 0.9111 / 0.6118 | 0.480105 | 0 |
| 2 | 3 | 0.537696 | 0.801489 | 0.638662 | 0.1818 / 0.5075 / 0.8849 / 0.5766 | 0.474675 | 0 |
| 3 | 9 | 0.646880 | 0.804455 | 0.634895 | 0.5000 / 0.6118 / 0.8723 / 0.6034 | 0.502425 | 0 |
| 4 | 14 | 0.675912 | 0.776675 | 0.614935 | 0.6667 / 0.6000 / 0.8468 / 0.5902 | 0.508819 | 0 |

The provisional selected mean Macro-F1 remains 0.641017889812455, sample SD
0.10281875126033155 and minimum 0.5376961278531225. Mean accuracy remains
0.8120937031668427, mean QWK 0.6454029273260625, mean class F1 is
`[0.4696969697,0.6074907987,0.8801560137,0.6067277772]`, and B/C/D mean is
0.6981248631842835. No selected checkpoint contains a severe error.

No fold improved its selected checkpoint between the matched first-20 and
first-30 horizons. Only fold0 has crossed 0.75; its crossing count increased
from five to nine, while folds1--4 remain at zero. This is materially below
the final mean, dispersion and minimum-fold criteria. Continue the registered
runs unchanged through epoch50; this milestone does not authorize selecting,
stopping or replacing individual folds.

W&B runs: fold0 `djz4e32c`, fold1 `txm9bun2`, fold2 `7jtlt2gq`, fold3
`7uqvm3ct`, fold4 `fpbres7g`.
