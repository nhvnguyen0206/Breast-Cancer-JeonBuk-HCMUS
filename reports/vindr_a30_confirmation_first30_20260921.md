# A30 common first30-epoch review

Array982 tasks1–4 RUNNING at43:48; actual epochs [50,30,30,32,32].
Evidence: remote history.json, including original981 fold0; all restricted
to first30 epochs. Selected DEV, not independent evaluation or final audit.

|Fold|Selected epoch|Macro-F1|A F1|
|---|---:|---:|---:|
|0|11|.7025951908901428|.6666666667|
|1|20|.7584943371085943|1|
|2|27|.6402752996676502|.5|
|3|2|.6864294857992337|.5|
|4|25|.6573706751312642|.6666666667|

Mean .689032997719377; sampleSD .045813220850101234;
minimum .6402752996676502. SD currently within .05, but mean below .70
and minimum below .65; no success claim, training incomplete.
Fold2 selected A F1 improved from .4 to .5 while D F1 fell from
.5740740741 to .5116279070. Fold4 A F1 improved from .5 to .6666666667;
do not attribute four-class gain to uniformly improved recognition.
Continue unchanged full50; next review common40 epochs. No new jobs.
