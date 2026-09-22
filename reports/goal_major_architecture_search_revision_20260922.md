# Active goal revision: major architecture redesign is allowed

Effective 2026-09-22, the project is no longer limited to small repairs or to
preserving DenseNet121 plus the original handcrafted hierarchical fusion.
The active goal is to find a materially stronger **single-model** architecture
for four-view breast-density classification. Large structural changes are not
only allowed: they are now the default direction when the current model family
cannot satisfy the stability gates. The research is no longer constrained to
DenseNet121, the original handcrafted hierarchical fusion, or the existing
multi-task heads.

The target is not a cosmetic increase in the mean. The new model must reduce
the failure of the weakest folds while preserving performance on the stronger
folds. A higher mean with one collapsed fold is explicitly not success.

## Success criteria

Updated 2026-09-22 from the latest active goal: final mean threshold is now
0.72 and sample SD threshold is 0.03. Earlier reports and running-arm
preregistrations retain their historical thresholds; they are not retroactively
rewritten. Final acceptance uses the new stricter thresholds. The user's
explicit authorization for major architecture changes remains recorded above.

The final claim requires one audited five-fold run with:

- mean four-class Macro-F1 >= 0.72;
- sample standard deviation across folds <= 0.03;
- minimum fold Macro-F1 >= 0.65;
- class-wise F1, accuracy, QWK and confusion matrices reported;
- one model and one registered inference path, with no ensemble.

The research stretch target remains mean Macro-F1 near 0.75, but it must not
be obtained by sacrificing fold stability or by selecting favorable folds.

## Fixed experimental invariants

- Keep the frozen grouped VinDR split, assignment SHA256, cache population,
  seed 42, four-view input and metric definitions unchanged.
- Use RTX 5090 only; never use Vesta/worker2.
- Log to W&B project `HCMUS-paper1` and retain reproducible snapshots,
  checkpoints, predictions and provenance audits.
- Treat all reported selection results as DEV results, not an independent
  test estimate.
- Do not infer robust class-A performance from the six class-A cases alone.

## Architecture search policy

Minor hyperparameter tuning is no longer the default next step. When a model
family has failed to repair the current weak-fold screen, move to a
structurally different hypothesis. Permitted changes include:

- replacing DenseNet121 with a modern convolutional or transformer backbone;
- retaining spatial feature maps and replacing global-average-pooled vectors
  with regional/token-level aggregation;
- replacing handcrafted absolute-difference/product fusion with learned
  cross-view attention or another view-aware fusion module;
- partially unsharing encoders or adding CC/MLO and left/right adapters;
- replacing the flat primary classifier with an ordinal, hierarchical or
  distributional head;
- jointly redesigning backbone, fusion and head when single-component
  ablations show that the original interface itself is the bottleneck.

The last item explicitly permits a full model redesign. This includes changing
the complete encoder--fusion--head interface, the optimization objective and
the way the four views interact. Such a redesign must still have a written
hypothesis and a matched comparison against the strongest audited reference.
It does not need to preserve any original internal block.

Candidate families are prioritized by how directly they address the observed
failure mode:

1. learned four-view token fusion with explicit view/side embeddings and
   missing-view masks;
2. hierarchical or ordinal density prediction whose probabilities remain a
   single normalized four-class output;
3. multi-scale spatial fusion so that global breast composition and local
   dense tissue patterns are both retained;
4. view-specific adapters or partially unshared CC/MLO encoders when shared
   features cause negative transfer;
5. stronger pretrained backbones, including ConvNeXt and mammography/domain-
   adapted encoders, with a controlled fine-tuning schedule;
6. if isolated changes fail, a full end-to-end redesign combining the best
   encoder, fusion and head hypotheses in one ablated model.

No ensemble, fold-specific model, fold-specific threshold or test-time model
selection is permitted. Large changes must improve one deployable inference
path rather than hide instability behind averaging multiple models.

## Decision protocol

For new candidates after A43, the latest active goal requests one screening
fold before CV5. Screen the weakest fold of the latest audited CV5 (A43
fold1), for50 epochs. Require audited selected-DEV Macro-F1 >=0.72 and
preserved B/C/D and QWK against the matched reference before expansion.
The two-fold procedure below records the historical A41--A43 registration;
it does not override this updated one-fold screening rule. Final CV5 gates
remain mean>=0.72, sample SD<=0.03 and minimum>=0.65.

1. Use A41 as the strongest mean reference and A30 as the stability reference;
   retain completed arms as negative evidence and do not repeat exhausted
   scalar-loss/dropout/learning-rate tweaks.
2. Determine the two weakest folds from the latest completed, audited CV5 run.
   For A41 these are fold 2 (`0.5583275`) and fold 3 (`0.7170961`). New major
   candidates after the already-running A42 screen must therefore be screened
   on folds 2 and 3, not on historically chosen folds 1 and 3.
3. Run a candidate for the registered 50 epochs on both weak folds and audit
   provenance, checkpoint selection and prediction reconstruction.
4. Expand to the remaining three folds only when both weak-fold audits PASS,
   the two-fold mean is >= 0.70, neither fold is below 0.65, and the gain is
   not explained only by the six rare class-A cases.
5. Reject a model family after a preregistered substantive architecture test
   fails the weak-fold gates. Diagnose the failure, then change the relevant
   representation/fusion/head family instead of accumulating small unrelated
   repairs.
6. Report checkpoints every 10--20 epochs or at completion; continuous epoch
   narration is not required.

## Milestones

- **M1 -- Weak-fold recovery:** fold 2 >= 0.65 and the fold-2/fold-3 mean >=
  0.70 on an audited two-fold screen.
- **M2 -- Stable CV5:** mean >= 0.72, sample SD <= 0.03 and minimum fold >=
  0.65 on one audited five-fold run.
- **M3 -- Stretch:** approach or exceed mean 0.75 without breaking M2.
- **M4 -- Scientific handoff:** document ablations, class-wise metrics,
  confusion matrices, W&B runs, immutable config/code hashes and limitations.

## Immediate direction

A41 already demonstrates that a major ConvNeXt plus hybrid spatial/view-token
change can reach CV5 mean `0.7523091`, but it is rejected because SD is
`0.1187419` and fold 2 is only `0.5583275`. A42 isolates a differentiable
A-vs-rest hierarchical gate on top of A41 and may finish as a registered
diagnostic control; it is not a reason to postpone the broader redesign.

If A42 does not recover the weak-fold gates, the next arm must change the
fusion/interface substantially: explicit view/side tokens, multi-scale spatial
features and learned cross-view attention, screened first on folds 2 and 3.
If that fails, test partial encoder unsharing or view-specific adapters. A new
loss-only or dropout-only arm is out of scope unless an ablation provides
specific evidence that it is necessary inside a successful new architecture.
