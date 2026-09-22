# A20 batch4 completed fold0 screen

The read-only screen audit passes. Job943_0 completed 50 epochs on the master
RTX 5090 with exit code 0, no restart/requeue, worker2/Vesta excluded, and a
finished matching W&B run.

Selected epoch 13 has Macro-F1 `0.773328`, accuracy `0.816832`, QWK `0.612385`,
class F1 A/B/C/D `1.000000 / 0.648649 / 0.881029 / 0.563636`, and no severe
errors. Epoch 50 is `0.538468`; one of 50 checkpoints reaches `0.75`.

A20 is below A5 fold0 (`0.789650`) and A6 fold0 (`0.782979`), and its B/C/D
mean is only `0.697771`. The score also depends on the one class-A DEV case.
Nevertheless it passes the preregistered numeric expansion gate, so retain
this fold0 and launch fresh folds1–4 from the identical A20 snapshot. This is
selected DEV evidence, not an independent test result.
