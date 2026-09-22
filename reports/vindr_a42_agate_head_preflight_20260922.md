# A42 hierarchical A-gate real-cache preflight

The registered A42 snapshot passed a real forward, multitask-loss, backward,
gradient-clipping and AdamW-update preflight on NVIDIA GeForce RTX 5090. The
batch came from the frozen fold-1 fit manifest and had shape
`[2,4,3,512,512]`.

- architecture: `convnext_tiny_hybrid_spatial_a_gate_multitask_v8`
- finite loss: 1.8092241287
- finite pre-clipping gradient norm: 39.7901191711
- AMP skipped updates before recovery: 2
- peak allocated GPU memory: 2.646594 GiB
- result: **PASS**

The gradient norm is high but finite and is clipped by the registered training
path exactly as in the preflight. No configuration change is introduced. A42
is cleared for only the fixed 50-epoch folds 1/3.
