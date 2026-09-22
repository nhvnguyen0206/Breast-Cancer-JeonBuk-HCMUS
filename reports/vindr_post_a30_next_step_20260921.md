# Post-A30 next-step review

A30 completed audited fold0 fails .75 expansion gate (.7025951909).
Do not expand or adopt. A28 stronger decay on A6 also failed complete CV5;
increasing regularization has not resolved the target stability problem.

Re-read completed O2 low-LR plus sampling report: CV5 mean .6058691026,
SD .1199382836 despite fold0 .819667. This is direct evidence against
assuming that a higher fold0 score predicts stability. O2 was an older
configuration, not an isolated LR change on augmented/dropout A6.
A15 backbone warmup and A16 backbone-only LR reduction on A5 failed their
screen gates. Do not repeat these as if untested.

Next bounded candidate: retain immutable A6 and change global LR only from
5e-5 to 2.5e-5, retaining dropout .3 and sampling .25. This tests a moderate
step-size reduction with the A6 augmentation/sampling configuration, not
stronger regularization. It is a hypothesis, not a diagnosed fix; older
low-LR failures limit confidence. No code or architecture change required.

Before launch: preregister exact config, compare against immutable A6,
verify source/split parity and snapshot tests. Fixed fold0 seed42 full50,
RTX5090 only, exclude worker2/no Vesta. Expand only after completed audit
and selected DEV >=.70 under the later documented user threshold revision.
Final acceptance remains mean>=.70, sampleSD<=.05,
minimum>=.65; aspiration mean>=.75. No ensemble or split modification.

No new job submitted by this review. All repeated DEV selection remains
exploratory; do not describe it as independent-test performance. Six total
A cases sharply limit stability claims even if numerical gates pass.
