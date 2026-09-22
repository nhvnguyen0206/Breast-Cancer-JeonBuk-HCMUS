# A47 preregistration: dual-endpoint hierarchical primary head

Registered before implementation or training results. A42 is the strongest
audited near-target model: CV5 mean Macro-F1 .7592604 and minimum .6773145,
but sample SD .0561945 fails the current <= .03 target. Its two lowest folds
are fold2 (.6773145) and fold3 (.7385653). Fold2 recognizes its A case but
misclassifies 31/52 D cases as C, producing D F1 .4941176. A42's A-vs-rest
factorization restored the rare-A decision relative to A41, so A47 extends
that successful decomposition to the opposite ordinal endpoint rather than
changing the split, sampling or checkpoint rule.

## Controlled structural change

Retain A42's ConvNeXt-Tiny backbone, global hierarchical relational path,
spatial-attention residual, augmentation, sampling, auxiliary CORAL/binary
heads, losses, optimizer and schedule. Replace only A42's conditional
three-way B/C/D linear head with:

- the unchanged differentiable A-vs-rest gate;
- a conditional D-vs-(B/C) gate within the non-A mass;
- a conditional two-way B/C head within the non-A, non-D mass.

The final distribution is
`P(A)=sigmoid(a)`, `P(D)=(1-P(A))*sigmoid(d)`, and
`P(B/C)=(1-P(A))*(1-sigmoid(d))*softmax(bc)`. Probabilities must be positive,
sum to one and enter the existing focal/neighbor objectives as log
probabilities. This is one dual-endpoint hierarchical head, not hard routing,
post-hoc thresholds, test-time augmentation or an ensemble. It has the same
four output projections and parameter count as A42. Inference remains one
model and one four-class distribution.

Architecture ID:
`convnext_tiny_hybrid_spatial_dual_endpoint_gate_multitask_v14`.

## Fixed two-fold screen

Screen the two lowest A42 folds, 2 and 3, for exactly 50 epochs using seed42,
the frozen grouped split/window16 cache and assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Use RTX5090 only, exclude worker2/Vesta, create fresh ImageNet initialization,
and log to W&B project `HCMUS-paper1`. Run a real-cache AMP forward/backward/
optimizer preflight from an immutable tested snapshot first.

A42 parent baselines over folds 2/3 are: Macro-F1 mean .7079398780, sample SD
.0433108229; B/C/D mean across folds .7216976152 with minimum .6808637798;
QWK mean .6572337361 with minimum .6050383049.

Expand only if both completed screen audits PASS and all gates hold:

- each fold Macro-F1 >= .72;
- two-fold Macro-F1 sample SD <= .03;
- two-fold mean B/C/D F1 >= .7216976152 and minimum >= .6808637798;
- two-fold mean QWK >= .6572337361 and minimum >= .6050383049.

Report D F1, A F1, positive-A epoch count and longest streak per fold, but do
not let the six-case A behavior replace the gates. If any gate fails, reject
A47 without tuning on the screen folds or launching folds 0/1/4.

Final audited CV5 acceptance remains mean Macro-F1 >= .72, sample SD <= .03
and minimum fold >= .65, with per-class F1, accuracy, QWK and confusion
matrices. All fold scores are DEV-selected and not an independent test.

Status: preregistered; implementation pending.
