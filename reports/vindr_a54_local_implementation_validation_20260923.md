# A54 local implementation validation

A54 implements the preregistered multi-task deep supervision architecture
`convnext_tiny_hybrid_bcd_multiscale_a_gate_deepsup_v21`. Its inference path
is A53: the multiscale exam supplies A-vs-rest and the hybrid A42 exam supplies
conditional B/C/D, ordinal and binary predictions. Only training adds
multiscale B/C/D, CORAL and binary heads at fixed objective weight `.5`.

Validation completed locally in the `paper_1` environment:

- syntax checks PASS for model, loss, engine, both auditors, CUDA verifier and
  A54 tests;
- focused A42/A47--A54 regression tests PASS `39/39`;
- the complete repository suite PASS `101/101`;
- A53/A54 shared state, construction RNG, training primary outputs and
  post-forward RNG are bit-exact before the auxiliary objective is added;
- evaluation returns only the three primary outputs, exactly matching A53;
- the auxiliary four-class distribution is normalized and all primary and
  auxiliary outputs are finite;
- the registered objective equals unchanged primary loss plus `.5` times the
  full auxiliary focal/neighbor/CORAL/binary loss;
- first-step gradients are finite and non-zero through the shared A gate,
  auxiliary B/C/D/CORAL/binary heads, fine/coarse projections and attention;
- strict state roundtrip PASS;
- production `1x4x3x512x512` CPU forward/backward is finite: total loss
  `3.8765199`, raw auxiliary objective `2.3840942`;
- A53 has `34,449,260` parameters and A54 `34,453,876`, a delta of only
  `4,616` parameters;
- the config delta is exactly the arm name, replacement flag to deep-
  supervision flag, and `loss.multiscale_auxiliary=.5`;
- both screen and CV5 auditors enforce architecture v21, mutual exclusion and
  the exact `.5` loss contract.

SHA256 receipts:

- model: `905394167b1cfe9f676fccda80e1ec914ab0fa1b6c2c69c16aed8754052b77af`;
- loss: `addbbf35d57fb6aae3fc96418e5ce8b99479835fbb93a9d36b7efadf465c2e6a`;
- engine: `7bf20bee25fd53db2efb91cc1387722225222ea7554046fe02adb1c6a83bf4f9`;
- screen auditor: `d7c81cc2d8c7ccf2a4a9a6c0bcd39582e5c3e6ff8138c17dd63161837a728fa1`;
- CV5 auditor: `4c1b4ea06752a02b7543f739deb16f166b9b182c9b9e5a38ef56b171c00b79d7`;
- CUDA verifier: `c1ada8abba377ff9851bb0f78a6fc322d703e9348e7e63f52f2d182d548e583c`;
- config: `69fb663c2015f1b85076025199fad7914deb969f05e8cc7f3875423d85d75680`;
- tests: `ec93d7911c80ac8af407bd2364b570d75e63f95972a0985020af7c86816e8c1f`.

Status: local implementation complete. Atlas deployment, CUDA parity,
real-cache preflight and training remain locked behind completed audited A53
rejection. No A54 performance result exists yet.

