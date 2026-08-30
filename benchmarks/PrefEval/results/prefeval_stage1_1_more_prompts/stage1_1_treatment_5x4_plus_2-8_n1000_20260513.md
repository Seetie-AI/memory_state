# PrefEval Automatic Retrieval

- Created UTC: `2026-05-13T09:46:32.881773+00:00`
- Task: `implicit_persona`
- Dataset: `siyanzhao/prefeval_implicit_persona`
- Items: `1000`
- Gold policy: `same_preference_text`
- Elapsed: `4h33m52s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `sweep_2-3-1_summarize_L29_both_k15` | 0.112 | 0.242 | 0.319 | 0.187 | 0.219 | 0.212 |
| 2 | `sweep_2-3-1_summarize_L30_both_k15` | 0.111 | 0.243 | 0.319 | 0.187 | 0.218 | 0.210 |
| 3 | `sweep_2-3-1_no_above_L30_both_k15` | 0.106 | 0.249 | 0.318 | 0.188 | 0.216 | 0.210 |
| 4 | `sweep_2-3-1_token_L30_both_k15` | 0.104 | 0.237 | 0.315 | 0.181 | 0.213 | 0.208 |
| 5 | `sweep_2-5_token_L29_both_k15` | 0.111 | 0.241 | 0.314 | 0.185 | 0.215 | 0.209 |
| 6 | `sweep_2-3-1_token_L29_both_k15` | 0.105 | 0.234 | 0.312 | 0.180 | 0.212 | 0.207 |
| 7 | `sweep_2-3-1_summarize_L28_both_k15` | 0.102 | 0.244 | 0.311 | 0.183 | 0.210 | 0.203 |
| 8 | `sweep_2-3-1_no_above_L29_both_k15` | 0.108 | 0.249 | 0.309 | 0.189 | 0.214 | 0.211 |
| 9 | `sweep_2-3-1_emoji_L30_both_k15` | 0.106 | 0.235 | 0.308 | 0.180 | 0.210 | 0.203 |
| 10 | `sweep_2-3-1_no_above_L31_both_k15` | 0.095 | 0.231 | 0.308 | 0.173 | 0.204 | 0.194 |
| 11 | `sweep_2-5_emoji_L29_both_k15` | 0.107 | 0.232 | 0.307 | 0.178 | 0.209 | 0.204 |
| 12 | `sweep_2-1_summarize_L29_both_k15` | 0.104 | 0.221 | 0.307 | 0.170 | 0.205 | 0.199 |
| 13 | `sweep_2-3-1_no_above_L28_both_k15` | 0.102 | 0.240 | 0.306 | 0.182 | 0.209 | 0.206 |
| 14 | `sweep_2-5_token_L30_both_k15` | 0.115 | 0.234 | 0.305 | 0.183 | 0.212 | 0.209 |
| 15 | `sweep_2-1_summarize_L30_both_k15` | 0.101 | 0.233 | 0.304 | 0.176 | 0.205 | 0.201 |
| 16 | `sweep_2-3-1_token_L31_both_k15` | 0.096 | 0.237 | 0.304 | 0.176 | 0.204 | 0.196 |
| 17 | `sweep_2-5_emoji_L30_both_k15` | 0.109 | 0.230 | 0.303 | 0.178 | 0.208 | 0.204 |
| 18 | `sweep_2-5_token_L28_both_k15` | 0.106 | 0.233 | 0.303 | 0.178 | 0.206 | 0.201 |
| 19 | `sweep_2-1_emoji_L30_both_k15` | 0.104 | 0.223 | 0.303 | 0.173 | 0.205 | 0.201 |
| 20 | `sweep_2-3-1_token_L28_both_k15` | 0.095 | 0.225 | 0.302 | 0.171 | 0.203 | 0.198 |
| 21 | `sweep_2-5_summarize_L29_both_k15` | 0.097 | 0.229 | 0.301 | 0.173 | 0.203 | 0.197 |
| 22 | `sweep_2-3-1_emoji_L29_both_k15` | 0.102 | 0.231 | 0.298 | 0.177 | 0.204 | 0.201 |
| 23 | `sweep_2-1_summarize_L31_both_k15` | 0.089 | 0.218 | 0.298 | 0.163 | 0.196 | 0.189 |
| 24 | `sweep_2-1_emoji_L29_both_k15` | 0.108 | 0.224 | 0.297 | 0.175 | 0.204 | 0.203 |
| 25 | `sweep_2-3-1_summarize_L31_both_k15` | 0.097 | 0.220 | 0.292 | 0.167 | 0.197 | 0.188 |
| 26 | `sweep_2-1_summarize_L28_both_k15` | 0.096 | 0.216 | 0.292 | 0.164 | 0.195 | 0.192 |
| 27 | `sweep_2-3-1_emoji_L28_both_k15` | 0.100 | 0.230 | 0.291 | 0.175 | 0.200 | 0.198 |
| 28 | `sweep_2-5_summarize_L30_both_k15` | 0.096 | 0.226 | 0.290 | 0.172 | 0.199 | 0.196 |
| 29 | `sweep_2-1_emoji_L28_both_k15` | 0.105 | 0.223 | 0.289 | 0.173 | 0.200 | 0.199 |
| 30 | `sweep_2-5_emoji_L28_both_k15` | 0.103 | 0.217 | 0.289 | 0.168 | 0.198 | 0.197 |
| 31 | `sweep_2-5_token_L31_both_k15` | 0.097 | 0.228 | 0.289 | 0.172 | 0.197 | 0.190 |
| 32 | `sweep_2-5_summarize_L28_both_k15` | 0.092 | 0.214 | 0.285 | 0.163 | 0.193 | 0.189 |
| 33 | `sweep_2-5_emoji_L31_both_k15` | 0.096 | 0.226 | 0.284 | 0.171 | 0.195 | 0.189 |
| 34 | `sweep_2-5_summarize_L31_both_k15` | 0.095 | 0.216 | 0.279 | 0.165 | 0.191 | 0.187 |
| 35 | `sweep_2-3-1_emoji_L31_both_k15` | 0.086 | 0.198 | 0.271 | 0.151 | 0.181 | 0.175 |
| 36 | `sweep_2-7_token_L30_both_k15` | 0.092 | 0.207 | 0.269 | 0.159 | 0.184 | 0.182 |
| 37 | `sweep_2-1_emoji_L31_both_k15` | 0.088 | 0.204 | 0.268 | 0.155 | 0.181 | 0.179 |
| 38 | `sweep_2-7_token_L29_both_k15` | 0.093 | 0.211 | 0.266 | 0.162 | 0.184 | 0.182 |
| 39 | `sweep_2-7_emoji_L29_both_k15` | 0.097 | 0.204 | 0.261 | 0.159 | 0.182 | 0.179 |
| 40 | `sweep_2-7_token_L31_both_k15` | 0.091 | 0.198 | 0.255 | 0.152 | 0.175 | 0.171 |
| 41 | `sweep_1-3_token_L30_both_k15` | 0.083 | 0.180 | 0.253 | 0.139 | 0.169 | 0.166 |
| 42 | `sweep_1-3_token_L29_both_k15` | 0.081 | 0.178 | 0.252 | 0.136 | 0.166 | 0.164 |
| 43 | `sweep_2-7_emoji_L28_both_k15` | 0.090 | 0.201 | 0.247 | 0.153 | 0.172 | 0.171 |
| 44 | `sweep_2-7_token_L28_both_k15` | 0.093 | 0.197 | 0.238 | 0.151 | 0.168 | 0.171 |
| 45 | `sweep_2-7_emoji_L30_both_k15` | 0.090 | 0.185 | 0.234 | 0.144 | 0.164 | 0.163 |
| 46 | `sweep_1-3_token_L28_both_k15` | 0.075 | 0.161 | 0.231 | 0.123 | 0.152 | 0.153 |
| 47 | `sweep_1-3_token_L31_both_k15` | 0.070 | 0.149 | 0.203 | 0.115 | 0.137 | 0.137 |
| 48 | `sweep_2-8_emoji_L28_both_k15` | 0.060 | 0.138 | 0.198 | 0.104 | 0.129 | 0.130 |
| 49 | `sweep_2-7_no_above_L30_both_k15` | 0.073 | 0.148 | 0.196 | 0.115 | 0.135 | 0.138 |
| 50 | `sweep_2-8_emoji_L29_both_k15` | 0.063 | 0.133 | 0.195 | 0.104 | 0.129 | 0.131 |
| 51 | `sweep_2-7_no_above_L31_both_k15` | 0.066 | 0.131 | 0.190 | 0.103 | 0.128 | 0.128 |
| 52 | `sweep_2-7_no_above_L29_both_k15` | 0.070 | 0.143 | 0.188 | 0.111 | 0.130 | 0.134 |
| 53 | `sweep_2-7_emoji_L31_both_k15` | 0.063 | 0.138 | 0.185 | 0.105 | 0.125 | 0.124 |
| 54 | `sweep_2-7_no_above_L28_both_k15` | 0.068 | 0.129 | 0.181 | 0.103 | 0.124 | 0.127 |
| 55 | `sweep_2-7_summarize_L31_both_k15` | 0.067 | 0.125 | 0.179 | 0.099 | 0.122 | 0.123 |
| 56 | `sweep_2-7_summarize_L30_both_k15` | 0.066 | 0.133 | 0.176 | 0.105 | 0.122 | 0.129 |
| 57 | `sweep_2-8_emoji_L30_both_k15` | 0.048 | 0.111 | 0.167 | 0.085 | 0.108 | 0.108 |
| 58 | `sweep_2-7_summarize_L29_both_k15` | 0.063 | 0.127 | 0.164 | 0.100 | 0.115 | 0.123 |
| 59 | `sweep_2-8_token_L30_both_k15` | 0.053 | 0.118 | 0.164 | 0.090 | 0.109 | 0.109 |
| 60 | `sweep_2-8_token_L29_both_k15` | 0.060 | 0.119 | 0.158 | 0.094 | 0.110 | 0.113 |
| 61 | `sweep_2-8_token_L31_both_k15` | 0.046 | 0.114 | 0.157 | 0.086 | 0.104 | 0.103 |
| 62 | `sweep_2-8_summarize_L30_both_k15` | 0.058 | 0.122 | 0.154 | 0.095 | 0.108 | 0.113 |
| 63 | `sweep_2-7_summarize_L28_both_k15` | 0.060 | 0.116 | 0.153 | 0.092 | 0.108 | 0.115 |
| 64 | `sweep_2-8_summarize_L29_both_k15` | 0.060 | 0.115 | 0.152 | 0.091 | 0.107 | 0.111 |
| 65 | `sweep_2-8_L30_both_k15` | 0.047 | 0.111 | 0.150 | 0.084 | 0.100 | 0.103 |
| 66 | `sweep_2-8_L28_both_k15` | 0.051 | 0.109 | 0.147 | 0.084 | 0.099 | 0.104 |
| 67 | `sweep_2-8_summarize_L28_both_k15` | 0.056 | 0.111 | 0.145 | 0.088 | 0.102 | 0.108 |
| 68 | `sweep_2-8_L29_both_k15` | 0.052 | 0.106 | 0.144 | 0.082 | 0.098 | 0.104 |
| 69 | `sweep_2-8_token_L28_both_k15` | 0.045 | 0.106 | 0.144 | 0.080 | 0.096 | 0.100 |
| 70 | `sweep_2-8_emoji_L31_both_k15` | 0.042 | 0.091 | 0.135 | 0.071 | 0.089 | 0.090 |
| 71 | `sweep_2-8_summarize_L31_both_k15` | 0.050 | 0.103 | 0.131 | 0.081 | 0.092 | 0.096 |
| 72 | `sweep_2-8_L31_both_k15` | 0.038 | 0.084 | 0.112 | 0.064 | 0.076 | 0.081 |
| 73 | `sweep_2-8_no_above_L29_both_k15` | 0.030 | 0.080 | 0.112 | 0.058 | 0.071 | 0.077 |
| 74 | `sweep_2-8_no_above_L30_both_k15` | 0.029 | 0.076 | 0.112 | 0.056 | 0.071 | 0.076 |
| 75 | `sweep_2-8_no_above_L28_both_k15` | 0.030 | 0.076 | 0.103 | 0.056 | 0.067 | 0.074 |
| 76 | `sweep_2-8_no_above_L31_both_k15` | 0.016 | 0.066 | 0.095 | 0.045 | 0.056 | 0.060 |

## Configs

- `sweep_2-3-1_summarize_L29_both_k15`: prompt sweep single cell: 2-3-1_summarize, L29, anti_pca_both_k15
- `sweep_2-3-1_summarize_L30_both_k15`: prompt sweep single cell: 2-3-1_summarize, L30, anti_pca_both_k15
- `sweep_2-3-1_no_above_L30_both_k15`: prompt sweep single cell: 2-3-1_no_above, L30, anti_pca_both_k15
- `sweep_2-3-1_token_L30_both_k15`: prompt sweep single cell: 2-3-1_token, L30, anti_pca_both_k15
- `sweep_2-5_token_L29_both_k15`: prompt sweep single cell: 2-5_token, L29, anti_pca_both_k15
- `sweep_2-3-1_token_L29_both_k15`: prompt sweep single cell: 2-3-1_token, L29, anti_pca_both_k15
- `sweep_2-3-1_summarize_L28_both_k15`: prompt sweep single cell: 2-3-1_summarize, L28, anti_pca_both_k15
- `sweep_2-3-1_no_above_L29_both_k15`: prompt sweep single cell: 2-3-1_no_above, L29, anti_pca_both_k15
- `sweep_2-3-1_emoji_L30_both_k15`: prompt sweep single cell: 2-3-1_emoji, L30, anti_pca_both_k15
- `sweep_2-3-1_no_above_L31_both_k15`: prompt sweep single cell: 2-3-1_no_above, L31, anti_pca_both_k15
- `sweep_2-5_emoji_L29_both_k15`: prompt sweep single cell: 2-5_emoji, L29, anti_pca_both_k15
- `sweep_2-1_summarize_L29_both_k15`: prompt sweep single cell: 2-1_summarize, L29, anti_pca_both_k15
- `sweep_2-3-1_no_above_L28_both_k15`: prompt sweep single cell: 2-3-1_no_above, L28, anti_pca_both_k15
- `sweep_2-5_token_L30_both_k15`: prompt sweep single cell: 2-5_token, L30, anti_pca_both_k15
- `sweep_2-1_summarize_L30_both_k15`: prompt sweep single cell: 2-1_summarize, L30, anti_pca_both_k15
- `sweep_2-3-1_token_L31_both_k15`: prompt sweep single cell: 2-3-1_token, L31, anti_pca_both_k15
- `sweep_2-5_emoji_L30_both_k15`: prompt sweep single cell: 2-5_emoji, L30, anti_pca_both_k15
- `sweep_2-5_token_L28_both_k15`: prompt sweep single cell: 2-5_token, L28, anti_pca_both_k15
- `sweep_2-1_emoji_L30_both_k15`: prompt sweep single cell: 2-1_emoji, L30, anti_pca_both_k15
- `sweep_2-3-1_token_L28_both_k15`: prompt sweep single cell: 2-3-1_token, L28, anti_pca_both_k15
- `sweep_2-5_summarize_L29_both_k15`: prompt sweep single cell: 2-5_summarize, L29, anti_pca_both_k15
- `sweep_2-3-1_emoji_L29_both_k15`: prompt sweep single cell: 2-3-1_emoji, L29, anti_pca_both_k15
- `sweep_2-1_summarize_L31_both_k15`: prompt sweep single cell: 2-1_summarize, L31, anti_pca_both_k15
- `sweep_2-1_emoji_L29_both_k15`: prompt sweep single cell: 2-1_emoji, L29, anti_pca_both_k15
- `sweep_2-3-1_summarize_L31_both_k15`: prompt sweep single cell: 2-3-1_summarize, L31, anti_pca_both_k15
- `sweep_2-1_summarize_L28_both_k15`: prompt sweep single cell: 2-1_summarize, L28, anti_pca_both_k15
- `sweep_2-3-1_emoji_L28_both_k15`: prompt sweep single cell: 2-3-1_emoji, L28, anti_pca_both_k15
- `sweep_2-5_summarize_L30_both_k15`: prompt sweep single cell: 2-5_summarize, L30, anti_pca_both_k15
- `sweep_2-1_emoji_L28_both_k15`: prompt sweep single cell: 2-1_emoji, L28, anti_pca_both_k15
- `sweep_2-5_emoji_L28_both_k15`: prompt sweep single cell: 2-5_emoji, L28, anti_pca_both_k15
- `sweep_2-5_token_L31_both_k15`: prompt sweep single cell: 2-5_token, L31, anti_pca_both_k15
- `sweep_2-5_summarize_L28_both_k15`: prompt sweep single cell: 2-5_summarize, L28, anti_pca_both_k15
- `sweep_2-5_emoji_L31_both_k15`: prompt sweep single cell: 2-5_emoji, L31, anti_pca_both_k15
- `sweep_2-5_summarize_L31_both_k15`: prompt sweep single cell: 2-5_summarize, L31, anti_pca_both_k15
- `sweep_2-3-1_emoji_L31_both_k15`: prompt sweep single cell: 2-3-1_emoji, L31, anti_pca_both_k15
- `sweep_2-7_token_L30_both_k15`: prompt sweep single cell: 2-7_token, L30, anti_pca_both_k15
- `sweep_2-1_emoji_L31_both_k15`: prompt sweep single cell: 2-1_emoji, L31, anti_pca_both_k15
- `sweep_2-7_token_L29_both_k15`: prompt sweep single cell: 2-7_token, L29, anti_pca_both_k15
- `sweep_2-7_emoji_L29_both_k15`: prompt sweep single cell: 2-7_emoji, L29, anti_pca_both_k15
- `sweep_2-7_token_L31_both_k15`: prompt sweep single cell: 2-7_token, L31, anti_pca_both_k15
- `sweep_1-3_token_L30_both_k15`: prompt sweep single cell: 1-3_token, L30, anti_pca_both_k15
- `sweep_1-3_token_L29_both_k15`: prompt sweep single cell: 1-3_token, L29, anti_pca_both_k15
- `sweep_2-7_emoji_L28_both_k15`: prompt sweep single cell: 2-7_emoji, L28, anti_pca_both_k15
- `sweep_2-7_token_L28_both_k15`: prompt sweep single cell: 2-7_token, L28, anti_pca_both_k15
- `sweep_2-7_emoji_L30_both_k15`: prompt sweep single cell: 2-7_emoji, L30, anti_pca_both_k15
- `sweep_1-3_token_L28_both_k15`: prompt sweep single cell: 1-3_token, L28, anti_pca_both_k15
- `sweep_1-3_token_L31_both_k15`: prompt sweep single cell: 1-3_token, L31, anti_pca_both_k15
- `sweep_2-8_emoji_L28_both_k15`: prompt sweep single cell: 2-8_emoji, L28, anti_pca_both_k15
- `sweep_2-7_no_above_L30_both_k15`: prompt sweep single cell: 2-7_no_above, L30, anti_pca_both_k15
- `sweep_2-8_emoji_L29_both_k15`: prompt sweep single cell: 2-8_emoji, L29, anti_pca_both_k15
- `sweep_2-7_no_above_L31_both_k15`: prompt sweep single cell: 2-7_no_above, L31, anti_pca_both_k15
- `sweep_2-7_no_above_L29_both_k15`: prompt sweep single cell: 2-7_no_above, L29, anti_pca_both_k15
- `sweep_2-7_emoji_L31_both_k15`: prompt sweep single cell: 2-7_emoji, L31, anti_pca_both_k15
- `sweep_2-7_no_above_L28_both_k15`: prompt sweep single cell: 2-7_no_above, L28, anti_pca_both_k15
- `sweep_2-7_summarize_L31_both_k15`: prompt sweep single cell: 2-7_summarize, L31, anti_pca_both_k15
- `sweep_2-7_summarize_L30_both_k15`: prompt sweep single cell: 2-7_summarize, L30, anti_pca_both_k15
- `sweep_2-8_emoji_L30_both_k15`: prompt sweep single cell: 2-8_emoji, L30, anti_pca_both_k15
- `sweep_2-7_summarize_L29_both_k15`: prompt sweep single cell: 2-7_summarize, L29, anti_pca_both_k15
- `sweep_2-8_token_L30_both_k15`: prompt sweep single cell: 2-8_token, L30, anti_pca_both_k15
- `sweep_2-8_token_L29_both_k15`: prompt sweep single cell: 2-8_token, L29, anti_pca_both_k15
- `sweep_2-8_token_L31_both_k15`: prompt sweep single cell: 2-8_token, L31, anti_pca_both_k15
- `sweep_2-8_summarize_L30_both_k15`: prompt sweep single cell: 2-8_summarize, L30, anti_pca_both_k15
- `sweep_2-7_summarize_L28_both_k15`: prompt sweep single cell: 2-7_summarize, L28, anti_pca_both_k15
- `sweep_2-8_summarize_L29_both_k15`: prompt sweep single cell: 2-8_summarize, L29, anti_pca_both_k15
- `sweep_2-8_L30_both_k15`: prompt sweep single cell: 2-8, L30, anti_pca_both_k15
- `sweep_2-8_L28_both_k15`: prompt sweep single cell: 2-8, L28, anti_pca_both_k15
- `sweep_2-8_summarize_L28_both_k15`: prompt sweep single cell: 2-8_summarize, L28, anti_pca_both_k15
- `sweep_2-8_L29_both_k15`: prompt sweep single cell: 2-8, L29, anti_pca_both_k15
- `sweep_2-8_token_L28_both_k15`: prompt sweep single cell: 2-8_token, L28, anti_pca_both_k15
- `sweep_2-8_emoji_L31_both_k15`: prompt sweep single cell: 2-8_emoji, L31, anti_pca_both_k15
- `sweep_2-8_summarize_L31_both_k15`: prompt sweep single cell: 2-8_summarize, L31, anti_pca_both_k15
- `sweep_2-8_L31_both_k15`: prompt sweep single cell: 2-8, L31, anti_pca_both_k15
- `sweep_2-8_no_above_L29_both_k15`: prompt sweep single cell: 2-8_no_above, L29, anti_pca_both_k15
- `sweep_2-8_no_above_L30_both_k15`: prompt sweep single cell: 2-8_no_above, L30, anti_pca_both_k15
- `sweep_2-8_no_above_L28_both_k15`: prompt sweep single cell: 2-8_no_above, L28, anti_pca_both_k15
- `sweep_2-8_no_above_L31_both_k15`: prompt sweep single cell: 2-8_no_above, L31, anti_pca_both_k15

## Prompt Notes

- Sweep: `prompt_sweep_l28_l29_l30_l31_both_k15`
- New preference prompts: `user_preference`, `user_avoidance`, `personalization_need`
- Token wording treatments: `2-1_token`, `user_preference_token`
- Pruned after n=100: `1-1_CN`, `1-1_CN_ASCII`, `1-1_EN`, `2-3-2_mem`, `2-4-1`, `2-6`, `2-7`, `2-8`, `2-4-1_user_word_represent`, `2-5_represent`, `2-7_represent`, `2-8_represent`
- Note: PrefEval n=1000 uses a pruned prompt sweep. The 2-1 topic prompt is useful for the target companion scenario but may partly fit PrefEval's topic-structured rows, so it is tracked with a token wording treatment.
