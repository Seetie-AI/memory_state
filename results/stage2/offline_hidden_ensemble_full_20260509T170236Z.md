# Offline Hidden-Only Ensemble

This run reads saved 9B Stage 2 vectors and does not run the model.

## Design Decisions

- N=100 evaluation only; N=30 is for elimination, not confirmation.
- RRF over rank with k=60; no score-linear fusion.
- Multi-vector anti-PCA is per-position independent.
- Strict hidden-only: no BM25 and no external embedding model.
- Bootstrap 95% CI is reported; R@5 deltas below +0.05 are treated as noise.

## Top Configs

| config | R@5 | R@5 95% CI | NDCG@5 | delta R@5 vs baseline | interpretation | n |
|---|---:|---:|---:|---:|---|---:|
| `hidden_only_rrf_k_5_10_15_20_layer30_last` | 0.766 | [0.681, 0.840] | 0.772 | +0.011 [+0.000, +0.032] | noise_range | 94 |
| `P0|layer30|last|anti_pca_both_k15` | 0.755 | [0.670, 0.830] | 0.779 | +0.000 [+0.000, +0.000] | baseline | 94 |
| `hidden_only_rrf_layers_28_29_30_31_k15_last` | 0.755 | [0.670, 0.840] | 0.771 | +0.000 [-0.032, +0.032] | noise_range | 94 |
| `hidden_only_rrf_layers_28_31_x_k_5_20_last` | 0.745 | [0.660, 0.819] | 0.772 | -0.011 [-0.064, +0.032] | noise_range | 94 |
| `hidden_only_multivector_layer30_positions_per_position_antipca_k15` | 0.702 | [0.606, 0.787] | 0.725 | -0.053 [-0.106, -0.011] | clear_regression | 94 |
| `hidden_only_rrf_positions_x_k_layer30` | 0.564 | [0.457, 0.660] | 0.473 | -0.191 [-0.277, -0.117] | clear_regression | 94 |
| `hidden_only_rrf_positions_layer30_k15` | 0.553 | [0.457, 0.649] | 0.475 | -0.202 [-0.287, -0.128] | clear_regression | 94 |
| `hidden_only_multivector_layer30_positions_raw` | 0.245 | [0.160, 0.330] | 0.210 | -0.511 [-0.606, -0.404] | clear_regression | 94 |
