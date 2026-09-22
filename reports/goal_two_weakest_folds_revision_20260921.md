# Goal protocol revision: screen on two weakest folds

The architecture-preservation sentence below was superseded later on
2026-09-21 by `goal_architecture_revision_20260921.md`. The two-fold screening
rules remain active.

The improvement target remains audited five-fold mean four-class Macro-F1
>=0.70 with sample SD <=0.05 and minimum fold >=0.65, using seed 42, the
frozen grouped split, DenseNet121 plus hierarchical fusion, no ensemble, RTX
5090 only, and no Vesta.

For every new experimental arm after A34, replace the former fold-0-only
screen with a fixed two-fold stress screen on **fold 1 and fold 3**. These are
chosen once from the aggregate of 25 completed CV5 result files, where they
have the lowest historical mean selected Macro-F1 (fold 1: 0.573657; fold 3:
0.619210). The pair must not be changed per arm or selected after observing a
new arm.

Run both screening folds for the full registered 50 epochs from one immutable
snapshot/config. Expand to the remaining three folds only after both screen
runs pass provenance/checkpoint/prediction/W&B audit and jointly satisfy:

- two-fold mean Macro-F1 >=0.70;
- neither screen fold Macro-F1 <0.65;
- report Macro-F1, class F1, accuracy, QWK and confusion matrices for both;
- do not treat success on the six total A cases as sufficient evidence.

After expansion, retain the original two screen runs rather than rerunning or
replacing them. Final success still depends on the complete audited CV5 gates,
not the two-fold screen. Continue using selected DEV terminology and do not
claim independent-test performance.

A34 had already passed its preregistered fold-0 screen and launched folds 1–4
before this revision. Do not interrupt or retrospectively alter A34; apply
the two-fold rule beginning with the next arm if A34 fails final acceptance.
