# A48 preregistration: fine-scale D texture expert

Registered before implementation or training results. A42 remains the closest
audited CV5 model (mean Macro-F1 .7592604, minimum .6773145, sample SD
.0561945). Its weakest fold2 recognizes A but maps 31/52 D cases to C, giving
D F1 .4941176. A47's output-level D gate improves early fold2 D F1 to .5894737
but reduces fold3 B/D and fails every expansion gate. This indicates that a
factorized D decision alone is insufficient; the next hypothesis targets
fine-scale texture representation while restoring A42's proven probability
head exactly.

## Controlled structural change

Retain A42's ConvNeXt-Tiny backbone, coarse global hierarchical relational
path, coarse spatial-attention residual, A-vs-rest gate, conditional B/C/D
softmax, CORAL/binary auxiliary heads, augmentation, losses, sampling,
optimizer and schedule.

Add one fine-scale D expert:

- capture the 384-channel ConvNeXt feature maps immediately after stage 5;
- fuse the four canonical fine maps with a spatial token-attention module
  using A42's registered attention dimension/heads/layers/grid settings;
- normalize the resulting fine exam vector and project it to one scalar;
- add that scalar only to the conditional D logit before the unchanged B/C/D
  softmax.

The final D projection is zero-initialized and constructed after every A42
module, so all shared A42 parameters initialize bit-exactly and the initial
four-class output is exactly A42. After the first update, the dedicated branch
can learn high-resolution dense-tissue evidence without changing the A gate or
introducing thresholds. This is one end-to-end model and one four-class
distribution, not an ensemble, post-hoc calibration or test-time averaging.

Architecture ID:
`convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_v15`.

## Fixed two-fold screen and gates

Screen A42's two lowest folds, 2 and 3, for exactly 50 epochs using seed42,
the frozen grouped split/window16 cache and assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Use RTX5090 only, exclude worker2/Vesta, fresh ImageNet initialization and W&B
project `HCMUS-paper1`. Require local tests, production-shape inference and a
real-cache AMP forward/backward/optimizer preflight from an immutable snapshot.

A42 parent baselines over folds2/3 are Macro mean/sample-SD/minimum
`.7079398780/.0433108229/.6773145015`; B/C/D mean/minimum
`.7216976152/.6808637798`; QWK mean/minimum `.6572337361/.6050383049`.

Expand only if both completed local audits PASS and all gates hold:

- each fold Macro-F1 >= .72;
- two-fold Macro-F1 sample SD <= .03;
- B/C/D mean >= .7216976152 and minimum >= .6808637798;
- QWK mean >= .6572337361 and minimum >= .6050383049.

Report D F1, A F1, positive-A epochs, longest streak and the learned D-residual
projection norm, but none replace the gates. Reject without tuning or folds
0/1/4 if any gate fails. Final CV5 acceptance remains mean Macro-F1 >= .72,
sample SD <= .03 and minimum >= .65. Scores remain selected DEV, not an
independent test.

Status: preregistered; implementation pending.
