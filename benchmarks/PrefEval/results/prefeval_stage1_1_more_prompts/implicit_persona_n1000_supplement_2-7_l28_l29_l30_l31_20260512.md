# PrefEval Automatic Retrieval

- Created UTC: `2026-05-13T00:37:17.945342+00:00`
- Task: `implicit_persona`
- Dataset: `siyanzhao/prefeval_implicit_persona`
- Items: `1000`
- Gold policy: `same_preference_text`
- Elapsed: `38m39s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `sweep_2-7_L30_both_k15` | 0.088 | 0.178 | 0.228 | 0.141 | 0.161 | 0.162 |
| 2 | `sweep_2-7_L31_both_k15` | 0.082 | 0.168 | 0.227 | 0.133 | 0.157 | 0.155 |
| 3 | `sweep_2-7_L29_both_k15` | 0.087 | 0.161 | 0.221 | 0.131 | 0.155 | 0.158 |
| 4 | `sweep_2-7_L28_both_k15` | 0.078 | 0.149 | 0.211 | 0.120 | 0.146 | 0.146 |

## Configs

- `sweep_2-7_L30_both_k15`: prompt sweep single cell: 2-7, L30, anti_pca_both_k15
- `sweep_2-7_L31_both_k15`: prompt sweep single cell: 2-7, L31, anti_pca_both_k15
- `sweep_2-7_L29_both_k15`: prompt sweep single cell: 2-7, L29, anti_pca_both_k15
- `sweep_2-7_L28_both_k15`: prompt sweep single cell: 2-7, L28, anti_pca_both_k15

## Prompt Notes

- Sweep: `prompt_sweep_l28_l29_l30_l31_both_k15`
- New preference prompts: `user_preference`, `user_avoidance`, `personalization_need`
- Token wording treatments: `2-1_token`, `user_preference_token`
- Pruned after n=100: `1-1_CN`, `1-1_CN_ASCII`, `1-1_EN`, `2-3-2_mem`, `2-4-1`, `2-6`, `2-7`, `2-8`, `2-4-1_user_word_represent`, `2-5_represent`, `2-7_represent`, `2-8_represent`
- Note: PrefEval n=1000 uses a pruned prompt sweep. The 2-1 topic prompt is useful for the target companion scenario but may partly fit PrefEval's topic-structured rows, so it is tracked with a token wording treatment.
