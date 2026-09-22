# A30 confirmation: common first10-epoch horizon

Array982 tasks1–4 RUNNING at14:45, all10 epochs recorded. Original981
fold0 completed50; restrict its history to10 here for matched horizon only.
This does not replace the final selected fold0 checkpoint (epoch11).

| Fold | Best epoch within first10 | DEV Macro-F1 | A F1 |
| --- | ---: | ---: | ---: |
|0|7|.5896463747990113|.3333333333|
|1|3|.5477628991832678|0|
|2|4|.6310390439700785|.4|
|3|2|.6864294857992337|.5|
|4|5|.5988595168161732|.4|

Matched-horizon mean .6107474641135529, sampleSD .05170384729439495,
minimum .5477628991832678. Preliminary tuning DEV only, no final audit.
Fold1 selected checkpoint misses its only true A case; rare-A limitation
persists. Continue unchanged full50; do not tune on weak confirmation fold.
Next score review common20-epoch horizon. No new training submitted.
