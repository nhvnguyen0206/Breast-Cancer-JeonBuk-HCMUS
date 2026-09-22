# A20 batch4 — first 30 epochs

Job943_0 remains healthy on RTX 5090. The selected checkpoint is unchanged at
epoch 13 with Macro-F1 `0.773328`, accuracy `0.816832`, QWK `0.612385` and
class F1 `1.000000 / 0.648649 / 0.881029 / 0.563636`. No epoch from 21–30
improved it; epoch 30 is `0.510812`.

A20 now trails A5's matched first-30/completed fold0 best (`0.789650`) by
`0.016321`. Only one of 30 checkpoints reaches `0.75`. Continue unchanged to
epoch 50 and complete the registered audit; no confirmation folds yet.
