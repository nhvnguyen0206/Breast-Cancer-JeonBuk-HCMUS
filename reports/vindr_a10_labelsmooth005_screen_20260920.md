# A10 completed fold-0 screen: label smoothing 0.05

A10 changes only flat-head focal label smoothing from 0 to 0.05 relative to
substantive best A5. Architecture, dropout .3, augmentation, optimizer, other
loss terms, sampling, preprocessing, seed and frozen split are unchanged.

Job803_0 completed all 50 epochs on slurm-b20a-master-0 with RTX 5090.
Slurm reports COMPLETED ExitCode=0:0, no restart/requeue and worker2 excluded.
Read-only audit PASS: exact frozen manifests/hash, architecture/config,
history/checkpoint, 404 unique fold0 predictions and labels, finite normalized
probabilities/argmax, recomputed metrics and finished W&B run `xtmvoors`.

Best epoch19 DEV Macro-F1 **0.7743055556**, accuracy 0.8094059406, QWK
0.6146141372 and class F1 `[1,.5555555556,.875,.6666666667]`. There is one
severe D-to-B error. Only 1/50 epochs reaches .75. Epoch50 Macro-F1 is
0.6400411737. The selected score is 1.5344 percentage points below A5 fold0
and depends on the single A case; calibration did not improve.

Despite weak substantive evidence, the preregistered numeric expansion gate
was completed audit plus fold0 Macro-F1 >=.75. A10 passes that rule. To avoid
changing the rule after observing results, retain job803 fold0 and run fresh
folds1--4 from the identical immutable snapshot. This is selected DEV only,
not CV5, independent-test or multiseed success; no ensemble.
