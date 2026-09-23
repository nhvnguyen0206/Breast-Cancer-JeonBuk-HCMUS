# A51 bilateral spatial relation: final two-fold screen

Training array job1084 completed 50 epochs on folds2/3 using RTX5090 with
worker2/Vesta excluded. Read-only audit jobs1086/1087 both PASS: frozen
assignment SHA256, all five manifests, v18 architecture/config provenance,
complete finite histories, selected checkpoints, DEV membership, saved
predictions, probability normalization and recomputed metrics all match. W&B
remained offline (`5hzj03pt`/`oeauqr5m`), so no cloud claim is made.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | Epoch50 Macro |
|---:|---:|---:|---:|---:|---|---:|---:|
| 2 | 7 | .615598 | .799007 | .625975 | .400000/.642857/.870861/.548673 | .687464 | .535508 |
| 3 | 40 | .740483 | .866337 | .705738 | .666667/.712329/.916272/.666667 | .765089 | .723414 |

Final selected aggregate:

- Macro-F1 mean `.6780406`, sample SD `.0883076`, minimum `.6155977`;
- accuracy mean `.8326720`;
- QWK mean/minimum `.6658567/.6259754`;
- B/C/D mean/minimum `.7262763/.6874635`;
- epoch50 Macro-F1 mean `.6294610`;
- A-positive epochs/longest streak: fold2 `1/50`/`1`, fold3 `26/50`/`9`;
- epochs with Macro-F1 >= `.72`: fold2 `0`, fold3 `14`;
- selected bilateral output-projection norms: fold2 `1.283545`, fold3
  `2.566162`.

## Gate decision

- each fold Macro-F1 >= `.72`: **FAIL** on fold2;
- two-fold sample SD <= `.03`: **FAIL** by `.0583076`;
- B/C/D mean >= `.7216976`: PASS;
- B/C/D minimum >= `.6808638`: PASS;
- QWK mean >= `.6572337`: PASS;
- QWK minimum >= `.6050383`: PASS.

A51 is rejected and folds0/1/4 must not be launched. Relative to A42 on the
same folds, A51 slightly improves fold3 and the B/C/D/QWK secondary metrics,
but lowers the two-fold Macro mean by about `.02990`, lowers the minimum by
about `.06172`, and roughly doubles selected spread. The bilateral branch is
not inactive; it learns much more strongly on fold3, while fold2's A region
appears in only one isolated epoch. This is amplified fold sensitivity, not
the registered stability improvement. These are selected DEV estimates, not
independent-test results.

Audit log hashes:

- fold2: `70a92d992414d4f592c53e6694fedf5d3136ad4d3d3b04fde45a58309fc39cc5`;
- fold3: `8ee1aa3fdb3f789956bfdb6175c8e60fbde0ce52260458308411bdb4522492a6`.

A52 was preregistered before first40/final A51 inspection and its local
implementation already passes all registered checks. A51 rejection unlocks
A52 Atlas hash/tests, CUDA parity and real-cache RTX5090 preflight; training
remains locked until those checks pass.
