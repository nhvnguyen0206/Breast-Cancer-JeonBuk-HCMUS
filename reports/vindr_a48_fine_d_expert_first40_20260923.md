# A48 folds2/3: matched first40

Both job1066 tasks remain RUNNING on RTX5090. Histories contain complete,
finite epochs1--40 with no runtime error markers. The A48 selected checkpoints
remain epochs3/6; no later epoch improves DEV Macro-F1.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs |
|---|---:|---:|---:|---:|---|---:|---:|
| A42/f2 | 25 | .677315 | .823821 | .605038 | .666667/.658537/.889937/.494118 | .680864 | 2/40 |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/40 |
| A48/f2 | 3 | .540083 | .831266 | .627450 | 0/.685714/.892800/.581818 | .720111 | 0/40 |
| A48/f3 | 6 | .738368 | .858911 | .701292 | .666667/.750000/.910543/.626263 | .762269 | 15/40 |

| Aggregate | A42 | A48 | Delta A48-A42 |
|---|---:|---:|---:|
| Macro-F1 mean | .707940 | .639226 | -.068714 |
| Macro-F1 sample SD | .043311 | .140209 | +.096898 |
| Minimum Macro-F1 | .677315 | .540083 | -.137231 |
| B/C/D mean across folds | .721698 | .741190 | +.019492 |
| B/C/D minimum | .680864 | .720111 | +.039247 |
| QWK mean | .657234 | .664371 | +.007137 |
| QWK minimum | .605038 | .627450 | +.022412 |

The fine-D hypothesis remains locally successful for dense-tissue separation:
relative to A42 at the matched horizon, fold2 D F1 rises .087701, B/C/D minimum
rises .039247, and all registered B/C/D and QWK gates pass. However, fold2
never obtains a positive A F1 in forty epochs, while A42 recovers the rare A
case at epoch25. This reduces A48 fold2 Macro-F1 by .137231 and expands the
two-fold sample SD to .140209. Fold2 Macro and the SD gate fail decisively;
fold3 alone passes .72.

Finish the preregistered 50 epochs and perform local audits. Do not tune on
screen folds and do not launch folds0/1/4. These are selected DEV results, not
an independent test. W&B remains offline on Atlas under local IDs
`qai5n15b`/`3ppb7vks`.
