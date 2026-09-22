# Evidence note for the next major architecture family

This note prepares the next structural hypothesis without launching or tuning
another arm before A43 finishes. It is not a preregistration.

## Primary evidence

Published four-view mammography work supports separating within-view spatial
reasoning from between-view reasoning. Chen et al. first apply local
Transformer blocks inside each of four mammograms, then concatenate their
representations for global Transformer blocks; their four-view model
outperformed multi-view CNN references on their five-fold study:
https://arxiv.org/abs/2206.10096.

For breast-density classification specifically, LG-DPTNet combines adaptive
local/global pyramid features with cross-view Transformer fusion and an
imbalance-aware focal objective:
https://pubmed.ncbi.nlm.nih.gov/37827166/.

Li et al. report that different mammographic views have different density
classification capacities and that a multi-stream design improves over naive
single-view processing:
https://pubmed.ncbi.nlm.nih.gov/32012021/.

A broader 2025 comparison on mammography finds Transformer and graph
multi-view inductive biases have different strengths, while also warning that
exam-level supervision on modest datasets can be suboptimal:
https://pubmed.ncbi.nlm.nih.gov/39244796/. The paper recommends ensembles for
robustness, but ensembles remain explicitly excluded in this project; the
relevant lesson here is architectural inductive bias, not model averaging.

## Proposed family if A43 fails substantive B/C/D recovery

The next candidate should use a **hierarchical local-global four-view
Transformer**, not another scalar hyperparameter change:

1. retain two ConvNeXt feature scales for each view;
2. perform shared local attention inside each view to summarize regional
   density distribution before views interact;
3. add small learned CC/MLO and left/right adapters so view-specific capacity
   is available without four fully independent encoders;
4. fuse only four learned view summary tokens plus one exam token in a global
   cross-view Transformer;
5. keep one normalized exam-level four-class output and one inference path;
6. optionally use per-view auxiliary density heads during training only, with
   the exam head remaining the sole inference output.

This differs materially from A43, which places all 80 multi-scale regional
tokens into one global self-attention sequence immediately. The new inductive
bias protects within-view tissue structure before cross-view interaction and
may reduce the B/C/D degradation observed in A43's first-10 result.

No implementation or launch decision is authorized by this note. A43 must
reach full50 and pass audits first. If A43 passes its numerical screen but its
gain remains explained almost entirely by the rare A cases, the next arm must
be judged against both A43 Macro-F1 and A41 B/C/D/QWK, not Macro-F1 alone.
