# A48 fine-scale D expert: final two-fold screen

Slurm array job1066 completed exactly 50 epochs for folds2/3 on
`slurm-b20a-master-0` NVIDIA RTX5090; Vesta was excluded. Both local auditors
PASS the frozen assignment SHA256, v15 provenance, full histories, selected
checkpoints, manifest membership, prediction membership, normalized
probabilities and independently recomputed metrics. No W&B API was called;
offline receipts remain local on Atlas.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | Epoch50 Macro |
|---:|---:|---:|---:|---:|---|---:|---:|
| 2 | 3 | .540083 | .831266 | .627450 | 0/.685714/.892800/.581818 | .720111 | .492916 |
| 3 | 6 | .738368 | .858911 | .701292 | .666667/.750000/.910543/.626263 | .762269 | .502290 |

Final selected aggregate:

- Macro-F1 mean `.6392256`, sample SD `.1402087`, minimum `.5400831`;
- B/C/D mean `.7411897`, minimum `.7201108`;
- QWK mean `.6643712`, minimum `.6274504`;
- positive-A epochs/longest streak: fold2 `0/0`, fold3 `15/4`;
- epochs with Macro-F1 >= .72: fold2 `0`, fold3 `3`;
- selected D-projection weight norms: fold2 `.015358`, fold3 `.022067`.

The B/C/D mean/minimum and QWK mean/minimum gates pass, confirming useful
fine-scale dense-tissue signal. The required per-fold Macro gate fails on
fold2, and sample SD exceeds `.03` by `.1102087`. Reject A48 and do not launch
folds0/1/4. These are selected DEV results, not an independent test.

## Post-run control audit

A deterministic diagnostic found a treatment-control confound not covered by
the original bit-exact initialization test. A42 and A48 shared parameters and
initial train-mode outputs are exact, but constructing A48's extra module
changes 2,486 bytes of the global CPU RNG state. Its attention/dropout forward
also leaves the global RNG state different from A42. Therefore later backbone
dropout/stochastic-depth masks diverge independently of the learned D
residual. A48 remains a valid measured arm, but its difference from A42 cannot
be attributed solely to the fine-D feature path. A49 is preregistered to repeat
the exact treatment with construction and forward RNG isolation.

Offline W&B IDs: fold2 `qai5n15b`, fold3 `3ppb7vks`. No images, case IDs,
per-patient predictions or checkpoints were uploaded.
