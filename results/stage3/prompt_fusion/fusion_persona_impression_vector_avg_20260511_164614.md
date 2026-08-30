# Stage 3 prompt fusion findings

This run reuses Stage 3 hidden vectors and does not rerun the model.

Storage budget: one bf16 prompt vector is 8KB; K=3 is 24KB per memory, inside the 10-100KB product target.

Single-vector baselines: best R@5=0.766; best NDCG@5=0.784.

## Selected Cells

| rank | cell | family |
|---:|---|---|
| 1 | `2-4-1|layer30|last|query_only_anti_pca_k2` | persona |
| 2 | `2-6|layer30|last|anti_pca_both_k15` | impression |

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
| 1 | `vector_average_norm_weighted K=2 2-4-1+2-6` | 0.670 | 0.730 | 0.734 | 0.760 | 0.989 | 0.769 | - | - | - | 94 |
| 2 | `vector_average_component_norm_uniform_l31_bothk15 K=2 2-4-1+2-6` | 0.660 | 0.715 | 0.734 | 0.745 | 0.979 | 0.774 | - | - | - | 94 |
| 3 | `vector_average_norm_weighted_uniform_l31_bothk15 K=2 2-4-1+2-6` | 0.681 | 0.724 | 0.734 | 0.745 | 0.979 | 0.774 | - | - | - | 94 |
| 4 | `vector_average_component_norm_uniform_l29_bothk15 K=2 2-4-1+2-6` | 0.670 | 0.735 | 0.723 | 0.760 | 0.979 | 0.786 | - | - | - | 94 |
| 5 | `vector_average_norm_weighted_uniform_l29_bothk15 K=2 2-4-1+2-6` | 0.681 | 0.732 | 0.723 | 0.753 | 0.979 | 0.777 | - | - | - | 94 |
| 6 | `vector_average_component_norm K=2 2-4-1+2-6` | 0.660 | 0.730 | 0.723 | 0.745 | 0.989 | 0.774 | - | - | - | 94 |
| 7 | `vector_average_component_norm_uniform_l30_bothk15 K=2 2-4-1+2-6` | 0.670 | 0.728 | 0.713 | 0.748 | 0.979 | 0.775 | - | - | - | 94 |
| 8 | `vector_average_norm_weighted_uniform_l30_bothk15 K=2 2-4-1+2-6` | 0.670 | 0.728 | 0.713 | 0.746 | 0.979 | 0.773 | - | - | - | 94 |

Elapsed: 2m27s
