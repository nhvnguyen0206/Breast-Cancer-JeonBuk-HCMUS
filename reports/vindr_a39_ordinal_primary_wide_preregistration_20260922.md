# A39 preregistration: corrected ordinal-primary threshold initialization

A39 is a conditional correction to A38 and must not launch before A38
completes/audits. A38 first-10 exposed a structural initialization defect:
unit-spaced cumulative thresholds make the maximum probability of either
interior class about 0.245, leaving B/C without a useful argmax region. The
observed confusion matrices consequently send most B/C cases to A/D.

A39 changes only initial threshold spacing from 1.0 to 2.0, yielding initial
thresholds `[-2, 0, 2]`. For equally spaced cumulative-logit thresholds, an
interior class beats its neighboring extreme only when the gap exceeds
`2*log(2) ~= 1.386`; spacing 2 satisfies this condition. A direct unit test
sets scalar scores to `[-5,-1,1,5]` and proves predicted argmax classes are
exactly A/B/C/D. All thresholds remain learned and strictly ordered.

Every other A38/A30 factor stays fixed: DenseNet121, hierarchical relational
fusion, data/cache/split, augmentation, sampling, loss weights, optimizer,
seed, heads and 50-epoch protocol. A39 remains one model and one inference
path, not an ensemble.

## Prepared snapshot

Prepared but not launched:
`/slurmshared/Ngoc/code/hcmus-density-relational-ordinalprimary-wide-20260922-v1`.
The snapshot passes 19/19 tests, including the four-class argmax-region test.
Strict checkpoint save/load is bit-exact. Matched-seed state and output hashes
prove A38's default unit-gap behavior is bit-exact after the extension.

- Trainable parameters: 11,159,687, identical to A38
- Config SHA256: `1f893e08aba4608e34af810a3cfcc0a859b5e699fd38ee9d95e190124334154e`
- Model SHA256: `aebd6cd8e8e3e6aa934812faf2198058a028e41daf74943d18f0b5acf7b1939c`
- Minimal engine SHA256: `777e9f3a3be24582eee0c38f067009b2a932702ca3260cbbdc025330d8199f36`
- Launcher SHA256: `dacaae0afe657135e845dc4f7a1fbcd917f09d2761ea892c99396308cb2cdefd`
- Frozen assignment SHA256:
  `43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a`

After A38 completed and failed its gates, the real cached-batch preflight
PASSed on `NVIDIA GeForce RTX 5090` with shape `[2,4,3,512,512]`. Forward,
multitask loss, backward, clipping and AdamW update were finite under AMP.
GradScaler recovered after two initial skipped updates; peak allocated memory
was 2.702 GiB. A39 is cleared for fixed folds 1 and 3 only under the existing
expansion gates.
