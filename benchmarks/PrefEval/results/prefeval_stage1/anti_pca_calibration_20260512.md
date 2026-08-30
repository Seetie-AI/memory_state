# PrefEval Stage 1 Offline Analysis

- Created UTC: `2026-05-12T18:36:11.496799+00:00`
- Analysis: `prefeval_stage1_anti_pca_calibration`
- Items: `1000`
- Tensor dir: `/Users/gordonxiong/Desktop/Repos/memory_state/benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- Elapsed: `28s`

## Notes

- Stored hidden vectors are raw extractor outputs; this offline pass applies retrieval transforms after loading.
- The n=1000 prompt-sweep table previously reported anti_pca_both_k15 plus L2-normalized cosine, not untreated raw cosine.
- candidate_only k=10 is a sanity check because earlier LongMemEval stages found candidate-only transforms harmful.

## Results

| rank | config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `2-3-1_L30_anti_pca_both_k15` | 0.110 | 0.254 | 0.311 | 0.218 | 0.214 |
| 2 | `2-3-1_L30_anti_pca_both_k5` | 0.102 | 0.235 | 0.310 | 0.209 | 0.207 |
| 3 | `2-3-2_query_L30_anti_pca_both_k15` | 0.097 | 0.241 | 0.310 | 0.208 | 0.198 |
| 4 | `2-3-1_L30_anti_pca_query_only_k15` | 0.100 | 0.235 | 0.309 | 0.209 | 0.200 |
| 5 | `2-1_L30_anti_pca_both_k5` | 0.097 | 0.215 | 0.305 | 0.203 | 0.201 |
| 6 | `2-1_L30_anti_pca_both_k10` | 0.095 | 0.215 | 0.304 | 0.203 | 0.198 |
| 7 | `2-3-1_L30_anti_pca_both_k20` | 0.105 | 0.245 | 0.302 | 0.210 | 0.203 |
| 8 | `2-5_L29_anti_pca_both_k15` | 0.096 | 0.233 | 0.301 | 0.204 | 0.199 |
| 9 | `2-1_L30_anti_pca_both_k15` | 0.100 | 0.209 | 0.299 | 0.201 | 0.195 |
| 10 | `2-3-1_L30_anti_pca_both_k10` | 0.101 | 0.238 | 0.297 | 0.206 | 0.206 |
| 11 | `2-5_L29_anti_pca_both_k30` | 0.102 | 0.218 | 0.295 | 0.202 | 0.192 |
| 12 | `2-1_L30_centered_cosine` | 0.086 | 0.204 | 0.295 | 0.193 | 0.194 |
| 13 | `2-5_L29_anti_pca_both_k20` | 0.101 | 0.230 | 0.294 | 0.204 | 0.198 |
| 14 | `2-3-1_L30_anti_pca_both_k2` | 0.099 | 0.227 | 0.294 | 0.201 | 0.202 |
| 15 | `2-3-1_L30_anti_pca_query_only_k20` | 0.096 | 0.225 | 0.293 | 0.199 | 0.192 |
| 16 | `2-3-1_L30_anti_pca_query_only_k5` | 0.097 | 0.215 | 0.293 | 0.198 | 0.197 |
| 17 | `2-3-2_query_L30_anti_pca_query_only_k15` | 0.093 | 0.219 | 0.293 | 0.196 | 0.189 |
| 18 | `2-1_L30_anti_pca_both_k2` | 0.086 | 0.200 | 0.292 | 0.190 | 0.191 |
| 19 | `2-5_L29_anti_pca_both_k10` | 0.095 | 0.219 | 0.291 | 0.198 | 0.196 |
| 20 | `2-3-1_L30_anti_pca_both_k30` | 0.105 | 0.224 | 0.290 | 0.201 | 0.191 |
| 21 | `2-1_L30_anti_pca_query_only_k15` | 0.095 | 0.204 | 0.290 | 0.193 | 0.188 |
| 22 | `2-3-2_query_L30_anti_pca_both_k5` | 0.077 | 0.216 | 0.290 | 0.187 | 0.185 |
| 23 | `2-1_L30_anti_pca_query_only_k5` | 0.093 | 0.206 | 0.289 | 0.193 | 0.194 |
| 24 | `2-3-1_L30_anti_pca_query_only_k10` | 0.099 | 0.222 | 0.288 | 0.197 | 0.195 |
| 25 | `2-3-2_query_L30_anti_pca_both_k20` | 0.096 | 0.225 | 0.287 | 0.196 | 0.188 |
| 26 | `2-1_L30_raw_cosine` | 0.094 | 0.205 | 0.287 | 0.193 | 0.196 |
| 27 | `2-1_L30_anti_pca_query_only_k10` | 0.093 | 0.203 | 0.287 | 0.192 | 0.190 |
| 28 | `2-3-2_query_L30_anti_pca_both_k10` | 0.087 | 0.213 | 0.287 | 0.191 | 0.188 |
| 29 | `2-3-1_L30_centered_cosine` | 0.096 | 0.216 | 0.285 | 0.196 | 0.200 |
| 30 | `2-1_L30_anti_pca_query_only_k20` | 0.083 | 0.200 | 0.283 | 0.184 | 0.175 |
| 31 | `2-1_L30_anti_pca_both_k20` | 0.096 | 0.209 | 0.279 | 0.191 | 0.186 |
| 32 | `2-3-1_L30_raw_cosine` | 0.102 | 0.209 | 0.278 | 0.194 | 0.200 |
| 33 | `2-3-2_query_L30_anti_pca_query_only_k20` | 0.084 | 0.201 | 0.277 | 0.183 | 0.174 |
| 34 | `2-3-1_L30_anti_pca_query_only_k2` | 0.098 | 0.200 | 0.275 | 0.188 | 0.190 |
| 35 | `2-3-2_query_L30_centered_cosine` | 0.085 | 0.196 | 0.275 | 0.182 | 0.183 |
| 36 | `2-5_L29_anti_pca_both_k50` | 0.083 | 0.222 | 0.274 | 0.186 | 0.173 |
| 37 | `2-3-2_query_L30_anti_pca_both_k2` | 0.087 | 0.210 | 0.274 | 0.185 | 0.187 |
| 38 | `2-5_L29_anti_pca_query_only_k10` | 0.084 | 0.198 | 0.271 | 0.183 | 0.181 |
| 39 | `2-5_L29_anti_pca_query_only_k15` | 0.088 | 0.209 | 0.270 | 0.184 | 0.183 |
| 40 | `2-1_L30_anti_pca_query_only_k2` | 0.089 | 0.192 | 0.269 | 0.181 | 0.188 |
| 41 | `2-3-1_L30_anti_pca_query_only_k30` | 0.097 | 0.205 | 0.267 | 0.185 | 0.179 |
| 42 | `2-3-2_query_L30_anti_pca_both_k30` | 0.085 | 0.206 | 0.267 | 0.181 | 0.171 |
| 43 | `2-5_L29_anti_pca_query_only_k20` | 0.080 | 0.204 | 0.267 | 0.177 | 0.172 |
| 44 | `2-3-2_query_L30_anti_pca_query_only_k10` | 0.081 | 0.189 | 0.264 | 0.174 | 0.171 |
| 45 | `2-3-2_query_L30_anti_pca_query_only_k5` | 0.087 | 0.195 | 0.263 | 0.177 | 0.180 |
| 46 | `2-1_L30_anti_pca_both_k30` | 0.092 | 0.201 | 0.259 | 0.179 | 0.173 |
| 47 | `2-3-2_query_L30_raw_cosine` | 0.078 | 0.180 | 0.258 | 0.170 | 0.171 |
| 48 | `2-1_L30_anti_pca_query_only_k30` | 0.080 | 0.187 | 0.256 | 0.170 | 0.162 |
| 49 | `2-3-1_L30_anti_pca_both_k50` | 0.101 | 0.204 | 0.254 | 0.183 | 0.176 |
| 50 | `2-3-2_query_L30_anti_pca_query_only_k30` | 0.083 | 0.182 | 0.254 | 0.170 | 0.161 |
| 51 | `2-5_L29_anti_pca_query_only_k30` | 0.078 | 0.185 | 0.253 | 0.168 | 0.162 |
| 52 | `2-5_L29_anti_pca_both_k5` | 0.077 | 0.180 | 0.241 | 0.164 | 0.170 |
| 53 | `2-3-1_L30_anti_pca_query_only_k50` | 0.077 | 0.186 | 0.238 | 0.162 | 0.154 |
| 54 | `2-5_L29_anti_pca_query_only_k50` | 0.076 | 0.181 | 0.236 | 0.160 | 0.153 |
| 55 | `2-3-2_query_L30_anti_pca_query_only_k2` | 0.080 | 0.172 | 0.235 | 0.158 | 0.166 |
| 56 | `2-3-2_query_L30_anti_pca_both_k50` | 0.083 | 0.186 | 0.229 | 0.162 | 0.156 |
| 57 | `2-1_L30_anti_pca_both_k50` | 0.088 | 0.186 | 0.227 | 0.162 | 0.156 |
| 58 | `2-5_L29_raw_cosine` | 0.064 | 0.163 | 0.227 | 0.149 | 0.153 |
| 59 | `2-1_L30_anti_pca_query_only_k50` | 0.077 | 0.168 | 0.224 | 0.153 | 0.145 |
| 60 | `2-3-2_query_L30_anti_pca_query_only_k50` | 0.071 | 0.170 | 0.215 | 0.146 | 0.140 |
| 61 | `2-5_L29_anti_pca_query_only_k5` | 0.064 | 0.149 | 0.212 | 0.141 | 0.147 |
| 62 | `2-5_L29_centered_cosine` | 0.060 | 0.150 | 0.204 | 0.133 | 0.140 |
| 63 | `2-5_L29_anti_pca_both_k2` | 0.059 | 0.142 | 0.203 | 0.132 | 0.137 |
| 64 | `2-3-2_query_L30_anti_pca_candidate_only_k10` | 0.066 | 0.131 | 0.180 | 0.125 | 0.125 |
| 65 | `2-5_L29_anti_pca_query_only_k2` | 0.050 | 0.117 | 0.165 | 0.109 | 0.117 |
| 66 | `2-3-1_L30_anti_pca_candidate_only_k10` | 0.053 | 0.118 | 0.164 | 0.110 | 0.110 |
| 67 | `2-1_L30_anti_pca_candidate_only_k10` | 0.057 | 0.120 | 0.159 | 0.110 | 0.113 |
| 68 | `2-5_L29_anti_pca_candidate_only_k10` | 0.047 | 0.110 | 0.149 | 0.099 | 0.102 |

## Configs

- `2-3-1_L30_anti_pca_both_k15`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=15)
- `2-3-1_L30_anti_pca_both_k5`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=5)
- `2-3-2_query_L30_anti_pca_both_k15`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=15)
- `2-3-1_L30_anti_pca_query_only_k15`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=15)
- `2-1_L30_anti_pca_both_k5`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=5)
- `2-1_L30_anti_pca_both_k10`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=10)
- `2-3-1_L30_anti_pca_both_k20`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=20)
- `2-5_L29_anti_pca_both_k15`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=15)
- `2-1_L30_anti_pca_both_k15`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=15)
- `2-3-1_L30_anti_pca_both_k10`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=10)
- `2-5_L29_anti_pca_both_k30`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=30)
- `2-1_L30_centered_cosine`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate mean subtracted from candidates and queries, then L2-normalized cosine (centered_cosine)
- `2-5_L29_anti_pca_both_k20`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=20)
- `2-3-1_L30_anti_pca_both_k2`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=2)
- `2-3-1_L30_anti_pca_query_only_k20`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=20)
- `2-3-1_L30_anti_pca_query_only_k5`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=5)
- `2-3-2_query_L30_anti_pca_query_only_k15`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=15)
- `2-1_L30_anti_pca_both_k2`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=2)
- `2-5_L29_anti_pca_both_k10`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=10)
- `2-3-1_L30_anti_pca_both_k30`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=30)
- `2-1_L30_anti_pca_query_only_k15`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=15)
- `2-3-2_query_L30_anti_pca_both_k5`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=5)
- `2-1_L30_anti_pca_query_only_k5`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=5)
- `2-3-1_L30_anti_pca_query_only_k10`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=10)
- `2-3-2_query_L30_anti_pca_both_k20`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=20)
- `2-1_L30_raw_cosine`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, raw hidden vectors with L2-normalized cosine (raw_cosine)
- `2-1_L30_anti_pca_query_only_k10`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=10)
- `2-3-2_query_L30_anti_pca_both_k10`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=10)
- `2-3-1_L30_centered_cosine`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate mean subtracted from candidates and queries, then L2-normalized cosine (centered_cosine)
- `2-1_L30_anti_pca_query_only_k20`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=20)
- `2-1_L30_anti_pca_both_k20`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=20)
- `2-3-1_L30_raw_cosine`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, raw hidden vectors with L2-normalized cosine (raw_cosine)
- `2-3-2_query_L30_anti_pca_query_only_k20`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=20)
- `2-3-1_L30_anti_pca_query_only_k2`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=2)
- `2-3-2_query_L30_centered_cosine`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate mean subtracted from candidates and queries, then L2-normalized cosine (centered_cosine)
- `2-5_L29_anti_pca_both_k50`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=50)
- `2-3-2_query_L30_anti_pca_both_k2`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=2)
- `2-5_L29_anti_pca_query_only_k10`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=10)
- `2-5_L29_anti_pca_query_only_k15`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=15)
- `2-1_L30_anti_pca_query_only_k2`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=2)
- `2-3-1_L30_anti_pca_query_only_k30`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=30)
- `2-3-2_query_L30_anti_pca_both_k30`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=30)
- `2-5_L29_anti_pca_query_only_k20`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=20)
- `2-3-2_query_L30_anti_pca_query_only_k10`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=10)
- `2-3-2_query_L30_anti_pca_query_only_k5`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=5)
- `2-1_L30_anti_pca_both_k30`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=30)
- `2-3-2_query_L30_raw_cosine`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, raw hidden vectors with L2-normalized cosine (raw_cosine)
- `2-1_L30_anti_pca_query_only_k30`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=30)
- `2-3-1_L30_anti_pca_both_k50`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=50)
- `2-3-2_query_L30_anti_pca_query_only_k30`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=30)
- `2-5_L29_anti_pca_query_only_k30`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=30)
- `2-5_L29_anti_pca_both_k5`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=5)
- `2-3-1_L30_anti_pca_query_only_k50`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=50)
- `2-5_L29_anti_pca_query_only_k50`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=50)
- `2-3-2_query_L30_anti_pca_query_only_k2`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=2)
- `2-3-2_query_L30_anti_pca_both_k50`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=50)
- `2-1_L30_anti_pca_both_k50`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=50)
- `2-5_L29_raw_cosine`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, raw hidden vectors with L2-normalized cosine (raw_cosine)
- `2-1_L30_anti_pca_query_only_k50`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=50)
- `2-3-2_query_L30_anti_pca_query_only_k50`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=50)
- `2-5_L29_anti_pca_query_only_k5`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=5)
- `2-5_L29_centered_cosine`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate mean subtracted from candidates and queries, then L2-normalized cosine (centered_cosine)
- `2-5_L29_anti_pca_both_k2`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate mean and top-k PCs removed from candidates and queries (anti_pca_both, k=2)
- `2-3-2_query_L30_anti_pca_candidate_only_k10`: PrefEval Stage 1 anti-PCA calibration: 2-3-2_query, L30, candidate subtracts candidate mean and removes top-10 PCs; query raw (anti_pca_candidate_only, k=10)
- `2-5_L29_anti_pca_query_only_k2`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate raw; query subtracts candidate mean and removes top-k candidate PCs (anti_pca_query_only, k=2)
- `2-3-1_L30_anti_pca_candidate_only_k10`: PrefEval Stage 1 anti-PCA calibration: 2-3-1, L30, candidate subtracts candidate mean and removes top-10 PCs; query raw (anti_pca_candidate_only, k=10)
- `2-1_L30_anti_pca_candidate_only_k10`: PrefEval Stage 1 anti-PCA calibration: 2-1, L30, candidate subtracts candidate mean and removes top-10 PCs; query raw (anti_pca_candidate_only, k=10)
- `2-5_L29_anti_pca_candidate_only_k10`: PrefEval Stage 1 anti-PCA calibration: 2-5, L29, candidate subtracts candidate mean and removes top-10 PCs; query raw (anti_pca_candidate_only, k=10)
