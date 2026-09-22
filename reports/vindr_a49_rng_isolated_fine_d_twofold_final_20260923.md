# A49 RNG-isolated fine-D expert: final two-fold screen

Slurm job1069 tasks2/3 completed all 50 epochs on
`slurm-b20a-master-0` RTX5090. Dependency audit jobs1073/1074 both PASS with
empty error logs. They verify the frozen five-fold manifests and assignment
SHA256, A49 v16 architecture/provenance, complete finite histories, selected
checkpoints, saved prediction membership, recomputed metrics and probability
normalization. No Vesta node was used.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | Epoch50 Macro |
|---:|---:|---:|---:|---:|---|---:|---:|
| 2 | 5 | .606284 | .799007 | .640927 | .333333/.649351/.871022/.571429 | .697267 | .517407 |
| 3 | 7 | .711244 | .787129 | .649892 | .666667/.761905/.850615/.565789 | .726103 | .547844 |

Final two-fold aggregates:

- Macro-F1 mean `.6587638`, sample SD `.0742182`, minimum `.6062836`;
- accuracy mean `.7930681`;
- QWK mean `.6454094`, minimum `.6409266`;
- mean F1 A/B/C/D `.500000/.705628/.860818/.568609`;
- B/C/D mean `.7116851`, minimum `.6972670`;
- epoch50 Macro-F1 mean `.5326251`;
- positive-A epochs/longest streak: fold2 `1/1`, fold3 `5/3`;
- epochs with Macro-F1 >= `.72`: fold2 `0`, fold3 `0`.

## Registered gate decision

- each fold Macro-F1 >= `.72`: FAIL on both folds;
- two-fold sample SD <= `.03`: FAIL by `.0442182`;
- B/C/D mean >= `.7216976`: FAIL by `.0100126`;
- B/C/D minimum >= `.6808638`: PASS;
- QWK mean >= `.6572337`: FAIL by `.0118243`;
- QWK minimum >= `.6050383`: PASS.

A49 is rejected and folds0/1/4 must not be launched. RNG isolation itself is
validated: CPU/CUDA audits prove exact A42 stochastic-state preservation, and
the observed early rare-A pattern returns toward A42 instead of A48. This
establishes A48's incidental RNG shift as a real confound. After the fine-D
residual starts learning, however, its intended treatment gradients lower
fold3 B/C/D performance and do not recover fold2 sufficiently. The fine-D
expert family is therefore not a stable improvement.

Offline W&B IDs are `7msbizh4` (fold2) and `7mch95l6` (fold3); no external
upload was performed. These are selected DEV results, not an independent test.
Audit SHA256 values are
`6665258412df15f6f45df060f30d5d67e316a26a369d8fbc85497c309eaeef51`
(fold2) and
`3bd9e34b10e42d68baf170db1836771f2125c2f418cd9e2f66131500b52f5262`
(fold3).

A50 was preregistered before this final inspection. Its implementation is now
unlocked, while training remains locked until every registered initialization,
RNG, gradient, test and real-cache RTX5090 preflight requirement passes.
