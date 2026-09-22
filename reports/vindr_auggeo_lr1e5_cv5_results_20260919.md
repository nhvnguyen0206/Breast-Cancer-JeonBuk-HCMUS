# A2: geometric augmentation + LR 1e-5 — completed CV5

All five runs completed 50 epochs, seed 42, unchanged grouped density split.
One change versus A1: learning rate 5e-5 → 1e-5. Architecture and single-checkpoint inference unchanged; no ensemble.

| Fold | Selected epoch | DEV Macro-F1 |
|---|---:|---:|
| 0 | 10 | 0.7927400468 |
| 1 | 4 | 0.5501173584 |
| 2 | 9 | 0.7032185181 |
| 3 | 27 | 0.6615987555 |
| 4 | 37 | 0.5987000034 |

Mean Macro-F1 **0.6612749364**, sample SD **0.0939601958**.
Mean accuracy 0.8319239368; QWK 0.6426477659.
Mean class F1 A/B/C/D: 0.5133333333, 0.6450817409, 0.8939865132, 0.5926981583.
Mean B/C/D F1 0.7105888042.
Epoch-50 mean Macro-F1 0.5185089841.

A2 is 1.87 percentage points below A1 (0.6799754745), despite fold-0 passing the screening gate.
B/C/D mean is slightly higher than A1 (0.7021895215), but the four-class target is not met.
Do not advance A2 to multi-seed confirmation as a successful candidate.

Audit PASS: exactly 50 epochs per fold; checkpoint/history selection; frozen assignment hash;
unique exact DEV IDs/labels; finite normalized probabilities and argmax; recomputed metrics;
all five W&B runs finished. Total 2017 cases, class support [6,196,1556,259].
Slurm confirms jobs 755_0 and 757_1–4 completed with exit 0; startup GPU logs identify RTX 5090,
with worker-2/Vesta excluded.

These are checkpoint-selected DEV results, not an independent test. Six A cases are insufficient
for a strong stability claim; no multi-seed validation or target success is claimed.
