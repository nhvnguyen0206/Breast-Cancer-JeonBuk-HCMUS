# A43 preregistration: multi-scale learned four-view Transformer

## Hypothesis

A41 reaches CV5 mean Macro-F1 `0.7523091` but fails stability because fold 2
is only `0.5583275`. Its spatial Transformer is merely a small residual on top
of the original globally pooled handcrafted ipsilateral/bilateral fusion. A43
tests whether that interface is the bottleneck by replacing it completely.

## Structural change

A43 keeps the ConvNeXt-Tiny image encoder but extracts two feature-map scales:
the 384-channel intermediate stage and 768-channel final stage. It creates
spatial tokens from every one of the four canonical views at both scales,
adds learned CC/MLO, left/right, scale and spatial embeddings, and jointly
fuses all tokens with a Transformer exam token. It has no `PairFusion`, no
absolute-difference/product relation and no bilateral side gate.

The normalized A-vs-rest plus conditional B/C/D head from A42 is retained so
that the architectural comparison from A42 to A43 isolates the replacement of
the representation/fusion interface. The output remains one differentiable,
normalized four-class distribution and one deployable inference path.

Registered architecture:
`convnext_tiny_multiscale_view_transformer_a_gate_v10`.

## Frozen factors

- frozen VinDR four-view cache and grouped five-fold assignment SHA256
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`;
- seed 42, 512x512 stretch input, augmentations, sampling power, losses,
  optimizer settings and full 50-epoch selection contract from A42;
- single model, no ensemble, no fold-specific threshold and no post-hoc
  calibration;
- RTX 5090 only, never Vesta/worker2; W&B project `HCMUS-paper1`.

## Gate and execution order

A43 is code-complete but must not launch before a real-cache RTX 5090
forward/loss/backward/update preflight passes. Under the revised goal, its
screen folds are the two weakest folds from the latest audited CV5: fold 2 and
fold 3. Run both for all 50 epochs and audit both. Expand to folds 0/1/4 only
if the two-fold mean is at least `0.70`, neither fold is below `0.65`, and the
improvement is not attributable only to the rare class-A observations.

A42 was already launched on folds 1/3 under the preceding protocol and will
finish as registered; A43 does not reuse or reinterpret those screen results.
