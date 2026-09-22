# A17 CV5 confirmation — matched first 10 epochs

Retained fold0 plus confirmation folds1--4 each have at least 10 epochs. All
four live jobs remain RUNNING on RTX5090 nodes, scalar training losses are
finite, and total AMP-skipped updates across five folds are 37.

Selected first-10 DEV results:

| Fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 8 | 0.755674 | 0.779703 | 0.597195 | 1.0000 / 0.6465 / 0.8499 / 0.5263 |
| 1 | 5 | 0.553133 | 0.851117 | 0.682527 | 0.0000 / 0.6897 / 0.9111 / 0.6118 |
| 2 | 3 | 0.537696 | 0.801489 | 0.638662 | 0.1818 / 0.5075 / 0.8849 / 0.5766 |
| 3 | 9 | 0.646880 | 0.804455 | 0.634895 | 0.5000 / 0.6118 / 0.8723 / 0.6034 |
| 4 | 9 | 0.611221 | 0.811414 | 0.569650 | 0.5000 / 0.6316 / 0.8847 / 0.4286 |

Provisional selected mean Macro-F1 is 0.6209207660432189, sample SD
0.08724668076898663 and minimum 0.5376961278531225. Mean accuracy is
0.8096356533916419, mean QWK 0.6245859212991274, mean class F1
`[0.4363636364,0.6173852317,0.8805988408,0.5493353553]`, and B/C/D mean is
0.6824398092697465.

Only fold0 has crossed 0.75 so far. This early horizon is below the final
criteria and demonstrates that the fold0 screen does not establish five-fold
performance. Continue every fold unchanged to the registered 50 epochs; do
not select or stop folds individually.

W&B runs: fold0 `djz4e32c`, fold1 `txm9bun2`, fold2 `7jtlt2gq`, fold3
`7uqvm3ct`, fold4 `fpbres7g`.
