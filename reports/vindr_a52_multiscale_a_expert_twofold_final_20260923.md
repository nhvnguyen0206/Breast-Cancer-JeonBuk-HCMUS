# A52 multiscale A expert: final two-fold screen

Training array job1090 completed 50 epochs on folds2/3 using RTX5090 with
worker2/Vesta excluded. Read-only audit jobs1092/1093 both PASS: frozen
assignments and all manifests, v19 provenance, finite 50-epoch histories,
selected checkpoints, DEV membership, predictions, probability normalization
and recomputed metrics all match. W&B remained offline
(`o8i8cjx5`/`q6zqr8i4`), so no cloud claim is made.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D | B/C/D mean | Epoch50 Macro |
|---:|---:|---:|---:|---:|---|---:|---:|
| 2 | 7 | .603462 | .781638 | .610149 | .400000/.622222/.857143/.534483 | .671283 | .514905 |
| 3 | 19 | .730541 | .856436 | .687798 | .666667/.727273/.909667/.618557 | .751832 | .526415 |

Final selected aggregate:

- Macro-F1 mean `.6670014`, sample SD `.0898583`, minimum `.6034620`;
- accuracy mean `.8190367`;
- QWK mean/minimum `.6489734/.6101486`;
- B/C/D mean/minimum `.7115574/.6712826`;
- epoch50 Macro-F1 mean `.5206603`;
- A-positive epochs/longest streak: fold2 `1/50`/`1`, fold3 `8/50`/`3`;
- epochs with Macro-F1 >= `.72`: fold2 `0`, fold3 `1`;
- selected A-expert output norms: fold2 `.174012`, fold3 `.347079`.

## Gate decision

- each fold Macro-F1 >= `.72`: **FAIL** on fold2;
- two-fold sample SD <= `.03`: **FAIL** by `.0598583`;
- B/C/D mean >= `.7216976`: **FAIL** by `.0101402`;
- B/C/D minimum >= `.6808638`: **FAIL** by `.0095812`;
- QWK mean >= `.6572337`: **FAIL** by `.0082604`;
- QWK minimum >= `.6050383`: PASS.

A52 is rejected and folds0/1/4 must not launch. The expert clearly trains, but
the zero-initialized residual learns more strongly on fold3 and never repairs
fold2 beyond one isolated positive-A epoch. Relative to A51 it reduces mean,
minimum, B/C/D and QWK while leaving spread equally unacceptable. This
supports the preregistered A53 hypothesis that the multi-scale A representation
must replace, rather than weakly correct, the A42 A-gate input. These are
selected DEV estimates, not independent-test results.

Audit log hashes:

- fold2: `b799def6ed4da62f3730ca4808c738f0a15933102cbab5a39c9c37bb0b80a26c`;
- fold3: `70521bb02112974d745279a92a9c34afd6ff182da8ee059984bc4726319c0bbc`.

A53 was preregistered before first40/final A52 inspection and passes local
validation. Audited A52 rejection unlocks A53 Atlas hash/tests, CUDA parity and
real-cache RTX5090 preflight; training remains locked until they pass.
