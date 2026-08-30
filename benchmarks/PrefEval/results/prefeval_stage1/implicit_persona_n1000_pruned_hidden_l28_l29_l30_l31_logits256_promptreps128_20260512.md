# PrefEval Automatic Retrieval

- Created UTC: `2026-05-12T08:02:45.096155+00:00`
- Task: `implicit_persona`
- Dataset: `siyanzhao/prefeval_implicit_persona`
- Items: `1000`
- Gold policy: `same_preference_text`
- Elapsed: `3h50m19s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `sweep_2-3-1_L30_both_k15` | 0.110 | 0.254 | 0.311 | 0.194 | 0.218 | 0.214 |
| 2 | `sweep_2-3-1_L29_both_k15` | 0.108 | 0.242 | 0.310 | 0.187 | 0.214 | 0.211 |
| 3 | `sweep_2-3-2_query_L30_both_k15` | 0.097 | 0.241 | 0.310 | 0.179 | 0.208 | 0.198 |
| 4 | `sweep_2-3-1_L28_both_k15` | 0.104 | 0.238 | 0.309 | 0.182 | 0.211 | 0.206 |
| 5 | `sweep_2-3-2_query_L29_both_k15` | 0.095 | 0.237 | 0.303 | 0.176 | 0.204 | 0.196 |
| 6 | `sweep_2-5_L29_both_k15` | 0.096 | 0.233 | 0.301 | 0.177 | 0.204 | 0.199 |
| 7 | `sweep_2-5_L30_both_k15` | 0.095 | 0.225 | 0.301 | 0.172 | 0.203 | 0.198 |
| 8 | `sweep_2-3-1_L31_both_k15` | 0.096 | 0.233 | 0.300 | 0.177 | 0.204 | 0.195 |
| 9 | `sweep_2-1_L30_both_k15` | 0.100 | 0.209 | 0.299 | 0.164 | 0.201 | 0.195 |
| 10 | `sweep_2-3-2_query_L28_both_k15` | 0.095 | 0.224 | 0.299 | 0.169 | 0.201 | 0.194 |
| 11 | `sweep_2-5_L28_both_k15` | 0.094 | 0.222 | 0.298 | 0.170 | 0.200 | 0.195 |
| 12 | `sweep_2-5_L31_both_k15` | 0.090 | 0.225 | 0.293 | 0.170 | 0.198 | 0.189 |
| 13 | `sweep_2-1_L29_both_k15` | 0.092 | 0.204 | 0.291 | 0.157 | 0.193 | 0.188 |
| 14 | `sweep_2-1_token_L30_both_k15` | 0.089 | 0.213 | 0.290 | 0.161 | 0.193 | 0.187 |
| 15 | `sweep_2-3-2_query_L31_both_k15` | 0.085 | 0.210 | 0.289 | 0.157 | 0.190 | 0.181 |
| 16 | `sweep_2-1_L28_both_k15` | 0.087 | 0.202 | 0.288 | 0.155 | 0.190 | 0.185 |
| 17 | `sweep_2-1_token_L31_both_k15` | 0.086 | 0.191 | 0.285 | 0.147 | 0.186 | 0.175 |
| 18 | `sweep_1-2_L30_both_k15` | 0.092 | 0.209 | 0.281 | 0.159 | 0.189 | 0.185 |
| 19 | `sweep_2-1_L31_both_k15` | 0.090 | 0.202 | 0.280 | 0.155 | 0.187 | 0.182 |
| 20 | `sweep_1-2_L29_both_k15` | 0.095 | 0.201 | 0.278 | 0.156 | 0.188 | 0.185 |
| 21 | `sweep_2-1_token_L29_both_k15` | 0.083 | 0.215 | 0.277 | 0.158 | 0.184 | 0.181 |
| 22 | `sweep_P0_L30_both_k15` | 0.093 | 0.197 | 0.271 | 0.154 | 0.184 | 0.178 |
| 23 | `sweep_2-1_token_L28_both_k15` | 0.086 | 0.200 | 0.271 | 0.152 | 0.182 | 0.180 |
| 24 | `sweep_1-2_L28_both_k15` | 0.087 | 0.199 | 0.267 | 0.151 | 0.179 | 0.176 |
| 25 | `sweep_1-3_L30_both_k15` | 0.092 | 0.206 | 0.264 | 0.158 | 0.182 | 0.180 |
| 26 | `sweep_P0_L29_both_k15` | 0.097 | 0.203 | 0.260 | 0.159 | 0.183 | 0.182 |
| 27 | `sweep_1-3_L29_both_k15` | 0.087 | 0.191 | 0.259 | 0.149 | 0.177 | 0.175 |
| 28 | `sweep_1-2_L31_both_k15` | 0.080 | 0.185 | 0.249 | 0.141 | 0.167 | 0.164 |
| 29 | `sweep_P0_L28_both_k15` | 0.082 | 0.178 | 0.246 | 0.139 | 0.168 | 0.166 |
| 30 | `sweep_1-3_L28_both_k15` | 0.086 | 0.182 | 0.241 | 0.142 | 0.167 | 0.168 |
| 31 | `sweep_P0_L31_both_k15` | 0.079 | 0.172 | 0.235 | 0.134 | 0.160 | 0.156 |
| 32 | `sweep_1-3_L31_both_k15` | 0.081 | 0.183 | 0.229 | 0.140 | 0.158 | 0.157 |
| 33 | `sweep_2-4-2_L30_both_k15` | 0.072 | 0.166 | 0.223 | 0.128 | 0.152 | 0.155 |
| 34 | `sweep_2-4-2_L31_both_k15` | 0.069 | 0.161 | 0.219 | 0.124 | 0.147 | 0.144 |
| 35 | `sweep_user_preference_L30_both_k15` | 0.072 | 0.153 | 0.214 | 0.120 | 0.145 | 0.149 |
| 36 | `sweep_2-4-2_L29_both_k15` | 0.072 | 0.159 | 0.211 | 0.123 | 0.145 | 0.151 |
| 37 | `sweep_2-4-1_user_word_L30_both_k15` | 0.070 | 0.153 | 0.209 | 0.119 | 0.142 | 0.142 |
| 38 | `sweep_user_preference_token_L30_both_k15` | 0.065 | 0.149 | 0.209 | 0.113 | 0.138 | 0.138 |
| 39 | `sweep_user_preference_token_L29_both_k15` | 0.061 | 0.149 | 0.208 | 0.112 | 0.136 | 0.137 |
| 40 | `sweep_2-4-2_L28_both_k15` | 0.064 | 0.148 | 0.207 | 0.114 | 0.138 | 0.142 |
| 41 | `sweep_2-4-1_user_word_L29_both_k15` | 0.062 | 0.143 | 0.207 | 0.110 | 0.136 | 0.135 |
| 42 | `sweep_user_preference_L29_both_k15` | 0.071 | 0.152 | 0.203 | 0.119 | 0.139 | 0.146 |
| 43 | `sweep_user_preference_token_L28_both_k15` | 0.057 | 0.154 | 0.198 | 0.112 | 0.130 | 0.132 |
| 44 | `sweep_user_preference_L28_both_k15` | 0.069 | 0.139 | 0.196 | 0.109 | 0.134 | 0.139 |
| 45 | `sweep_user_preference_L31_both_k15` | 0.060 | 0.137 | 0.193 | 0.105 | 0.128 | 0.127 |
| 46 | `sweep_personalization_need_L29_both_k15` | 0.070 | 0.145 | 0.191 | 0.113 | 0.132 | 0.136 |
| 47 | `sweep_2-4-1_user_word_L31_both_k15` | 0.062 | 0.125 | 0.191 | 0.098 | 0.126 | 0.122 |
| 48 | `sweep_personalization_need_L30_both_k15` | 0.066 | 0.146 | 0.189 | 0.111 | 0.130 | 0.131 |
| 49 | `sweep_2-4-1_user_word_L28_both_k15` | 0.057 | 0.133 | 0.189 | 0.101 | 0.124 | 0.124 |
| 50 | `sweep_personalization_need_L28_both_k15` | 0.059 | 0.132 | 0.183 | 0.101 | 0.122 | 0.125 |
| 51 | `sweep_user_preference_token_L31_both_k15` | 0.036 | 0.099 | 0.148 | 0.072 | 0.093 | 0.095 |
| 52 | `sweep_personalization_need_L31_both_k15` | 0.049 | 0.106 | 0.145 | 0.083 | 0.099 | 0.101 |
| 53 | `sweep_user_avoidance_L30_both_k15` | 0.044 | 0.096 | 0.128 | 0.073 | 0.086 | 0.091 |
| 54 | `sweep_user_avoidance_L29_both_k15` | 0.034 | 0.091 | 0.127 | 0.067 | 0.081 | 0.085 |
| 55 | `sweep_user_avoidance_L31_both_k15` | 0.047 | 0.089 | 0.125 | 0.072 | 0.086 | 0.092 |
| 56 | `sweep_user_avoidance_L28_both_k15` | 0.029 | 0.075 | 0.111 | 0.055 | 0.070 | 0.074 |
| 57 | `bm25` | 0.035 | 0.074 | 0.094 | 0.058 | 0.066 | 0.067 |

## Configs

- `sweep_2-3-1_L30_both_k15`: prompt sweep single cell: 2-3-1, L30, anti_pca_both_k15
- `sweep_2-3-1_L29_both_k15`: prompt sweep single cell: 2-3-1, L29, anti_pca_both_k15
- `sweep_2-3-2_query_L30_both_k15`: prompt sweep single cell: 2-3-2_query, L30, anti_pca_both_k15
- `sweep_2-3-1_L28_both_k15`: prompt sweep single cell: 2-3-1, L28, anti_pca_both_k15
- `sweep_2-3-2_query_L29_both_k15`: prompt sweep single cell: 2-3-2_query, L29, anti_pca_both_k15
- `sweep_2-5_L29_both_k15`: prompt sweep single cell: 2-5, L29, anti_pca_both_k15
- `sweep_2-5_L30_both_k15`: prompt sweep single cell: 2-5, L30, anti_pca_both_k15
- `sweep_2-3-1_L31_both_k15`: prompt sweep single cell: 2-3-1, L31, anti_pca_both_k15
- `sweep_2-1_L30_both_k15`: prompt sweep single cell: 2-1, L30, anti_pca_both_k15
- `sweep_2-3-2_query_L28_both_k15`: prompt sweep single cell: 2-3-2_query, L28, anti_pca_both_k15
- `sweep_2-5_L28_both_k15`: prompt sweep single cell: 2-5, L28, anti_pca_both_k15
- `sweep_2-5_L31_both_k15`: prompt sweep single cell: 2-5, L31, anti_pca_both_k15
- `sweep_2-1_L29_both_k15`: prompt sweep single cell: 2-1, L29, anti_pca_both_k15
- `sweep_2-1_token_L30_both_k15`: prompt sweep single cell: 2-1_token, L30, anti_pca_both_k15
- `sweep_2-3-2_query_L31_both_k15`: prompt sweep single cell: 2-3-2_query, L31, anti_pca_both_k15
- `sweep_2-1_L28_both_k15`: prompt sweep single cell: 2-1, L28, anti_pca_both_k15
- `sweep_2-1_token_L31_both_k15`: prompt sweep single cell: 2-1_token, L31, anti_pca_both_k15
- `sweep_1-2_L30_both_k15`: prompt sweep single cell: 1-2, L30, anti_pca_both_k15
- `sweep_2-1_L31_both_k15`: prompt sweep single cell: 2-1, L31, anti_pca_both_k15
- `sweep_1-2_L29_both_k15`: prompt sweep single cell: 1-2, L29, anti_pca_both_k15
- `sweep_2-1_token_L29_both_k15`: prompt sweep single cell: 2-1_token, L29, anti_pca_both_k15
- `sweep_P0_L30_both_k15`: prompt sweep single cell: P0, L30, anti_pca_both_k15
- `sweep_2-1_token_L28_both_k15`: prompt sweep single cell: 2-1_token, L28, anti_pca_both_k15
- `sweep_1-2_L28_both_k15`: prompt sweep single cell: 1-2, L28, anti_pca_both_k15
- `sweep_1-3_L30_both_k15`: prompt sweep single cell: 1-3, L30, anti_pca_both_k15
- `sweep_P0_L29_both_k15`: prompt sweep single cell: P0, L29, anti_pca_both_k15
- `sweep_1-3_L29_both_k15`: prompt sweep single cell: 1-3, L29, anti_pca_both_k15
- `sweep_1-2_L31_both_k15`: prompt sweep single cell: 1-2, L31, anti_pca_both_k15
- `sweep_P0_L28_both_k15`: prompt sweep single cell: P0, L28, anti_pca_both_k15
- `sweep_1-3_L28_both_k15`: prompt sweep single cell: 1-3, L28, anti_pca_both_k15
- `sweep_P0_L31_both_k15`: prompt sweep single cell: P0, L31, anti_pca_both_k15
- `sweep_1-3_L31_both_k15`: prompt sweep single cell: 1-3, L31, anti_pca_both_k15
- `sweep_2-4-2_L30_both_k15`: prompt sweep single cell: 2-4-2, L30, anti_pca_both_k15
- `sweep_2-4-2_L31_both_k15`: prompt sweep single cell: 2-4-2, L31, anti_pca_both_k15
- `sweep_user_preference_L30_both_k15`: prompt sweep single cell: user_preference, L30, anti_pca_both_k15
- `sweep_2-4-2_L29_both_k15`: prompt sweep single cell: 2-4-2, L29, anti_pca_both_k15
- `sweep_2-4-1_user_word_L30_both_k15`: prompt sweep single cell: 2-4-1_user_word, L30, anti_pca_both_k15
- `sweep_user_preference_token_L30_both_k15`: prompt sweep single cell: user_preference_token, L30, anti_pca_both_k15
- `sweep_user_preference_token_L29_both_k15`: prompt sweep single cell: user_preference_token, L29, anti_pca_both_k15
- `sweep_2-4-2_L28_both_k15`: prompt sweep single cell: 2-4-2, L28, anti_pca_both_k15
- `sweep_2-4-1_user_word_L29_both_k15`: prompt sweep single cell: 2-4-1_user_word, L29, anti_pca_both_k15
- `sweep_user_preference_L29_both_k15`: prompt sweep single cell: user_preference, L29, anti_pca_both_k15
- `sweep_user_preference_token_L28_both_k15`: prompt sweep single cell: user_preference_token, L28, anti_pca_both_k15
- `sweep_user_preference_L28_both_k15`: prompt sweep single cell: user_preference, L28, anti_pca_both_k15
- `sweep_user_preference_L31_both_k15`: prompt sweep single cell: user_preference, L31, anti_pca_both_k15
- `sweep_personalization_need_L29_both_k15`: prompt sweep single cell: personalization_need, L29, anti_pca_both_k15
- `sweep_2-4-1_user_word_L31_both_k15`: prompt sweep single cell: 2-4-1_user_word, L31, anti_pca_both_k15
- `sweep_personalization_need_L30_both_k15`: prompt sweep single cell: personalization_need, L30, anti_pca_both_k15
- `sweep_2-4-1_user_word_L28_both_k15`: prompt sweep single cell: 2-4-1_user_word, L28, anti_pca_both_k15
- `sweep_personalization_need_L28_both_k15`: prompt sweep single cell: personalization_need, L28, anti_pca_both_k15
- `sweep_user_preference_token_L31_both_k15`: prompt sweep single cell: user_preference_token, L31, anti_pca_both_k15
- `sweep_personalization_need_L31_both_k15`: prompt sweep single cell: personalization_need, L31, anti_pca_both_k15
- `sweep_user_avoidance_L30_both_k15`: prompt sweep single cell: user_avoidance, L30, anti_pca_both_k15
- `sweep_user_avoidance_L29_both_k15`: prompt sweep single cell: user_avoidance, L29, anti_pca_both_k15
- `sweep_user_avoidance_L31_both_k15`: prompt sweep single cell: user_avoidance, L31, anti_pca_both_k15
- `sweep_user_avoidance_L28_both_k15`: prompt sweep single cell: user_avoidance, L28, anti_pca_both_k15
- `bm25`: BM25 over preference memory strings

## Prompt Notes

- Sweep: `prompt_sweep_l28_l29_l30_l31_both_k15`
- New preference prompts: `user_preference`, `user_avoidance`, `personalization_need`
- Token wording treatments: `2-1_token`, `user_preference_token`
- Pruned after n=100: `1-1_CN`, `1-1_CN_ASCII`, `1-1_EN`, `2-3-2_mem`, `2-4-1`, `2-6`, `2-7`, `2-8`, `2-4-1_user_word_represent`, `2-5_represent`, `2-7_represent`, `2-8_represent`
- Note: PrefEval n=1000 uses a pruned prompt sweep. The 2-1 topic prompt is useful for the target companion scenario but may partly fit PrefEval's topic-structured rows, so it is tracked with a token wording treatment.
