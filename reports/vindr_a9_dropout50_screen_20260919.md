# A9 dropout 0.5 completed fold-0 screen

Job790_0 completed all 50 epochs on RTX 5090 master with Slurm
COMPLETED/0:0, no restart/requeue and worker2 excluded. The read-only screen
audit PASS: architecture/config provenance, frozen split hash and all five
fold manifests, checkpoint/history, exact DEV predictions, normalized
probabilities/argmax, recomputed metrics and finished W&B run all agree.

Best epoch 18 DEV Macro-F1 is **0.7983834791**, accuracy 0.8366336634 and
QWK 0.6632653061. F1 A/B/C/D is 1.0000 / 0.6667 / 0.8932 / 0.6337;
confusion matrix `[[1,0,0,0],[0,29,11,0],[0,18,276,17],[0,0,20,32]]`.
Three of 50 epochs reached 0.75. Epoch50 Macro-F1 was 0.5661339637.

The screen exceeds the registered 0.75 gate and A5 fold0 by 0.8734
percentage points. It is still selected DEV with one A case, not CV5,
independent-test or multiseed success. Retain fold0 and run fresh folds1--4
from the identical immutable snapshot; no ensemble.
