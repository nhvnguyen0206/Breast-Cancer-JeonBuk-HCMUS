# A13 completed screening audit

Job852_0 COMPLETED ExitCode0:0, Restarts0/Requeue0, master node,
worker2 excluded. Exact50 epochs, finite scalar training losses.
Screen audit PASS: architecture/seed42/provenance, all frozen manifests,
checkpoint selection, prediction-derived metrics and finished W&B runzk46dx49.

Selected epoch20 Macro-F1 .7580533506398416, accuracy .7970297029702971,
QWK .5906446690825864; class F1 [1,.5656565656565656,.8665568369028006,.6].
One severe D->B error. Only1 of50 epochs reaches .75.
Epoch50 Macro-F1 .5358465566354522 with A F1 zero.
Total AMP skipped updates17; finite losses do not imply every optimizer step ran.

The registered numerical expansion gate is passed, but this is not evidence
of stability: A5 fold0 selected .7896498561536562 with better B/C/D and QWK.
No CV5 improvement established; selected DEV is not independent test.
Goal remains unmet under accepted SD<=.05 and minimum-fold>=.65 requirements.
No confirmation submitted during this audit; retain this fold0 if expanding.
Audit does not include fresh inference or visual label/crop validation.
