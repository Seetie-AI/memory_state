# Stage 2 offline analysis: anti_pca_sweep

This analysis reads saved Stage 2 compact vectors and does not rerun the model.

| config | R@5 | NDCG@5 | n |
|---|---:|---:|---:|
| `P0|layer30|last|anti_pca_both_k15` | 0.755 | 0.779 | 94 |
| `P0|layer30|last|anti_pca_query_only_k2` | 0.755 | 0.754 | 94 |
| `P0|layer30|last|anti_pca_both_k5` | 0.745 | 0.768 | 94 |
| `P0|layer30|last|anti_pca_both_k20` | 0.734 | 0.779 | 94 |
| `P0|layer30|last|anti_pca_both_k2` | 0.734 | 0.758 | 94 |
| `P0|layer30|last|anti_pca_query_only_k15` | 0.734 | 0.747 | 94 |
| `P0|layer30|last|anti_pca_query_only_k5` | 0.734 | 0.740 | 94 |
| `P0|layer30|last|anti_pca_both_k10` | 0.723 | 0.760 | 94 |
| `P0|layer30|last|anti_pca_query_only_k20` | 0.723 | 0.751 | 94 |
| `P0|layer30|last|anti_pca_query_only_k10` | 0.723 | 0.745 | 94 |
