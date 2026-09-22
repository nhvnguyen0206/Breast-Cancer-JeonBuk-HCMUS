# A38 preregistration: monotonic ordinal-primary head

A38 is a conditional successor to A37 and must not launch before A37 finishes
and passes its final audit. A36/A37 show that adding cross-view fusion capacity
does not recover the hardest fold. Across both, the flat four-class head often
assigns no case to class A. The next hypothesis is therefore that the output
parameterization, rather than fusion capacity, is the limiting factor.

A38 returns to the strongest audited A30 parent: ImageNet DenseNet121,
handcrafted hierarchical relational fusion, dropout 0.40 and sampling power
0.25. Cache, augmentation, losses and their weights, optimizer, seed and
50-epoch protocol are unchanged. It replaces the independent four-logit flat
primary head and auxiliary free-bias CORAL head with one shared scalar density
score and three strictly ordered learned thresholds. Ordered cumulative
probabilities are converted into a valid A/B/C/D distribution; that single
distribution is used for both focal/neighbor training and inference. Binary
remains auxiliary. This is one model and one inference path, not an ensemble.

The structural hypothesis is that an explicitly ordered primary output shares
statistical strength across adjacent density classes and cannot learn crossed
thresholds, which may help a six-case class A without inventing new samples.
The risk is underfitting class boundaries that are not well represented by a
single latent density axis.

## Prepared snapshot

Prepared but not launched:
`/slurmshared/Ngoc/code/hcmus-density-relational-ordinalprimary-20260922-v1`.
The isolated snapshot passes 18/18 tests. Tests verify strictly ordered logits,
positive normalized class probabilities, finite/nonzero gradients for score
and threshold parameters, invalid-configuration rejection, and the existing
pipeline. Strict checkpoint save/load is bit-exact. A matched-seed comparison
proves that the default A30 model's state and outputs remain bit-exact after
the source extension.

A38 has 11,159,687 trainable parameters versus A30's 11,163,787; the change
does not increase capacity.

- Config SHA256: `d220edd2cdd674adadce3dc07fcf40d55b7e3c3d150e4e803b9aa2079a4782ee`
- Model SHA256: `92f5b861023b5e84311d8a86f1cfdf07b2fbffd12b65d35ad00f9c12c401d358`
- Minimal engine SHA256: `d5cbf2ea2f4cfc135ffd1bf08ea3deb21860ae2b60cb46288b1cad0d9da39a2a`
- Launcher SHA256: `dacaae0afe657135e845dc4f7a1fbcd917f09d2761ea892c99396308cb2cdefd`
- Frozen assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

After A37 completed and failed its gates, the real cached-batch preflight
PASSed on `NVIDIA GeForce RTX 5090` with shape `[2,4,3,512,512]`. Forward,
multitask loss, backward, clipping and AdamW update were finite under AMP,
with zero skipped updates and 2.702 GiB peak allocated memory. A38 is cleared
for fixed folds 1 and 3 only. Expand only after both audits PASS, mean >=0.70
and minimum >=0.65.
