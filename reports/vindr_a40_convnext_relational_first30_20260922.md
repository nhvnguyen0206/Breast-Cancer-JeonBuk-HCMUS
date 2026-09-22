# A40 ConvNeXt-Tiny two-fold screen: common first 30 epochs

Both job-1022 tasks remain healthy on the permitted RTX 5090 node. At the
matched first-30 horizon, neither selected checkpoint changes from first10.

| Fold | Best epoch <=30 | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---|---:|---:|---:|---:|---:|
| 1 | 4 | 0.8126870715 | 0.8560794045 | 0.6873629019 | 1.000000 / 0.655172 / 0.907051 / 0.688525 |
| 3 | 2 | 0.6822455124 | 0.8440594059 | 0.6206403148 | 0.666667 / 0.740741 / 0.904908 / 0.416667 |

The mean is **0.7474662919**, sample SD **0.0922361110**, and minimum
**0.6822455124**. The two numerical screen gates remain met. Epoch-30 scores
are 0.5497798434 and 0.5187137665, and no epoch after 4 has improved either
selection. Cumulative AMP skipped updates are 13 and 14; both trainings have
continued successfully after those skipped updates.

Continue unchanged to 50 epochs and completed audits. Do not expand or tune
from this intermediate result. The high two-fold dispersion and dependence on
very early checkpoints remain risks for final five-fold stability.
