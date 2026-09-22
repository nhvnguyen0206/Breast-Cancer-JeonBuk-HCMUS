# Goal revision: allow substantive architecture changes

> Superseded on 2026-09-22 by
> `goal_major_architecture_search_revision_20260922.md`. The evaluation
> invariants and two-fold screening rules below remain active, but the newer
> revision removes the conservative, sequential architecture roadmap.

This revision supersedes the earlier constraint that the model must remain
close to the existing DenseNet121 plus handcrafted hierarchical relational
fusion. The research objective is now to reach an audited five-fold
four-class Macro-F1 mean >=0.70, sample SD <=0.05, and minimum fold >=0.65.
Substantive architecture changes are explicitly allowed when supported by a
clear hypothesis and controlled comparison.

## Invariants

- Keep the frozen grouped VinDR split, assignments SHA256, cache population,
  seed 42, four-view input, and evaluation definitions unchanged.
- Use RTX 5090 only; never use worker2/Vesta.
- Do not use an ensemble to meet the target. One trained model and one
  registered inference path must produce each result.
- Continue reporting selected DEV rather than independent-test performance.
- Keep full provenance, checkpoint/prediction audit, and W&B project
  `HCMUS-paper1`.
- Do not claim success from the six class-A cases alone.

## Experimental policy

Large changes may include replacing the handcrafted feature fusion, adding
view/laterality-aware attention, introducing view-specific adapters or
partially unshared encoders, changing the classifier to an ordinal-aware or
hierarchical head, and replacing the ImageNet backbone when justified.

Even for major changes, each arm must isolate one architectural hypothesis.
Do not simultaneously change the backbone, fusion, losses and data pipeline;
otherwise attribution is impossible. Compare every architecture against the
strongest audited A30 reference under identical data, optimizer and loss
settings unless the tested architecture strictly requires a documented
change.

Use the fixed two-fold stress screen on folds 1 and 3 for 50 epochs. Expand to
folds 0, 2 and 4 only when both audits PASS, their mean Macro-F1 is >=0.70,
and neither fold is below 0.65. Preserve screen runs during expansion. Final
success still requires all three audited CV5 gates.

## Architecture roadmap

1. Finish A35, the already-running loss-direction control, without altering
   it. This closes the scalar-loss question.
2. If A35 fails, prioritize a new view-token attention fusion arm: retain the
   pretrained DenseNet121 feature extractor initially, but replace fixed
   gate/absolute-difference/product pair and bilateral fusion with a
   learnable attention block over the four view vectors. Add explicit CC/MLO
   and left/right embeddings. Keep the existing loss and optimizer fixed.
3. If attention fusion fails, test partial encoder specialization through
   small CC/MLO and left/right adapters while retaining a shared DenseNet
   trunk. This tests view heterogeneity without immediately quadrupling the
   backbone parameter count.
4. Then test an ordinal-aware/hierarchical primary prediction head instead of
   the flat four-class head, still using a single inference output.
5. Consider a different pretrained backbone only after fusion and head
   hypotheses have been isolated. A backbone change must not be bundled with
   a fusion redesign.

The roadmap is conditional, not a commitment to run every item. Evidence at
each two-fold screen determines the next action. Architecture size, memory,
parameter count and inference behavior must be documented alongside metrics.
