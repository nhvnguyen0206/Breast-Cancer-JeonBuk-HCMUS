# A37 completed two-fold stress screen

A37 replaced four globally pooled view tokens with 64 regional spatial tokens.
Fold 3 completed in original job 1011_3. Original fold 1 job 1011_1 ended at
epoch 25 because of a DataLoader shared-memory unlink error; its one exact
technical retry, job 1013_1, reproduced all first 25 records bit-for-bit
except wall-clock seconds and then completed 50 epochs. Both completed fold
audits PASS.

| Fold | Best epoch | Macro-F1 | F1 A/B/C/D | QWK | W&B |
|---|---:|---:|---|---:|---|
| 1 | 1 | 0.570846 | 0.0000 / 0.6667 / 0.9140 / 0.7027 | 0.693358 | `zg75vjst` |
| 3 | 3 | 0.619532 | 0.3636 / 0.6154 / 0.8837 / 0.6154 | 0.670562 | `q6fj2umt` |

The two-fold mean is 0.595189, sample SD 0.034426 and minimum 0.570846.
A37 fails the mean >=0.70 and minimum >=0.65 gates, so folds 0/2/4 must not
run. Neither completed fold reached 0.75 at any epoch.

The audits verify the frozen split hash, 50 epochs, checkpoint/prediction
consistency, manifests, probability normalization and finished W&B runs.
These are selected DEV results, not independent-test estimates.

Conclusion: spatial tokens reduce the observed two-fold dispersion but reduce
mean performance materially. Reject A37 and proceed to the preregistered A38
monotonic ordinal-primary preflight.

