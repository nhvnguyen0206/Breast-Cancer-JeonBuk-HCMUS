# A13 first20 matched-horizon observation

Job852_0 verified RUNNING on slurm-b20a-master-0; 20 completed epochs,
all recorded scalar training losses finite. No configuration or split change.

Both A13 and A5 select epoch20 within their first20 epochs.
A13 Macro-F1 .7580533506398416, accuracy .7970297029702971,
QWK .5906446690825864, class F1 [1,.5656565656565656,
.8665568369028006,.6]. Confusion matrix (true rows A/B/C/D):
[[1,0,0,0],[0,28,12,0],[0,30,263,18],[0,1,21,30]].
One severe error D->B. Ordinal training loss .113144780099952.

A5 same-horizon selected Macro-F1 .7654421854687274,
accuracy .7970297029702971, QWK .6126648582920213,
class F1 [1,.6086956521739131,.8637873754152824,.5892857142857143],
zero severe errors; ordinal train loss .6524312927069948.

A13 exceeds .75 provisionally but is below A5 at the same horizon.
Lower ordinal training loss does not establish better generalization.
Continue registered full50 and screen audit before any fresh folds1--4.
No expansion submitted; next metric report at30. Selected DEV, not test;
the single A case prevents a stability claim.
