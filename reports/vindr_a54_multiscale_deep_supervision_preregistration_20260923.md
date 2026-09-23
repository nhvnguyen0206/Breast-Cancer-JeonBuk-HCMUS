# A54 preregistration: multiscale multi-task deep supervision

Registered after A53 first20 and before inspecting its first40/final results.
A54 is conditional and cannot train unless A53 completes, both audits pass,
and at least one registered expansion gate fails.

## Evidence and hypothesis

A53 first20 has strong B/C/D and ordinal behavior: B/C/D mean/minimum are
`.7401487/.7384914` and QWK mean/minimum are `.6677687/.6587139`. Fold3 reaches
Macro-F1 `.7205352`, but fold2 remains `.5563545` with A F1 zero in every
epoch. Replacing A42's A input therefore does not reproduce A43's fold2
recovery.

The discriminating difference is supervision. In A43, the multiscale exam
vector received four-class, ordinal and binary gradients. In A53 it receives
only A-vs-rest gradients, while every B/C/D, ordinal and binary gradient is
routed exclusively through the A42 exam vector. The registered hypothesis is
that dense auxiliary multi-task supervision will make the multiscale geometry
identifiable without surrendering A42's stronger inference path for B/C/D.

## Structural change

Retain A53's one shared ConvNeXt-Tiny backbone, A42 hybrid exam vector, A43
multiscale exam vector and final hierarchical distribution. The inference
prediction is unchanged: the multiscale vector supplies the one A-vs-rest
logit; the A42 vector supplies the conditional B/C/D, ordinal and binary
outputs.

Add training-only heads on the multiscale exam vector:

- a conditional B/C/D projection, combined with the same primary A gate to
  form an auxiliary normalized four-class distribution;
- an auxiliary CORAL score/bias head;
- an auxiliary binary A/B-vs-C/D head.

Apply the existing class-balanced focal, neighbor, CORAL and binary objective
to those auxiliary outputs and add it to the unchanged primary objective with
a fixed coefficient of `.5`. The coefficient is fixed before implementation;
there is no DEV sweep. Auxiliary logits never participate in checkpoint
selection or inference. There is no second backbone, checkpoint averaging,
probability averaging, TTA or calibration, so this remains one model rather
than an ensemble. Register architecture
`convnext_tiny_hybrid_bcd_multiscale_a_gate_deepsup_v21`.

Construct all new heads in a CPU RNG fork after every A53 module. Under matched
seeds, all A53 state, construction RNG, stochastic inference outputs and
primary-loss values must remain bit-exact before the auxiliary term is added.
Require finite normalized primary/auxiliary outputs, non-zero first-step
gradients through the shared A gate, auxiliary B/C/D/CORAL/binary heads,
fine/coarse projections and Transformer attention, strict checkpoint
roundtrip, production 512x512 CUDA forward/backward and a real-cache update.

## Frozen protocol and gates

Keep the exact cache, assignments SHA256, seed42, augmentation, sampling
power `.25`, primary losses, optimizer, schedule, 512x512 input and 50-epoch
selection rule. Keep W&B offline and use RTX5090 only, excluding worker2/Vesta.
Screen folds2/3 first and expand only if both audits PASS and:

- each fold Macro-F1 >= `.72`;
- two-fold Macro-F1 sample SD <= `.03`;
- B/C/D mean >= `.7216976152`, minimum >= `.6808637798`;
- QWK mean >= `.6572337361`, minimum >= `.6050383049`.

Report per-class metrics/confusions, A-positive count/streak and epochs at or
above `.72`. These are selected DEV estimates, not independent-test results.
Final CV5 acceptance remains mean Macro-F1 >= `.72`, sample SD <= `.03`, and
minimum fold >= `.65`.

Status: conditionally preregistered; implementation may proceed in isolation,
but Atlas validation and training stay locked behind audited A53 rejection.

