# A16 backbone-LR 0.1x — fold-0 first 20 epochs

Job906_0 remains RUNNING on RTX5090. All scalar train losses are finite and
the backbone remains trainable for every epoch as registered.

A16 selected within epochs1--20: epoch20, Macro-F1 0.6647013473177328,
accuracy 0.8292079207920792, QWK 0.6636583011583012, class F1
[0.5, 0.6206896551724138, 0.8910569105691057, 0.6470588235294118], no
severe errors. Confusion matrix:
[[1,0,0,0],[2,27,11,0],[0,20,274,17],[0,0,19,33]].

Matched A5 first20 selected epoch20: Macro-F1 0.7654421854687274,
accuracy 0.7970297029702971, QWK 0.6126648582920213, class F1
[1.0, 0.6086956521739131, 0.8637873754152824, 0.5892857142857143]. Both
arms have 11 AMP-skipped updates.

A16 improves accuracy, QWK and every B/C/D class F1; its descriptive B/C/D
mean is 0.7196017964236438 versus 0.6872562472916365 for A5. However, A16
trails four-class Macro-F1 by 0.1007408381509946 because its correct single A
case has two false-A predictions, giving A F1 0.5 versus 1.0. This is not
evidence sufficient to override the registered four-class gate. Continue the
full50 unchanged; do not submit folds1--4. Next report at epoch30.
