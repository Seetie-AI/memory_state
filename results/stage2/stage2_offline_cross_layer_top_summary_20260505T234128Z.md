# Stage 2 offline analysis: cross_layer_top_summary

This analysis reads saved Stage 2 compact vectors and does not rerun the model.

| config | R@5 | NDCG@5 | n |
|---|---:|---:|---:|
| `P0|layer30|last|centered_cosine` | 0.691 | 0.689 | 94 |
| `P0|layer29|last|centered_cosine` | 0.681 | 0.683 | 94 |
| `P0|layer28|last|centered_cosine` | 0.638 | 0.665 | 94 |
| `P0|layer27|last|centered_cosine` | 0.628 | 0.642 | 94 |
| `P0|layer29|last|cosine` | 0.617 | 0.632 | 94 |
| `P0|layer30|last|cosine` | 0.606 | 0.630 | 94 |
| `P0|layer28|last|cosine` | 0.574 | 0.606 | 94 |
| `P0|layer27|last|cosine` | 0.553 | 0.602 | 94 |
| `P0|layer30|minus2|centered_cosine` | 0.553 | 0.547 | 94 |
| `P0|layer31|last|centered_cosine` | 0.543 | 0.560 | 94 |
