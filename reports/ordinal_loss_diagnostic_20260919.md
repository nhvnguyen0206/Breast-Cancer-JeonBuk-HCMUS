# Ordinal loss magnitude diagnostic

Read-only analysis of saved fold-0 checkpoints, 2026-09-19.

The current ordinal head emits three logits s+b[k] using one shared score s.
For each label y, the threshold targets are 1[y>k]. Holding the saved biases
fixed, the sum of three BCE terms is minimized over s by solving
sum(sigmoid(s+b[k])) = y. For the endpoint classes A/D its infimum is zero;
for interior B/C finite bias gaps imply a positive infimum.

CPU bisection over [-80,80], 100 iterations, with stable softplus evaluation
gave the following values from the actual saved biases:

| Arm | Selected epoch | B infimum | C infimum | Sample-count weighted infimum | Observed epoch-average ordinal loss |
|---|---:|---:|---:|---:|---:|
| A1 | 38 | 0.954581 | 0.554500 | 0.520315 | 0.524929 |
| L2 | 22 | 0.978151 | 0.655493 | 0.600546 | 0.616705 |
| O2 | 6 | 1.110094 | 1.091558 | 0.894671 | 0.984752 |

The weighted column uses that epoch's realized training class counts, including
sampling for O2. The observed loss is an average during the epoch, whereas the
biases are saved at its end; the two are not evaluated at an identical model
state. These values are a diagnostic of scale, not a proof of attained minima.
The infimum also assumes each case's score can be optimized independently.

In particular, A1's large ordinal loss is close to the floor imposed by its
saved threshold spacing. Its magnitude alone does not establish large shared
backbone gradients or harmful interference. Earlier campaign rationales based
on the ordinal term's share of total loss should therefore be treated as
hypotheses, not demonstrated mechanisms. L2's reduced-coefficient experiment
must be judged by completed CV5 performance. Any future claim about gradient
interference requires direct gradient measurements on training data.

No model, split, checkpoint or running job was changed by this diagnostic.
