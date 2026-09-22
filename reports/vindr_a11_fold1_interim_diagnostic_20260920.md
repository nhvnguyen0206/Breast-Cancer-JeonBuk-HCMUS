# A11 fold1 interim diagnosis

Read-only observation of array843; no training, split, or configuration changes.
At the diagnostic snapshot, fold1 had24 completed epochs and folds2--4 had18.
Scheduler subsequently confirmed all four jobs RUNNING on master/worker1;
all recorded scalar training losses were finite.

## Observations

Fold1 DEV support A/B/C/D is1/39/312/51; FIT support5/157/1244/208.
This is comparable to the other frozen folds, not evidence of a density-count
split defect. Class balance within a fold remains very poor.

Fold1 best checkpoint is epoch2: Macro-F1 .5584428851144086,
accuracy .8610421836228288, QWK .6614359866782682, class F1
[0,.6956521739130435,.9144634525660964,.6236559139784946].
Confusion matrix (true rows, predicted columns A/B/C/D):
[[0,1,0,0],[0,24,15,0],[0,5,294,13],[0,0,22,29]].
The sole A case is missed in all24 epochs. BCD mean F1 is .7445905134858782;
this is diagnostic only, not a replacement for four-class Macro-F1.
There are substantive adjacent-class errors:15/39 B->C and22/51 D->C.

At the same first18-epoch horizon, best Macro-F1 for folds0--4 is
[.6488095238095238,.5584428851144086,.5359221568728612,
.5676297187477672,.5289415171795353]. Fold1 is not uniquely poor among
confirmation folds at this horizon. Comparing it directly to fold0's
full50 selected score .819363312392079 confounds training horizon.

## Limits and decision

These observations identify the metric contribution of scarce A support,
not the cause of the A prediction failure. Previous numerical cache checks
do not establish anatomical crop or label correctness. Visual review remains
outstanding. No numerical-loss failure was detected; this alone does not
prove optimization is healthy. Do not resplit, remove fold1, alter this
running experiment, or tune to its single A case. Finish the registered50
epochs, audit all folds, and compare B/C/D and A separately before choosing
the next controlled experiment. No independent-test or multi-seed claim.
