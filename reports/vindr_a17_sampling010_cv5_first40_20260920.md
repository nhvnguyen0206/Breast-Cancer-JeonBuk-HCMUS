# A17 CV5 confirmation — matched first 40 epochs

Retained fold0 plus confirmation folds1--4 each have at least 40 epochs. All
four confirmation tasks remain RUNNING on RTX5090 nodes, scalar training
losses are finite, and total AMP-skipped updates across the five folds are 75.

Selected first-40 DEV results:

| Fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | Epoch-40 Macro-F1 | >=0.75 |
|---:|---:|---:|---:|---:|---|---:|---:|
| 0 | 17 | 0.791469 | 0.826733 | 0.655995 | 1.0000 / 0.6286 / 0.8856 / 0.6517 | 0.678865 | 12 |
| 1 | 5 | 0.553133 | 0.851117 | 0.682527 | 0.0000 / 0.6897 / 0.9111 / 0.6118 | 0.484791 | 0 |
| 2 | 3 | 0.537696 | 0.801489 | 0.638662 | 0.1818 / 0.5075 / 0.8849 / 0.5766 | 0.482492 | 0 |
| 3 | 9 | 0.646880 | 0.804455 | 0.634895 | 0.5000 / 0.6118 / 0.8723 / 0.6034 | 0.510611 | 0 |
| 4 | 14 | 0.675912 | 0.776675 | 0.614935 | 0.6667 / 0.6000 / 0.8468 / 0.5902 | 0.524325 | 0 |

The provisional selected mean Macro-F1 remains 0.641017889812455, sample SD
0.10281875126033155 and minimum 0.5376961278531225. Mean accuracy remains
0.8120937031668427, mean QWK 0.6454029273260625, mean class F1 is
`[0.4696969697,0.6074907987,0.8801560137,0.6067277772]`, and B/C/D mean is
0.6981248631842835. No selected checkpoint contains a severe error.

No fold improved its selected checkpoint between the matched first-20 and
first-40 horizons. Fold0 now has twelve checkpoints at or above 0.75, but
folds1--4 have zero. The current result remains below the final mean,
dispersion and minimum-fold criteria. Continue all jobs unchanged to the
registered epoch50 completion and perform a full audit; do not stop, replace
or select folds individually.

W&B runs: fold0 `djz4e32c`, fold1 `txm9bun2`, fold2 `7jtlt2gq`, fold3
`7uqvm3ct`, fold4 `fpbres7g`.
