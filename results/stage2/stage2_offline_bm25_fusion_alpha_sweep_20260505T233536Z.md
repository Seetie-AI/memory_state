# Stage 2 offline analysis: bm25_fusion_alpha_sweep

This analysis reads saved Stage 2 compact vectors and does not rerun the model.

| config | R@5 | NDCG@5 | n |
|---|---:|---:|---:|
| `P0|layer30|last|centered_cosine_bm25_fusion_alpha0.5` | 0.745 | 0.753 | 94 |
| `P0|layer30|last|centered_cosine_bm25_fusion_alpha0.75` | 0.734 | 0.731 | 94 |
| `P0|layer30|last|centered_cosine_bm25_fusion_alpha1` | 0.691 | 0.689 | 94 |
| `P0|layer30|last|centered_cosine_bm25_fusion_alpha0.25` | 0.681 | 0.658 | 94 |
| `P0|layer30|last|centered_cosine_bm25_fusion_alpha0` | 0.606 | 0.551 | 94 |
