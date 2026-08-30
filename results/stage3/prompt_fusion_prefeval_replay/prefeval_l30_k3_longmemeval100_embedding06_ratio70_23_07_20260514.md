# PrefEval final replay on LongMemEval

Offline replay of the PrefEval K3 setup on LongMemEval-S round candidates.

| rank | config | phase | R@1 | R@3 | NDCG@3 | R@5 | NDCG@5 | R@50 | MRR | n |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `mixed_ratio_full_basealpha0.85_base0.75_qwen0.25` | full_score_fusion | 0.543 | 0.723 | 0.793 | 0.755 | 0.805 | 0.979 | 0.830 | 94 |
| 2 | `k3_bm25_full_d0.75_b0.25` | full_score_fusion | 0.543 | 0.723 | 0.785 | 0.766 | 0.798 | 0.968 | 0.823 | 94 |
| 3 | `prefeval_ratio_full_d0.70_b0.07_e0.23` | full_score_fusion | 0.532 | 0.723 | 0.785 | 0.755 | 0.794 | 0.968 | 0.819 | 94 |
| 4 | `k3_embedding_full_d0.90_e0.10` | full_score_fusion | 0.489 | 0.723 | 0.757 | 0.745 | 0.763 | 0.957 | 0.781 | 94 |
| 5 | `source_ge3_plus_embedding_top20_d0.90_e0.10` | shortlist_score_fusion | 0.489 | 0.723 | 0.757 | 0.745 | 0.764 | 0.979 | 0.782 | 94 |
| 6 | `k3_vector_average` | baseline | 0.468 | 0.723 | 0.744 | 0.745 | 0.752 | 0.957 | 0.767 | 94 |
| 7 | `prefeval_final_full_d0.60_b0.10_e0.30` | full_score_fusion | 0.532 | 0.713 | 0.790 | 0.755 | 0.801 | 0.979 | 0.824 | 94 |
| 8 | `five_source_top20_source_ge2_prefeval_final` | shortlist_score_fusion | 0.532 | 0.713 | 0.790 | 0.755 | 0.801 | 0.979 | 0.824 | 94 |
| 9 | `prefeval_alt_full_d0.60_b0.30_e0.10` | full_score_fusion | 0.521 | 0.713 | 0.776 | 0.766 | 0.798 | 0.968 | 0.818 | 94 |
| 10 | `embedding_only` | baseline | 0.521 | 0.691 | 0.801 | 0.734 | 0.811 | 0.989 | 0.854 | 94 |
| 11 | `bm25_only` | baseline | 0.340 | 0.521 | 0.515 | 0.585 | 0.547 | 0.734 | 0.559 | 94 |

## Inputs

- dump_dir: `/Users/gordonxiong/Desktop/Repos/memory_state/tensors/stage3/prompt_sweep/prefeval_final_l30_lme100`
- embedding_dir: `tensors/stage3/embedding_eval/qwen3_embedding_06b_dwq_subset0-100`
- cells: 2-3-1_mark, 2-5_token, 2-8_emoji
- elapsed: 47.3s
