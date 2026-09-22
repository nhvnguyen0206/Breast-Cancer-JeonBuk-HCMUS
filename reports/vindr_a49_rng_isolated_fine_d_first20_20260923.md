# A49 folds2/3: matched first20

Both Slurm job1069 tasks remain RUNNING on `slurm-b20a-master-0` RTX5090.
Each log contains complete epochs1--20 with finite losses and no runtime error
markers. Selection is independently restricted to the common first-20 horizon
on the frozen cache/split and seed42.

| Arm/fold | Epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | A-positive epochs | Macro >=.72 epochs |
|---|---:|---:|---:|---:|---|---:|---:|---:|
| A42/f2 | 8 | .606175 | .774194 | .606120 | .4/.641026/.850340/.533333 | .674900 | 1/20 | n/a |
| A42/f3 | 7 | .738565 | .851485 | .709429 | .666667/.757895/.903437/.626263 | .762531 | 4/20 | n/a |
| A48/f2 | 3 | .540083 | .831266 | .627450 | 0/.685714/.892800/.581818 | .720111 | 0/20 | n/a |
| A48/f3 | 6 | .738368 | .858911 | .701292 | .666667/.750000/.910543/.626263 | .762269 | 8/20 | n/a |
| A49/f2 | 5 | .606284 | .799007 | .640927 | .333333/.649351/.871022/.571429 | .697267 | 1/20 | 0 |
| A49/f3 | 7 | .711244 | .787129 | .649892 | .666667/.761905/.850615/.565789 | .726103 | 4/20 | 0 |

| Aggregate | A42 | A48 | A49 | Delta A49-A42 | Delta A49-A48 |
|---|---:|---:|---:|---:|---:|
| Macro-F1 mean | .672370 | .639226 | .658764 | -.013606 | +.019538 |
| Macro-F1 sample SD | .093614 | .140209 | .074218 | -.019396 | -.065991 |
| Minimum Macro-F1 | .606175 | .540083 | .606284 | +.000109 | +.066201 |
| B/C/D mean across folds | .718716 | .741190 | .711685 | -.007031 | -.029505 |
| QWK mean | .657775 | .664371 | .645409 | -.012366 | -.018962 |

The selected checkpoints and all aggregate values are unchanged from first10.
RNG isolation continues to restore A42-like rare-A behavior and materially
reduces A48's imbalance, but the treatment has not created a single epoch at or
above `.72` on either fold. Fold3's C/D regression keeps A49 below A42 on mean,
B/C/D mean and QWK. Therefore the fine-D representation hypothesis is currently
unsupported as an improvement, although the fixed protocol requires completion
to epoch50 before rejection.

Continue unchanged to40/50 and run the queued local audits. Folds0/1/4 remain
locked. These are selected DEV metrics, not an independent test. W&B remains
offline with IDs `7msbizh4` and `7mch95l6`.
