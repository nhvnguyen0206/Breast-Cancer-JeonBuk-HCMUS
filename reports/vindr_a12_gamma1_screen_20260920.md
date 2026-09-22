# A12 completed fixed-fold screen

Audit PASS: 50 epochs, finite scalar losses, checkpoint/prediction metrics,
all frozen manifests and finished W&B fax28rks verified. Job847_0 completed
ExitCode0:0 with no restarts/requeue on master; worker2 excluded.

Selected epoch27 Macro-F1 .7946366892484166, accuracy .844059405940594,
QWK .6576823757262751; class F1 [1,.6593406593406593,
.9001584786053882,.6190476190476191]. Zero severe errors.
A5 fold0 Macro-F1 .7896498561536562: A unchanged, B/C improve, D decreases.
Only two epochs reach .75; final epoch Macro-F1 .5973763269497734.
This passes the preregistered selected-DEV screen gate, not stability or CV5
success. Retain fold0 and expand fresh folds1--4 with unchanged configuration.
No independent test, multi-seed confirmation, visual crop review or fresh
forward-inference verification is claimed by this audit.
