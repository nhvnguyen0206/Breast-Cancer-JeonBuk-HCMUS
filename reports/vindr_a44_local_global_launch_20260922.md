# A44 fold1 launch after real-cache preflight

The user explicitly approved running after the exact Atlas source-transfer
destination was requested. Transfer subsequently succeeded. Source hashes
match the locally validated A44 files, and all four A44 tests also PASS in
the Atlas environment. Do not mutate the deployed training snapshot.

Snapshot: `/slurmshared/Ngoc/code/hcmus-density-localglobal-20260922-v1`.
Config: `configs/vindr_density_convnext_local_global_a_gate.yaml`.
Architecture: `convnext_tiny_local_global_view_transformer_a_gate_v11`.

Real-cache AMP preflight job1049 PASS on NVIDIA GeForce RTX5090:
- FIT fold1, batch [2,4,3,512,512], labels [2,2].
- Loss1.2283797264, gradient norm12.0918846130 before clipping.
- Zero skipped updates; peak allocated memory2.6521182060 GiB.
- Log: `/slurmshared/Ngoc/logs/hcmus-a44-preflight-1049.log`.

Training job1050_1 observed RUNNING on `slurm-b20a-master-0`; startup log
verifies RTX5090, seed42, 50/min50 epochs and frozen assignment SHA256
43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.
The node allowlist is master/worker1/worker3; worker2/Vesta is excluded.
Output: `/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1050-fold1`.
Log: `/slurmshared/Ngoc/logs/hcmus-density-cv5-1050_1.log`.
W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2031sdoy

This is startup/preflight evidence, not a model-quality result. Report at
10--20 epoch intervals or completion. Finish50 and audit before applying the
registered screen gates or expanding to the remaining four folds. Final goal
remains CV5 mean>=.72, sample SD<=.03 and minimum>=.65, single model/seed42.

Early health verification: scheduler1050_1 and W&B2031sdoy both RUNNING,
two completed epochs synchronized, finite latest training loss. No model
quality milestone is reported before10 epochs. Local horizon-summary tool
now defaults to explicit .72/.03/.65 thresholds (three tests PASS) and can
reproduce historical thresholds via CLI flags. The deployed A44 snapshot
was not altered by this reporting-tool update.
