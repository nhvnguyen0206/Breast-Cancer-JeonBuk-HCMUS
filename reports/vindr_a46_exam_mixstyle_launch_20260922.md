# A46 fold1 launch after real-cache preflight

The user granted full authorization for the registered A46 Atlas experiment.
The exact locally tested files were deployed to the new snapshot
`/slurmshared/Ngoc/code/hcmus-density-localglobal-perviewaux-mixstyle-20260922-v1`.
Remote SHA256 values match the local implementation report and the 16 focused
A44--A46 tests PASS in the deployed environment. The snapshot was then made
read-only.

RTX5090 preflight job 1056 PASSed on `slurm-b20a-master-0` with architecture
`convnext_tiny_local_global_view_transformer_perview_aux_mixstyle_v13`. A real
cached batch `[2,4,3,512,512]` completed AMP forward, backward and optimizer
update after two normal GradScaler recovery skips. Peak allocated GPU memory
was 2.6990 GiB. The allocation reported NVIDIA GeForce RTX 5090; worker2/Vesta
was excluded by the registered launcher.

Fold1-only full50 job 1057_1 was then submitted and observed RUNNING on
`slurm-b20a-master-0`, again reporting NVIDIA GeForce RTX 5090. It uses frozen
assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`,
seed42, the window16 cache, A46's registered config and output directory
`/slurmshared/Ngoc/runs/hcmus-density-cv5-v1-1057-fold1`.

W&B run: https://wandb.ai/TN_Mammo_BreastDensity/HCMUS-paper1/runs/2rzbst10

No other fold is running. Expansion remains conditional on the completed
50-epoch audit and all preregistered Macro-F1, B/C/D and QWK gates.
