# Post-A45 rare-A generalization diagnostic

This read-only diagnostic explains why simply increasing rare-class loss is
not a justified A46. It uses the selected A43/A44/A45 checkpoints, frozen
fold1 FIT/DEV manifests and the same window16 cache. RTX5090 job1055 performs
inference only on FIT A/B cases; no parameters or predictions are changed.

## Learned gate behavior

All three selected checkpoints correctly classify all five FIT A cases.
A44/A45 also classify all 157 FIT B cases as B. A45 is the most saturated:
its five FIT A probabilities are all at least .9999990, while every FIT B
has P(A) at most .0001553. Nevertheless, the sole fold1 DEV A case is
classified as B with P(A)=.0001702 and P(B)=.9998125.

| Arm | FIT A correct | FIT B predicted A | DEV A P(A) | DEV A prediction |
|---|---:|---:|---:|---|
| A43 | 5/5 | 22/157 | .789450 | A |
| A44 | 5/5 | 0/157 | .996097 | A |
| A45 | 5/5 | 0/157 | .000170 | B |

A45 therefore does not suffer from insufficient rare-class gradient. It
memorizes the five FIT A cases with extreme confidence but fails to generalize
to the held-out A case. Stronger class weights or an extra A-vs-rest loss
would target the wrong mechanism and may worsen saturation.

## Fixed-cache breast-mask statistics

A second CPU-only diagnostic averages eleven intensity/mask statistics over
the four cached views. The fold1 DEV A case is farther from the standardized
FIT-A centroid (distance 10.2865) than the FIT-B centroid (9.0717). Its mean,
standard deviation, median, upper quantiles and bright-pixel fractions exceed
the FIT-A range in multiple dimensions while remaining inside the broad B
range. For example:

| Statistic | DEV A | FIT A range | Percentile in FIT B |
|---|---:|---:|---:|
| mean | .345403 | .267699--.317460 | .8217 |
| std | .142207 | .078178--.107918 | .9873 |
| q90 | .577287 | .366316--.416114 | .9936 |
| fraction >= .50 | .099240 | .007266--.016969 | .8535 |
| fraction >= .75 | .046832 | .000004--.000156 | .9936 |

This rules against adding a direct raw-statistics A branch: on the difficult
case it would likely reinforce B. It instead supports a domain/style
generalization intervention that reduces reliance on acquisition-specific
feature statistics.

Artifacts:

- Gate report:
  /slurmshared/Ngoc/runs/hcmus-a45-gate-diagnostic-1053/report.json
  (SHA256 a2843742bbdfba30f357152e9c6cbd28ab947db9c2633facc44184618bed70e8)
- Cache-statistics report:
  /slurmshared/Ngoc/runs/hcmus-a45-gate-diagnostic-1053/cache_statistics.json
  (SHA256 036811259414fd0f40c8de74f85a40193f222ce89eee8a49a0700dd12e798df0)

Limitations: only five FIT A and one DEV A cases exist in fold1; the analysis
is descriptive, DEV-informed and not independent evidence.
