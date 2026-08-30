# Stage 3 prompt fusion findings

This run reuses Stage 3 hidden vectors and does not rerun the model.

Storage budget: one bf16 prompt vector is 8KB; K=3 is 24KB per memory, inside the 10-100KB product target.

Single-vector baselines: best R@5=0.766; best NDCG@5=0.784.

## Selected Cells

| rank | cell | family |
|---:|---|---|
| 1 | `2-3-2_mem|layer31|last|anti_pca_both_k15` | mem-key |
| 2 | `2-4-1_user_word|layer30|last|anti_pca_both_k15` | persona |
| 3 | `1-3|layer31|last|anti_pca_both_k15` | tag |

## Phase 1 Audit

| rank | config | R@5 | NDCG@5 | session_hit@5 | MRR | n |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `2-3-2_mem|layer31|last|anti_pca_both_k15` | 0.766 | 0.757 | 0.979 | 0.780 | 94 |
| 2 | `2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.766 | 0.751 | 0.979 | 0.777 | 94 |
| 3 | `1-3|layer31|last|anti_pca_both_k15` | 0.755 | 0.784 | 1.000 | 0.806 | 94 |
| 4 | `P0|layer30|last|anti_pca_both_k15` | 0.755 | 0.779 | 0.989 | 0.814 | 94 |
| 5 | `1-1_CN|layer29|last|centered_cosine` | 0.755 | 0.756 | 0.979 | 0.783 | 94 |
| 6 | `2-1|layer30|last|anti_pca_both_k15` | 0.755 | 0.730 | 0.968 | 0.734 | 94 |
| 7 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.755 | 0.719 | 0.979 | 0.724 | 94 |
| 8 | `2-3-2_query|layer29|last|anti_pca_both_k15` | 0.745 | 0.764 | 0.989 | 0.796 | 94 |
| 9 | `2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.762 | 0.968 | 0.795 | 94 |
| 10 | `1-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.762 | 0.979 | 0.772 | 94 |
| 11 | `2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.747 | 0.968 | 0.771 | 94 |
| 12 | `2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.718 | 0.989 | 0.731 | 94 |
| 13 | `2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.700 | 0.989 | 0.713 | 94 |
| 14 | `1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.689 | 0.979 | 0.685 | 94 |
| 15 | `2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.648 | 0.968 | 0.647 | 94 |
| 16 | `2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.672 | 0.968 | 0.686 | 94 |
| 17 | `2-8|layer31|last|anti_pca_both_k15` | 0.574 | 0.510 | 0.915 | 0.519 | 94 |

## Phase 1 Pairwise Complementarity

| pair | top5_jaccard | only_left_hit@5 | only_right_hit@5 | both_hit@5 |
|---|---:|---:|---:|---:|
| `2-4-1|layer30|last|query_only_anti_pca_k2 vs 2-8|layer31|last|anti_pca_both_k15` | 0.290 | 0.191 | 0.043 | 0.532 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.294 | 0.213 | 0.021 | 0.553 |
| `2-3-2_query|layer29|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.295 | 0.181 | 0.011 | 0.564 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.304 | 0.202 | 0.011 | 0.564 |
| `2-5|layer29|last|query_only_anti_pca_k2 vs 2-8|layer31|last|anti_pca_both_k15` | 0.307 | 0.170 | 0.021 | 0.553 |
| `1-3|layer31|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.316 | 0.202 | 0.021 | 0.553 |
| `1-1_CN|layer29|last|centered_cosine vs 2-8|layer31|last|anti_pca_both_k15` | 0.318 | 0.202 | 0.021 | 0.553 |
| `2-6|layer30|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.319 | 0.160 | 0.011 | 0.564 |
| `2-3-1|layer30|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.321 | 0.181 | 0.011 | 0.564 |
| `2-1|layer30|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.325 | 0.213 | 0.032 | 0.543 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 2-8|layer31|last|anti_pca_both_k15` | 0.325 | 0.202 | 0.021 | 0.553 |
| `2-4-2|layer29|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.327 | 0.170 | 0.032 | 0.543 |
| `P0|layer30|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.328 | 0.191 | 0.011 | 0.564 |
| `1-2|layer29|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.340 | 0.191 | 0.021 | 0.553 |
| `1-1_EN|layer31|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.344 | 0.160 | 0.021 | 0.553 |
| `2-7|layer31|last|anti_pca_both_k15 vs 2-8|layer31|last|anti_pca_both_k15` | 0.361 | 0.138 | 0.011 | 0.564 |
| `2-5|layer29|last|query_only_anti_pca_k2 vs 1-1_EN|layer31|last|anti_pca_both_k15` | 0.442 | 0.032 | 0.021 | 0.691 |
| `2-5|layer29|last|query_only_anti_pca_k2 vs 2-7|layer31|last|anti_pca_both_k15` | 0.442 | 0.043 | 0.021 | 0.681 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-7|layer31|last|anti_pca_both_k15` | 0.443 | 0.074 | 0.011 | 0.691 |
| `2-4-1|layer30|last|query_only_anti_pca_k2 vs 2-7|layer31|last|anti_pca_both_k15` | 0.449 | 0.064 | 0.043 | 0.660 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 1-1_EN|layer31|last|anti_pca_both_k15` | 0.458 | 0.064 | 0.011 | 0.702 |
| `2-6|layer30|last|anti_pca_both_k15 vs 1-1_EN|layer31|last|anti_pca_both_k15` | 0.459 | 0.032 | 0.021 | 0.691 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.459 | 0.064 | 0.021 | 0.702 |
| `2-4-1|layer30|last|query_only_anti_pca_k2 vs 2-4-2|layer29|last|anti_pca_both_k15` | 0.461 | 0.064 | 0.053 | 0.660 |
| `2-3-2_query|layer29|last|anti_pca_both_k15 vs 2-7|layer31|last|anti_pca_both_k15` | 0.464 | 0.064 | 0.021 | 0.681 |
| `2-4-1|layer30|last|query_only_anti_pca_k2 vs 1-1_EN|layer31|last|anti_pca_both_k15` | 0.467 | 0.053 | 0.043 | 0.670 |
| `1-1_EN|layer31|last|anti_pca_both_k15 vs 2-4-2|layer29|last|anti_pca_both_k15` | 0.468 | 0.043 | 0.043 | 0.670 |
| `1-1_CN|layer29|last|centered_cosine vs 2-7|layer31|last|anti_pca_both_k15` | 0.468 | 0.074 | 0.021 | 0.681 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 2-7|layer31|last|anti_pca_both_k15` | 0.468 | 0.074 | 0.021 | 0.681 |
| `1-3|layer31|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.471 | 0.043 | 0.011 | 0.713 |

### Centered Future Work

- 1-1_CN|layer29|last|centered_cosine shows complementarity but is excluded from Phase 4 because centered cosine's per-query candidate mean is not a persistable vector transform.

## Phase 2 Asymmetric

| rank | config | R@5 | NDCG@5 | session_hit@5 | MRR | n |
|---:|---|---:|---:|---:|---:|---:|

## Phase 3 Score Fusion

| rank | config | R@5 | NDCG@5 | session_hit@5 | MRR | n |
|---:|---|---:|---:|---:|---:|---:|

## Phase 4 Vector Fusion

| rank | config | R@5 | NDCG@5 | session_hit@5 | MRR | n |
|---:|---|---:|---:|---:|---:|---:|

Elapsed: 5m10s
