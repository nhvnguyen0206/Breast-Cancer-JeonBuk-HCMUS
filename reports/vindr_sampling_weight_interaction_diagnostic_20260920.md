# Sampling and class-weight interaction diagnostic

This calculation uses fold0 FIT counts `[5,156,1245,207]`. It normalizes
`sampling_probability * effective_number_class_weight` across A/B/C/D. The
result describes static expected class pressure in the focal term before the
dynamic focal factor `(1 - pt)^gamma`; it does not include the ordinal,
binary or neighbor losses and is not a prediction of model performance.

| Parent/candidate | Sampling power | Beta | Sampling A/B/C/D | Normalized static focal pressure A/B/C/D |
|---|---:|---:|---|---|
| A5 | 0 | .999 | .0031 / .0967 / .7719 / .1283 | .2030 / .2187 / .3541 / .2242 |
| A17 | .10 | .999 | .0051 / .1134 / .7352 / .1463 | .2833 / .2164 / .2847 / .2156 |
| A6 | .25 | .999 | .0107 / .1416 / .6725 / .1751 | .4291 / .1956 / .1885 / .1868 |
| Diagnostic candidate | .25 | .995 | .0107 / .1416 / .6725 / .1751 | .2644 / .1592 / .4110 / .1654 |
| Diagnostic candidate | .25 | .99 | .0107 / .1416 / .6725 / .1751 | .1723 / .1408 / .5293 / .1575 |

A6's sampler increases the expected number of A draws but, combined with
beta .999, also makes A account for about 42.9% of this static focal pressure.
That double compensation is consistent with A6 improving A stability while
reducing every mean class F1, but the calculation does not establish
causality. A17 reduces the A pressure to about 28.3%, yet its matched first30
CV result remains weak.

If A17 fails its completed audit, a scientifically controlled follow-up can
use A6 as the parent and change beta only. Beta .995 retains the proven .25
sampling exposure while reducing static A pressure to about 26.4% and
restoring C pressure. This is a candidate rationale only; no arm is
registered or launched by this diagnostic.
