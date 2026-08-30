# PrefEval Automatic Retrieval

- Created UTC: `2026-05-13T01:57:23.418567+00:00`
- Task: `implicit_persona`
- Dataset: `siyanzhao/prefeval_implicit_persona`
- Items: `1000`
- Gold policy: `same_preference_text`
- Elapsed: `8m15s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `qwen3_embedding_bm25` | 0.087 | 0.195 | 0.267 | 0.148 | 0.178 | 0.180 |
| 2 | `bm25` | 0.035 | 0.074 | 0.094 | 0.058 | 0.066 | 0.067 |

## Configs

- `qwen3_embedding_bm25`: Qwen3-Embedding-8B + BM25 z-score fusion, alpha=0.75
- `bm25`: BM25 over preference memory strings

## Prompt Notes

- Sweep: `prompt_sweep_l28_l29_l30_l31_both_k15`
- New preference prompts: `user_preference`, `user_avoidance`, `personalization_need`
- Token wording treatments: `2-1_token`, `user_preference_token`
- Pruned after n=100: `1-1_CN`, `1-1_CN_ASCII`, `1-1_EN`, `2-3-2_mem`, `2-4-1`, `2-6`, `2-7`, `2-8`, `2-4-1_user_word_represent`, `2-5_represent`, `2-7_represent`, `2-8_represent`
- Note: PrefEval n=1000 uses a pruned prompt sweep. The 2-1 topic prompt is useful for the target companion scenario but may partly fit PrefEval's topic-structured rows, so it is tracked with a token wording treatment.
