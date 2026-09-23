# A51 folds2/3: matched first40

Array job1084 remains healthy on RTX5090 under the immutable v18 protocol.
This interim selected-DEV analysis is strictly truncated to epochs1--40 even
though fold3 had already started later work when the report was generated.

| Run | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Longest A streak | Epochs Macro >= .72 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| A51/f2 | 7 | .615598 | .799007 | .625975 | .400000/.642857/.870861/.548673 | .687464 | 1/40 | 1 | 0 |
| A51/f3 | 40 | .740483 | .866337 | .705738 | .666667/.712329/.916272/.666667 | .765089 | 17/40 | 3 | 7 |

Fold3 improves at epoch40, but fold2 remains frozen at its isolated epoch7
event. Aggregate Macro-F1 is mean `.6780406`, sample SD `.0883076`, and
minimum `.6155977`; mean accuracy is `.8326720`. Mean/minimum B/C/D are
`.7262763/.6874635`, and mean/minimum QWK are `.6658567/.6259754`.

Thus both B/C/D gates and both QWK gates now pass, and fold3 passes its Macro
gate. Fold2 still fails `.72` by `.1044023`, has no epoch at or above `.72`,
and the two-fold SD fails `.03` by `.0583076`. The zero-initialized bilateral
output projection is active (selected norms `1.283545/2.566162`), but it helps
the already stronger fold far more than the weak fold. This increases rather
than closes the selected-score gap after epoch20.

Finish the preregistered 50 epochs and execute queued audits1086/1087. Do not
expand to folds0/1/4. A52 was preregistered before this first40 inspection and
is locally validated, but remains Atlas/training-locked until audited A51
rejection.
