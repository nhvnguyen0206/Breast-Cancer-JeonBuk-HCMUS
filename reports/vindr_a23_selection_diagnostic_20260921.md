# A23 first30 checkpoint-selection diagnostic

Read-only calculation from job955_0 log, restricted to epochs1--30.
The registered four-class Macro-F1 selection remains epoch4 (.6504998124).
Its BCD mean is .6451108610 and A F1 is .6666666667.

The highest diagnostic BCD mean within the same horizon is .7276517581 at
epoch10, with accuracy .8415841584, QWK .6489246144 and class F1
[0,.6744186047,.8998410175,.6086956522]. Its four-class Macro-F1 is only
.5457388186. Three of the first30 epochs have nonzero A F1.

Therefore, the earlier statement that sampling .35 makes the model learn
B/C/D poorly was too strong. The selected checkpoint has weak BCD, but the
model attains substantially better BCD at another epoch. Rare-A behavior
affects which checkpoint is selected. These observations do not establish
the causal effect of sampling or independent generalization.

Do not replace the registered selection rule or reported four-class metric
with this diagnostic. Continue the existing full50 screen and audit its
registered selection before any expansion.
