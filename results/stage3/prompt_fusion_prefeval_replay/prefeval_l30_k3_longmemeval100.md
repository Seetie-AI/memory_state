# PrefEval final replay on LongMemEval

Offline replay of the PrefEval K3 setup on LongMemEval-S round candidates.

| rank | config | phase | R@1 | R@3 | NDCG@3 | R@5 | NDCG@5 | R@50 | MRR | n |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `prefeval_final_full_d0.60_b0.10_e0.30` | full_score_fusion | 0.532 | 0.745 | 0.797 | 0.766 | 0.805 | 0.989 | 0.831 | 94 |
| 2 | `five_source_top20_source_ge2_prefeval_final` | shortlist_score_fusion | 0.532 | 0.745 | 0.797 | 0.766 | 0.805 | 0.979 | 0.831 | 94 |
| 3 | `k3_bm25_full_d0.75_b0.25` | full_score_fusion | 0.543 | 0.723 | 0.785 | 0.766 | 0.798 | 0.968 | 0.823 | 94 |
| 4 | `prefeval_alt_full_d0.60_b0.30_e0.10` | full_score_fusion | 0.521 | 0.723 | 0.782 | 0.766 | 0.802 | 0.968 | 0.825 | 94 |
| 5 | `k3_embedding_full_d0.90_e0.10` | full_score_fusion | 0.489 | 0.723 | 0.759 | 0.745 | 0.765 | 0.957 | 0.784 | 94 |
| 6 | `source_ge3_plus_embedding_top20_d0.90_e0.10` | shortlist_score_fusion | 0.489 | 0.723 | 0.759 | 0.745 | 0.766 | 0.979 | 0.784 | 94 |
| 7 | `k3_vector_average` | baseline | 0.468 | 0.723 | 0.744 | 0.745 | 0.752 | 0.957 | 0.767 | 94 |
| 8 | `embedding_only` | baseline | 0.511 | 0.681 | 0.765 | 0.755 | 0.789 | 0.979 | 0.826 | 94 |
| 9 | `bm25_only` | baseline | 0.340 | 0.521 | 0.515 | 0.585 | 0.547 | 0.734 | 0.559 | 94 |

## Inputs

- dump_dir: `/Users/gordonxiong/Desktop/Repos/memory_state/tensors/stage3/prompt_sweep/prefeval_final_l30_lme100`
- embedding_dir: `/Users/gordonxiong/Desktop/Repos/memory_state/tensors/stage3/embedding_eval/qwen3_embedding_8b_dwq_subset0-100`
- cells: 2-3-1_mark, 2-5_token, 2-8_emoji
- elapsed: 52.2s
