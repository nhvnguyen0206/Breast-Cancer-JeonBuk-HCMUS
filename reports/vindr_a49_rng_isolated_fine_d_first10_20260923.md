# A49 folds2/3: matched first10

Both Slurm job1069 tasks remain RUNNING on `slurm-b20a-master-0` RTX5090.
Each log contains complete epochs1--10 with finite losses and no runtime error
markers. Values below select best DEV Macro-F1 independently within the same
first-ten-epoch horizon on the frozen cache/split and seed42.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | D-head norm |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| A42/f2 | 8 | .606175 | .774194 | .606120 | .4/.641026/.850340/.533333 | .674900 | 1/10 | n/a |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/10 | n/a |
| A48/f2 | 3 | .540083 | .831266 | .627450 | 0/.685714/.892800/.581818 | .720111 | 0/10 | .015358 |
| A48/f3 | 6 | .738368 | .858911 | .701292 | .666667/.750000/.910543/.626263 | .762269 | 5/10 | .022067 |
| A49/f2 | 5 | .606284 | .799007 | .640927 | .333333/.649351/.871022/.571429 | .697267 | 1/10 | .017473 |
| A49/f3 | 7 | .711244 | .787129 | .649892 | .666667/.761905/.850615/.565789 | .726103 | 4/10 | .024728 |

| Aggregate | A42 | A48 | A49 | Delta A49-A42 | Delta A49-A48 |
|---|---:|---:|---:|---:|---:|
| Macro-F1 mean | .672370 | .639226 | .658764 | -.013606 | +.019538 |
| Macro-F1 sample SD | .093614 | .140209 | .074218 | -.019396 | -.065991 |
| Minimum Macro-F1 | .606175 | .540083 | .606284 | +.000109 | +.066201 |
| B/C/D mean across folds | .718716 | .741190 | .711685 | -.007031 | -.029505 |
| QWK mean | .657775 | .664371 | .645409 | -.012366 | -.018962 |

RNG isolation has the intended observable effect: A49 exactly restores A42's
early rare-A persistence counts (fold2 `1/10`, fold3 `4/10`) and removes most
of A48's fold imbalance. Fold2 Macro-F1 recovers by `.066201` over A48 and is
essentially equal to A42. However, fold3 B/C/D performance is lower, so the
mean remains below A42 and neither fold reaches the registered `.72` gate at
this horizon. This supports the RNG-confound diagnosis but does not yet support
the fine-D expert as a performance improvement.

No gate is final at first10. Continue both unchanged to20/40/50; folds0/1/4
remain locked. These are selected DEV metrics, not an independent test. W&B
remains offline with IDs `7msbizh4` and `7mch95l6`.
