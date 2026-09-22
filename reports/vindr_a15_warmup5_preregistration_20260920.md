# A15: five-epoch backbone warm-up on A5

Only training change from A5: freeze DenseNet features, including BatchNorm
statistics, for epochs1--5; train fusion/heads; unfreeze the backbone at
epoch6. The optimizer and cosine schedule continue without reset. Same
stretch512 cache input, augmentation, dropout, losses, LR, sampling,
architecture and seed42.

R1 tested the same warm-up on the older baseline and reached fold0 .69598,
below its gate. Its interaction with A5's geometric augmentation and dropout
has not been measured. Hypothesis: stabilize task heads before joint tuning;
prior R1 means improvement is uncertain, not assumed.

Fixed fold0, full50, fresh ImageNet, frozen grouped split. Audit both the
frozen epochs and epoch6 transition. Only completed audited selected DEV
Macro-F1 >=.75 permits fresh folds1--4, retaining fold0. No ensemble, resplit
or independent-test claim. RTX5090 only, worker2/Vesta excluded. Final joint
criteria remain mean>=.70, sample SD<=.05, minimum fold>=.65 at seed42.
