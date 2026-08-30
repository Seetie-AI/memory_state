# Stage 3 prompt fusion findings

This run reuses Stage 3 hidden vectors and does not rerun the model.

Storage budget: one bf16 prompt vector is 8KB; K=3 is 24KB per memory, inside the 10-100KB product target.

Single-vector baselines: best R@5=0.766; best NDCG@5=0.784.

## Selected Cells

| rank | cell | family |
|---:|---|---|
| 1 | `2-4-1_user_word|layer30|last|anti_pca_both_k15` | persona |
| 2 | `1-3|layer31|last|anti_pca_both_k15` | tag |
| 3 | `2-5|layer29|last|query_only_anti_pca_k2` | association |

## Phase 1 Audit

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

## Phase 1 Pairwise Complementarity

| pair | top5_jaccard | only_left_hit@5 | only_right_hit@5 | both_hit@5 |
|---|---:|---:|---:|---:|

## Phase 2 Asymmetric

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

## Phase 3 Score Fusion

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|

## Phase 4 Vector Fusion

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `vector_average_component_norm_uniform_l30_bothk15 K=2 2-4-1_user_word+1-3` | 0.691 | 0.764 | 0.777 | 0.788 | 0.989 | 0.820 | - | - | - | 94 |
| 2 | `vector_average_component_norm_uniform_l29_bothk15 K=2 2-4-1_user_word+1-3` | 0.681 | 0.757 | 0.777 | 0.784 | 0.989 | 0.804 | - | - | - | 94 |
| 3 | `vector_average_norm_weighted_uniform_l29_bothk15 K=2 2-4-1_user_word+1-3` | 0.681 | 0.754 | 0.777 | 0.783 | 0.989 | 0.803 | - | - | - | 94 |
| 4 | `vector_average_norm_weighted_uniform_l30_bothk15 K=2 2-4-1_user_word+1-3` | 0.691 | 0.757 | 0.777 | 0.780 | 0.989 | 0.806 | - | - | - | 94 |
| 5 | `vector_average_component_norm K=3 2-4-1_user_word+1-3+2-5` | 0.702 | 0.767 | 0.766 | 0.790 | 1.000 | 0.815 | - | - | - | 94 |
| 6 | `vector_average_component_norm K=2 2-4-1_user_word+2-5` | 0.723 | 0.755 | 0.766 | 0.767 | 1.000 | 0.793 | - | - | - | 94 |
| 7 | `vector_average_component_norm K=2 1-3+2-5` | 0.723 | 0.784 | 0.755 | 0.795 | 1.000 | 0.820 | - | - | - | 94 |
| 8 | `vector_average_norm_weighted K=3 2-4-1_user_word+1-3+2-5` | 0.723 | 0.783 | 0.755 | 0.794 | 1.000 | 0.825 | - | - | - | 94 |
| 9 | `vector_average_component_norm_uniform_l31_bothk15 K=3 2-4-1_user_word+1-3+2-5` | 0.713 | 0.761 | 0.755 | 0.788 | 0.989 | 0.815 | - | - | - | 94 |
| 10 | `vector_average_norm_weighted K=2 2-4-1_user_word+1-3` | 0.713 | 0.774 | 0.755 | 0.786 | 1.000 | 0.813 | - | - | - | 94 |
| 11 | `vector_average_component_norm_uniform_l29_bothk15 K=3 2-4-1_user_word+1-3+2-5` | 0.713 | 0.766 | 0.755 | 0.785 | 0.989 | 0.814 | - | - | - | 94 |
| 12 | `vector_average_component_norm K=2 2-4-1_user_word+1-3` | 0.713 | 0.775 | 0.755 | 0.784 | 0.989 | 0.818 | - | - | - | 94 |
| 13 | `vector_average_norm_weighted_uniform_l31_bothk15 K=3 2-4-1_user_word+1-3+2-5` | 0.713 | 0.759 | 0.755 | 0.784 | 0.989 | 0.805 | - | - | - | 94 |
| 14 | `vector_average_component_norm_uniform_l30_bothk15 K=3 2-4-1_user_word+1-3+2-5` | 0.723 | 0.764 | 0.755 | 0.782 | 0.989 | 0.806 | - | - | - | 94 |
| 15 | `vector_average_norm_weighted_uniform_l31_bothk15 K=2 2-4-1_user_word+1-3` | 0.713 | 0.761 | 0.755 | 0.774 | 0.989 | 0.803 | - | - | - | 94 |
| 16 | `vector_average_component_norm_uniform_l31_bothk15 K=2 2-4-1_user_word+1-3` | 0.713 | 0.759 | 0.755 | 0.771 | 0.989 | 0.801 | - | - | - | 94 |
| 17 | `vector_average_component_norm_uniform_l29_bothk15 K=2 2-4-1_user_word+2-5` | 0.713 | 0.748 | 0.755 | 0.769 | 0.989 | 0.788 | - | - | - | 94 |
| 18 | `vector_average_norm_weighted K=2 1-3+2-5` | 0.734 | 0.803 | 0.745 | 0.809 | 1.000 | 0.847 | - | - | - | 94 |
| 19 | `vector_average_norm_weighted K=2 2-4-1_user_word+2-5` | 0.723 | 0.773 | 0.745 | 0.788 | 0.979 | 0.826 | - | - | - | 94 |
| 20 | `vector_average_norm_weighted_uniform_l30_bothk15 K=3 2-4-1_user_word+1-3+2-5` | 0.713 | 0.762 | 0.745 | 0.783 | 0.989 | 0.810 | - | - | - | 94 |

Elapsed: 3m47s
