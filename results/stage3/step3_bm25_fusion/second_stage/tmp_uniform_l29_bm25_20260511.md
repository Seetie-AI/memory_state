# Temporary uniform-layer BM25 check

Same three product prompts, all forced to one layer and `anti_pca_both_k15`.

| rank | scope | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `vector_top50` | 0.75 | 0.713 | 0.780 | 0.766 | 0.805 | 0.827 | 0.989 | 94 |
| 2 | `vector_top20` | 0.75 | 0.702 | 0.770 | 0.766 | 0.800 | 0.823 | 0.989 | 94 |
| 3 | `vector_top20` | 1.00 | 0.723 | 0.761 | 0.745 | 0.778 | 0.799 | 0.989 | 94 |

## Config

- `2-4-1_user_word` L29 `anti_pca_both_k15`
- `1-3` L29 `anti_pca_both_k15`
- `2-5` L29 `anti_pca_both_k15`

elapsed_seconds: 53.1
