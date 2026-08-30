# Stage 3 prompt fusion findings

This run reuses Stage 3 hidden vectors and does not rerun the model.

Storage budget: one bf16 prompt vector is 8KB; K=3 is 24KB per memory, inside the 10-100KB product target.

Single-vector baselines: best R@5=0.766; best NDCG@5=0.784.

## Selected Cells

| rank | cell | family |
|---:|---|---|
| 1 | `2-3-2_query|layer29|last|anti_pca_both_k15` | query-key |
| 2 | `2-4-1|layer30|last|query_only_anti_pca_k2` | persona |

## Phase 1 Audit

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `2-3-2_mem|layer31|last|anti_pca_both_k15` | 0.670 | 0.727 | 0.766 | 0.757 | 0.979 | 0.780 | - | - | - | 94 |
| 2 | `2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.681 | 0.734 | 0.766 | 0.751 | 0.979 | 0.777 | - | - | - | 94 |
| 3 | `1-3|layer31|last|anti_pca_both_k15` | 0.702 | 0.779 | 0.755 | 0.784 | 1.000 | 0.806 | - | - | - | 94 |
| 4 | `P0|layer30|last|anti_pca_both_k15` | 0.617 | 0.743 | 0.755 | 0.779 | 0.989 | 0.814 | - | - | - | 94 |
| 5 | `1-1_CN|layer29|last|centered_cosine` | 0.638 | 0.722 | 0.755 | 0.756 | 0.979 | 0.783 | - | - | - | 94 |
| 6 | `2-1|layer30|last|anti_pca_both_k15` | 0.660 | 0.689 | 0.755 | 0.730 | 0.968 | 0.734 | - | - | - | 94 |
| 7 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.628 | 0.674 | 0.755 | 0.719 | 0.979 | 0.724 | - | - | - | 94 |
| 8 | `2-3-2_query|layer29|last|anti_pca_both_k15` | 0.670 | 0.739 | 0.745 | 0.764 | 0.989 | 0.796 | - | - | - | 94 |
| 9 | `2-3-1|layer30|last|anti_pca_both_k15` | 0.702 | 0.744 | 0.745 | 0.762 | 0.968 | 0.795 | - | - | - | 94 |
| 10 | `1-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.739 | 0.745 | 0.762 | 0.979 | 0.772 | - | - | - | 94 |
| 11 | `2-5|layer29|last|query_only_anti_pca_k2` | 0.691 | 0.726 | 0.723 | 0.747 | 0.968 | 0.771 | - | - | - | 94 |
| 12 | `2-4-1|layer30|last|query_only_anti_pca_k2` | 0.638 | 0.681 | 0.723 | 0.718 | 0.989 | 0.731 | - | - | - | 94 |

## Phase 1 Pairwise Complementarity

| pair | top5_jaccard | only_left_hit@5 | only_right_hit@5 | both_hit@5 |
|---|---:|---:|---:|---:|
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.459 | 0.064 | 0.021 | 0.702 |
| `1-3|layer31|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.471 | 0.043 | 0.011 | 0.713 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 1-1_CN|layer29|last|centered_cosine` | 0.486 | 0.043 | 0.032 | 0.723 |
| `2-5|layer29|last|query_only_anti_pca_k2 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.487 | 0.043 | 0.043 | 0.681 |
| `1-3|layer31|last|anti_pca_both_k15 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.489 | 0.043 | 0.011 | 0.713 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.490 | 0.043 | 0.032 | 0.723 |
| `P0|layer30|last|anti_pca_both_k15 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.491 | 0.064 | 0.032 | 0.691 |
| `2-3-2_query|layer29|last|anti_pca_both_k15 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.505 | 0.053 | 0.032 | 0.691 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.508 | 0.064 | 0.021 | 0.702 |
| `1-3|layer31|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.514 | 0.021 | 0.021 | 0.734 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.514 | 0.032 | 0.021 | 0.723 |
| `1-2|layer29|last|anti_pca_both_k15 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.524 | 0.053 | 0.032 | 0.691 |
| `2-3-1|layer30|last|anti_pca_both_k15 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.525 | 0.053 | 0.032 | 0.691 |
| `1-3|layer31|last|anti_pca_both_k15 vs 1-1_CN|layer29|last|centered_cosine` | 0.525 | 0.021 | 0.021 | 0.734 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.529 | 0.053 | 0.011 | 0.713 |
| `2-1|layer30|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.530 | 0.043 | 0.011 | 0.713 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.530 | 0.043 | 0.011 | 0.713 |
| `1-1_CN|layer29|last|centered_cosine vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.532 | 0.053 | 0.021 | 0.702 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-3-1|layer30|last|anti_pca_both_k15` | 0.534 | 0.053 | 0.032 | 0.713 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.539 | 0.053 | 0.011 | 0.713 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.540 | 0.053 | 0.032 | 0.713 |
| `2-1|layer30|last|anti_pca_both_k15 vs 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.541 | 0.043 | 0.011 | 0.713 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 2-3-1|layer30|last|anti_pca_both_k15` | 0.542 | 0.032 | 0.021 | 0.723 |
| `P0|layer30|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.544 | 0.053 | 0.021 | 0.702 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.546 | 0.021 | 0.011 | 0.745 |
| `P0|layer30|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.548 | 0.021 | 0.021 | 0.734 |
| `1-1_CN|layer29|last|centered_cosine vs 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.551 | 0.032 | 0.021 | 0.723 |
| `1-1_CN|layer29|last|centered_cosine vs 2-1|layer30|last|anti_pca_both_k15` | 0.553 | 0.021 | 0.021 | 0.734 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.554 | 0.032 | 0.032 | 0.734 |
| `1-3|layer31|last|anti_pca_both_k15 vs 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.554 | 0.032 | 0.021 | 0.723 |

## Phase 2 Asymmetric

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `2-3-2_query|layer29|last|anti_pca_both_k15 -> 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.670 | 0.739 | 0.745 | 0.764 | 0.989 | 0.796 | - | - | - | 94 |
| 2 | `2-4-1|layer30|last|query_only_anti_pca_k2 -> 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.638 | 0.681 | 0.723 | 0.718 | 0.989 | 0.731 | - | - | - | 94 |
| 3 | `2-3-2_query|layer29|last|anti_pca_both_k15 -> 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.468 | 0.511 | 0.574 | 0.563 | 0.883 | 0.587 | - | - | - | 94 |
| 4 | `2-4-1|layer30|last|query_only_anti_pca_k2 -> 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.415 | 0.468 | 0.521 | 0.513 | 0.862 | 0.549 | - | - | - | 94 |

## Phase 3 Score Fusion

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `zsum K=2 2-3-2_query+2-4-1` | 0.723 | 0.758 | 0.766 | 0.766 | 0.989 | 0.785 | 0.557 | 0.021 | 0.011 | 94 |
| 2 | `rrf K=2 2-3-2_query+2-4-1` | 0.691 | 0.717 | 0.766 | 0.750 | 0.989 | 0.749 | 0.553 | 0.011 | 0.000 | 94 |

## Phase 4 Vector Fusion

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `vector_average_norm_weighted K=2 2-3-2_query+2-4-1` | 0.702 | 0.764 | 0.787 | 0.786 | 0.989 | 0.823 | 0.571 | 0.032 | 0.000 | 94 |
| 2 | `vertical_concat_norm_weighted K=2 2-3-2_query+2-4-1` | 0.713 | 0.757 | 0.766 | 0.778 | 0.989 | 0.807 | 0.553 | 0.011 | 0.000 | 94 |
| 3 | `row_aligned_weighted_selected_layers K=2 2-3-2_query+2-4-1` | 0.691 | 0.748 | 0.766 | 0.775 | 0.989 | 0.798 | 0.558 | 0.011 | 0.000 | 94 |
| 4 | `vector_average_norm_weighted_uniform_l31_bothk15 K=2 2-3-2_query+2-4-1` | 0.702 | 0.750 | 0.766 | 0.772 | 0.989 | 0.788 | 0.652 | 0.011 | 0.000 | 94 |
| 5 | `vector_average_component_norm_uniform_l29_bothk15 K=2 2-3-2_query+2-4-1` | 0.702 | 0.737 | 0.766 | 0.752 | 0.979 | 0.770 | 0.583 | 0.011 | 0.000 | 94 |
| 6 | `vector_average_component_norm K=2 2-3-2_query+2-4-1` | 0.713 | 0.767 | 0.755 | 0.774 | 0.989 | 0.814 | 0.590 | 0.011 | 0.011 | 94 |
| 7 | `vector_average_norm_weighted_uniform_l30_bothk15 K=2 2-3-2_query+2-4-1` | 0.702 | 0.756 | 0.755 | 0.770 | 0.989 | 0.804 | 0.596 | 0.011 | 0.011 | 94 |
| 8 | `row_aligned_unweighted_selected_layers K=2 2-3-2_query+2-4-1` | 0.723 | 0.760 | 0.755 | 0.769 | 0.989 | 0.801 | 0.565 | 0.011 | 0.011 | 94 |
| 9 | `maxsim_sum_uniform_l31_bothk15 K=2 2-3-2_query+2-4-1` | 0.691 | 0.744 | 0.755 | 0.767 | 0.989 | 0.791 | 0.648 | 0.011 | 0.011 | 94 |
| 10 | `vertical_concat_component_norm K=2 2-3-2_query+2-4-1` | 0.713 | 0.747 | 0.755 | 0.766 | 0.989 | 0.795 | 0.570 | 0.021 | 0.021 | 94 |
| 11 | `vector_average_component_norm_uniform_l30_bothk15 K=2 2-3-2_query+2-4-1` | 0.681 | 0.739 | 0.755 | 0.763 | 0.989 | 0.792 | 0.594 | 0.011 | 0.011 | 94 |
| 12 | `vertical_concat_norm_weighted_uniform_l31_bothk15 K=2 2-3-2_query+2-4-1` | 0.681 | 0.735 | 0.755 | 0.763 | 0.989 | 0.787 | 0.643 | 0.011 | 0.011 | 94 |
| 13 | `row_aligned_weighted_selected_layers_uniform_l31_bothk15 K=2 2-3-2_query+2-4-1` | 0.681 | 0.735 | 0.755 | 0.763 | 0.989 | 0.787 | 0.645 | 0.011 | 0.011 | 94 |
| 14 | `vector_average_norm_weighted_uniform_l29_bothk15 K=2 2-3-2_query+2-4-1` | 0.702 | 0.751 | 0.755 | 0.762 | 0.979 | 0.796 | 0.588 | 0.011 | 0.011 | 94 |
| 15 | `maxsim_sum_uniform_l29_bothk15 K=2 2-3-2_query+2-4-1` | 0.702 | 0.744 | 0.755 | 0.761 | 0.979 | 0.792 | 0.600 | 0.011 | 0.011 | 94 |
| 16 | `vector_average_component_norm_uniform_l31_bothk15 K=2 2-3-2_query+2-4-1` | 0.702 | 0.739 | 0.755 | 0.760 | 0.989 | 0.772 | 0.655 | 0.011 | 0.011 | 94 |
| 17 | `maxsim_sum K=2 2-3-2_query+2-4-1` | 0.681 | 0.749 | 0.745 | 0.760 | 0.989 | 0.797 | 0.585 | 0.021 | 0.032 | 94 |
| 18 | `vertical_concat_component_norm_uniform_l30_bothk15 K=2 2-3-2_query+2-4-1` | 0.681 | 0.736 | 0.745 | 0.759 | 0.979 | 0.787 | 0.591 | 0.011 | 0.021 | 94 |
| 19 | `vertical_concat_component_norm_uniform_l31_bothk15 K=2 2-3-2_query+2-4-1` | 0.681 | 0.740 | 0.745 | 0.759 | 0.989 | 0.787 | 0.632 | 0.011 | 0.021 | 94 |
| 20 | `maxsim_sum_uniform_l30_bothk15 K=2 2-3-2_query+2-4-1` | 0.681 | 0.737 | 0.745 | 0.758 | 0.979 | 0.790 | 0.597 | 0.011 | 0.021 | 94 |

Elapsed: 8m17s
