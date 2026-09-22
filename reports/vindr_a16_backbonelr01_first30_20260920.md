# A16 backbone-LR 0.1x — fold-0 first 30 epochs

Job906_0 remains RUNNING on RTX5090. All scalar train losses are finite and
the backbone remains trainable for every epoch as registered.

A16 selected within epochs1--30 remains epoch20: Macro-F1
0.6647013473177328, accuracy 0.8292079207920792, QWK
0.6636583011583012, class F1 [0.5, 0.6206896551724138,
0.8910569105691057, 0.6470588235294118], no severe errors. Epoch30 Macro-F1
is 0.5869457893858427.

Matched A5 first30 selected epoch30: Macro-F1 0.7896498561536562,
accuracy 0.8267326732673267, QWK 0.6486083499005965, class F1
[1.0, 0.6419753086419753, 0.8859934853420195, 0.6306306306306306].
A16/A5 AMP-skipped updates are 14/12.

A16 trails A5 by 0.1249485088359233 four-class Macro-F1. Their selected
descriptive B/C/D means are effectively identical (0.7196017964236438 versus
0.7195331415382085); A16's apparent advantage at epoch20 does not persist
against A5's best available by epoch30. A16 remains below the 0.75 gate.
Continue the registered full50 unchanged; do not submit folds1--4. Next report
at epoch40.
