# Post-A30 final decision

A30 completed and passed the provenance/data/W&B audit. Its mean Macro-F1
0.709931 passes the revised 0.70 mean target, but sample SD 0.051267 and the
minimum fold 0.640275 miss the registered stability limits of 0.05 and 0.65.
Do not mark the scientific objective complete and do not present A30 as an
independent-test result.

Proceed with the already preregistered A31 bounded screen: return to A6 and
change only global learning rate from 5e-5 to 2.5e-5. This directly tests
whether a smaller update step improves checkpoint/fold stability without an
architecture change. It is a hypothesis with limited confidence because
older low-LR arms did not generalize.

Run fixed fold 0 for all 50 epochs on RTX 5090, excluding worker2/Vesta.
Expand the unchanged original fold 0 with folds 1–4 only if the completed,
audited selected-DEV fold-0 Macro-F1 is at least 0.70. Final acceptance still
requires five-fold mean >= 0.70, sample SD <= 0.05, and minimum >= 0.65.
No ensemble, split change, or favorable-fold substitution is allowed.

