# PrefEval Automatic Retrieval

- Created UTC: `2026-05-12T23:55:54.311219+00:00`
- Task: `implicit_persona`
- Dataset: `synthetic`
- Items: `6`
- Gold policy: `same_preference_text`
- Elapsed: `0s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `sweep_2-7_L31_both_k15` | 0.000 | 0.500 | 0.833 | 0.294 | 0.423 | 0.317 |

## Configs

- `sweep_2-7_L31_both_k15`: prompt sweep single cell: 2-7, L31, anti_pca_both_k15

## Prompt Notes

- Sweep: `prompt_sweep_l28_l29_l30_l31_both_k15`
- New preference prompts: `user_preference`, `user_avoidance`, `personalization_need`
- Token wording treatments: `2-1_token`, `user_preference_token`
- Pruned after n=100: `1-1_CN`, `1-1_CN_ASCII`, `1-1_EN`, `2-3-2_mem`, `2-4-1`, `2-6`, `2-7`, `2-8`, `2-4-1_user_word_represent`, `2-5_represent`, `2-7_represent`, `2-8_represent`
- Note: PrefEval n=1000 uses a pruned prompt sweep. The 2-1 topic prompt is useful for the target companion scenario but may partly fit PrefEval's topic-structured rows, so it is tracked with a token wording treatment.
