# A22 CV5 confirmation — first 10 epochs

All four confirmation tasks remain healthy on RTX 5090 nodes with no requeue
or restart. Using the best selected DEV checkpoint within epochs 1--10 for
each fold:

| Fold | Best epoch | Macro-F1 | Accuracy | QWK | F1 A/B/C/D |
|---:|---:|---:|---:|---:|---|
| 0 | 10 | 0.560716 | 0.834158 | 0.656362 | 0.200000 / 0.437500 / 0.905363 / 0.700000 |
| 1 | 10 | 0.566206 | 0.848635 | 0.672144 | 0.000000 / 0.763158 / 0.903537 / 0.598131 |
| 2 | 9 | 0.681848 | 0.821340 | 0.615531 | 0.666667 / 0.673267 / 0.887460 / 0.500000 |
| 3 | 8 | 0.548888 | 0.846535 | 0.647800 | 0.000000 / 0.649351 / 0.906200 / 0.640000 |
| 4 | 8 | 0.524670 | 0.794045 | 0.623131 | 0.000000 / 0.631579 / 0.860544 / 0.606557 |

Temporary aggregate: mean Macro-F1 **0.576466**, sample SD **0.061037**, and
minimum **0.524670**. This is an early selected-DEV diagnostic, not a final or
independent-test result. Continue all folds unchanged through epoch 50; next
review is epoch 20.
