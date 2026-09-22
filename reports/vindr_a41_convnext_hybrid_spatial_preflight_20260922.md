# A41 ConvNeXt hybrid-spatial real-cache preflight

Before model execution, the deployment check detected that the first copied
snapshot contained local `/scratch` paths. No model batch ran. The snapshot's
split directory was replaced byte-for-byte with the frozen A40 cluster
manifests, restoring assignment SHA256
`43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`;
a recursive comparison confirms the split directories are identical.

The corrected snapshot then passed a real forward, multitask-loss, backward,
gradient-clipping and AdamW-update preflight on an NVIDIA GeForce RTX 5090.
The batch came from the frozen fold-1 fit manifest and had shape
`[2,4,3,512,512]`.

- architecture: `convnext_tiny_hybrid_relational_spatial_multitask_v7`
- finite loss: 1.1766175032
- finite pre-clipping gradient norm: 16.8164176941
- AMP skipped updates before recovery: 2
- peak allocated GPU memory: 2.646593 GiB
- result: **PASS**

The failed packaging check is not a failed model attempt and produced no
training result. A41 is now cleared for only the fixed 50-epoch folds 1/3.
