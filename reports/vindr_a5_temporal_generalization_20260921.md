# A5 temporal generalization diagnostic

Read-only recomputation from all 50 history entries per original run on
2026-09-21: job770 fold0, job771 folds1–4. Compare epoch1–10 with41–50;
no checkpoint reselection, new inference, or alteration of reported CV5.
BCD below is the mean of class B/C/D F1 per epoch, averaged over each window.

| Fold | Train loss first10 | Train loss last10 | DEV BCD first10 | DEV BCD last10 |
|---|---:|---:|---:|---:|
|0|.743030|.259866|.696506|.664541|
|1|.726587|.259695|.691395|.680289|
|2|.738844|.261743|.683505|.658927|
|3|.711511|.261083|.709229|.690614|
|4|.742802|.260167|.690410|.667612|

All five folds reduce training objective while BCD DEV performance declines
by1.11–3.20 percentage points. This is consistent with deteriorating
generalization, beyond the sparse A-class effect, but not causal proof of
overfitting: train objective and DEV F1 are different quantities, and no
matched unaugmented FIT evaluation is available in these histories.

Nonzero A-F1 epochs first10/last10: fold0 1/0, fold1 0/0, fold2 1/0,
fold3 0/0, fold4 0/10. Thus later training does not uniformly erase A
performance, and A alone cannot explain the BCD decline.

Next candidate: return to immutable A5 and test stronger geometric
augmentation only (rotation5->10 degrees, translation .03->.05), retaining
brightness, input size, natural sampling, all losses, dropout, optimizer,
architecture and single-checkpoint inference. This treats generalization
without adding heads or ensembles; previous dropout/weight-decay attempts
are already recorded and should not be blindly repeated. Check breast-mask
retention/transform implementation before approving deployment; additional
cropping may be harmful. Candidate not launched and no benefit is claimed.
Keep fixed fold0/seed42/full50 and the existing strict .75 expansion gate.
Selected DEV remains repeatedly tuned, not an independent test.
