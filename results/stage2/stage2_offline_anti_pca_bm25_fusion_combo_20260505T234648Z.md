# Stage 2 offline analysis: anti_pca_bm25_fusion_combo

This analysis reads saved Stage 2 compact vectors and does not rerun the model.

| config | R@5 | NDCG@5 | n |
|---|---:|---:|---:|
| `P0|layer30|last|anti_pca_both_k15_bm25_fusion_alpha0.75` | 0.766 | 0.791 | 94 |
| `P0|layer30|last|anti_pca_both_k15_bm25_fusion_alpha1` | 0.755 | 0.779 | 94 |
| `P0|layer30|last|anti_pca_both_k15_bm25_fusion_alpha0.5` | 0.745 | 0.762 | 94 |
| `P0|layer30|last|anti_pca_both_k15_bm25_fusion_alpha0.25` | 0.681 | 0.689 | 94 |
| `P0|layer30|last|anti_pca_both_k15_bm25_fusion_alpha0` | 0.606 | 0.543 | 94 |
