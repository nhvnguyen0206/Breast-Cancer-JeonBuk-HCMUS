# A49 preregistration: RNG-isolated fine-D expert

Registered after A48 completed and before A49 implementation or training.
A48 improved fold2 D F1 and passed every B/C/D and QWK aggregate gate, but
lost the rare A case on fold2 and failed Macro/SD gates. A post-run diagnostic
proved that its additional module construction and stochastic forward changed
the global RNG stream relative to A42, so subsequent A42-path dropout and
stochastic-depth masks were not controlled.

## Controlled change

A49 is identical to A48 in model topology, output equations, zero-initialized
D residual, losses, augmentation, sampling, optimizer, schedule, cache, split
and seed42. It adds only RNG isolation:

- save and restore the CPU RNG state around construction of all fine-D modules;
- execute the fine-D attention branch inside a PyTorch RNG fork that restores
  CPU and active CUDA RNG states on exit;
- do not isolate or alter the original A42 path's random operations.

Required validation before launch:

- A42/A49 shared state and initial eval/train outputs are bit-exact;
- RNG state after A49 construction equals A42 under the same seed;
- RNG state after one train-mode A49 forward equals A42 under the same forward
  seed, while the treatment head still receives gradient and learns;
- A48 remains v15-compatible; A49 receives a new registered architecture ID,
  `convnext_tiny_hybrid_spatial_a_gate_fine_d_expert_rngisolated_v16`.

This is still one end-to-end deployable model with one four-class distribution,
not an ensemble, threshold or post-hoc calibration. After its residual becomes
non-zero, gradient differences caused by the treatment are intended; only
incidental RNG divergence is removed.

## Fixed screen and gates

Run only the same preregistered low A42 folds2/3 for 50 epochs on RTX5090,
excluding Vesta, with assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`.
Keep W&B offline until aggregate-upload permission is explicit.

Expand to folds0/1/4 only if both local audits PASS and all gates hold:

- each fold Macro-F1 >= `.72`;
- two-fold Macro-F1 sample SD <= `.03`;
- B/C/D mean >= `.7216976152`, minimum >= `.6808637798`;
- QWK mean >= `.6572337361`, minimum >= `.6050383049`.

Report F1 A/B/C/D, A-positive epochs/streak, learned D-head norm and A42/A48
matched comparisons, but none replace the gates. If any gate fails, reject
without tuning or folds0/1/4. Scores remain selected DEV, not an independent
test. Final CV5 acceptance remains mean Macro-F1 >= `.72`, sample SD <= `.03`
and minimum >= `.65`.

Status: preregistered; implementation pending.
