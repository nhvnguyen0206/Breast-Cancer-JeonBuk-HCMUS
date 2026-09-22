# A44 fold1 matched first20: A recovery without secondary-gate recovery

Job1050_1 verified RUNNING on master RTX5090. Both histories contain
complete epochs1--20; checkpoint selection is best DEV Macro-F1 within
that same horizon. Frozen split/cache and seed42 remain fixed.

| Arm | Best epoch | Macro-F1 | Accuracy | QWK | B/C/D mean F1 | A-positive epochs |
|---|---:|---:|---:|---:|---:|---:|
| A43 | 4 | .5850244052 | .8114143921 | .6936709874 | .7133658737 | 1/20 |
| A44 | 19 | .7641791946 | .8337468983 | .5916055358 | .6855722594 | 1/20 |

A44 selected F1 A/B/C/D: [1,.6129032258,.8964451314,.5473684211].
Confusion matrix (true rows/predicted columns in A/B/C/D order):
[[1,0,0,0],[0,19,20,0],[0,4,290,18],[0,0,25,26]].

Relative to A43, A F1 rises from.2 to1; its contribution alone is +.20 to
four-class Macro-F1, while the total gain is only .1791547893 because the
B/C/D average declines. The only A exam is correct without A false positives
at epoch19, but A F1 returns to0 at epoch20. At epoch20 Macro-F1 is
.4949260182 and QWK .5513460630. This does not establish durable recovery.

The Macro-F1 screening threshold .72 passes at the selected checkpoint;
registered B/C/D preservation (.7133658737) and QWK (.6936709874) gates fail.
Do not expand or loosen gates. Continue unchanged to50, audit, then apply
the preregistered decision. These are selected DEV estimates, not independent
test performance. Next scheduled reports are40 and completion.
W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2031sdoy
