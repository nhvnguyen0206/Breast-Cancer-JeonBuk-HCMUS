# A43 multi-scale four-view Transformer CV5 — common first 30 epochs

Expansion job `1046` remains RUNNING on worker1 RTX 5090. The comparison uses
the independently best DEV Macro-F1 in the same epoch-1--30 horizon for every
fold; no test-set selection, fold-specific threshold, or ensemble is used.

| Fold | Selected epoch <=30 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 6 | 0.816001 | 0.841584 | 0.694806 | 1.0000 / 0.7033 / 0.8940 / 0.6667 |
| 1 | 4 | 0.585024 | 0.811414 | 0.693671 | 0.2000 / 0.5778 / 0.8844 / 0.6780 |
| 2 | 7 | 0.799443 | 0.836228 | 0.668040 | 1.0000 / 0.7158 / 0.8925 / 0.5895 |
| 3 | 30 | 0.715252 | 0.841584 | 0.654839 | 0.6667 / 0.7397 / 0.9002 / 0.5545 |
| 4 | 28 | 0.718825 | 0.831266 | 0.664422 | 0.6667 / 0.7200 / 0.8903 / 0.5983 |

CV5 mean is `0.7269090`, sample SD `0.0915573`, minimum `0.5850244`, mean
accuracy `0.8324153`, mean QWK `0.6751555`, and B/C/D F1 mean `0.7336564`.
The mean gate passes, but the SD and minimum gates fail. Fold4 recovered by
epoch28, while fold1 remains the bottleneck because its rare-A F1 is only
`0.20`. Continue full50 unchanged and audit all folds before accepting or
rejecting A43.
