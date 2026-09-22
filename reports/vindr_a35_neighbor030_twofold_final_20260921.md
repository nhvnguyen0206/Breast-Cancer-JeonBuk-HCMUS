# A35 completed two-fold stress screen

A35 changed only neighbor-loss weight 0.20 -> 0.30 relative to A30 and ran
the preregistered 50 epochs on the fixed historically weakest folds 1 and 3.
Both runs completed on the permitted master RTX 5090, with Vesta/worker2
excluded, and both final read-only audits PASS.

| Fold | Best epoch | Macro-F1 | Class F1 A/B/C/D | QWK | W&B |
|---|---:|---:|---|---:|---|
| 1 | 2 | 0.559404 | 0.0000 / 0.6957 / 0.9056 / 0.6364 | 0.6753 | `ksdm0x9c` |
| 3 | 21 | 0.704229 | 0.6667 / 0.7342 / 0.8952 / 0.5208 | 0.6415 | `jytyd5ja` |

The two-fold mean is 0.631816 and the minimum is 0.559404. A35 therefore
fails both expansion requirements (mean >=0.70 and minimum >=0.65) and must
not proceed to folds 0/2/4. Neither fold reached Macro-F1 0.75 at any epoch.

Audit checks confirmed the frozen assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
50 epochs, valid manifests, normalized probabilities, finished W&B runs,
and saved checkpoint/prediction consistency. These are selected DEV results,
not independent-test estimates.

Conclusion: increasing the neighbor penalty does not solve the persistent
fold-1 failure and is rejected. Close the scalar-loss direction and proceed
to A36, the preregistered view-token attention architecture, after its real
RTX 5090 cached-batch preflight passes.

