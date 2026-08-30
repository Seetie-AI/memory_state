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

## Phase 1 Pairwise Complementarity

| pair | top5_jaccard | only_left_hit@5 | only_right_hit@5 | both_hit@5 |
|---|---:|---:|---:|---:|
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.459 | 0.064 | 0.021 | 0.702 |
| `1-3|layer31|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.471 | 0.043 | 0.011 | 0.713 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 1-1_CN|layer29|last|centered_cosine` | 0.486 | 0.043 | 0.032 | 0.723 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.490 | 0.043 | 0.032 | 0.723 |
| `1-3|layer31|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.514 | 0.021 | 0.021 | 0.734 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.514 | 0.032 | 0.021 | 0.723 |
| `1-3|layer31|last|anti_pca_both_k15 vs 1-1_CN|layer29|last|centered_cosine` | 0.525 | 0.021 | 0.021 | 0.734 |
| `2-1|layer30|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.530 | 0.043 | 0.011 | 0.713 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.530 | 0.043 | 0.011 | 0.713 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-3-1|layer30|last|anti_pca_both_k15` | 0.534 | 0.053 | 0.032 | 0.713 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.539 | 0.053 | 0.011 | 0.713 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.540 | 0.053 | 0.032 | 0.713 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 2-3-1|layer30|last|anti_pca_both_k15` | 0.542 | 0.032 | 0.021 | 0.723 |
| `P0|layer30|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.544 | 0.053 | 0.021 | 0.702 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.546 | 0.021 | 0.011 | 0.745 |
| `P0|layer30|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.548 | 0.021 | 0.021 | 0.734 |
| `1-1_CN|layer29|last|centered_cosine vs 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.551 | 0.032 | 0.021 | 0.723 |
| `1-1_CN|layer29|last|centered_cosine vs 2-1|layer30|last|anti_pca_both_k15` | 0.553 | 0.021 | 0.021 | 0.734 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.554 | 0.032 | 0.032 | 0.734 |
| `1-3|layer31|last|anti_pca_both_k15 vs 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.554 | 0.032 | 0.021 | 0.723 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs P0|layer30|last|anti_pca_both_k15` | 0.556 | 0.032 | 0.021 | 0.734 |
| `2-1|layer30|last|anti_pca_both_k15 vs 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.559 | 0.021 | 0.021 | 0.734 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 1-3|layer31|last|anti_pca_both_k15` | 0.560 | 0.021 | 0.011 | 0.745 |
| `2-3-2_mem|layer31|last|anti_pca_both_k15 vs 1-1_CN|layer29|last|centered_cosine` | 0.566 | 0.021 | 0.011 | 0.745 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 1-2|layer29|last|anti_pca_both_k15` | 0.569 | 0.053 | 0.032 | 0.713 |
| `2-3-2_query|layer29|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.570 | 0.032 | 0.011 | 0.713 |
| `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 vs 1-2|layer29|last|anti_pca_both_k15` | 0.571 | 0.021 | 0.011 | 0.734 |
| `1-2|layer29|last|anti_pca_both_k15 vs 2-5|layer29|last|query_only_anti_pca_k2` | 0.574 | 0.032 | 0.011 | 0.713 |
| `1-3|layer31|last|anti_pca_both_k15 vs 2-1|layer30|last|anti_pca_both_k15` | 0.579 | 0.011 | 0.011 | 0.745 |
| `2-4-1_user_word|layer30|last|anti_pca_both_k15 vs 2-1|layer30|last|anti_pca_both_k15` | 0.581 | 0.032 | 0.021 | 0.734 |

### Centered Future Work

- 1-1_CN|layer29|last|centered_cosine shows complementarity but is excluded from Phase 4 because centered cosine's per-query candidate mean is not a persistable vector transform.

## Phase 2 Asymmetric

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 -> 2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.681 | 0.734 | 0.766 | 0.751 | 0.979 | 0.777 | - | - | - | 94 |
| 2 | `1-3|layer31|last|anti_pca_both_k15 -> 1-3|layer31|last|anti_pca_both_k15` | 0.702 | 0.779 | 0.755 | 0.784 | 1.000 | 0.806 | - | - | - | 94 |
| 3 | `2-5|layer29|last|query_only_anti_pca_k2 -> 2-5|layer29|last|query_only_anti_pca_k2` | 0.691 | 0.726 | 0.723 | 0.747 | 0.968 | 0.771 | - | - | - | 94 |
| 4 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 -> 2-5|layer29|last|query_only_anti_pca_k2` | 0.628 | 0.626 | 0.702 | 0.666 | 0.957 | 0.670 | - | - | - | 94 |
| 5 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 -> 1-3|layer31|last|anti_pca_both_k15` | 0.638 | 0.662 | 0.691 | 0.686 | 0.957 | 0.710 | - | - | - | 94 |
| 6 | `2-5|layer29|last|query_only_anti_pca_k2 -> 1-3|layer31|last|anti_pca_both_k15` | 0.479 | 0.539 | 0.585 | 0.584 | 0.936 | 0.624 | - | - | - | 94 |
| 7 | `2-5|layer29|last|query_only_anti_pca_k2 -> 2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.319 | 0.387 | 0.404 | 0.426 | 0.787 | 0.474 | - | - | - | 94 |
| 8 | `1-3|layer31|last|anti_pca_both_k15 -> 2-5|layer29|last|query_only_anti_pca_k2` | 0.106 | 0.075 | 0.191 | 0.112 | 0.426 | 0.134 | - | - | - | 94 |
| 9 | `1-3|layer31|last|anti_pca_both_k15 -> 2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.117 | 0.106 | 0.160 | 0.129 | 0.404 | 0.173 | - | - | - | 94 |

## Phase 3 Score Fusion

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `zsum K=3 2-4-1_user_word+1-3+2-5` | 0.702 | 0.766 | 0.777 | 0.789 | 1.000 | 0.815 | 0.679 | 0.021 | 0.000 | 94 |
| 2 | `rrf K=3 2-4-1_user_word+1-3+2-5` | 0.713 | 0.767 | 0.766 | 0.783 | 1.000 | 0.808 | 0.646 | 0.011 | 0.000 | 94 |
| 3 | `rrf K=2 2-4-1_user_word+1-3` | 0.702 | 0.753 | 0.766 | 0.769 | 0.989 | 0.792 | 0.718 | 0.011 | 0.000 | 94 |
| 4 | `zsum K=2 2-4-1_user_word+1-3` | 0.713 | 0.771 | 0.755 | 0.782 | 0.989 | 0.814 | 0.750 | 0.000 | 0.000 | 94 |
| 5 | `rrf K=2 1-3+2-5` | 0.723 | 0.801 | 0.745 | 0.805 | 1.000 | 0.840 | 0.649 | 0.000 | 0.011 | 94 |
| 6 | `zsum K=2 1-3+2-5` | 0.734 | 0.789 | 0.745 | 0.794 | 1.000 | 0.827 | 0.625 | 0.011 | 0.021 | 94 |
| 7 | `rrf K=2 2-4-1_user_word+2-5` | 0.723 | 0.778 | 0.745 | 0.790 | 0.989 | 0.822 | 0.543 | 0.011 | 0.021 | 94 |
| 8 | `zsum K=2 2-4-1_user_word+2-5` | 0.723 | 0.759 | 0.745 | 0.770 | 0.989 | 0.803 | 0.554 | 0.011 | 0.021 | 94 |

## Phase 4 Vector Fusion

| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `vertical_concat_component_norm_uniform_l29_bothk15 K=2 2-4-1_user_word+1-3` | 0.681 | 0.763 | 0.777 | 0.787 | 0.989 | 0.813 | 0.664 | 0.021 | 0.000 | 94 |
| 2 | `row_aligned_weighted_same_layer30 K=2 2-4-1_user_word+1-3` | 0.702 | 0.769 | 0.777 | 0.786 | 0.989 | 0.814 | 0.699 | 0.021 | 0.000 | 94 |
| 3 | `row_aligned_weighted_selected_layers_uniform_l30_bothk15 K=2 2-4-1_user_word+1-3` | 0.702 | 0.769 | 0.777 | 0.786 | 0.989 | 0.814 | 0.699 | 0.021 | 0.000 | 94 |
| 4 | `vertical_concat_norm_weighted_uniform_l29_bothk15 K=2 2-4-1_user_word+1-3` | 0.681 | 0.755 | 0.777 | 0.786 | 0.989 | 0.804 | 0.688 | 0.021 | 0.000 | 94 |
| 5 | `vertical_concat_norm_weighted_uniform_l30_bothk15 K=2 2-4-1_user_word+1-3` | 0.691 | 0.763 | 0.777 | 0.785 | 0.989 | 0.814 | 0.690 | 0.021 | 0.000 | 94 |
| 6 | `maxsim_sum_uniform_l30_bothk15 K=2 2-4-1_user_word+1-3` | 0.691 | 0.758 | 0.777 | 0.784 | 0.989 | 0.812 | 0.656 | 0.021 | 0.000 | 94 |
| 7 | `vertical_concat_component_norm_uniform_l30_bothk15 K=2 2-4-1_user_word+1-3` | 0.691 | 0.762 | 0.777 | 0.777 | 0.989 | 0.808 | 0.669 | 0.021 | 0.000 | 94 |
| 8 | `vertical_concat_norm_weighted K=3 2-4-1_user_word+1-3+2-5` | 0.713 | 0.788 | 0.766 | 0.806 | 1.000 | 0.839 | 0.644 | 0.021 | 0.011 | 94 |
| 9 | `row_aligned_weighted_selected_layers K=3 2-4-1_user_word+1-3+2-5` | 0.713 | 0.777 | 0.766 | 0.800 | 1.000 | 0.827 | 0.664 | 0.021 | 0.011 | 94 |
| 10 | `vertical_concat_component_norm K=2 1-3+2-5` | 0.713 | 0.781 | 0.766 | 0.793 | 1.000 | 0.820 | 0.727 | 0.011 | 0.000 | 94 |
| 11 | `maxsim_sum K=2 1-3+2-5` | 0.691 | 0.769 | 0.766 | 0.789 | 1.000 | 0.809 | 0.768 | 0.011 | 0.000 | 94 |
| 12 | `vertical_concat_component_norm K=3 2-4-1_user_word+1-3+2-5` | 0.702 | 0.772 | 0.766 | 0.786 | 1.000 | 0.816 | 0.712 | 0.011 | 0.000 | 94 |
| 13 | `maxsim_sum K=3 2-4-1_user_word+1-3+2-5` | 0.691 | 0.753 | 0.766 | 0.781 | 1.000 | 0.802 | 0.727 | 0.011 | 0.000 | 94 |
| 14 | `row_aligned_weighted_selected_layers_uniform_l29_bothk15 K=2 2-4-1_user_word+1-3` | 0.702 | 0.760 | 0.766 | 0.781 | 0.989 | 0.801 | 0.690 | 0.021 | 0.011 | 94 |
| 15 | `maxsim_sum_uniform_l29_bothk15 K=2 2-4-1_user_word+1-3` | 0.681 | 0.749 | 0.766 | 0.773 | 0.989 | 0.796 | 0.640 | 0.011 | 0.000 | 94 |
| 16 | `vertical_concat_norm_weighted K=2 1-3+2-5` | 0.734 | 0.799 | 0.755 | 0.806 | 1.000 | 0.840 | 0.625 | 0.011 | 0.011 | 94 |
| 17 | `vertical_concat_norm_weighted_uniform_l31_bothk15 K=3 2-4-1_user_word+1-3+2-5` | 0.723 | 0.771 | 0.755 | 0.795 | 0.989 | 0.819 | 0.712 | 0.011 | 0.011 | 94 |
| 18 | `vertical_concat_component_norm_uniform_l31_bothk15 K=3 2-4-1_user_word+1-3+2-5` | 0.723 | 0.771 | 0.755 | 0.789 | 0.989 | 0.814 | 0.697 | 0.011 | 0.011 | 94 |
| 19 | `row_aligned_unweighted_selected_layers K=3 2-4-1_user_word+1-3+2-5` | 0.723 | 0.765 | 0.755 | 0.787 | 1.000 | 0.810 | 0.634 | 0.011 | 0.011 | 94 |
| 20 | `vertical_concat_component_norm K=2 2-4-1_user_word+1-3` | 0.713 | 0.772 | 0.755 | 0.783 | 0.989 | 0.813 | 0.773 | 0.000 | 0.000 | 94 |

Elapsed: 12m52s
