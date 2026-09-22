# A43 multi-scale four-view Transformer preflight

The registered A43 architecture passed a real cached-batch forward,
multitask-loss, backward, gradient-clipping and AdamW-update preflight on
`slurm-b40a-worker-1` with an NVIDIA GeForce RTX 5090. The batch came from the
frozen fold-2 fit manifest and had shape `[2,4,3,512,512]`.

- architecture: `convnext_tiny_multiscale_view_transformer_a_gate_v10`
- parameters: `29,906,793`
- finite loss: `1.6765291691`
- finite pre-clipping gradient norm: `20.9744777679`
- AMP skipped updates before recovery: `2`
- peak allocated GPU memory: `2.640089 GiB`
- strict checkpoint round-trip maximum output difference: `0.0`
- four-class probability sum: `1.0`
- complete remote unit suite: `44/44 PASS`
- result: **PASS**

An independent gradient-connectivity audit also confirmed finite, nonzero
gradients through both ConvNeXt feature stages, both scale projections, the
view/laterality/scale embeddings, exam token, A gate and conditional B/C/D
head. Runtime inspection confirmed that the instantiated model has no
`pair_fusion`, `side_gate` or `bilateral` module. Thus the arm is a real
fusion-interface replacement rather than an inactive auxiliary branch.

The first preflight submission (`1039`) did not reach model execution because
the worker's nonexistent default home directory prevented torchvision from
locating pretrained weights. Job `1040` set the same `TORCH_HOME` used by the
registered training launcher and passed. This was an environment-only repair;
no model, data or training setting changed.

A43 is cleared for the fixed fold-2/fold-3 weak-fold screen only.
