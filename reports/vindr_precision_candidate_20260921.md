# Candidate after A23: isolate training precision

Status: diagnostic candidate only; not registered or submitted. Await A23
completion and audit before selecting the next experiment.

Evidence reviewed in the existing campaign:

- A5 has sparse AMP skipped updates in every fold (16/18/16/17/15).
- A18 encountered NaN forward outputs under FP16 on a finite batch and finite
  parameters; the same saved state/input produced finite FP32 loss.
- A18 also freezes BatchNorm statistics, so that failure does not demonstrate
  a corresponding forward failure in ordinary A5 or A23.
- The current engine uses default CUDA autocast (FP16), GradScaler and
  unscaled gradient clipping at5. Scalar loss finiteness alone cannot prove
  finite gradients or that every optimizer update ran.

A controlled numerical question is A5 with only training.amp=false. This
retains architecture, losses, sampling, augmentation, optimizer, batch size,
seed and inference. It does not combine precision with BN freezing. Direct
parent would be A5, not A18. Full FP32 may take longer and use more GPU memory;
a real batch2/512 forward-backward preflight on RTX5090 is needed first.

Hypothesis: eliminating FP16 overflow/skipped updates may alter optimization
and rare-class stability. The sparse skip counts do not establish them as
the cause of fold dispersion, and no F1 improvement is predicted as certain.
Use the existing fixed fold0 full50 screen and >=.75 audited expansion gate
if this candidate is selected. Final acceptance remains mean>=.70, SD<=.05,
minimum>=.65 on all five fixed folds.

## Feasibility preflight

Ran one real fold0 FIT batch using the immutable A5 snapshot on an allocated
RTX5090 on worker1 (worker2 excluded). Fresh ImageNet model, batch shape
[2,4,3,512,512], training augmentation, FP32 forward/backward, clip5 and AdamW
update completed. Loss1.4965289831, pre-clip gradient norm20.7384376526;
parameters remained finite. Peak allocated GPU memory5.1951GiB; timed
forward/backward/update0.6736s (single batch, not a throughput estimate).
No checkpoint, W&B run or full training experiment was created. This proves
one-batch feasibility only, not full-run numerical stability or F1 benefit.
