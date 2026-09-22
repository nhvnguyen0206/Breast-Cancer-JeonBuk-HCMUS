# A45 fold1 launch after real-cache preflight

The user granted authorization to deploy and run A45 on Atlas. The tested
source was copied to the new immutable snapshot:

/slurmshared/Ngoc/code/hcmus-density-localglobal-perviewaux-20260922-v1

Five critical source/config/test hashes match local validation, the ten
focused A44/A45 tests PASS remotely, and the frozen grouped split assignment
SHA256 is:

43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a

Preflight job 1051 failed in the launcher before loading model/data because
the newly added generic launcher contained literal escape characters in
three shell parameter expansions. It is invalid evidence and was not reused.
The launcher was corrected, passed local and remote shell syntax checks, and
has SHA256:

45b34cc70af9deef20d70d49ccb299dceb9416c8cf5ea9c2fb87db22547e57e4

Replacement real-cache AMP preflight job 1052 PASS on NVIDIA GeForce RTX
5090 with architecture
convnext_tiny_local_global_view_transformer_perview_aux_v12:

- Batch shape: [2,4,3,512,512], labels [2,2].
- Loss: 1.5845574141; view auxiliary loss: 0.0546375997.
- Gradient norm before clipping: 22.9666137695.
- AMP skipped two overflowing updates before a successful finite update.
- Peak allocated memory: 2.6990032196 GiB.
- Log: /slurmshared/Ngoc/logs/hcmus-density-preflight-1052.log.

The snapshot was then hash-manifested and made read-only. Training job
1053_1 was observed RUNNING on slurm-b20a-master-0 with NVIDIA GeForce RTX
5090. It uses fold1 only, seed42, 50/min50 epochs, the registered A45
configuration, and excludes slurm-b40a-worker-2/Vesta.

- Output: /slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1053-fold1
- Log: /slurmshared/Ngoc/logs/hcmus-density-cv5-1053_1.log
- W&B: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/1k59zmph

This is launch evidence, not a model-quality result. Do not expand beyond
fold1 until all 50 epochs complete, the audit passes, and every preregistered
screen gate passes. Report training quality only at 10--20 epoch intervals.
