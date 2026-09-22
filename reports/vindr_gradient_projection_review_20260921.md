# Gradient projection review

A6 shared-fusion diagnostic has64 batches, class draws [1,20,84,23].
Exclude gradients with either norm<=1e-6 before interpreting cosine;
45 batches remain for each auxiliary component.

|Component|Negative count|Sum negative projection|Sum positive projection|
|---|---:|---:|---:|
|Ordinal|6|-.04577560|1.15844765|
|Binary|14|-.00696125|1.06278409|
|Neighbor|1|-.06297139|8.35719664|

Projection is auxiliary gradient norm times cosine to focal, at the final
bilateral linear weight. Despite more negative binary cosines, their total
magnitude is small relative to positive projections. No evidence here that
binary conflict dominates. Do not select a loss reduction based on counts alone.
These projections are not optimizer updates or causal generalization evidence.

Ran the same64-batch diagnostic on A5 original770-fold0 best checkpoint;
raw results in vindr_a5_shared_fusion_gradient_20260921.json. This is a
reference, not a matched-batch causal comparison: A5 uses natural sampling,
A6 replacement sampling, and selected checkpoint epochs differ.
No training/model/checkpoint changes and no new50-epoch arm launched.
