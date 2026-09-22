# FIT-only augmentation retention diagnostic

Executed scripts/audit_augmentation_retention.py against immutable A5 fold0
FIT manifest, using remote training environment plus snapshot .deps.
32 randomly selected studies (seed42),128 views,16 shared random affine
draws per view. Actual cached packed CVAT masks, area resize512 and torchvision
bilinear affine matching training. No DEV labels or model scores used.

| Rotation / translation | Mean retained mask mass | Minimum | 5th percentile | Fraction retaining <95% |
|---|---:|---:|---:|---:|
|5 degrees / .03 (A5)|.9847811855|.9474181533|.9635802418|.0014648438|
|10 degrees / .05|.9702542865|.8993028402|.9365159124|.1445312500|
|10 degrees / .03|.9772161828|.9225813150|.9523184448|.0239257813|

Ratios estimate raster mask mass retained, not clinical information retained.
Transforms and views within a study are correlated, and these are sampled,
not whole-FIT or worst-case bounds. Mask interpolation introduces small
numerical area differences. Results cannot predict generalization benefit.

Decision: do not launch the previously proposed joint rotation/translation
increase; it causes materially more clipping (14.45% below95% retention).
Rotation-only increase has less clipping but still exceeds A5; consider it
only as an explicitly registered augmentation ablation after broader checks,
not a demonstrated correction. No new training job submitted, no split,
loss, model or default augmentation changed. Existing goal remains unmet.
