# A51 local implementation validation

A51 implements the preregistered orientation-aligned bilateral spatial
relation as architecture
`convnext_tiny_hybrid_spatial_a_gate_bilateral_relation_v18`.

The treatment preserves A42 and adds a parallel residual at the final
768-channel map stage. Right maps are horizontally flipped; same-projection
left/right maps form symmetric mean, absolute-difference and product maps. A
shared 2304-to-256 spatial block processes CC/MLO relations, and a
zero-initialized projection returns the concatenated summaries to the
768-dimensional exam feature. Inference still uses one model and one output.

## Local validation

- syntax compilation PASS;
- focused A42/A47/A48/A49/A50/A51 tests PASS 25/25;
- complete repository tests PASS 87/87;
- A42/A51 shared state, construction CPU RNG, initial train outputs and
  post-forward CPU RNG are bit-exact under matched seeds;
- side-swap symmetry after orientation normalization agrees within `1e-6`;
- output projection gets a finite non-zero first-step gradient; shared 1x1 and
  depthwise spatial paths get finite non-zero gradients after its first update;
- strict state-dict roundtrip PASS;
- production config 512x512 forward is finite with logits shaped 4/3/2;
- A42 parameters: 32,367,980; A51 parameters: 33,355,628; treatment adds
  987,648 parameters;
- A51 config differs from A42 only in arm identity, the registered bilateral
  flags and offline W&B mode.

## Local identities

- model: `09d0aeda6fad70fcb1a1cb42b5120c2f9830f4fcb605d5cb4081ced4fe77f0d2`
- engine: `dce9461585e40abcfb687259cfceca40be63a328fe31ccc97895dddf231feea2`
- screen auditor: `067dd5c4ed3db87a1f4568f76719d9d11419b5e2ebf1ef41da1ecb016a10e783`
- CV5 auditor: `1961e49d3abd8afcc73af4f6d14a623650ca600478097e5d80539afa19bc03f6`
- CUDA verifier: `a0c02c1525b2a463c3d54c048152f127e7844aaa854abef71d831c5be5d1aaac`
- config: `fdce2e8ef6129cc98babd3d541b9ea4b05194e89c095fd34d66f639e7215ec36`
- tests: `ee24429909476c3e7260237b83282f1fd661d184dac00ed0dfb125215403ea90`

Atlas deployment, CUDA parity, real-cache preflight and training remain locked
until the user explicitly authorizes sending this source/test/config/report
payload to the named Atlas snapshot path.
