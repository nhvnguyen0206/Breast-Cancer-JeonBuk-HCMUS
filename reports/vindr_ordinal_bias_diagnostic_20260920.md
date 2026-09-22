# Ordinal head diagnostic after A12

Read-only inspection of model/loss/optimizer and trusted fold0 checkpoints.
CORAL uses one scalar score plus three learned biases, with summed BCE.
All parameters share LR5e-5 and cosine decay, including threshold biases.
No target/reduction implementation defect was identified in this inspection.

A5 selected epoch30 biases: [1.7776434422,.6977819204,-1.7990821600].
A12 selected epoch27 biases: [1.7386560440,.6628488302,-1.7537330389].
For each fixed bias vector, independently minimizing summed BCE over an
unconstrained per-example scalar score on a dense [-25,25] grid gives:

| Checkpoint | A minimum | B minimum | C minimum | D minimum | FIT-weighted minimum |
|---|---:|---:|---:|---:|---:|
| A5 epoch30 | approximately0 | .963184 | .588232 | approximately0 | .547182 |
| A12 epoch27 | approximately0 | .968264 | .609882 | approximately0 | .564384 |

FIT counts [5,156,1245,207]. These are numerical approximations to the
fixed-bias minimum, not measured gradients or a bound across training while
biases change. A5 epoch30 recorded train ordinal loss .557008 and A12
epoch27 .577423 are close, but epoch averages and end-of-epoch parameters
are not exactly comparable. A substantial nonzero ordinal loss can therefore
arise from narrow learned threshold spacing even with well-separated scores.
Do not infer that ordinal loss magnitude proves backbone gradient dominance.

Potential controlled next experiment: adjust only ordinal-bias learning rate
relative to A5, preserving the CORAL head, all other optimizer settings,
fixed fold0 screen and original gate. Requires implementation/tests and
preregistration before any submission. No new training job launched here.
