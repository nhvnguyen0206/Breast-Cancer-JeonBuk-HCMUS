# A19 sampling .25 + beta .995 — completed fold0 screen

Job936 completed 50 epochs with Slurm state COMPLETED and ExitCode0:0 on
master RTX5090. Requeue and restarts were zero; worker2 and Vesta were not
used. The read-only audit passed for all five frozen manifests, assignment
hash, architecture and experiment provenance, checkpoint selection, exact
prediction membership and labels, normalized probabilities, recomputed
metrics and finished W&B state.

Selected epoch11:

- Macro-F1: **0.7623856925078064**
- Accuracy: 0.7772277227722773
- QWK: 0.6014556296036478
- F1 A/B/C/D: `[1.0,0.6419753086,0.8464163823,0.5611510791]`
- Confusion matrix: `[[1,0,0,0],[0,26,14,0],[0,15,248,48],[0,0,13,39]]`
- Severe errors: 0
- Checkpoints at or above .75: 3/50
- AMP-skipped updates: 16

Epoch50 Macro-F1 is 0.548142117173749, showing a large selected-to-final gap.
The selected result passes the preregistered numeric expansion gate of .75,
but it is below A6 fold0 by 0.0205935650 and below A5 fold0 by 0.0272641636.
Its four-class score also includes the only A case in this DEV fold, while
B/C/D mean is only 0.6831809233. This screen is not evidence of improved CV5
performance.

Per protocol, retain completed job936 fold0 and launch fresh folds1--4 from
the identical snapshot. Final utility requires the full audited CV5 mean,
sample SD, minimum fold and common-class metrics. DEV is not an independent
test.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6wtyzm62
