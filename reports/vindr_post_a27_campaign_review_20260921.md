# Post-A27 campaign review

Recomputed from local completed CV5 JSON reports with audit=PASS and five
fold best metrics; deduplicated by arm. This review does not rerun remote
audits, inference or checkpoint selection.20 unique arms matched that schema;
older reports with other schemas are not covered.

| Arm | Mean Macro-F1 | Sample SD | Minimum | Mean BCD F1 | BCD SD |
|---|---:|---:|---:|---:|---:|
|A5 dropout.3|.7028|.1173|.5702|.7371|.0291|
|A6 sampling.25|.6766|.0644|.6195|.7154|.0209|
|A8 weight_decay.01|.6980|.1008|.5686|.7196|.0346|
|A24 FP32|.6809|.0841|.5698|.7301|.0197|

No inspected arm meets joint mean>=.70,SD<=.05,min>=.65.
A5 A-class F1 across folds [1,0,1,0,1]; A6 [1,.4,.5,.5,.4].
BCD dispersion is much smaller than four-class dispersion. This supports
rare-A instability as a major contributor, but is not a causal attribution
of variance (covariance also contributes). Do not drop A or change the metric.

Revisited ordinal code and prior diagnostic: narrow CORAL bias spacing
already explains a nonzero loss floor; scalar magnitude alone does not imply
dominant gradients. A13 bias-LR10 reduced ordinal training loss yet yielded
CV5 mean .6083934606/SD .0840343084/min .5632771274. Do not repeat that arm.

Next candidate should use A6 as parent, retaining tempered sampling. Test
effective weight decay .0001->.01 only, rather than another single change on
A5 that leaves zero A F1 in weak folds. This interaction is untested in the
inspected configs: A8 tested decay on A5, not A6. It may harm A6 and offers
no guarantee of success. Architecture and heads remain unchanged; no
ensemble. Require source/config parity and preregistration before launch.
Fixed fold0 seed42 full50 then existing strict .75 confirmation gate;
do not use weak folds to tune directly or replace favorable folds.
No new training job submitted by this review. Selected DEV is not independent
evaluation; repeated tuning increases selection optimism.
