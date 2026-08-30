# Temporary agreement second-stage rerank

All rows keep only candidates with `source_count >= 2`, then rerank with concat+BM25.

## Strategy Oracle

### `prompt3_bm25_top20`

| min source count | avg candidate count | oracle recall_all |
|---:|---:|---:|
| 1 | 49.8 | 0.968 |
| 2 | 17.4 | 0.915 |
| 3 | 9.5 | 0.862 |
| 4 | 3.3 | 0.660 |

### `concat_bm25_top20`

| min source count | avg candidate count | oracle recall_all |
|---:|---:|---:|
| 1 | 34.9 | 0.947 |
| 2 | 5.1 | 0.670 |

### `concat_bm25_top50`

| min source count | avg candidate count | oracle recall_all |
|---:|---:|---:|
| 1 | 85.2 | 1.000 |
| 2 | 14.8 | 0.723 |

## Rerank Results

| rank | strategy | mode | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `prompt3_bm25_top20` | `score_only` | 0.50 | 0.691 | 0.766 | 0.777 | 0.801 | 0.814 | 1.000 | 94 |
| 2 | `prompt3_bm25_top20` | `score_only` | 0.85 | 0.734 | 0.807 | 0.766 | 0.819 | 0.854 | 1.000 | 94 |
| 3 | `prompt3_bm25_top20` | `score_only` | 0.75 | 0.723 | 0.801 | 0.766 | 0.817 | 0.847 | 1.000 | 94 |
| 4 | `prompt3_bm25_top20` | `score_only` | 0.65 | 0.723 | 0.800 | 0.766 | 0.810 | 0.839 | 0.989 | 94 |
| 5 | `prompt3_bm25_top20` | `score_only` | 1.00 | 0.713 | 0.788 | 0.766 | 0.806 | 0.839 | 1.000 | 94 |
| 6 | `prompt3_bm25_top20` | `agreement_first` | 0.50 | 0.691 | 0.756 | 0.766 | 0.785 | 0.801 | 1.000 | 94 |
| 7 | `prompt3_bm25_top20` | `agreement_first` | 0.85 | 0.702 | 0.780 | 0.755 | 0.798 | 0.825 | 1.000 | 94 |
| 8 | `prompt3_bm25_top20` | `agreement_first` | 0.75 | 0.702 | 0.776 | 0.755 | 0.796 | 0.821 | 1.000 | 94 |
| 9 | `prompt3_bm25_top20` | `agreement_first` | 0.65 | 0.702 | 0.777 | 0.755 | 0.795 | 0.813 | 1.000 | 94 |
| 10 | `prompt3_bm25_top20` | `agreement_first` | 1.00 | 0.702 | 0.762 | 0.755 | 0.784 | 0.811 | 1.000 | 94 |
| 11 | `concat_bm25_top50` | `score_only` | 0.65 | 0.638 | 0.719 | 0.702 | 0.739 | 0.763 | 0.979 | 94 |
| 12 | `concat_bm25_top50` | `agreement_first` | 0.65 | 0.638 | 0.719 | 0.702 | 0.739 | 0.763 | 0.979 | 94 |
| 13 | `concat_bm25_top50` | `score_only` | 1.00 | 0.649 | 0.718 | 0.702 | 0.732 | 0.763 | 0.979 | 94 |
| 14 | `concat_bm25_top50` | `agreement_first` | 1.00 | 0.649 | 0.718 | 0.702 | 0.732 | 0.763 | 0.979 | 94 |
| 15 | `concat_bm25_top50` | `score_only` | 0.85 | 0.660 | 0.741 | 0.691 | 0.743 | 0.780 | 0.979 | 94 |
| 16 | `concat_bm25_top50` | `agreement_first` | 0.85 | 0.660 | 0.741 | 0.691 | 0.743 | 0.780 | 0.979 | 94 |
| 17 | `concat_bm25_top50` | `score_only` | 0.75 | 0.649 | 0.736 | 0.691 | 0.742 | 0.772 | 0.979 | 94 |
| 18 | `concat_bm25_top50` | `agreement_first` | 0.75 | 0.649 | 0.736 | 0.691 | 0.742 | 0.772 | 0.979 | 94 |
| 19 | `concat_bm25_top50` | `score_only` | 0.50 | 0.617 | 0.700 | 0.691 | 0.725 | 0.750 | 0.979 | 94 |
| 20 | `concat_bm25_top50` | `agreement_first` | 0.50 | 0.617 | 0.700 | 0.691 | 0.725 | 0.750 | 0.979 | 94 |
| 21 | `concat_bm25_top20` | `score_only` | 0.65 | 0.617 | 0.704 | 0.660 | 0.713 | 0.739 | 0.947 | 94 |
| 22 | `concat_bm25_top20` | `agreement_first` | 0.65 | 0.617 | 0.704 | 0.660 | 0.713 | 0.739 | 0.947 | 94 |
| 23 | `concat_bm25_top20` | `score_only` | 0.75 | 0.617 | 0.704 | 0.649 | 0.713 | 0.739 | 0.947 | 94 |
| 24 | `concat_bm25_top20` | `agreement_first` | 0.75 | 0.617 | 0.704 | 0.649 | 0.713 | 0.739 | 0.947 | 94 |
| 25 | `concat_bm25_top20` | `score_only` | 0.85 | 0.617 | 0.705 | 0.649 | 0.712 | 0.742 | 0.947 | 94 |
| 26 | `concat_bm25_top20` | `agreement_first` | 0.85 | 0.617 | 0.705 | 0.649 | 0.712 | 0.742 | 0.947 | 94 |
| 27 | `concat_bm25_top20` | `score_only` | 1.00 | 0.617 | 0.696 | 0.649 | 0.704 | 0.744 | 0.947 | 94 |
| 28 | `concat_bm25_top20` | `agreement_first` | 1.00 | 0.617 | 0.696 | 0.649 | 0.704 | 0.744 | 0.947 | 94 |
| 29 | `concat_bm25_top20` | `score_only` | 0.50 | 0.596 | 0.681 | 0.649 | 0.698 | 0.725 | 0.947 | 94 |
| 30 | `concat_bm25_top20` | `agreement_first` | 0.50 | 0.596 | 0.681 | 0.649 | 0.698 | 0.725 | 0.947 | 94 |

## Inputs

- dump_dir: `/Users/gordonxiong/Desktop/Repos/memory_state/tensors/stage3/prompt_sweep/merged_subset0-100_cache2gb_logits256`
- config: `concat_k3_norm_weighted_userword_tag_assoc`
- alphas: [0.5, 0.65, 0.75, 0.85, 1.0]
- elapsed_seconds: 57.3
