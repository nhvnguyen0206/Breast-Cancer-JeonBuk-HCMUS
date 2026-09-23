# A53 local implementation validation

A53 implements the preregistered multi-scale A-gate replacement as
`convnext_tiny_hybrid_bcd_multiscale_a_gate_v20`.

One shared ConvNeXt backbone feeds both A42's hybrid exam representation and a
parallel A43-style multi-scale four-view Transformer. A42's existing `a_gate`
is applied exclusively to the multi-scale vector; conditional B/C/D, ordinal
and binary heads remain exclusively on the A42 vector. The model has one
normalized four-class output and is not an ensemble.

## Local validation

- syntax compilation PASS;
- focused A42/A47--A53 tests PASS 34/34;
- complete repository tests PASS 96/96;
- A42/A53 shared state and construction CPU RNG are bit-exact;
- under matched train-mode seeds, post-forward CPU RNG, ordinal logits and
  binary logits are bit-exact, while flat logits change intentionally through
  the replaced A-gate input;
- the conditional B/C/D distribution is unchanged at initialization;
- the A gate, fine/coarse projections and Transformer attention all receive
  finite non-zero gradient on the first update;
- strict state-dict roundtrip PASS;
- production 512x512 forward is finite with logits shaped 4/3/2;
- A42 parameters: 32,367,980; A53 parameters: 34,449,260; treatment adds
  2,081,280 parameters;
- semantic config delta from A42 is exactly arm identity, the registered
  replacement flag, and W&B online-to-offline mode.

## Local identities

- model: `89cef1e80187ff2422bc2895bf88799996f3efc1419c71c7736165e47a0a9a6f`
- engine: `9008682f04f10ad3348404c2f9dcac5d199ae2e0b70abc2002589ebd717b8224`
- screen auditor: `3c88206066b1ba1b3b12e8256c27816afdce8f3a765c4fdc77cb8b358a19e84e`
- CV5 auditor: `4523a508e4a2711afdd25f2ee9d062856ae843620cc1b4fdce20222a8fc52ba0`
- CUDA verifier: `5e7d2c59512593fba49de203d0aaff8f6870791931d6328a67e648f429c18ad5`
- config: `9b23cd6e7099839ad0b4cedb2e67c9b127c3c1d135d4ee1b40b62d612c7a18c2`
- tests: `3b5dcbac9d03a26d582e3945d9dc2094fc46e9ef894e5a527402bcf71d74f042`

Audited A52 rejection now unlocks Atlas deployment, CUDA parity and real-cache
RTX5090 preflight. Training remains locked until those checks pass.
