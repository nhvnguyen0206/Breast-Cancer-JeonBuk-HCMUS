# A44 implementation and local validation

Implemented architecture `convnext_tiny_local_global_view_transformer_a_gate_v11`:
shared two-layer within-view Transformer, four view summaries, zero-start
CC/MLO and left/right adapters, then two-layer global Transformer. A43's
backbone/head/loss and training settings remain fixed. The model factory,
inference registry and both auditors recognize the new architecture.

Local CPU validation in `/home/tyler/miniconda3/envs/paper_1`:
- All50 repository tests PASS in27.927 seconds, including four new A44 tests.
- Local view independence, global sensitivity, masking invariance including
  NaN-filled absent views, finite nonzero gradients and strict checkpoint
  roundtrip PASS. Adapter down-projection gradients activate after the first
  update, as expected from zero-initialized output weights.
- Production configuration forward on synthetic `[1,4,3,512,512]` PASS;
  finite outputs and probability sum1.0. Parameter count31,553,769.
- A43/A44 config comparison confirms only experiment arm and fusion differ.
- Syntax compilation and whitespace checks PASS.

Source SHA256:
- model.py: 3582d99b092a0f29af549dd205edb4e3b677efee8f72130bf22f5f646bc6cb08
- engine.py: 105aca490b8d3cef17204186b303c11cb4fad47393a3ac23de96ebb4fba3b21d
- A44 config: 3723a41a0d9e367f3fac1cd6951fa3129e48392a0396f67390cca453177bcc49
- A44 tests: 8d723a5f0f514bb58a9a09cef016280ed4051919fe690915ae6e6ac7f4c48d53

## Historical deployment approval issue — resolved

Update: the user replied "cho phép chạy" to the explicit destination
question. Source transfer succeeded, remote tests and RTX5090 real-cache
preflight1049 PASS; training1050_1 was observed RUNNING. See
`vindr_a44_local_global_launch_20260922.md`. The account below records the
earlier block and no longer describes current deployment status.

Automatic approval review rejected transfer of source/scripts/configs/tests
to `tyler@atlas.jbnu.ac.kr:21233`, citing unestablished destination ownership
in trusted user content. Do not bypass this rejection. The proposed target is
`/slurmshared/Ngoc/code/hcmus-density-localglobal-20260922-v1`.
The remote directory and links to existing data/dependencies were created
before the transfer denial; A44 source was not deployed and no A44 job was
submitted. Prior training snapshots are unchanged.

Need user confirmation of this exact code-transfer destination. Once resolved:
deploy the tested files, run registered real-cache512 AMP preflight on RTX5090,
then submit fold1 for50 epochs with worker2/Vesta excluded. No claim of GPU
validation, training improvement, or completed research goal is made.

## Additional checkpoint replay validation prepared locally

`scripts/replay_density_checkpoint.py` reconstructs a completed50 run from
its immutable code snapshot and saved checkpoint, rereads the DEV cache,
and compares all IDs, labels, probabilities and recomputed metrics against
saved predictions. It verifies checkpoint SHA256 did not change. Probability
tolerances are rtol1e-5/atol1e-6; discrete predictions must match exactly.
Two local comparison tests PASS (row reordering allowed; duplicate IDs,
membership/label/probability corruption rejected).

Deployment to the separate
`/slurmshared/Ngoc/code/hcmus-density-multiscale-view-transformer-20260922-dev/scripts/`
directory was rejected by automatic approval review as outside the specifically
approved A44 destination. No replay was submitted; no snapshot was changed.
This is a supplementary validation block, not a training block: job1050_1
was independently verified RUNNING at15 completed epochs after the rejection.
Explicit approval for that additional code destination is needed to run it
as planned. Existing artifact audits remain valid within their documented
scope (saved predictions, not fresh image inference).
