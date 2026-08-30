# Temporary uniform-layer BM25 check

Same three product prompts, all forced to one layer and `anti_pca_both_k15`.

| rank | scope | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `vector_top20` | 0.75 | 0.734 | 0.797 | 0.777 | 0.822 | 0.851 | 0.989 | 94 |
| 2 | `vector_top50` | 0.75 | 0.734 | 0.790 | 0.777 | 0.811 | 0.838 | 0.989 | 94 |
| 3 | `vector_top20` | 1.00 | 0.723 | 0.771 | 0.755 | 0.795 | 0.819 | 0.989 | 94 |

## Config

- `2-4-1_user_word` L31 `anti_pca_both_k15`
- `1-3` L31 `anti_pca_both_k15`
- `2-5` L31 `anti_pca_both_k15`

elapsed_seconds: 53.1
