# PrefEval External Embedding Fusion

- Created UTC: `2026-05-13T02:40:59.208705+00:00`
- Items: `1000`
- Hidden tensor dir: `/Users/gordonxiong/Desktop/Repos/memory_state/benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- Embedding cache dir: `/Users/gordonxiong/Desktop/Repos/memory_state/benchmarks/PrefEval/tensors/qwen3_embedding_implicit_persona_n1000_d19e54c734`
- Embedding model: `models/Qwen3-Embedding-0.6B-4bit-DWQ`
- Source rule: `top20 source_count>=2`
- Elapsed: `3m19s`

## Notes

- External embeddings are used only as a score matrix/source, not concatenated with 9B hidden vectors.
- Primary K3 dense baseline is 2-3-1 + 2-5 + 2-1 with vector_average_component_norm.
- source_count>=2 experiments use per-source top-k lists, with prompt components kept as separate sources.
- Concat experiments use source_count>=concat_source_min plus embedding top-k candidates, then rerank only that candidate set.

## Results

| rank | config | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR | avg shortlist | oracle@shortlist |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.120 | 0.266 | 0.358 | 0.204 | 0.242 | 0.236 | 23.3 | 0.639 |
| 2 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.117 | 0.265 | 0.358 | 0.203 | 0.241 | 0.236 | 23.3 | 0.639 |
| 3 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.125 | 0.265 | 0.357 | 0.205 | 0.243 | 0.237 | 23.3 | 0.639 |
| 4 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.120 | 0.264 | 0.357 | 0.203 | 0.242 | 0.237 | 23.3 | 0.639 |
| 5 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.121 | 0.261 | 0.357 | 0.202 | 0.241 | 0.236 | 23.3 | 0.639 |
| 6 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.119 | 0.268 | 0.357 | 0.204 | 0.241 | 0.235 | 23.3 | 0.639 |
| 7 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.116 | 0.260 | 0.357 | 0.199 | 0.238 | 0.232 | 23.3 | 0.639 |
| 8 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.128 | 0.266 | 0.356 | 0.207 | 0.244 | 0.239 | 23.3 | 0.639 |
| 9 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.122 | 0.264 | 0.356 | 0.203 | 0.241 | 0.236 | 23.3 | 0.639 |
| 10 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.119 | 0.262 | 0.356 | 0.201 | 0.240 | 0.235 | 23.3 | 0.639 |
| 11 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.120 | 0.262 | 0.356 | 0.201 | 0.240 | 0.234 | 23.3 | 0.639 |
| 12 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.121 | 0.264 | 0.355 | 0.204 | 0.242 | 0.238 | 23.3 | 0.639 |
| 13 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.123 | 0.264 | 0.355 | 0.204 | 0.241 | 0.238 | 23.3 | 0.639 |
| 14 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.122 | 0.265 | 0.355 | 0.204 | 0.241 | 0.237 | 23.3 | 0.639 |
| 15 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.122 | 0.267 | 0.355 | 0.205 | 0.241 | 0.237 | 23.3 | 0.639 |
| 16 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.116 | 0.267 | 0.355 | 0.203 | 0.240 | 0.235 | 23.3 | 0.639 |
| 17 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.117 | 0.261 | 0.355 | 0.199 | 0.238 | 0.231 | 23.3 | 0.639 |
| 18 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.114 | 0.265 | 0.355 | 0.200 | 0.237 | 0.231 | 23.3 | 0.639 |
| 19 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.124 | 0.269 | 0.354 | 0.207 | 0.241 | 0.237 | 23.3 | 0.639 |
| 20 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.124 | 0.265 | 0.354 | 0.205 | 0.241 | 0.237 | 23.3 | 0.639 |
| 21 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.118 | 0.260 | 0.354 | 0.199 | 0.238 | 0.233 | 23.3 | 0.639 |
| 22 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.116 | 0.261 | 0.354 | 0.199 | 0.237 | 0.230 | 23.3 | 0.639 |
| 23 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.124 | 0.263 | 0.353 | 0.205 | 0.242 | 0.239 | 23.3 | 0.639 |
| 24 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.127 | 0.262 | 0.353 | 0.204 | 0.241 | 0.237 | 23.3 | 0.639 |
| 25 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.123 | 0.264 | 0.353 | 0.204 | 0.241 | 0.237 | 23.3 | 0.639 |
| 26 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.121 | 0.261 | 0.353 | 0.201 | 0.239 | 0.235 | 23.3 | 0.639 |
| 27 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.119 | 0.265 | 0.353 | 0.202 | 0.239 | 0.233 | 23.3 | 0.639 |
| 28 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.117 | 0.265 | 0.353 | 0.202 | 0.238 | 0.233 | 23.3 | 0.639 |
| 29 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.117 | 0.261 | 0.353 | 0.200 | 0.237 | 0.233 | 23.3 | 0.639 |
| 30 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.116 | 0.264 | 0.353 | 0.200 | 0.237 | 0.231 | 23.3 | 0.639 |
| 31 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.116 | 0.257 | 0.353 | 0.197 | 0.236 | 0.230 | 23.3 | 0.639 |
| 32 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.128 | 0.264 | 0.352 | 0.206 | 0.242 | 0.239 | 23.3 | 0.639 |
| 33 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.125 | 0.261 | 0.352 | 0.203 | 0.241 | 0.238 | 23.3 | 0.639 |
| 34 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.124 | 0.266 | 0.352 | 0.205 | 0.240 | 0.237 | 23.3 | 0.639 |
| 35 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.123 | 0.266 | 0.352 | 0.205 | 0.240 | 0.236 | 23.3 | 0.639 |
| 36 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.122 | 0.266 | 0.352 | 0.204 | 0.239 | 0.236 | 23.3 | 0.639 |
| 37 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.122 | 0.263 | 0.352 | 0.203 | 0.239 | 0.235 | 23.3 | 0.639 |
| 38 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.118 | 0.264 | 0.352 | 0.202 | 0.238 | 0.233 | 23.3 | 0.639 |
| 39 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.118 | 0.265 | 0.352 | 0.202 | 0.238 | 0.232 | 23.3 | 0.639 |
| 40 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.116 | 0.269 | 0.352 | 0.202 | 0.237 | 0.231 | 23.3 | 0.639 |
| 41 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.118 | 0.256 | 0.352 | 0.197 | 0.236 | 0.232 | 23.3 | 0.639 |
| 42 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.117 | 0.260 | 0.352 | 0.198 | 0.236 | 0.230 | 23.3 | 0.639 |
| 43 | `k3_bm25_embedding_full_d0.75_b0.20_e0.05` | 0.114 | 0.257 | 0.352 | 0.196 | 0.235 | 0.225 |  |  |
| 44 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.130 | 0.263 | 0.351 | 0.206 | 0.242 | 0.240 | 23.3 | 0.639 |
| 45 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.124 | 0.264 | 0.351 | 0.205 | 0.241 | 0.238 | 23.3 | 0.639 |
| 46 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.124 | 0.268 | 0.351 | 0.206 | 0.240 | 0.237 | 23.3 | 0.639 |
| 47 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.124 | 0.268 | 0.351 | 0.206 | 0.240 | 0.237 | 23.3 | 0.639 |
| 48 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.124 | 0.264 | 0.351 | 0.204 | 0.240 | 0.237 | 23.3 | 0.639 |
| 49 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.121 | 0.266 | 0.351 | 0.204 | 0.239 | 0.236 | 23.3 | 0.639 |
| 50 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.116 | 0.258 | 0.351 | 0.197 | 0.236 | 0.232 | 23.3 | 0.639 |
| 51 | `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10` | 0.116 | 0.255 | 0.351 | 0.195 | 0.235 | 0.227 | 22.1 | 0.635 |
| 52 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.128 | 0.268 | 0.350 | 0.208 | 0.242 | 0.239 | 23.3 | 0.639 |
| 53 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.127 | 0.266 | 0.350 | 0.207 | 0.241 | 0.239 | 23.3 | 0.639 |
| 54 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.127 | 0.267 | 0.350 | 0.207 | 0.241 | 0.238 | 23.3 | 0.639 |
| 55 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.126 | 0.270 | 0.350 | 0.208 | 0.241 | 0.238 | 23.3 | 0.639 |
| 56 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.125 | 0.270 | 0.350 | 0.207 | 0.240 | 0.237 | 23.3 | 0.639 |
| 57 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.125 | 0.267 | 0.350 | 0.206 | 0.240 | 0.236 | 23.3 | 0.639 |
| 58 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.116 | 0.263 | 0.350 | 0.200 | 0.236 | 0.231 | 23.3 | 0.639 |
| 59 | `source_ge3_plus_embedding_only_top20_rerank_k3bm25_ratio60_10` | 0.116 | 0.257 | 0.350 | 0.197 | 0.235 | 0.227 | 19.1 | 0.572 |
| 60 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.128 | 0.262 | 0.349 | 0.204 | 0.240 | 0.237 | 23.3 | 0.639 |
| 61 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.122 | 0.263 | 0.349 | 0.203 | 0.238 | 0.235 | 23.3 | 0.639 |
| 62 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.121 | 0.264 | 0.349 | 0.203 | 0.238 | 0.234 | 23.3 | 0.639 |
| 63 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.118 | 0.261 | 0.349 | 0.200 | 0.236 | 0.232 | 23.3 | 0.639 |
| 64 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.118 | 0.257 | 0.349 | 0.198 | 0.236 | 0.232 | 23.3 | 0.639 |
| 65 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.125 | 0.263 | 0.348 | 0.205 | 0.240 | 0.240 | 23.3 | 0.639 |
| 66 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.121 | 0.258 | 0.348 | 0.199 | 0.236 | 0.233 | 23.3 | 0.639 |
| 67 | `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05` | 0.117 | 0.258 | 0.348 | 0.197 | 0.234 | 0.227 | 22.1 | 0.635 |
| 68 | `k3_bm25_embedding_full_d0.70_b0.20_e0.10` | 0.116 | 0.257 | 0.348 | 0.196 | 0.234 | 0.227 |  |  |
| 69 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.115 | 0.251 | 0.348 | 0.194 | 0.234 | 0.231 | 23.3 | 0.639 |
| 70 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.116 | 0.254 | 0.348 | 0.195 | 0.233 | 0.230 | 23.3 | 0.639 |
| 71 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.117 | 0.253 | 0.348 | 0.195 | 0.233 | 0.229 | 23.3 | 0.639 |
| 72 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.128 | 0.261 | 0.347 | 0.205 | 0.240 | 0.240 | 23.3 | 0.639 |
| 73 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.128 | 0.263 | 0.347 | 0.206 | 0.240 | 0.239 | 23.3 | 0.639 |
| 74 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.128 | 0.264 | 0.347 | 0.206 | 0.240 | 0.238 | 23.3 | 0.639 |
| 75 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.127 | 0.265 | 0.347 | 0.206 | 0.240 | 0.238 | 23.3 | 0.639 |
| 76 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.127 | 0.268 | 0.347 | 0.207 | 0.239 | 0.238 | 23.3 | 0.639 |
| 77 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.124 | 0.265 | 0.347 | 0.205 | 0.239 | 0.239 | 23.3 | 0.639 |
| 78 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.124 | 0.261 | 0.347 | 0.203 | 0.239 | 0.237 | 23.3 | 0.639 |
| 79 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.117 | 0.263 | 0.347 | 0.200 | 0.235 | 0.232 | 23.3 | 0.639 |
| 80 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.120 | 0.259 | 0.347 | 0.199 | 0.235 | 0.232 | 23.3 | 0.639 |
| 81 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.119 | 0.258 | 0.347 | 0.198 | 0.234 | 0.231 | 23.3 | 0.639 |
| 82 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.119 | 0.257 | 0.347 | 0.197 | 0.234 | 0.230 | 23.3 | 0.639 |
| 83 | `result_fusion_k3bm25_ratio60_10_slots_1_2_4_5_embedding_slot3` | 0.118 | 0.240 | 0.347 | 0.188 | 0.232 | 0.225 |  |  |
| 84 | `source_ge3_plus_embedding_only_top20_rerank_k3bm25_075_025` | 0.120 | 0.257 | 0.346 | 0.198 | 0.234 | 0.228 | 19.1 | 0.572 |
| 85 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.119 | 0.262 | 0.346 | 0.200 | 0.234 | 0.232 | 23.3 | 0.639 |
| 86 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.121 | 0.255 | 0.346 | 0.197 | 0.234 | 0.232 | 23.3 | 0.639 |
| 87 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.118 | 0.260 | 0.346 | 0.198 | 0.234 | 0.230 | 23.3 | 0.639 |
| 88 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.127 | 0.264 | 0.345 | 0.206 | 0.239 | 0.240 | 23.3 | 0.639 |
| 89 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.128 | 0.268 | 0.345 | 0.208 | 0.239 | 0.239 | 23.3 | 0.639 |
| 90 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.127 | 0.270 | 0.344 | 0.208 | 0.239 | 0.238 | 23.3 | 0.639 |
| 91 | `k3_bm25_dense_top20_d0.75_b0.25` | 0.122 | 0.264 | 0.344 | 0.203 | 0.235 | 0.230 |  |  |
| 92 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.121 | 0.259 | 0.344 | 0.199 | 0.234 | 0.231 | 23.3 | 0.639 |
| 93 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.119 | 0.258 | 0.344 | 0.198 | 0.233 | 0.230 | 23.3 | 0.639 |
| 94 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.117 | 0.250 | 0.344 | 0.194 | 0.232 | 0.229 | 23.3 | 0.639 |
| 95 | `five_source_top10_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.117 | 0.251 | 0.343 | 0.195 | 0.233 | 0.229 | 29.8 | 0.635 |
| 96 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.129 | 0.269 | 0.342 | 0.208 | 0.238 | 0.238 | 23.3 | 0.639 |
| 97 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.121 | 0.258 | 0.342 | 0.199 | 0.233 | 0.232 | 23.3 | 0.639 |
| 98 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.121 | 0.257 | 0.342 | 0.198 | 0.233 | 0.230 | 23.3 | 0.639 |
| 99 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.118 | 0.259 | 0.342 | 0.199 | 0.233 | 0.232 | 23.3 | 0.639 |
| 100 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.121 | 0.256 | 0.342 | 0.197 | 0.232 | 0.231 | 23.3 | 0.639 |
| 101 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.118 | 0.258 | 0.342 | 0.198 | 0.232 | 0.230 | 23.3 | 0.639 |
| 102 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.120 | 0.252 | 0.342 | 0.195 | 0.232 | 0.230 | 23.3 | 0.639 |
| 103 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.119 | 0.258 | 0.342 | 0.198 | 0.232 | 0.230 | 23.3 | 0.639 |
| 104 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.120 | 0.257 | 0.341 | 0.198 | 0.232 | 0.231 | 23.3 | 0.639 |
| 105 | `five_source_top3_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.114 | 0.254 | 0.341 | 0.195 | 0.231 | 0.225 | 9.6 | 0.402 |
| 106 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.120 | 0.256 | 0.340 | 0.198 | 0.232 | 0.232 | 23.3 | 0.639 |
| 107 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.120 | 0.261 | 0.340 | 0.199 | 0.231 | 0.230 | 23.3 | 0.639 |
| 108 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.118 | 0.256 | 0.340 | 0.197 | 0.231 | 0.229 | 23.3 | 0.639 |
| 109 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.119 | 0.250 | 0.340 | 0.194 | 0.230 | 0.229 | 23.3 | 0.639 |
| 110 | `k3_key_assoc_topic_vector_average` | 0.126 | 0.265 | 0.339 | 0.205 | 0.235 | 0.231 |  |  |
| 111 | `five_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.119 | 0.255 | 0.339 | 0.196 | 0.231 | 0.226 | 22.1 | 0.635 |
| 112 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.119 | 0.254 | 0.339 | 0.196 | 0.230 | 0.229 | 23.3 | 0.639 |
| 113 | `five_source_top5_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.111 | 0.251 | 0.339 | 0.192 | 0.228 | 0.223 | 15.6 | 0.499 |
| 114 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.122 | 0.252 | 0.338 | 0.195 | 0.230 | 0.230 | 23.3 | 0.639 |
| 115 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.120 | 0.253 | 0.338 | 0.195 | 0.230 | 0.230 | 23.3 | 0.639 |
| 116 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.119 | 0.255 | 0.337 | 0.196 | 0.229 | 0.228 | 23.3 | 0.639 |
| 117 | `four_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.117 | 0.254 | 0.337 | 0.195 | 0.229 | 0.223 | 17.9 | 0.568 |
| 118 | `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10` | 0.123 | 0.254 | 0.336 | 0.198 | 0.231 | 0.229 | 22.1 | 0.635 |
| 119 | `k3_bm25_embedding_full_d0.65_b0.25_e0.10` | 0.121 | 0.254 | 0.336 | 0.197 | 0.230 | 0.227 |  |  |
| 120 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.116 | 0.254 | 0.336 | 0.195 | 0.229 | 0.228 | 23.3 | 0.639 |
| 121 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.120 | 0.257 | 0.335 | 0.198 | 0.230 | 0.229 | 23.3 | 0.639 |
| 122 | `k3_bm25_full_d0.75_b0.25` | 0.117 | 0.251 | 0.335 | 0.193 | 0.228 | 0.222 |  |  |
| 123 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.120 | 0.253 | 0.333 | 0.196 | 0.228 | 0.229 | 23.3 | 0.639 |
| 124 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.120 | 0.256 | 0.333 | 0.197 | 0.228 | 0.228 | 23.3 | 0.639 |
| 125 | `k3_bm25_embedding_full_d0.60_b0.25_e0.15` | 0.121 | 0.251 | 0.333 | 0.195 | 0.228 | 0.226 |  |  |
| 126 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.118 | 0.255 | 0.333 | 0.196 | 0.228 | 0.228 | 23.3 | 0.639 |
| 127 | `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15` | 0.119 | 0.254 | 0.333 | 0.196 | 0.228 | 0.227 | 22.1 | 0.635 |
| 128 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.120 | 0.258 | 0.331 | 0.199 | 0.228 | 0.229 | 23.3 | 0.639 |
| 129 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.119 | 0.249 | 0.331 | 0.193 | 0.227 | 0.229 | 23.3 | 0.639 |
| 130 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.116 | 0.256 | 0.331 | 0.196 | 0.227 | 0.227 | 23.3 | 0.639 |
| 131 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.118 | 0.254 | 0.330 | 0.196 | 0.227 | 0.229 | 23.3 | 0.639 |
| 132 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.119 | 0.256 | 0.330 | 0.197 | 0.227 | 0.228 | 23.3 | 0.639 |
| 133 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.119 | 0.256 | 0.330 | 0.197 | 0.227 | 0.228 | 23.3 | 0.639 |
| 134 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.116 | 0.254 | 0.330 | 0.195 | 0.226 | 0.227 | 23.3 | 0.639 |
| 135 | `result_fusion_k3bm25_075_025_slots_1_2_4_5_embedding_slot3` | 0.117 | 0.233 | 0.330 | 0.184 | 0.224 | 0.220 |  |  |
| 136 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.114 | 0.253 | 0.329 | 0.194 | 0.225 | 0.226 | 23.3 | 0.639 |
| 137 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.117 | 0.252 | 0.326 | 0.194 | 0.224 | 0.225 | 23.3 | 0.639 |
| 138 | `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25` | 0.115 | 0.251 | 0.326 | 0.193 | 0.223 | 0.224 | 22.1 | 0.635 |
| 139 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.116 | 0.255 | 0.325 | 0.195 | 0.223 | 0.225 | 23.3 | 0.639 |
| 140 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.112 | 0.254 | 0.325 | 0.194 | 0.223 | 0.225 | 23.3 | 0.639 |
| 141 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.111 | 0.253 | 0.324 | 0.193 | 0.222 | 0.224 | 23.3 | 0.639 |
| 142 | `k3_bm25_embedding_full_d0.50_b0.25_e0.25` | 0.117 | 0.250 | 0.323 | 0.193 | 0.223 | 0.225 |  |  |
| 143 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.107 | 0.245 | 0.323 | 0.186 | 0.218 | 0.220 | 23.3 | 0.639 |
| 144 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.116 | 0.253 | 0.322 | 0.194 | 0.222 | 0.225 | 23.3 | 0.639 |
| 145 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.109 | 0.251 | 0.322 | 0.191 | 0.220 | 0.223 | 23.3 | 0.639 |
| 146 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.108 | 0.257 | 0.321 | 0.193 | 0.219 | 0.221 | 23.3 | 0.639 |
| 147 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.107 | 0.251 | 0.319 | 0.189 | 0.217 | 0.219 | 23.3 | 0.639 |
| 148 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.102 | 0.243 | 0.310 | 0.183 | 0.210 | 0.215 | 23.3 | 0.639 |
| 149 | `external_embedding` | 0.084 | 0.207 | 0.287 | 0.155 | 0.187 | 0.189 |  |  |
| 150 | `bm25` | 0.035 | 0.074 | 0.094 | 0.058 | 0.066 | 0.067 |  |  |
| 151 | `embedding_only_top20_rerank_k3bm25_075_025` | 0.019 | 0.043 | 0.087 | 0.033 | 0.050 | 0.091 | 6.7 | 0.054 |
| 152 | `embedding_only_top20_rerank_k3bm25_ratio60_10` | 0.020 | 0.045 | 0.085 | 0.034 | 0.050 | 0.093 | 6.7 | 0.054 |

## Configs

- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.30 + BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.20 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.35 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.35 + BM25 0.05.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.20 + BM25 0.15.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.10 + BM25 0.15.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.20 + BM25 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.25 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.10 + BM25 0.20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.15 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.75_b0.20_e0.05`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.35 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.25 + BM25 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.30 + BM25 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.25 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.15 + BM25 0.15.
- `source_ge3_plus_embedding_only_top20_rerank_k3bm25_ratio60_10`: Candidate set=top20 source_count>=3 plus embedding-only top20; rerank by K3+BM25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.10 + BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.25 + BM25 0.15.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.35 + BM25 0.15.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.30 + BM25 0.15.
- `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_bm25_embedding_full_d0.70_b0.20_e0.10`: Full-corpus z-score fusion: K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.30 + BM25 0.20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.20 + BM25 0.00.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.85 + embedding 0.10 + BM25 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.15 + BM25 0.05.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.30 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.25 + BM25 0.20.
- `result_fusion_k3bm25_ratio60_10_slots_1_2_4_5_embedding_slot3`: Result-level fusion: K3+BM25 supplies slots 1/2/4/5, external embedding supplies slot 3 using its first non-duplicate candidate.
- `source_ge3_plus_embedding_only_top20_rerank_k3bm25_075_025`: Candidate set=top20 source_count>=3 plus embedding-only top20; rerank by K3+BM25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.85 + embedding 0.15 + BM25 0.00.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.90 + embedding 0.10 + BM25 0.00.
- `k3_bm25_dense_top20_d0.75_b0.25`: Dense top-20 shortlist reranked by K3 dense 0.75 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top10_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top10 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.10 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.20 + BM25 0.20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.35 + BM25 0.20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top3_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top3 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_key_assoc_topic_vector_average`: Current clean K3 dense baseline: 2-3-1 + 2-5 + 2-1, vector_average_component_norm.
- `five_source_top20_source_ge2_rerank_d0.75_b0.25`: Five-source candidate screening: 3 prompt sources + BM25 + external embedding, source_count>=2, rerank=K3/BM25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.15 + BM25 0.20.
- `five_source_top5_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top5 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.20 + BM25 0.25.
- `four_source_top20_source_ge2_rerank_d0.75_b0.25`: Four-source candidate screening: 3 prompt sources + BM25, source_count>=2, rerank=K3/BM25.
- `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_bm25_embedding_full_d0.65_b0.25_e0.10`: Full-corpus z-score fusion: K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.25 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.15 + BM25 0.25.
- `k3_bm25_full_d0.75_b0.25`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.60_b0.25_e0.15`: Full-corpus z-score fusion: K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.30 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.40 + embedding 0.35 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `result_fusion_k3bm25_075_025_slots_1_2_4_5_embedding_slot3`: Result-level fusion: K3+BM25 supplies slots 1/2/4/5, external embedding supplies slot 3 using its first non-duplicate candidate.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.10 + BM25 0.30.
- `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.15 + BM25 0.30.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.50_b0.25_e0.25`: Full-corpus z-score fusion: K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.20 + BM25 0.30.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.25 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.40 + embedding 0.30 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.35 + embedding 0.35 + BM25 0.30.
- `external_embedding`: External Qwen embedding standalone reference loaded from cache.
- `bm25`: BM25 standalone reference.
- `embedding_only_top20_rerank_k3bm25_075_025`: Only candidates that appear in embedding top20 and no other source top20; rerank by K3+BM25.
- `embedding_only_top20_rerank_k3bm25_ratio60_10`: Only candidates that appear in embedding top20 and no other source top20; rerank by K3+BM25.
