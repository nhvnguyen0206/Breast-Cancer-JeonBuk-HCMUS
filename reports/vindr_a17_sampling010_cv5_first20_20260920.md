# A17 CV5 confirmation — matched first 20 epochs

Retained fold0 plus confirmation folds1--4 each have at least 20 epochs. All
four confirmation tasks were still active at this milestone, scalar training
losses were finite, and total AMP-skipped updates across the five folds were
52.

Selected first-20 DEV results:

| Fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | Epoch-20 Macro-F1 | >=0.75 |
|---:|---:|---:|---:|---:|---|---:|---:|
| 0 | 17 | 0.791469 | 0.826733 | 0.655995 | 1.0000 / 0.6286 / 0.8856 / 0.6517 | 0.509205 | 5 |
| 1 | 5 | 0.553133 | 0.851117 | 0.682527 | 0.0000 / 0.6897 / 0.9111 / 0.6118 | 0.444059 | 0 |
| 2 | 3 | 0.537696 | 0.801489 | 0.638662 | 0.1818 / 0.5075 / 0.8849 / 0.5766 | 0.484817 | 0 |
| 3 | 9 | 0.646880 | 0.804455 | 0.634895 | 0.5000 / 0.6118 / 0.8723 / 0.6034 | 0.524736 | 0 |
| 4 | 14 | 0.675912 | 0.776675 | 0.614935 | 0.6667 / 0.6000 / 0.8468 / 0.5902 | 0.501194 | 0 |

The provisional selected mean Macro-F1 is 0.641017889812455, sample SD
0.10281875126033155 and minimum 0.5376961278531225. Mean accuracy is
0.8120937031668427, mean QWK 0.6454029273260625, mean class F1 is
`[0.4696969697,0.6074907987,0.8801560137,0.6067277772]`, and the B/C/D mean
is 0.6981248631842835. No selected checkpoint contains a severe error.

The mean improved by 0.0200971238 from the matched first-10 milestone, but
sample SD increased by 0.0155720705. Only fold0 has crossed 0.75 (five
checkpoints); folds1--4 have not. The result remains below every final CV5
criterion. Continue all registered runs unchanged to epoch50 and assess only
the preregistered selected checkpoints, without per-fold early stopping or
replacement.

W&B runs: fold0 `djz4e32c`, fold1 `txm9bun2`, fold2 `7jtlt2gq`, fold3
`7uqvm3ct`, fold4 `fpbres7g`.
