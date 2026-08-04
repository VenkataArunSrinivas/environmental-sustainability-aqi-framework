# Methodology and Decision Rules

1. Preserve raw source files unchanged.
2. Record source URL, file name, date, coverage, schema, units, and redistribution status.
3. Parse dates and numeric fields; retain null values as null.
4. Quantify duplicate, missingness, station-network, and common-period risks.
5. Treat Odisha as conditional unless at least 12 contiguous common months satisfy all source requirements.
6. Use station-month outcomes only with an explicit completeness rule; separately report unique state-month exposure periods.
7. Do not use same-period pollutant components as predictors when AQI is the target.
8. Keep all records sharing a state-month industrial exposure in the same validation fold.
9. Use chronological, not shuffled, validation.
10. Interpret SHAP/permutation values as model-behavior explanations, not causal effects.
11. Report uncertainty, omitted-variable limitations, and monitoring-coverage sensitivity.
