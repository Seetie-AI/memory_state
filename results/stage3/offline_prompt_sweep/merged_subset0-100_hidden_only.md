# Stage 3 offline prompt sweep: hidden-only

This analysis reads the merged Stage 3 prompt-sweep vectors and does not rerun the model.

LongMemEval is evidence-retrieval biased. In a chatbot-memory product, persona, preference, style, or strategy prompts may still be useful even when this leaderboard ranks them below fact/topic prompts.

BM25 score fusion is intentionally excluded here; prompt-vector fusion and late interaction are future experiments over the same stored vectors.

## Top Configs

| rank | config | R@5 | NDCG@5 | session_hit@5 | MRR | n |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `2-3-2_mem|layer31|last|anti_pca_both_k15` | 0.766 | 0.757 | 0.979 | 0.780 | 94 |
| 2 | `2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.766 | 0.751 | 0.979 | 0.777 | 94 |
| 3 | `1-3|layer31|last|anti_pca_both_k15` | 0.755 | 0.784 | 1.000 | 0.805 | 94 |
| 4 | `1-3|layer29|last|query_only_anti_pca_k2` | 0.755 | 0.781 | 1.000 | 0.804 | 94 |
| 5 | `1-3|layer30|last|query_only_anti_pca_k2` | 0.755 | 0.780 | 1.000 | 0.800 | 94 |
| 6 | `P0|layer30|last|anti_pca_both_k15` | 0.755 | 0.779 | 0.989 | 0.814 | 94 |
| 7 | `1-1_CN|layer29|last|centered_cosine` | 0.755 | 0.756 | 0.979 | 0.783 | 94 |
| 8 | `P0|layer30|last|query_only_anti_pca_k2` | 0.755 | 0.754 | 0.979 | 0.772 | 94 |
| 9 | `2-3-2_mem->2-3-2_query|layer31|last|anti_pca_both_k15` | 0.755 | 0.751 | 0.957 | 0.773 | 94 |
| 10 | `1-1_CN|layer30|last|centered_cosine` | 0.755 | 0.737 | 0.979 | 0.749 | 94 |
| 11 | `2-1|layer30|last|anti_pca_both_k15` | 0.755 | 0.730 | 0.968 | 0.734 | 94 |
| 12 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.755 | 0.719 | 0.979 | 0.723 | 94 |
| 13 | `1-3|layer30|last|anti_pca_both_k15` | 0.745 | 0.783 | 0.989 | 0.804 | 94 |
| 14 | `2-3-2_mem->2-3-2_query|layer29|last|anti_pca_both_k15` | 0.745 | 0.768 | 0.968 | 0.799 | 94 |
| 15 | `2-3-2_query|layer29|last|anti_pca_both_k15` | 0.745 | 0.764 | 0.989 | 0.796 | 94 |
| 16 | `2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.762 | 0.968 | 0.795 | 94 |
| 17 | `1-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.762 | 0.979 | 0.772 | 94 |
| 18 | `2-3-2_mem->2-3-2_query|layer30|last|anti_pca_both_k15` | 0.745 | 0.759 | 0.968 | 0.789 | 94 |
| 19 | `2-3-2_query|layer30|last|anti_pca_both_k15` | 0.745 | 0.758 | 0.989 | 0.792 | 94 |
| 20 | `2-4-1_user_word|layer29|last|anti_pca_both_k15` | 0.745 | 0.739 | 0.979 | 0.763 | 94 |
| 21 | `2-1|layer31|last|anti_pca_both_k15` | 0.745 | 0.738 | 0.979 | 0.751 | 94 |
| 22 | `2-1|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.735 | 0.979 | 0.751 | 94 |
| 23 | `2-4-1_user_word|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.728 | 0.989 | 0.740 | 94 |
| 24 | `2-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.728 | 0.968 | 0.740 | 94 |
| 25 | `1-1_CN_ASCII|layer30|last|centered_cosine` | 0.745 | 0.716 | 0.979 | 0.718 | 94 |

## Query-Only Anti-PCA k=2

| rank | candidate prompt | query prompt | layer | R@5 | NDCG@5 | session_hit@5 |
|---:|---|---|---:|---:|---:|---:|
| 1 | `1-3` | `1-3` | 29 | 0.755 | 0.781 | 1.000 |
| 2 | `1-3` | `1-3` | 30 | 0.755 | 0.780 | 1.000 |
| 3 | `P0` | `P0` | 30 | 0.755 | 0.754 | 0.979 |
| 4 | `1-1_CN_ASCII` | `1-1_CN_ASCII` | 29 | 0.755 | 0.719 | 0.979 |
| 5 | `2-1` | `2-1` | 29 | 0.745 | 0.735 | 0.979 |
| 6 | `2-4-1_user_word` | `2-4-1_user_word` | 30 | 0.745 | 0.728 | 0.989 |
| 7 | `2-1` | `2-1` | 30 | 0.745 | 0.728 | 0.968 |
| 8 | `2-3-2_query` | `2-3-2_query` | 30 | 0.734 | 0.764 | 0.979 |
| 9 | `2-3-2_mem` | `2-3-2_mem` | 29 | 0.734 | 0.762 | 0.979 |
| 10 | `2-3-1` | `2-3-1` | 29 | 0.734 | 0.758 | 0.968 |
| 11 | `2-3-1` | `2-3-1` | 30 | 0.734 | 0.756 | 0.968 |
| 12 | `2-3-2_mem` | `2-3-2_mem` | 30 | 0.734 | 0.756 | 0.968 |
| 13 | `2-3-2_query` | `2-3-2_query` | 29 | 0.734 | 0.754 | 0.979 |
| 14 | `P0` | `P0` | 29 | 0.734 | 0.753 | 0.979 |
| 15 | `1-1_CN_ASCII` | `1-1_CN_ASCII` | 30 | 0.734 | 0.728 | 0.979 |

## Anti-PCA Both k=15

| rank | candidate prompt | query prompt | layer | R@5 | NDCG@5 | session_hit@5 |
|---:|---|---|---:|---:|---:|---:|
| 1 | `2-3-2_mem` | `2-3-2_mem` | 31 | 0.766 | 0.757 | 0.979 |
| 2 | `2-4-1_user_word` | `2-4-1_user_word` | 30 | 0.766 | 0.751 | 0.979 |
| 3 | `1-3` | `1-3` | 31 | 0.755 | 0.784 | 1.000 |
| 4 | `P0` | `P0` | 30 | 0.755 | 0.779 | 0.989 |
| 5 | `2-3-2_mem` | `2-3-2_query` | 31 | 0.755 | 0.751 | 0.957 |
| 6 | `2-1` | `2-1` | 30 | 0.755 | 0.730 | 0.968 |
| 7 | `1-3` | `1-3` | 30 | 0.745 | 0.783 | 0.989 |
| 8 | `2-3-2_mem` | `2-3-2_query` | 29 | 0.745 | 0.768 | 0.968 |
| 9 | `2-3-2_query` | `2-3-2_query` | 29 | 0.745 | 0.764 | 0.989 |
| 10 | `2-3-1` | `2-3-1` | 30 | 0.745 | 0.762 | 0.968 |
| 11 | `1-2` | `1-2` | 29 | 0.745 | 0.762 | 0.979 |
| 12 | `2-3-2_mem` | `2-3-2_query` | 30 | 0.745 | 0.759 | 0.968 |
| 13 | `2-3-2_query` | `2-3-2_query` | 30 | 0.745 | 0.758 | 0.989 |
| 14 | `2-4-1_user_word` | `2-4-1_user_word` | 29 | 0.745 | 0.739 | 0.979 |
| 15 | `2-1` | `2-1` | 31 | 0.745 | 0.738 | 0.979 |

## Asymmetric Memory/Query Cell

Anti-PCA for the asymmetric cell fits the mean and PCs on `2-3-2_mem` candidate rows, then applies that candidate-side geometry to `2-3-2_query` query rows. If this cell is weak, inspect that cross-prompt centering mismatch before treating the prompt idea as failed.

| score | layer | R@5 | NDCG@5 | session_hit@5 |
|---|---:|---:|---:|---:|
| `anti_pca_both_k15` | 31 | 0.755 | 0.751 | 0.957 |
| `anti_pca_both_k15` | 29 | 0.745 | 0.768 | 0.968 |
| `anti_pca_both_k15` | 30 | 0.745 | 0.759 | 0.968 |
| `query_only_anti_pca_k2` | 30 | 0.723 | 0.737 | 0.957 |
| `query_only_anti_pca_k2` | 29 | 0.713 | 0.741 | 0.957 |
| `query_only_anti_pca_k2` | 31 | 0.702 | 0.722 | 0.957 |
| `centered_cosine` | 29 | 0.638 | 0.643 | 0.894 |
| `centered_cosine` | 30 | 0.638 | 0.637 | 0.894 |
| `centered_cosine` | 31 | 0.553 | 0.529 | 0.798 |

Elapsed: 1h28m09s
