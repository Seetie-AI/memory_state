# Stage 3 prompt fusion + BM25 sweep

This run adds BM25 score fusion over saved Stage 3 prompt-vector configs.

BM25 scope: `full`.

| rank | config | alpha | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `concat_k3_norm_weighted_userword_tag_assoc` | 1.00 | 0.766 | 0.806 | 0.839 | 1.000 | 94 |
| 2 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.50 | 0.755 | 0.772 | 0.794 | 1.000 | 94 |
| 3 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.00 | 0.585 | 0.547 | 0.559 | 0.862 | 94 |

## Alpha=1.0 Self-Checks

All alpha=1.0 rows are checked against hard-coded vector-only baselines at 1e-6 tolerance.

## Inputs

- configs: concat_k3_norm_weighted_userword_tag_assoc
- alphas: [0.0, 0.5, 1.0]
- elapsed: 56s
