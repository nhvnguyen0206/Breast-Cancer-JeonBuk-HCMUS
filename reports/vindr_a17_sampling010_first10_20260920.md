# A17 sampling power 0.10 — first 10 epochs

Job907_0 is RUNNING on `slurm-b20a-master-0`. All scalar training losses are
finite. The registered weighted sampler drew aggregate class counts
`[95,1876,11853,2306]` over the first 10 epochs, compared with the natural
FIT counts repeated ten times `[50,1560,12450,2070]`. Total AMP-skipped
updates are 7, equal to A5 and A6 through the same horizon.

A17's selected first-10 checkpoint is epoch8: DEV Macro-F1
0.7556740297265725, accuracy 0.7797029702970297, QWK 0.5971948377845492,
class F1 `[1.0,0.6464646464646465,0.8499156829679595,0.5263157894736842]`,
no severe errors. Confusion matrix:
`[[1,0,0,0],[0,32,8,0],[0,27,252,32],[0,0,22,30]]`.

Matched first-10 selected Macro-F1 is 0.5452488631717199 for A5 and
0.782979257528481 for A6. A17 provisionally crosses the 0.75 screen threshold,
but the apparent gain over A5 is driven by correctly classifying the single
fold0 A case: its selected B/C/D mean F1 is 0.6742320396354301 versus
0.7269984842289599 for A5, and its accuracy/QWK are lower. Therefore this is
not yet evidence of a stable improvement and does not authorize expansion.

Continue the preregistered run unchanged to epoch50. Only the completed audit
determines whether folds1--4 may be submitted. DEV is not an independent test.

W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/djz4e32c
