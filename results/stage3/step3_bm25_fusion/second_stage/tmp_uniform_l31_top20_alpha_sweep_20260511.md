# Temporary uniform-layer BM25 check

Same three product prompts, all forced to one layer and `anti_pca_both_k15`.

| rank | scope | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `vector_top20` | 0.75 | 0.734 | 0.797 | 0.777 | 0.822 | 0.851 | 0.989 | 94 |
| 2 | `vector_top20` | 0.80 | 0.734 | 0.793 | 0.777 | 0.816 | 0.839 | 0.989 | 94 |
| 3 | `vector_top20` | 0.70 | 0.734 | 0.797 | 0.777 | 0.815 | 0.842 | 1.000 | 94 |
| 4 | `vector_top20` | 0.60 | 0.723 | 0.800 | 0.766 | 0.816 | 0.848 | 1.000 | 94 |
| 5 | `vector_top20` | 0.65 | 0.734 | 0.799 | 0.766 | 0.810 | 0.835 | 1.000 | 94 |

## Config

- `2-4-1_user_word` L31 `anti_pca_both_k15`
- `1-3` L31 `anti_pca_both_k15`
- `2-5` L31 `anti_pca_both_k15`

elapsed_seconds: 48.5
