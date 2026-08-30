# Temporary union top20 prompt + BM25 fusion

Candidate set per query: top20 from each of the three prompt cells plus top20 BM25, then rerank inside the union.

## Union Ceiling

- avg union size: 49.8
- max union size: 63
- oracle recall_all within union: 0.968

## Source Oracle Recall

- `1-3|layer31|last|anti_pca_both_k15`: 0.883
- `2-4-1_user_word|layer30|last|anti_pca_both_k15`: 0.894
- `2-5|layer29|last|query_only_anti_pca_k2`: 0.926
- `bm25`: 0.681

## Rerank Results

| rank | method | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `prompt_zsum_bm25` | 1.00 | 0.713 | 0.768 | 0.777 | 0.793 | 0.819 | 1.000 | 94 |
| 2 | `concat_bm25` | 0.65 | 0.713 | 0.805 | 0.766 | 0.821 | 0.854 | 0.989 | 94 |
| 3 | `concat_bm25` | 0.85 | 0.734 | 0.805 | 0.766 | 0.816 | 0.844 | 1.000 | 94 |
| 4 | `concat_bm25` | 0.75 | 0.723 | 0.803 | 0.766 | 0.815 | 0.842 | 1.000 | 94 |
| 5 | `prompt_zsum_bm25` | 0.85 | 0.723 | 0.793 | 0.766 | 0.809 | 0.846 | 1.000 | 94 |
| 6 | `prompt_zsum_bm25` | 0.75 | 0.691 | 0.785 | 0.766 | 0.808 | 0.851 | 1.000 | 94 |
| 7 | `concat_bm25` | 1.00 | 0.713 | 0.788 | 0.766 | 0.806 | 0.839 | 1.000 | 94 |
| 8 | `prompt_zsum_bm25` | 0.65 | 0.691 | 0.778 | 0.766 | 0.804 | 0.838 | 1.000 | 94 |
| 9 | `concat_bm25` | 0.50 | 0.670 | 0.744 | 0.766 | 0.782 | 0.797 | 1.000 | 94 |
| 10 | `rrf_prompt3_bm25` |  | 0.702 | 0.762 | 0.755 | 0.784 | 0.815 | 1.000 | 94 |
| 11 | `prompt_zsum_bm25` | 0.50 | 0.681 | 0.752 | 0.755 | 0.778 | 0.803 | 1.000 | 94 |
| 12 | `concat_bm25` | 0.25 | 0.574 | 0.629 | 0.660 | 0.663 | 0.688 | 0.936 | 94 |
| 13 | `prompt_zsum_bm25` | 0.25 | 0.574 | 0.628 | 0.649 | 0.662 | 0.688 | 0.936 | 94 |
| 14 | `concat_bm25` | 0.00 | 0.521 | 0.515 | 0.585 | 0.547 | 0.562 | 0.862 | 94 |
| 15 | `prompt_zsum_bm25` | 0.00 | 0.521 | 0.515 | 0.585 | 0.547 | 0.562 | 0.862 | 94 |

## Inputs

- dump_dir: `/Users/gordonxiong/Desktop/Repos/memory_state/tensors/stage3/prompt_sweep/merged_subset0-100_cache2gb_logits256`
- config: `concat_k3_norm_weighted_userword_tag_assoc`
- per_source_top_k: 20
- alphas: [0.0, 0.25, 0.5, 0.65, 0.75, 0.85, 1.0]
- elapsed_seconds: 54.8
