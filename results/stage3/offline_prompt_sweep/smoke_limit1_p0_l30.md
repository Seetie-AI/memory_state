# Stage 3 offline prompt sweep: hidden-only

This analysis reads the merged Stage 3 prompt-sweep vectors and does not rerun the model.

LongMemEval is evidence-retrieval biased. In a chatbot-memory product, persona, preference, style, or strategy prompts may still be useful even when this leaderboard ranks them below fact/topic prompts.

BM25 score fusion is intentionally excluded here; prompt-vector fusion and late interaction are future experiments over the same stored vectors.

## Top Configs

| rank | config | R@5 | NDCG@5 | session_hit@5 | MRR | n |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `P0|layer30|last|anti_pca_both_k15` | 0.755 | 0.779 | 0.989 | 0.814 | 94 |
| 2 | `P0|layer30|last|query_only_anti_pca_k2` | 0.755 | 0.754 | 0.979 | 0.772 | 94 |
| 3 | `P0|layer30|last|centered_cosine` | 0.691 | 0.689 | 0.968 | 0.719 | 94 |

## Query-Only Anti-PCA k=2

| rank | candidate prompt | query prompt | layer | R@5 | NDCG@5 | session_hit@5 |
|---:|---|---|---:|---:|---:|---:|
| 1 | `P0` | `P0` | 30 | 0.755 | 0.754 | 0.979 |

## Anti-PCA Both k=15

| rank | candidate prompt | query prompt | layer | R@5 | NDCG@5 | session_hit@5 |
|---:|---|---|---:|---:|---:|---:|
| 1 | `P0` | `P0` | 30 | 0.755 | 0.779 | 0.989 |

## Asymmetric Memory/Query Cell

Anti-PCA for the asymmetric cell fits the mean and PCs on `2-3-2_mem` candidate rows, then applies that candidate-side geometry to `2-3-2_query` query rows. If this cell is weak, inspect that cross-prompt centering mismatch before treating the prompt idea as failed.

| score | layer | R@5 | NDCG@5 | session_hit@5 |
|---|---:|---:|---:|---:|

Elapsed: 3m34s
