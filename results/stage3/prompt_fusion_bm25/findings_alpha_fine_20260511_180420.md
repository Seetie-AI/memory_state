# Stage 3 prompt fusion + BM25 sweep

This run adds BM25 score fusion over saved Stage 3 prompt-vector configs.

BM25 scope: `full`.

| rank | config | alpha | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.65 | 0.777 | 0.810 | 0.834 | 1.000 | 94 |
| 2 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.60 | 0.777 | 0.806 | 0.825 | 1.000 | 94 |
| 3 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.80 | 0.766 | 0.820 | 0.853 | 1.000 | 94 |
| 4 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.85 | 0.766 | 0.819 | 0.849 | 1.000 | 94 |
| 5 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.75 | 0.766 | 0.818 | 0.848 | 1.000 | 94 |
| 6 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.70 | 0.766 | 0.816 | 0.844 | 0.989 | 94 |
| 7 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.95 | 0.766 | 0.809 | 0.842 | 1.000 | 94 |
| 8 | `concat_k3_norm_weighted_userword_tag_assoc` | 0.90 | 0.766 | 0.807 | 0.836 | 1.000 | 94 |
| 9 | `concat_k3_norm_weighted_userword_tag_assoc` | 1.00 | 0.766 | 0.806 | 0.839 | 1.000 | 94 |
| 10 | `single_P0_l30_both` | 0.70 | 0.766 | 0.790 | 0.821 | 0.989 | 94 |
| 11 | `single_P0_l30_both` | 0.80 | 0.766 | 0.788 | 0.819 | 0.989 | 94 |
| 12 | `single_P0_l30_both` | 0.75 | 0.766 | 0.785 | 0.813 | 0.989 | 94 |
| 13 | `single_P0_l30_both` | 0.85 | 0.766 | 0.784 | 0.808 | 0.989 | 94 |
| 14 | `single_P0_l30_both` | 0.65 | 0.766 | 0.782 | 0.802 | 0.989 | 94 |
| 15 | `single_P0_l30_both` | 0.90 | 0.766 | 0.781 | 0.808 | 0.989 | 94 |
| 16 | `single_1-3_l31_both` | 0.90 | 0.755 | 0.787 | 0.815 | 1.000 | 94 |
| 17 | `single_1-3_l31_both` | 0.95 | 0.755 | 0.786 | 0.805 | 1.000 | 94 |
| 18 | `single_1-3_l31_both` | 1.00 | 0.755 | 0.784 | 0.805 | 1.000 | 94 |
| 19 | `single_P0_l30_both` | 1.00 | 0.755 | 0.779 | 0.814 | 0.989 | 94 |
| 20 | `single_P0_l30_both` | 0.95 | 0.755 | 0.779 | 0.812 | 0.989 | 94 |
| 21 | `single_P0_l30_both` | 0.60 | 0.755 | 0.771 | 0.796 | 0.989 | 94 |
| 22 | `single_1-3_l31_both` | 0.75 | 0.745 | 0.802 | 0.836 | 1.000 | 94 |
| 23 | `single_1-3_l31_both` | 0.85 | 0.745 | 0.791 | 0.826 | 1.000 | 94 |
| 24 | `single_1-3_l31_both` | 0.70 | 0.734 | 0.801 | 0.841 | 1.000 | 94 |
| 25 | `single_1-3_l31_both` | 0.80 | 0.734 | 0.797 | 0.837 | 1.000 | 94 |
| 26 | `single_1-3_l31_both` | 0.65 | 0.734 | 0.787 | 0.820 | 1.000 | 94 |
| 27 | `single_1-3_l31_both` | 0.60 | 0.734 | 0.779 | 0.808 | 1.000 | 94 |

## Alpha=1.0 Self-Checks

All alpha=1.0 rows are checked against hard-coded vector-only baselines at 1e-6 tolerance.

## Inputs

- configs: concat_k3_norm_weighted_userword_tag_assoc, single_1-3_l31_both, single_P0_l30_both
- alphas: [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
- elapsed: 1m33s
