# A48 folds2/3: matched first20

Both job1066 tasks remain RUNNING on RTX5090. Histories contain complete,
finite epochs1--20 with no runtime error markers. Best selected DEV
checkpoints within the common first20 horizon are unchanged from first10.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs |
|---|---:|---:|---:|---:|---|---:|---:|
| A42/f2 | 8 | .606175 | .774194 | .606120 | .4/.641026/.850340/.533333 | .674900 | 1/20 |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/20 |
| A48/f2 | 3 | .540083 | .831266 | .627450 | 0/.685714/.892800/.581818 | .720111 | 0/20 |
| A48/f3 | 6 | .738368 | .858911 | .701292 | .666667/.750000/.910543/.626263 | .762269 | 8/20 |

| Aggregate | A42 | A48 | Delta A48-A42 |
|---|---:|---:|---:|
| Macro-F1 mean | .672370 | .639226 | -.033144 |
| Macro-F1 sample SD | .093614 | .140209 | +.046594 |
| Minimum Macro-F1 | .606175 | .540083 | -.066092 |
| B/C/D mean across folds | .718716 | .741190 | +.022474 |
| B/C/D minimum | .674900 | .720111 | +.045211 |
| QWK mean | .657775 | .664371 | +.006597 |
| QWK minimum | .606120 | .627450 | +.021331 |

A48 continues to pass both registered B/C/D gates and both QWK gates, but
fold2 fails the per-fold Macro-F1 gate and sample SD fails by .110209. Fold2
has no positive A F1 in any of twenty epochs, so the early result is no longer
just a one-epoch fluctuation. The fine-D branch improves dense-tissue classes
without preserving A42's rare-A behavior on fold2. The selected D-head norms
remain .015358/.022067 because no later checkpoint exceeded epochs3/6.

Continue unchanged to the registered 40/50 horizons. Do not tune on screen
folds or launch folds0/1/4. Results are selected DEV, not an independent test;
W&B remains offline on Atlas under local IDs `qai5n15b`/`3ppb7vks`.
