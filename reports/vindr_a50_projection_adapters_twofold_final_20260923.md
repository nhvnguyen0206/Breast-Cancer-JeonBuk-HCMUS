# A50 projection adapters: final two-fold screen

Training array job1078 completed 50 epochs on folds2/3 using RTX5090 with
worker2/Vesta excluded. Read-only audit jobs1080/1081 both PASS: frozen
assignment SHA256, all five manifests, v17 architecture/config provenance,
complete finite histories, selected checkpoints, DEV membership, saved
predictions, probability normalization and recomputed metrics all match.
W&B remained offline (`h663tspa`/`dwm4ttxc`), so no cloud claim is made.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | Epoch50 Macro |
|---:|---:|---:|---:|---:|---|---:|---:|
| 2 | 4 | .539110 | .838710 | .630947 | .000000/.695652/.900787/.560000 | .718813 | .507469 |
| 3 | 40 | .726897 | .858911 | .681406 | .666667/.720000/.912226/.608696 | .746974 | .545429 |

Final selected aggregate:

- Macro-F1 mean `.6330034`, sample SD `.1327855`, minimum `.5391099`;
- accuracy mean `.8488103`;
- QWK mean/minimum `.6561764/.6309472`;
- B/C/D mean/minimum `.7328935/.7188132`;
- epoch50 Macro-F1 mean `.5264489`;
- A-positive epochs/streak: fold2 `0/50`/`0`, fold3 `8/50`/`3`;
- epochs with Macro-F1 >= `.72`: fold2 `0`, fold3 `1`;
- selected CC/MLO adapter output norms: fold2 `.217559/.212518`, fold3
  `.754466/.705281`.

## Gate decision

- each fold Macro-F1 >= `.72`: **FAIL** on fold2;
- two-fold sample SD <= `.03`: **FAIL** by `.1027855`;
- B/C/D mean >= `.7216976`: PASS;
- B/C/D minimum >= `.6808638`: PASS;
- QWK mean >= `.6572337`: **FAIL** by `.0010573`;
- QWK minimum >= `.6050383`: PASS.

A50 is rejected and folds0/1/4 must not be launched. Projection-specific
adapters can help the already stronger fold3 late in training, but amplify
rather than repair fold sensitivity: fold2 never develops an A decision
region and remains `.1382046` below its A42 final score. Relative to the A42
fold2/3 control, A50 Macro mean falls by `.0749365`, while B/C/D mean rises by
`.0111959`; this is not an acceptable four-class tradeoff. These scores are
selected DEV estimates, not independent-test results.

Audit log hashes:

- fold2: `9dfd59ea4a3f66665db0467d07510734529ef0da86041e4441092bc64efdb51b`;
- fold3: `0c36471e3183c5958e22debfb179e3637a4773398c9d45a2054946da845a1c5e`.

A51 was preregistered before first20/final A50 inspection. Its implementation
is now unlocked; training remains locked pending all registered local/Atlas
validation and real-cache RTX5090 preflight.
