# A46 preregistration: exam-consistent feature MixStyle

Registered before implementation or training results. A45 improves B/C/D but
memorizes all five FIT A cases with near-unit confidence while assigning the
sole fold1 DEV A case P(A)=.000170. Direct mask/intensity statistics also place
that held-out A closer to B. The next hypothesis is that the ConvNeXt path
relies on acquisition/style statistics that fail to transfer to this atypical
A case.

## Controlled change

Retain A45's ConvNeXt-Tiny backbone, two-scale local/global four-view
Transformer, A-gate conditional B/C/D exam head, training-only per-view
auxiliary head and coefficient .25, all other losses, augmentation, sampling,
optimizer, seed and 50-epoch schedule.

Add training-only MixStyle immediately after the ConvNeXt fine stage. For
each exam and corresponding canonical views, normalize each channel by its
spatial mean/standard deviation, mix those statistics with a different exam
in the same batch, and restore the normalized content. Use one mixing
coefficient across all four views of an exam, Beta alpha .1, probability .5.
For batch size two, pair the two exams rather than permitting an identity
permutation. Evaluation/inference disables MixStyle exactly.

This is one hypothesis group: feature-statistics domain regularization. It
adds no trainable parameters, thresholds, test-time augmentation, averaging
or ensemble. The sole inference output remains the exam-level four-class
distribution.

## Protocol and gates

Use frozen VinDR cache/grouped split, seed42, fold1, assignment SHA256
43daa86936ee7b1bae1b200836fb1afdfe0c8294c7c865d8f5758bf989f12a9a.
Run 50 epochs on RTX5090 only, excluding worker2/Vesta, and log to W&B project
HCMUS-paper1 from a tested immutable snapshot after real-cache AMP preflight.

Expand only if completed fold1 audit PASSes and selected checkpoint meets all
three gates: Macro-F1 >= .72, B/C/D mean F1 >= .7133658737, and QWK >=
.6936709874. Report positive-A epoch count and longest streak as diagnostic;
they cannot replace the gates. If any gate fails, reject A46 without retuning
or expanding.

Final CV5 acceptance remains mean Macro-F1 >= .72, sample SD <= .03 and
minimum fold >= .65, with per-class F1/accuracy/QWK/confusion matrices and one
registered inference path. All screen/CV estimates remain selected DEV unless
a genuinely independent evaluation is introduced.

Status: preregistered; implementation and launch pending.
