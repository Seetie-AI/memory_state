# PrefEval Automatic Retrieval

- Created UTC: `2026-05-12T01:07:43.294297+00:00`
- Task: `implicit_persona`
- Dataset: `synthetic`
- Items: `6`
- Gold policy: `same_preference_text`
- Elapsed: `0s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `k3_concat_selected` | 0.333 | 0.833 | 1.000 | 0.605 | 0.670 | 0.561 |
| 2 | `sweep_1-3_L31_both_k15` | 0.333 | 0.667 | 1.000 | 0.522 | 0.658 | 0.547 |
| 3 | `sweep_2-8_represent_L31_both_k15` | 0.333 | 0.667 | 1.000 | 0.522 | 0.651 | 0.539 |
| 4 | `sweep_2-3-2_mem_L31_both_k15` | 0.167 | 0.500 | 1.000 | 0.377 | 0.592 | 0.458 |
| 5 | `sweep_2-4-1_L31_both_k15` | 0.167 | 0.667 | 1.000 | 0.438 | 0.575 | 0.436 |
| 6 | `sweep_2-8_L31_both_k15` | 0.167 | 0.667 | 1.000 | 0.438 | 0.575 | 0.436 |
| 7 | `k3_concat_selected_represent_control` | 0.000 | 0.833 | 1.000 | 0.504 | 0.568 | 0.422 |
| 8 | `sweep_2-5_L31_both_k15` | 0.000 | 0.667 | 1.000 | 0.377 | 0.521 | 0.361 |
| 9 | `bm25` | 0.000 | 0.500 | 1.000 | 0.315 | 0.516 | 0.358 |
| 10 | `sweep_2-6_L31_both_k15` | 0.000 | 0.333 | 1.000 | 0.210 | 0.483 | 0.317 |
| 11 | `sweep_1-1_CN_L31_both_k15` | 0.000 | 0.500 | 1.000 | 0.272 | 0.480 | 0.311 |
| 12 | `sweep_2-3-1_L31_both_k15` | 0.000 | 0.333 | 1.000 | 0.188 | 0.454 | 0.281 |
| 13 | `sweep_P0_L31_both_k15` | 0.000 | 0.500 | 1.000 | 0.250 | 0.443 | 0.267 |
| 14 | `sweep_2-4-1_user_word_L31_both_k15` | 0.500 | 0.667 | 0.833 | 0.605 | 0.677 | 0.653 |
| 15 | `sweep_2-4-2_L31_both_k15` | 0.167 | 0.667 | 0.833 | 0.460 | 0.525 | 0.450 |
| 16 | `sweep_2-7_represent_L31_both_k15` | 0.167 | 0.167 | 0.833 | 0.167 | 0.439 | 0.344 |
| 17 | `sweep_1-1_EN_L31_both_k15` | 0.000 | 0.500 | 0.833 | 0.294 | 0.437 | 0.333 |
| 18 | `sweep_2-7_L31_both_k15` | 0.000 | 0.500 | 0.833 | 0.294 | 0.423 | 0.317 |
| 19 | `sweep_2-4-1_user_word_represent_L31_both_k15` | 0.000 | 0.333 | 0.833 | 0.210 | 0.418 | 0.311 |
| 20 | `sweep_2-1_L31_both_k15` | 0.167 | 0.500 | 0.667 | 0.355 | 0.420 | 0.394 |
| 21 | `sweep_2-3-2_query_L31_both_k15` | 0.000 | 0.333 | 0.667 | 0.210 | 0.339 | 0.289 |
| 22 | `sweep_2-5_represent_L31_both_k15` | 0.000 | 0.167 | 0.667 | 0.105 | 0.306 | 0.247 |
| 23 | `sweep_1-1_CN_ASCII_L31_both_k15` | 0.000 | 0.167 | 0.667 | 0.083 | 0.299 | 0.236 |
| 24 | `sweep_1-2_L31_both_k15` | 0.333 | 0.500 | 0.500 | 0.417 | 0.417 | 0.472 |

## Configs

- `k3_concat_selected`: Stage 3 selected K3 concat layers/transforms, mark-default prompt wording
- `sweep_1-3_L31_both_k15`: prompt sweep single cell: 1-3, L31, anti_pca_both_k15
- `sweep_2-8_represent_L31_both_k15`: prompt sweep single cell: 2-8_represent, L31, anti_pca_both_k15
- `sweep_2-3-2_mem_L31_both_k15`: prompt sweep single cell: 2-3-2_mem, L31, anti_pca_both_k15
- `sweep_2-4-1_L31_both_k15`: prompt sweep single cell: 2-4-1, L31, anti_pca_both_k15
- `sweep_2-8_L31_both_k15`: prompt sweep single cell: 2-8, L31, anti_pca_both_k15
- `k3_concat_selected_represent_control`: Stage 3 selected K3 concat with old represent wording for user/association controls
- `sweep_2-5_L31_both_k15`: prompt sweep single cell: 2-5, L31, anti_pca_both_k15
- `bm25`: BM25 over preference memory strings
- `sweep_2-6_L31_both_k15`: prompt sweep single cell: 2-6, L31, anti_pca_both_k15
- `sweep_1-1_CN_L31_both_k15`: prompt sweep single cell: 1-1_CN, L31, anti_pca_both_k15
- `sweep_2-3-1_L31_both_k15`: prompt sweep single cell: 2-3-1, L31, anti_pca_both_k15
- `sweep_P0_L31_both_k15`: prompt sweep single cell: P0, L31, anti_pca_both_k15
- `sweep_2-4-1_user_word_L31_both_k15`: prompt sweep single cell: 2-4-1_user_word, L31, anti_pca_both_k15
- `sweep_2-4-2_L31_both_k15`: prompt sweep single cell: 2-4-2, L31, anti_pca_both_k15
- `sweep_2-7_represent_L31_both_k15`: prompt sweep single cell: 2-7_represent, L31, anti_pca_both_k15
- `sweep_1-1_EN_L31_both_k15`: prompt sweep single cell: 1-1_EN, L31, anti_pca_both_k15
- `sweep_2-7_L31_both_k15`: prompt sweep single cell: 2-7, L31, anti_pca_both_k15
- `sweep_2-4-1_user_word_represent_L31_both_k15`: prompt sweep single cell: 2-4-1_user_word_represent, L31, anti_pca_both_k15
- `sweep_2-1_L31_both_k15`: prompt sweep single cell: 2-1, L31, anti_pca_both_k15
- `sweep_2-3-2_query_L31_both_k15`: prompt sweep single cell: 2-3-2_query, L31, anti_pca_both_k15
- `sweep_2-5_represent_L31_both_k15`: prompt sweep single cell: 2-5_represent, L31, anti_pca_both_k15
- `sweep_1-1_CN_ASCII_L31_both_k15`: prompt sweep single cell: 1-1_CN_ASCII, L31, anti_pca_both_k15
- `sweep_1-2_L31_both_k15`: prompt sweep single cell: 1-2, L31, anti_pca_both_k15

## Prompt Notes

- `2-7`: `
用一个词标记上面这段对话的互动模式，这个词是：“`
- `2-8`: `
用一个词标记回答上面这段对话中的对方时最该采用的策略，这个词是：“`
