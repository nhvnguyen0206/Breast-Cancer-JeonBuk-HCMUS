# A40 ConvNeXt-Tiny real-cache preflight

The registered A40 snapshot passed a real forward, multitask-loss, backward,
gradient-clipping and AdamW-update preflight on an NVIDIA GeForce RTX 5090.
The batch came from the frozen fold-1 fit manifest and had shape
`[2, 4, 3, 512, 512]`.

- architecture: `convnext_tiny_hierarchical_bilateral_multitask_v6`
- finite loss: 1.1935553551
- finite pre-clipping gradient norm: 15.1572332382
- AMP skipped updates before recovery: 2
- peak allocated GPU memory: 2.632205 GiB
- result: **PASS**

This establishes runtime compatibility only; it is not model-quality evidence.
A40 is cleared to run the fixed 50-epoch fold-1/fold-3 stress screen. Expansion
to folds 0/2/4 remains forbidden unless both completed audits PASS, the
two-fold mean Macro-F1 is >=0.70 and the minimum is >=0.65.
