# A14: letterbox on A5

Only learning-input change from A5: stretch512 -> aspect-preserving resize
with centered zero padding512. Existing implementation; same augmentation
ranges, losses, optimizer, dropout, DenseNet121 hierarchical architecture.
Geometry augmentation operates on the padded canvas; breast pixel footprint
therefore changes too. This is a preprocessing ablation, not a pure shape test.

Earlier letterbox on baseline did not meet CV5 goal; interaction with A5
regularization/geometric augmentation has not been measured. Hypothesis:
avoid anatomy distortion, accepting reduced occupied resolution. No promise
of improved rare-A performance or fold stability.

Fixed fold0, fresh ImageNet, seed42, frozen grouped CV5 split, full50.
Only completed audited selected DEV Macro-F1 >=.75 permits fresh folds1--4;
retain fold0. No ensemble, resplit or independent-test claim. RTX5090 only,
worker2/Vesta excluded. Joint final criteria mean>=.70, sample SD<=.05,
minimum fold>=.65, seed42 only; .75 mean aspirational. Report per-class F1,
accuracy/QWK and epoch50 as well as selected DEV. Only6 A cases total.
