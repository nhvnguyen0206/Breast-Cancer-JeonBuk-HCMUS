# A20 CV5 confirmation — common epoch 10

All job944 confirmation folds reached epoch 10 without failure.

Using the same first-10 horizon for every fold, selected Macro-F1 values are
`[0.726423, 0.558851, 0.772299, 0.555345, 0.655784]`: mean `0.653740`, sample
SD `0.097505`, minimum `0.555345`. A5 at the same horizon is mean `0.605267`,
SD `0.109963`, minimum `0.532567`.

For the registered CV confirmation, fold0 remains its completed audited
checkpoint (`0.773328`); combining that fixed value with folds1–4 through
epoch 10 gives provisional mean `0.663122`, sample SD `0.107943`, minimum
`0.555345`. Folds1–4 are incomplete, so this is not the final CV5 result.
Continue all tasks unchanged to epoch 50; next review at common epoch 20.
