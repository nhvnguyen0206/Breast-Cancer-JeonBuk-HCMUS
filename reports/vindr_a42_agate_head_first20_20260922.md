# A42 A-gate diagnostic control — common first 20 epochs

Both job-1037 tasks remain RUNNING on master RTX 5090 and have completed epoch
20. The tested horizon tool selected DEV Macro-F1 independently within epochs
1--20 for each fixed fold.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 1 | 19 | 0.761529 | 0.851117 | 0.587921 | 1.0000 / 0.5862 / 0.9099 / 0.5500 |
| 3 | 7 | 0.738565 | 0.851485 | 0.709429 | 0.6667 / 0.7579 / 0.9034 / 0.6263 |

The two-fold mean is `0.7500472`, sample SD `0.0162380`, and minimum
`0.7385653`. A42 therefore provisionally meets both numerical screen gates at
the common first-20 horizon, after failing them at first10.

This is not yet evidence of a generally stronger representation. The mean of
the six selected B/C/D F1 values across both folds is `0.7222852`, below A41's
matched first-20 B/C/D mean `0.7550412`. Fold 1 gains A F1 `1.0` but has B F1
`0.5862`, D F1 `0.5500` and QWK `0.5879`. Thus A42's low two-fold SD is driven
substantially by aligning the rare-A contribution, while substantive classes
partly regress.

Continue the registered 50 epochs and audit both runs. Do not expand early.
A final screen pass would justify expansion under the preregistered numerical
gate, but the scientific conclusion must state that A stability improved at
the cost of weaker B/D performance on fold 1.
