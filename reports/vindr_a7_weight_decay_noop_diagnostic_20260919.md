# A7 weight-decay no-op diagnostic

A7 was intended to change only AdamW weight decay from 1e-4 to 5e-4 while
keeping the A5 learning rate at 5e-5. Runtime checkpoints correctly preserve
the two distinct configuration values, and the training source passes
`training.weight_decay` to `torch.optim.AdamW`.

Despite that, the evidence shows A7 is numerically identical to A5:

- Fold0: all 50 validation records and all logged train scalars are exactly
  equal. The selected epoch30 state dictionaries have the same SHA256 and all
  tensors compare bit-for-bit equal.
- At the current confirmation checkpoint, folds1/2 have 26 equal validation
  records and train scalars, while folds3/4 have 27 equal records and train
  scalars. Their selected state dictionaries also compare bit-for-bit equal.
- All five best epochs and Macro-F1 values currently reproduce A5 exactly.

The cause is float32 update granularity. AdamW's decoupled decay factor is
`1 - learning_rate * weight_decay`. At learning rate 5e-5:

- wd=1e-4 gives 0.999999995 in Python but 1.0 in float32;
- wd=5e-4 gives 0.999999975 in Python but 1.0 in float32;
- wd=1e-3 gives 0.99999995, represented as 0.9999999403953552 in float32.

Therefore both A5 and A7 configured decay factors round to one and have no
effective decoupled weight decay in this runtime. A7 must be treated as a
no-op replication, not as evidence that stronger regularization fails. Finish
the already-running 50-epoch audit for provenance, then any valid follow-up
must use a numerically effective value (at least 1e-3; a standard 1e-2 screen
would provide a materially nonzero effect) while changing no other factor.

