# PrefEval Automatic Retrieval

- Created UTC: `2026-05-12T00:48:00.345860+00:00`
- Task: `implicit_persona`
- Dataset: `synthetic`
- Items: `6`
- Gold policy: `same_preference_text`
- Elapsed: `0s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `k3_concat_selected` | 0.333 | 0.833 | 1.000 | 0.605 | 0.670 | 0.561 |
| 2 | `single_1-3` | 0.333 | 0.667 | 1.000 | 0.522 | 0.658 | 0.547 |
| 3 | `k3_concat_uniform_l31_both_k15` | 0.167 | 0.667 | 1.000 | 0.460 | 0.604 | 0.472 |
| 4 | `persona_2-8` | 0.167 | 0.667 | 1.000 | 0.438 | 0.575 | 0.436 |
| 5 | `bm25` | 0.000 | 0.500 | 1.000 | 0.315 | 0.516 | 0.358 |
| 6 | `persona_2-7` | 0.000 | 0.500 | 0.833 | 0.294 | 0.423 | 0.317 |
| 7 | `qwen3_embedding_bm25` | 0.000 | 0.333 | 0.833 | 0.188 | 0.397 | 0.283 |

## Configs

- `k3_concat_selected`: best Stage 3 K3 concat: selected layers/transforms, vertical_concat_norm_weighted
- `single_1-3`: single hidden-state prompt 1-3, L31, anti_pca_both_k15
- `k3_concat_uniform_l31_both_k15`: same three prompts, all L31, all anti_pca_both_k15; overfit check
- `persona_2-8`: single answer-strategy prompt 2-8, L31, anti_pca_both_k15, verb=标记
- `bm25`: BM25 over preference memory strings
- `persona_2-7`: single persona/interaction-pattern prompt 2-7, L31, anti_pca_both_k15, verb=标记
- `qwen3_embedding_bm25`: Qwen3-Embedding-8B + BM25 z-score fusion, alpha=0.75

## Prompt Notes

- `2-7`: `
用一个词标记上面这段对话的互动模式，这个词是：“`
- `2-8`: `
用一个词标记回答上面这段对话中的对方时最该采用的策略，这个词是：“`
