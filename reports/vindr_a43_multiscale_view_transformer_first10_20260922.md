# A43 multi-scale four-view Transformer — common first 10 epochs

Both job-1041 tasks remain RUNNING on worker1 RTX 5090 and completed epoch 10.
The tested common-horizon tool selected DEV Macro-F1 independently within
epochs 1--10 on the current weak folds 2 and 3.

| Fold | Selected epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 2 | 7 | 0.799443 | 0.836228 | 0.668040 | 1.0000 / 0.7158 / 0.8925 / 0.5895 |
| 3 | 7 | 0.678563 | 0.806931 | 0.611126 | 0.6667 / 0.6882 / 0.8752 / 0.4842 |

The two-fold mean is `0.7390029`, sample SD `0.0854750`, and minimum
`0.6785630`. A43 provisionally passes its registered expansion screen's mean
>= `0.70` and minimum >= `0.65` at this early horizon. It is the first
ConvNeXt arm to recover the fold-2 A case and raises fold 2 far above A41's
`0.5583275`.

The improvement is not yet sufficient scientific evidence. Fold-2 B/C/D mean
is `0.7325904`, slightly below A41's `0.7444367`; fold-3 B/C/D mean is
`0.6825284`, below A41's `0.7339060`. Across the two folds, A43 B/C/D mean is
`0.7075594` versus A41 `0.7391713`. Thus most of the Macro-F1 gain comes from
recovering the rare A decision, while D and QWK regress, particularly on fold
3. The two-fold SD also remains above the final CV5 stability target.

Continue unchanged through epoch 20 and the registered full 50 epochs. Do not
expand early. A43 must show that later selection preserves fold-2 recovery
while improving substantive B/C/D performance and must pass both final audits.
