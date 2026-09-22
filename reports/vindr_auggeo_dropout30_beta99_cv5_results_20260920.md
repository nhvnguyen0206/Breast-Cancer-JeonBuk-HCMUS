# A11 completed CV5: beta .99 on A5

Audit PASS: 50 epochs each, common configuration, frozen split membership,
checkpoint selection, prediction-derived metrics and finished source W&B runs.
All confirmation jobs completed with ExitCode0:0, no restarts, on allowed nodes.

Mean selected-DEV four-class Macro-F1: **.6181916009106782**;
sample SD **.11503828758684345**. Accuracy .8448001375819965;
QWK .6563818201449779. Class F1 means A/B/C/D:
[.28,.68984106660163,.902753551725075,.6001717853160075].
BCD mean .7309221345475708; epoch50 Macro-F1 mean .5765811177119131.
Fold scores: [.819363312392079,.5639564704060698,.5359221568728612,
.5676297187477672,.6040863461346134].

Reject as replacement for A5 (.7028282800839902). A11 improves mean B/C
but degrades D and A, and BCD mean is below A5 (.7371043734453203).
The fold0 screen gain did not generalize across the fixed folds.
Retain A5 as substantive parent for the next single-factor screen.
No ensemble, independent-test, or multi-seed success claim.
Visual crop/label review and new forward-inference verification were not
part of this audit.

W&B summary: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/6kdi88iz
Exact metrics and source URLs are in the adjacent JSON report.
