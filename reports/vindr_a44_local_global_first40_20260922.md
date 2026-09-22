# A44 fold1 matched first40

Job1050_1 verified RUNNING on master RTX5090. Both A43 and A44 have complete
epochs1--40; best DEV Macro-F1 is selected within this identical horizon.

| Arm | Best epoch | Macro-F1 | Accuracy | QWK | B/C/D F1 mean | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/40 |
| A44 | 19 | .7641791946 | .8337468983 | .5916055358 | .6855722594 | 1/40 |

Selected A44 F1 A/B/C/D: [1,.6129032258,.8964451314,.5473684211].
The selected checkpoint and decision are unchanged from first20. A44 has
not regained positive A F1 in epochs20--40. At epoch40 Macro-F1 is
.5219888182, accuracy .8461538462, QWK .5955780001 and F1 A/B/C/D
[0,.6129032258,.9068702290,.5681818182].
Epoch40 confusion matrix (true rows/predicted columns A/B/C/D):
[[0,1,0,0],[0,19,20,0],[0,3,297,12],[0,0,26,25]].

Macro-F1>=.72 passes only at the selected checkpoint; registered B/C/D
and QWK preservation gates fail. No expansion. Finish registered50, audit
the final saved outputs/W&B state, then reject or accept under the unchanged
screen protocol. Current evidence does not establish stable rare-A recovery.
All scores are selected DEV or epoch40 DEV, not independent test estimates.
W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2031sdoy
