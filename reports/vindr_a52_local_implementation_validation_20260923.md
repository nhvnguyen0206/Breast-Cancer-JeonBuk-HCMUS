# A52 local implementation validation

A52 implements the preregistered multi-scale rare-A expert as architecture
`convnext_tiny_hybrid_spatial_a_gate_multiscale_a_expert_v19`.

The complete A42 hybrid relational/spatial path remains responsible for the
base A gate, conditional B/C/D, ordinal and binary outputs. A parallel A43-style
multi-scale four-view Transformer sees 384/768-channel feature maps and adds
one zero-initialized residual only to the A-vs-rest logit. It is one end-to-end
model and produces one normalized four-class distribution.

## Local validation

- syntax compilation PASS;
- focused A42/A47/A48/A49/A50/A51/A52 tests PASS 30/30;
- complete repository tests PASS 92/92;
- A42/A52 shared state, construction CPU RNG, initial train outputs and
  post-forward CPU RNG are bit-exact under matched seeds;
- the zero-initialized A-expert head receives finite non-zero gradient on the
  first update; fine/coarse projections and Transformer attention receive
  finite non-zero gradient after that update;
- changing the expert residual changes A probability while preserving the
  conditional B/C/D distribution and leaving ordinal/binary logits exact;
- strict state-dict roundtrip PASS;
- production 512x512 forward is finite with logits shaped 4/3/2;
- A42 parameters: 32,367,980; A52 parameters: 34,450,029; treatment adds
  2,082,049 parameters;
- semantic config delta from A42 is exactly arm identity, the registered
  `multiscale_a_expert: true` flag, and W&B online-to-offline mode.

## Local identities

- model: `3bf9a31d478a9623ca81c27afacfc0fdcab209089b65ced86abbb5387d87b83d`
- engine: `5cc618b75cbd4aa3030868dfca41dc9052fc25864e1f23daa8cb17dee45ee59a`
- screen auditor: `5b309f1e20bf352fd871d8431626ac7431a32995a944c3c99a161b46964ca80a`
- CV5 auditor: `6793cfb6db70ba3477282df96892fee139c284061bf14865919d6f762a57e775`
- CUDA verifier: `c57d79deb86d8be252a5d5de663be7e36f1349f382eacecdccdb7a720dd7474d`
- config: `2d52bd67d9eb5c99ce35b02a6db96c1d91c37414c9ee55cce351371a823e5a14`
- tests: `0a8dc1c9965c9ef7603ea721189fcdfd1b9ed9259792a3e27f4cd0ab718cfa34`

Audited A51 rejection now unlocks Atlas deployment, CUDA parity and real-cache
RTX5090 preflight. Training remains locked until those checks pass.
