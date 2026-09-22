# A42 preregistration: hierarchical A-gate primary head

## Evidence and hypothesis

A41 reaches audited CV5 mean Macro-F1 0.7523091061 and strong mean B/C/D F1,
but fails stability because fold 2 scores 0.5583275293. Across all 50 fold-2
epochs, both ConvNeXt arms A40 and A41 have class-A F1 exactly zero. In
contrast, A30 DenseNet has positive fold-2 A F1 in 47/50 epochs. A41 fold-2
B/C/D mean F1 is already 0.7444367057. The remaining failure is therefore
localized to loss of the rare-A decision region, not a general representation
failure.

A42 retains A41's complete ConvNeXt hybrid relational-spatial representation
and changes only the primary four-class head. It tests whether explicitly
factorizing the rare A boundary can restore that decision region without
damaging B/C/D.

## Registered change

The flat `Linear(768,4)` primary head becomes one differentiable hierarchical
distribution:

- `a_gate`: A versus not-A;
- `bcd_head`: conditional B/C/D distribution;
- `P(A)=sigmoid(a_gate)`;
- `P(B/C/D)=(1-P(A))*softmax(bcd_head)`.

The four probabilities sum to one and are returned as log-probabilities to the
same class-balanced focal and neighbor objectives. There is no hard routing,
separate model, ensemble or post-hoc threshold. The CORAL and binary auxiliary
heads are unchanged. Total parameters remain **32,367,980**, exactly the A41
count because the factorized output layers contain the same number of weights
as `Linear(768,4)`.

## Fixed protocol

Cache, four-view order, resize, augmentation, ConvNeXt backbone, hybrid
fusion, residual initialization, losses and weights, sampling power,
optimizer, seed 42, grouped split, assignment SHA256 and 50-epoch contract are
unchanged. Use RTX 5090 only and never worker2/Vesta.

## Verification

- 40/40 repository tests PASS.
- Tests prove normalized probabilities, valid A/B/C/D argmax regions and
  finite nonzero gradients through A gate, B/C/D head and spatial branch.
- Strict state-dict roundtrip reproduces every output bit-for-bit.
- The unchanged A41 flat path is matched-seed bit-exact across snapshots:
  state SHA256 `b07b98e34d459f3bec0bfb3d645566c08bc22e249aca2465c93aed6940f32d60`
  and output SHA256
  `93690f87a495baafb69cc97f65b8d16efeaec0153b278531c96d066a1cf8bbd3`.

Architecture ID: `convnext_tiny_hybrid_spatial_a_gate_multitask_v8`.
Snapshot:
`/slurmshared/Ngoc/code/hcmus-density-convnext-hybrid-agate-20260922-v1`.

Relevant SHA256 values:

- config: `aa6703d857572f53464c910747759fd1e42e144477756ad7903b481054299dc2`
- model: `9d588c41e89241e1687cfd04f54c67245dcbf90516fb8e2136e4e4c801951efb`
- engine: `1ef1210280ba51d83c90535c28abb8f03297bf859eb5e444b172ddeff2cb5d7c`
- launcher: `01e5c7689f4ba0fed29ca0ebfffee6b47f7619c394d8f80dea8d81212107ea06`
- assignments: `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

## Execution rule

Require a real cached 512-pixel RTX 5090 forward/backward/update preflight.
If it passes, run the fixed folds 1 and 3 for 50 epochs. Expand only after both
audits PASS, mean >=0.70 and minimum >=0.65. Final acceptance requires audited
CV5 mean >=0.70, sample SD <=0.05 and minimum >=0.65.
