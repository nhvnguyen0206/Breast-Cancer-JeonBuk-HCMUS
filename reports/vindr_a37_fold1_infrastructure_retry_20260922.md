# A37 fold-1 infrastructure failure and registered retry

Original A37 job `1011_1` terminated after writing epoch 25. Its log records a
PyTorch DataLoader worker failure while collating a batch:
`RuntimeError: could not unlink the shared memory file ... No such file or
directory`. The W&B run `jr97gvza` finished in a failed/incomplete state and
the original run directory is retained unchanged. This was not a metric-based
stop and the selected score through epoch 25 remained the preregistered
first-20 value 0.570846.

One technical retry was registered and launched as job `1013_1`, W&B
`zg75vjst`. It uses the exact immutable A37 snapshot, config, seed 42, fold 1,
frozen split and full 50-epoch contract. No model, data, worker, loss or
selection setting was changed. It runs on `slurm-b20a-master-0` RTX 5090 with
worker2/Vesta excluded, requeue disabled and zero restarts at launch.

To guard against an accidental favorable rerun, compare the retry's common
first-25 history with the retained failed run once available. Any divergence
must be disclosed; never select between the two histories based on score. If
the same shared-memory failure recurs, stop and diagnose before another run.

At common epoch 10, the retry reproduces the original run exactly after
excluding wall-clock seconds: every training loss component, validation
metric/confusion matrix, sampled class count, learning rate and AMP skipped-
update count is bit-for-bit identical. This supports treating job 1013_1 as a
technical continuation-by-reproduction rather than a favorable rerun. Repeat
the same comparison at common epoch 25.

At common epoch 25, all 25 records again match bit-for-bit after excluding
wall-clock seconds. The selected checkpoint remains epoch 1 with Macro-F1
0.5708455271 in both histories. The retry is therefore accepted as a faithful
technical reproduction and may continue to epoch 50; no score-based choice
between the two runs occurred.
