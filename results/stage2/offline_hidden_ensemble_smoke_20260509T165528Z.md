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
