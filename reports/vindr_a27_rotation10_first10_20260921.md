# A27 first10 (incomplete screen)

Job964_0 verified RUNNING on master; first10 history entries inspected.
All training scalar losses finite,7 AMP skipped updates. Natural FIT class
counts [5,156,1245,207], seed42 and registered schedule unchanged.

Best so far epoch10: Macro-F1 .590697983014862, accuracy .8366336633663366,
QWK .6769409712125618, classF1 [.25,.5,.9044585987261147,.7083333333333334].
Confusion rows true A/B/C/D:
[[1,0,0,0],[6,19,15,0],[0,17,284,10],[0,0,18,34]]. Severe errors0.

Matched A5 first10 best epoch7 Macro-F1 .5452488631717199,
classF1 [0,.6086956521739131,.8826446280991735,.6896551724137931].
A27 four-class increase .0454491198 is driven by A; BCD mean .7042639774
is below A5 .7269984842. C/D improve but B declines. Six B cases predicted
A yield only .25 A F1 despite recovering the lone DEV A study. This is not
evidence of robust minority learning or cross-fold stability.

Below .75 gate. Continue unchanged full50; no confirmation folds. Next
review20 epochs. Selected DEV, not independent test; no final audit yet.
W&B https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/wjz7dz8t.
