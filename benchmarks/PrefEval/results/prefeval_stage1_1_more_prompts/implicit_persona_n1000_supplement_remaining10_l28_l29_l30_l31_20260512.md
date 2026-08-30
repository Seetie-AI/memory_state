# PrefEval Automatic Retrieval

- Created UTC: `2026-05-13T03:55:53.416168+00:00`
- Task: `implicit_persona`
- Dataset: `siyanzhao/prefeval_implicit_persona`
- Items: `1000`
- Gold policy: `same_preference_text`
- Elapsed: `3h06m38s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `sweep_2-1-2_L30_both_k15` | 0.107 | 0.228 | 0.321 | 0.177 | 0.215 | 0.207 |
| 2 | `sweep_2-1-2_L29_both_k15` | 0.103 | 0.226 | 0.309 | 0.174 | 0.209 | 0.204 |
| 3 | `sweep_2-1-2_L28_both_k15` | 0.106 | 0.215 | 0.306 | 0.169 | 0.207 | 0.202 |
| 4 | `sweep_2-1-2_L31_both_k15` | 0.095 | 0.219 | 0.296 | 0.166 | 0.198 | 0.193 |
| 5 | `sweep_2-3-3_L30_both_k15` | 0.098 | 0.222 | 0.291 | 0.170 | 0.198 | 0.193 |
| 6 | `sweep_2-5-3_L29_both_k15` | 0.091 | 0.231 | 0.290 | 0.173 | 0.197 | 0.191 |
| 7 | `sweep_2-3-3_L29_both_k15` | 0.094 | 0.212 | 0.289 | 0.162 | 0.194 | 0.189 |
| 8 | `sweep_2-5-3_L30_both_k15` | 0.092 | 0.230 | 0.288 | 0.173 | 0.197 | 0.191 |
| 9 | `sweep_2-5-3_L28_both_k15` | 0.093 | 0.221 | 0.288 | 0.168 | 0.195 | 0.190 |
| 10 | `sweep_1-1_EMOJI_L29_both_k15` | 0.098 | 0.225 | 0.284 | 0.174 | 0.198 | 0.195 |
| 11 | `sweep_2-3-3_L28_both_k15` | 0.086 | 0.212 | 0.284 | 0.159 | 0.188 | 0.183 |
| 12 | `sweep_1-1_EMOJI_L30_both_k15` | 0.107 | 0.226 | 0.283 | 0.176 | 0.200 | 0.199 |
| 13 | `sweep_2-5-2_L30_both_k15` | 0.083 | 0.219 | 0.283 | 0.163 | 0.189 | 0.184 |
| 14 | `sweep_2-5-2_L29_both_k15` | 0.085 | 0.221 | 0.282 | 0.167 | 0.191 | 0.188 |
| 15 | `sweep_1-1_EMOJI_L28_both_k15` | 0.101 | 0.205 | 0.274 | 0.162 | 0.190 | 0.190 |
| 16 | `sweep_2-5-2_L28_both_k15` | 0.080 | 0.210 | 0.273 | 0.157 | 0.183 | 0.180 |
| 17 | `sweep_2-5-2_L31_both_k15` | 0.088 | 0.212 | 0.270 | 0.160 | 0.183 | 0.178 |
| 18 | `sweep_2-3-3_L31_both_k15` | 0.082 | 0.196 | 0.267 | 0.147 | 0.177 | 0.166 |
| 19 | `sweep_1-1-2_L30_both_k15` | 0.094 | 0.200 | 0.260 | 0.155 | 0.181 | 0.180 |
| 20 | `sweep_1-1-2_L29_both_k15` | 0.092 | 0.196 | 0.258 | 0.153 | 0.178 | 0.178 |
| 21 | `sweep_1-1_EMOJI_L31_both_k15` | 0.084 | 0.196 | 0.258 | 0.149 | 0.175 | 0.168 |
| 22 | `sweep_1-1_CN_explicit_L29_both_k15` | 0.083 | 0.194 | 0.257 | 0.149 | 0.175 | 0.173 |
| 23 | `sweep_1-1_CN_explicit_L30_both_k15` | 0.085 | 0.189 | 0.257 | 0.146 | 0.174 | 0.173 |
| 24 | `sweep_2-5-3_L31_both_k15` | 0.083 | 0.196 | 0.256 | 0.147 | 0.172 | 0.165 |
| 25 | `sweep_1-1_EN_explicit_L29_both_k15` | 0.090 | 0.171 | 0.252 | 0.138 | 0.171 | 0.173 |
| 26 | `sweep_1-1_JA_explicit_L30_both_k15` | 0.085 | 0.197 | 0.251 | 0.151 | 0.173 | 0.174 |
| 27 | `sweep_1-1_CN_explicit_L28_both_k15` | 0.083 | 0.184 | 0.248 | 0.143 | 0.169 | 0.168 |
| 28 | `sweep_1-1_JA_explicit_L29_both_k15` | 0.082 | 0.189 | 0.246 | 0.144 | 0.167 | 0.170 |
| 29 | `sweep_1-1_EN_explicit_L30_both_k15` | 0.090 | 0.178 | 0.245 | 0.142 | 0.169 | 0.172 |
| 30 | `sweep_1-1-2_L28_both_k15` | 0.085 | 0.182 | 0.245 | 0.142 | 0.168 | 0.168 |
| 31 | `sweep_1-1_JA_explicit_L28_both_k15` | 0.076 | 0.172 | 0.240 | 0.131 | 0.159 | 0.160 |
| 32 | `sweep_1-1_EN_explicit_L31_both_k15` | 0.075 | 0.168 | 0.237 | 0.128 | 0.157 | 0.154 |
| 33 | `sweep_1-1_EN_explicit_L28_both_k15` | 0.082 | 0.172 | 0.236 | 0.135 | 0.161 | 0.165 |
| 34 | `sweep_1-1-2_L31_both_k15` | 0.081 | 0.182 | 0.235 | 0.139 | 0.160 | 0.157 |
| 35 | `sweep_1-1_JA_explicit_L31_both_k15` | 0.074 | 0.176 | 0.232 | 0.133 | 0.157 | 0.154 |
| 36 | `sweep_1-1_CN_explicit_L31_both_k15` | 0.074 | 0.161 | 0.230 | 0.125 | 0.153 | 0.149 |
| 37 | `sweep_1-1_RU_explicit_L29_both_k15` | 0.037 | 0.071 | 0.112 | 0.056 | 0.073 | 0.076 |
| 38 | `sweep_1-1_RU_explicit_L30_both_k15` | 0.035 | 0.074 | 0.107 | 0.058 | 0.071 | 0.076 |
| 39 | `sweep_1-1_RU_explicit_L31_both_k15` | 0.037 | 0.073 | 0.099 | 0.058 | 0.069 | 0.072 |
| 40 | `sweep_1-1_RU_explicit_L28_both_k15` | 0.024 | 0.051 | 0.078 | 0.039 | 0.050 | 0.057 |

## Configs

- `sweep_2-1-2_L30_both_k15`: prompt sweep single cell: 2-1-2, L30, anti_pca_both_k15
- `sweep_2-1-2_L29_both_k15`: prompt sweep single cell: 2-1-2, L29, anti_pca_both_k15
- `sweep_2-1-2_L28_both_k15`: prompt sweep single cell: 2-1-2, L28, anti_pca_both_k15
- `sweep_2-1-2_L31_both_k15`: prompt sweep single cell: 2-1-2, L31, anti_pca_both_k15
- `sweep_2-3-3_L30_both_k15`: prompt sweep single cell: 2-3-3, L30, anti_pca_both_k15
- `sweep_2-5-3_L29_both_k15`: prompt sweep single cell: 2-5-3, L29, anti_pca_both_k15
- `sweep_2-3-3_L29_both_k15`: prompt sweep single cell: 2-3-3, L29, anti_pca_both_k15
- `sweep_2-5-3_L30_both_k15`: prompt sweep single cell: 2-5-3, L30, anti_pca_both_k15
- `sweep_2-5-3_L28_both_k15`: prompt sweep single cell: 2-5-3, L28, anti_pca_both_k15
- `sweep_1-1_EMOJI_L29_both_k15`: prompt sweep single cell: 1-1_EMOJI, L29, anti_pca_both_k15
- `sweep_2-3-3_L28_both_k15`: prompt sweep single cell: 2-3-3, L28, anti_pca_both_k15
- `sweep_1-1_EMOJI_L30_both_k15`: prompt sweep single cell: 1-1_EMOJI, L30, anti_pca_both_k15
- `sweep_2-5-2_L30_both_k15`: prompt sweep single cell: 2-5-2, L30, anti_pca_both_k15
- `sweep_2-5-2_L29_both_k15`: prompt sweep single cell: 2-5-2, L29, anti_pca_both_k15
- `sweep_1-1_EMOJI_L28_both_k15`: prompt sweep single cell: 1-1_EMOJI, L28, anti_pca_both_k15
- `sweep_2-5-2_L28_both_k15`: prompt sweep single cell: 2-5-2, L28, anti_pca_both_k15
- `sweep_2-5-2_L31_both_k15`: prompt sweep single cell: 2-5-2, L31, anti_pca_both_k15
- `sweep_2-3-3_L31_both_k15`: prompt sweep single cell: 2-3-3, L31, anti_pca_both_k15
- `sweep_1-1-2_L30_both_k15`: prompt sweep single cell: 1-1-2, L30, anti_pca_both_k15
- `sweep_1-1-2_L29_both_k15`: prompt sweep single cell: 1-1-2, L29, anti_pca_both_k15
- `sweep_1-1_EMOJI_L31_both_k15`: prompt sweep single cell: 1-1_EMOJI, L31, anti_pca_both_k15
- `sweep_1-1_CN_explicit_L29_both_k15`: prompt sweep single cell: 1-1_CN_explicit, L29, anti_pca_both_k15
- `sweep_1-1_CN_explicit_L30_both_k15`: prompt sweep single cell: 1-1_CN_explicit, L30, anti_pca_both_k15
- `sweep_2-5-3_L31_both_k15`: prompt sweep single cell: 2-5-3, L31, anti_pca_both_k15
- `sweep_1-1_EN_explicit_L29_both_k15`: prompt sweep single cell: 1-1_EN_explicit, L29, anti_pca_both_k15
- `sweep_1-1_JA_explicit_L30_both_k15`: prompt sweep single cell: 1-1_JA_explicit, L30, anti_pca_both_k15
- `sweep_1-1_CN_explicit_L28_both_k15`: prompt sweep single cell: 1-1_CN_explicit, L28, anti_pca_both_k15
- `sweep_1-1_JA_explicit_L29_both_k15`: prompt sweep single cell: 1-1_JA_explicit, L29, anti_pca_both_k15
- `sweep_1-1_EN_explicit_L30_both_k15`: prompt sweep single cell: 1-1_EN_explicit, L30, anti_pca_both_k15
- `sweep_1-1-2_L28_both_k15`: prompt sweep single cell: 1-1-2, L28, anti_pca_both_k15
- `sweep_1-1_JA_explicit_L28_both_k15`: prompt sweep single cell: 1-1_JA_explicit, L28, anti_pca_both_k15
- `sweep_1-1_EN_explicit_L31_both_k15`: prompt sweep single cell: 1-1_EN_explicit, L31, anti_pca_both_k15
- `sweep_1-1_EN_explicit_L28_both_k15`: prompt sweep single cell: 1-1_EN_explicit, L28, anti_pca_both_k15
- `sweep_1-1-2_L31_both_k15`: prompt sweep single cell: 1-1-2, L31, anti_pca_both_k15
- `sweep_1-1_JA_explicit_L31_both_k15`: prompt sweep single cell: 1-1_JA_explicit, L31, anti_pca_both_k15
- `sweep_1-1_CN_explicit_L31_both_k15`: prompt sweep single cell: 1-1_CN_explicit, L31, anti_pca_both_k15
- `sweep_1-1_RU_explicit_L29_both_k15`: prompt sweep single cell: 1-1_RU_explicit, L29, anti_pca_both_k15
- `sweep_1-1_RU_explicit_L30_both_k15`: prompt sweep single cell: 1-1_RU_explicit, L30, anti_pca_both_k15
- `sweep_1-1_RU_explicit_L31_both_k15`: prompt sweep single cell: 1-1_RU_explicit, L31, anti_pca_both_k15
- `sweep_1-1_RU_explicit_L28_both_k15`: prompt sweep single cell: 1-1_RU_explicit, L28, anti_pca_both_k15

## Prompt Notes

- Sweep: `prompt_sweep_l28_l29_l30_l31_both_k15`
- New preference prompts: `user_preference`, `user_avoidance`, `personalization_need`
- Token wording treatments: `2-1_token`, `user_preference_token`
- Pruned after n=100: `1-1_CN`, `1-1_CN_ASCII`, `1-1_EN`, `2-3-2_mem`, `2-4-1`, `2-6`, `2-7`, `2-8`, `2-4-1_user_word_represent`, `2-5_represent`, `2-7_represent`, `2-8_represent`
- Note: PrefEval n=1000 uses a pruned prompt sweep. The 2-1 topic prompt is useful for the target companion scenario but may partly fit PrefEval's topic-structured rows, so it is tracked with a token wording treatment.
