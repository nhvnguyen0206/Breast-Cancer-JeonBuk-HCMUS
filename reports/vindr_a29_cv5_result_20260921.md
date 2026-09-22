# A29 completed CV5 decision

All five runs completed50. Audit PASS for saved predictions, checkpoint
selection/provenance, frozen manifests and finished W&B runs. This audit
does not perform fresh forward inference.

Selected DEV Macro-F1 mean .6463024255251005, sampleSD .10190081319645893,
minimum .5573547226154507. Fold vector:
[.810309343483078,.5669240437708984,.6340591473743648,
.5573547226154507,.6628648703817106].
Accuracy mean .845305014372405; QWK mean .656326018354595.
Class F1 means [.4133333333,.6698531035,.9044118901,.5976113752].
BCD mean .7239587896. Epoch50 Macro-F1 mean .6010365564.

Reject: fails mean>=.70, sampleSD<=.05 and minimum>=.65. Relative to A5,
mean falls from .7028282801; dispersion improves slightly from .1172888127
but remains excessive. Relative to A6 (.6765513839/.0644461991/.6194960833),
all three acceptance metrics are worse. Broader darkening is not selected.
Do not combine its fold0 with other arms or replace any weak fold.
No independent-test or ensemble claim. Retain A5 mean and A6 stability as
separate research references, neither as an accepted solution.

Summary: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/fjxlv4dk
