# A42 cannot satisfy the registered CV5 SD gate

Direct history inspection on 2026-09-22 confirms folds0/1/2/3 completed50.
Their selected DEV Macro-F1 values are fixed at:
`[0.8243696483568552, 0.7615292016154085, 0.6773145015023957,
0.7385652545786925]`.
Fold4 had completed45 and its best score was `0.7945236039670045`.

With four fixed scores, sample variance as a function of the fifth score is
minimized when the fifth score equals the mean of the fixed four:
`0.750444651513338`. The registered best-DEV selection rule means fold4's
final selected score cannot be less than its existing best `0.7945236039670045`.
Thus the feasible minimum final sample SD is `0.05619447161635032`, already
above `0.05`. Any further fold4 best-score improvement increases this SD.

A42 therefore cannot pass the final stability gate under the registered
protocol. Allow the final fold to finish50, audit and report its actual final
results. Do not lower a strong fold's checkpoint deliberately, change the
selection rule, or round 5.62 percentage points down to the 5-point gate.
This conclusion is conditional on the recorded histories/checkpoints passing
the remaining CV5 audit; it is not a claim that all five final audits passed.

## Audit tool verification

The updated CV5 auditor was copied only to the development snapshot and
validated end-to-end on completed A41 runs [1033,1031,1033,1031,1033] in
fold order. Audit PASS: 2017 unique cases, support [6,196,1556,259], all W&B
runs finished, identical training configs across folds, and reproduced mean
`0.7523091060697951`, SD `0.11874185882676959`, B/C/D mean
`0.7586343636486156`. The immutable training snapshots were not changed.
This validates the auditor on real completed data, not A42/A43 acceptance.
