# A38 completed two-fold stress screen

A38 replaced A30's flat primary head with a monotonic cumulative-link primary
head initialized at unit threshold gaps. Both fixed folds completed 50 epochs
on permitted RTX 5090 devices and both final audits PASS.

| Fold | Best epoch | Macro-F1 | F1 A/B/C/D | QWK | W&B |
|---|---:|---:|---|---:|---|
| 1 | 32 | 0.552137 | 0.2222 / 0.4615 / 0.9034 / 0.6214 | 0.626037 | `z534lziw` |
| 3 | 33 | 0.498309 | 0.1667 / 0.3333 / 0.9074 / 0.5859 | 0.650590 | `wwjt35v9` |

The two-fold mean is 0.525223, sample SD 0.038062 and minimum 0.498309.
A38 eventually escapes its first-20 collapse enough to recognize all classes,
but remains materially below A30 and fails both expansion gates. Folds 0/2/4
must not run.

Audits verify frozen split provenance, all 50 epochs, checkpoint/prediction
consistency, manifests, normalized probabilities and finished W&B states.
These are selected DEV results, not independent-test estimates.

Conclusion: monotonic ordinal-primary is not rejected in principle, but unit-
gap initialization wastes much of training before interior classes obtain
usable argmax regions. Reject A38 and proceed to the preregistered A39 wide-
gap correction.

