# PrefEval External Embedding Fusion

- Created UTC: `2026-05-13T17:05:50.554302+00:00`
- Items: `1000`
- Hidden tensor dir: `benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- K3 combo: `2-3-1 + 2-5_token + 2-8_emoji`
- Embedding cache dir: `benchmarks/PrefEval/tensors/qwen3_embedding_implicit_persona_n1000_d19e54c734`
- Embedding model: `models/Qwen3-Embedding-0.6B-4bit-DWQ`
- Source rule: `top20 source_count>=2`
- Eval split: `holdout300_seed0`
- Elapsed: `1m30s`

## Notes

- External embeddings are used only as a score matrix/source, not concatenated with 9B hidden vectors.
- Primary K3 dense baseline is 2-3-1 + 2-5_token + 2-8_emoji with vector_average_component_norm.
- source_count>=2 experiments use per-source top-k lists, with prompt components kept as separate sources.
- Concat experiments use source_count>=concat_source_min plus embedding top-k candidates, then rerank only that candidate set.

## Results

| rank | config | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR | avg shortlist | oracle@shortlist |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.123 | 0.250 | 0.337 | 0.197 | 0.233 | 0.227 | 22.4 | 0.616 |
| 2 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.120 | 0.267 | 0.333 | 0.205 | 0.232 | 0.227 | 22.4 | 0.616 |
| 3 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.113 | 0.243 | 0.333 | 0.189 | 0.226 | 0.220 | 22.4 | 0.616 |
| 4 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.127 | 0.267 | 0.330 | 0.208 | 0.233 | 0.231 | 22.4 | 0.616 |
| 5 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.123 | 0.257 | 0.330 | 0.202 | 0.231 | 0.229 | 22.4 | 0.616 |
| 6 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.117 | 0.257 | 0.330 | 0.198 | 0.229 | 0.225 | 22.4 | 0.616 |
| 7 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.127 | 0.233 | 0.330 | 0.189 | 0.228 | 0.225 | 22.4 | 0.616 |
| 8 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.123 | 0.237 | 0.330 | 0.190 | 0.228 | 0.224 | 22.4 | 0.616 |
| 9 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.123 | 0.237 | 0.330 | 0.190 | 0.228 | 0.224 | 22.4 | 0.616 |
| 10 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.120 | 0.237 | 0.330 | 0.188 | 0.226 | 0.222 | 22.4 | 0.616 |
| 11 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.130 | 0.263 | 0.327 | 0.207 | 0.233 | 0.232 | 22.4 | 0.616 |
| 12 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.127 | 0.263 | 0.327 | 0.205 | 0.230 | 0.230 | 22.4 | 0.616 |
| 13 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.120 | 0.267 | 0.327 | 0.205 | 0.230 | 0.227 | 22.4 | 0.616 |
| 14 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.123 | 0.253 | 0.327 | 0.199 | 0.229 | 0.228 | 22.4 | 0.616 |
| 15 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.123 | 0.243 | 0.327 | 0.194 | 0.229 | 0.227 | 22.4 | 0.616 |
| 16 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.117 | 0.267 | 0.327 | 0.204 | 0.228 | 0.226 | 22.4 | 0.616 |
| 17 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.123 | 0.253 | 0.327 | 0.198 | 0.228 | 0.225 | 22.4 | 0.616 |
| 18 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.127 | 0.237 | 0.327 | 0.190 | 0.227 | 0.224 | 22.4 | 0.616 |
| 19 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.123 | 0.247 | 0.327 | 0.195 | 0.227 | 0.224 | 22.4 | 0.616 |
| 20 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.120 | 0.247 | 0.327 | 0.193 | 0.226 | 0.222 | 22.4 | 0.616 |
| 21 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.120 | 0.240 | 0.327 | 0.190 | 0.226 | 0.223 | 22.4 | 0.616 |
| 22 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.123 | 0.233 | 0.327 | 0.187 | 0.226 | 0.222 | 22.4 | 0.616 |
| 23 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.123 | 0.233 | 0.327 | 0.187 | 0.225 | 0.221 | 22.4 | 0.616 |
| 24 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.097 | 0.250 | 0.327 | 0.187 | 0.218 | 0.212 | 22.4 | 0.616 |
| 25 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.130 | 0.257 | 0.323 | 0.203 | 0.230 | 0.230 | 22.4 | 0.616 |
| 26 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.123 | 0.267 | 0.323 | 0.206 | 0.229 | 0.229 | 22.4 | 0.616 |
| 27 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.127 | 0.260 | 0.323 | 0.203 | 0.229 | 0.229 | 22.4 | 0.616 |
| 28 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.127 | 0.250 | 0.323 | 0.197 | 0.227 | 0.226 | 22.4 | 0.616 |
| 29 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.123 | 0.253 | 0.323 | 0.198 | 0.227 | 0.226 | 22.4 | 0.616 |
| 30 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.120 | 0.253 | 0.323 | 0.198 | 0.226 | 0.224 | 22.4 | 0.616 |
| 31 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.123 | 0.243 | 0.323 | 0.193 | 0.225 | 0.223 | 22.4 | 0.616 |
| 32 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.120 | 0.250 | 0.323 | 0.195 | 0.225 | 0.223 | 22.4 | 0.616 |
| 33 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.120 | 0.240 | 0.323 | 0.190 | 0.224 | 0.222 | 22.4 | 0.616 |
| 34 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.117 | 0.253 | 0.323 | 0.195 | 0.223 | 0.219 | 22.4 | 0.616 |
| 35 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.107 | 0.263 | 0.323 | 0.199 | 0.223 | 0.219 | 22.4 | 0.616 |
| 36 | `k3_bm25_embedding_full_d0.70_b0.20_e0.10` | 0.113 | 0.260 | 0.323 | 0.197 | 0.223 | 0.214 |  |  |
| 37 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.107 | 0.260 | 0.323 | 0.196 | 0.223 | 0.219 | 22.4 | 0.616 |
| 38 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.107 | 0.260 | 0.323 | 0.196 | 0.222 | 0.217 | 22.4 | 0.616 |
| 39 | `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25` | 0.103 | 0.260 | 0.323 | 0.195 | 0.221 | 0.215 | 20.3 | 0.596 |
| 40 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.117 | 0.233 | 0.323 | 0.184 | 0.221 | 0.215 | 22.4 | 0.616 |
| 41 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.103 | 0.243 | 0.323 | 0.187 | 0.220 | 0.215 | 22.4 | 0.616 |
| 42 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.137 | 0.260 | 0.320 | 0.207 | 0.231 | 0.234 | 22.4 | 0.616 |
| 43 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.133 | 0.267 | 0.320 | 0.210 | 0.231 | 0.234 | 22.4 | 0.616 |
| 44 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.130 | 0.267 | 0.320 | 0.207 | 0.229 | 0.231 | 22.4 | 0.616 |
| 45 | `k3_bm25_embedding_full_d0.60_b0.10_e0.30` | 0.127 | 0.263 | 0.320 | 0.205 | 0.228 | 0.228 |  |  |
| 46 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.127 | 0.253 | 0.320 | 0.200 | 0.227 | 0.228 | 22.4 | 0.616 |
| 47 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.127 | 0.263 | 0.320 | 0.204 | 0.227 | 0.228 | 22.4 | 0.616 |
| 48 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.130 | 0.247 | 0.320 | 0.197 | 0.227 | 0.227 | 22.4 | 0.616 |
| 49 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.123 | 0.253 | 0.320 | 0.198 | 0.225 | 0.225 | 22.4 | 0.616 |
| 50 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.123 | 0.247 | 0.320 | 0.195 | 0.225 | 0.224 | 22.4 | 0.616 |
| 51 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.117 | 0.253 | 0.320 | 0.196 | 0.224 | 0.223 | 22.4 | 0.616 |
| 52 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.120 | 0.247 | 0.320 | 0.193 | 0.224 | 0.224 | 22.4 | 0.616 |
| 53 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.123 | 0.233 | 0.320 | 0.188 | 0.224 | 0.222 | 22.4 | 0.616 |
| 54 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.120 | 0.240 | 0.320 | 0.190 | 0.224 | 0.222 | 22.4 | 0.616 |
| 55 | `five_source_top3_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.117 | 0.253 | 0.320 | 0.197 | 0.224 | 0.218 | 10.5 | 0.389 |
| 56 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.123 | 0.233 | 0.320 | 0.187 | 0.223 | 0.222 | 22.4 | 0.616 |
| 57 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.120 | 0.240 | 0.320 | 0.190 | 0.223 | 0.221 | 22.4 | 0.616 |
| 58 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.120 | 0.237 | 0.320 | 0.188 | 0.223 | 0.222 | 22.4 | 0.616 |
| 59 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.123 | 0.230 | 0.320 | 0.185 | 0.222 | 0.219 | 22.4 | 0.616 |
| 60 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.120 | 0.237 | 0.320 | 0.187 | 0.221 | 0.218 | 22.4 | 0.616 |
| 61 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.110 | 0.253 | 0.320 | 0.193 | 0.221 | 0.217 | 22.4 | 0.616 |
| 62 | `k3_bm25_embedding_full_d0.50_b0.25_e0.25` | 0.107 | 0.260 | 0.320 | 0.196 | 0.221 | 0.216 |  |  |
| 63 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.110 | 0.257 | 0.320 | 0.195 | 0.221 | 0.218 | 22.4 | 0.616 |
| 64 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.117 | 0.237 | 0.320 | 0.186 | 0.220 | 0.216 | 22.4 | 0.616 |
| 65 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.103 | 0.263 | 0.320 | 0.196 | 0.220 | 0.216 | 22.4 | 0.616 |
| 66 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.100 | 0.267 | 0.320 | 0.198 | 0.220 | 0.216 | 22.4 | 0.616 |
| 67 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.103 | 0.250 | 0.320 | 0.191 | 0.219 | 0.216 | 22.4 | 0.616 |
| 68 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.103 | 0.250 | 0.320 | 0.189 | 0.218 | 0.214 | 22.4 | 0.616 |
| 69 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.103 | 0.257 | 0.320 | 0.193 | 0.218 | 0.213 | 22.4 | 0.616 |
| 70 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.100 | 0.240 | 0.320 | 0.183 | 0.216 | 0.212 | 22.4 | 0.616 |
| 71 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.097 | 0.243 | 0.320 | 0.184 | 0.215 | 0.210 | 22.4 | 0.616 |
| 72 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.130 | 0.257 | 0.317 | 0.203 | 0.228 | 0.230 | 22.4 | 0.616 |
| 73 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.127 | 0.257 | 0.317 | 0.202 | 0.227 | 0.227 | 22.4 | 0.616 |
| 74 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.127 | 0.257 | 0.317 | 0.201 | 0.226 | 0.227 | 22.4 | 0.616 |
| 75 | `five_source_top20_source_ge2_rerank_d0.60_b0.10_e0.30` | 0.123 | 0.253 | 0.317 | 0.199 | 0.225 | 0.225 | 20.3 | 0.596 |
| 76 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.123 | 0.257 | 0.317 | 0.200 | 0.224 | 0.225 | 22.4 | 0.616 |
| 77 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.127 | 0.237 | 0.317 | 0.191 | 0.223 | 0.224 | 22.4 | 0.616 |
| 78 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.120 | 0.257 | 0.317 | 0.198 | 0.223 | 0.223 | 22.4 | 0.616 |
| 79 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.127 | 0.230 | 0.317 | 0.187 | 0.223 | 0.223 | 22.4 | 0.616 |
| 80 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.120 | 0.257 | 0.317 | 0.198 | 0.223 | 0.222 | 22.4 | 0.616 |
| 81 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.123 | 0.247 | 0.317 | 0.194 | 0.223 | 0.222 | 22.4 | 0.616 |
| 82 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.117 | 0.257 | 0.317 | 0.198 | 0.223 | 0.222 | 22.4 | 0.616 |
| 83 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.123 | 0.233 | 0.317 | 0.187 | 0.221 | 0.221 | 22.4 | 0.616 |
| 84 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.110 | 0.253 | 0.317 | 0.195 | 0.221 | 0.220 | 22.4 | 0.616 |
| 85 | `k3_bm25_embedding_full_d0.60_b0.25_e0.15` | 0.113 | 0.260 | 0.317 | 0.198 | 0.221 | 0.215 |  |  |
| 86 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.120 | 0.237 | 0.317 | 0.188 | 0.220 | 0.220 | 22.4 | 0.616 |
| 87 | `five_source_top5_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.113 | 0.247 | 0.317 | 0.192 | 0.220 | 0.217 | 17.1 | 0.482 |
| 88 | `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15` | 0.113 | 0.253 | 0.317 | 0.194 | 0.220 | 0.216 | 20.3 | 0.596 |
| 89 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.123 | 0.230 | 0.317 | 0.185 | 0.220 | 0.218 | 22.4 | 0.616 |
| 90 | `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10` | 0.113 | 0.260 | 0.317 | 0.197 | 0.220 | 0.214 | 20.3 | 0.596 |
| 91 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.107 | 0.250 | 0.317 | 0.192 | 0.220 | 0.218 | 22.4 | 0.616 |
| 92 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.113 | 0.250 | 0.317 | 0.193 | 0.220 | 0.218 | 22.4 | 0.616 |
| 93 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.120 | 0.230 | 0.317 | 0.184 | 0.219 | 0.217 | 22.4 | 0.616 |
| 94 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.107 | 0.260 | 0.317 | 0.196 | 0.219 | 0.217 | 22.4 | 0.616 |
| 95 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.120 | 0.233 | 0.317 | 0.185 | 0.219 | 0.216 | 22.4 | 0.616 |
| 96 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.107 | 0.263 | 0.317 | 0.196 | 0.218 | 0.215 | 22.4 | 0.616 |
| 97 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.103 | 0.260 | 0.317 | 0.194 | 0.217 | 0.215 | 22.4 | 0.616 |
| 98 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.100 | 0.250 | 0.317 | 0.189 | 0.217 | 0.214 | 22.4 | 0.616 |
| 99 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.100 | 0.257 | 0.317 | 0.191 | 0.216 | 0.212 | 22.4 | 0.616 |
| 100 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.100 | 0.253 | 0.317 | 0.189 | 0.215 | 0.211 | 22.4 | 0.616 |
| 101 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.133 | 0.263 | 0.313 | 0.207 | 0.227 | 0.232 | 22.4 | 0.616 |
| 102 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.130 | 0.257 | 0.313 | 0.203 | 0.226 | 0.229 | 22.4 | 0.616 |
| 103 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.130 | 0.253 | 0.313 | 0.201 | 0.226 | 0.230 | 22.4 | 0.616 |
| 104 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.130 | 0.250 | 0.313 | 0.200 | 0.226 | 0.229 | 22.4 | 0.616 |
| 105 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.127 | 0.257 | 0.313 | 0.201 | 0.225 | 0.228 | 22.4 | 0.616 |
| 106 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.127 | 0.257 | 0.313 | 0.201 | 0.224 | 0.227 | 22.4 | 0.616 |
| 107 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.120 | 0.267 | 0.313 | 0.204 | 0.223 | 0.225 | 22.4 | 0.616 |
| 108 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.120 | 0.250 | 0.313 | 0.194 | 0.220 | 0.219 | 22.4 | 0.616 |
| 109 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.123 | 0.230 | 0.313 | 0.185 | 0.220 | 0.219 | 22.4 | 0.616 |
| 110 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.113 | 0.260 | 0.313 | 0.198 | 0.220 | 0.219 | 22.4 | 0.616 |
| 111 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.113 | 0.257 | 0.313 | 0.196 | 0.219 | 0.218 | 22.4 | 0.616 |
| 112 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.120 | 0.240 | 0.313 | 0.189 | 0.219 | 0.219 | 22.4 | 0.616 |
| 113 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.123 | 0.233 | 0.313 | 0.186 | 0.219 | 0.218 | 22.4 | 0.616 |
| 114 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.117 | 0.253 | 0.313 | 0.194 | 0.218 | 0.218 | 22.4 | 0.616 |
| 115 | `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10` | 0.110 | 0.257 | 0.313 | 0.195 | 0.218 | 0.213 | 20.3 | 0.596 |
| 116 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.110 | 0.253 | 0.313 | 0.193 | 0.218 | 0.216 | 22.4 | 0.616 |
| 117 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.110 | 0.253 | 0.313 | 0.193 | 0.218 | 0.217 | 22.4 | 0.616 |
| 118 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.110 | 0.253 | 0.313 | 0.193 | 0.217 | 0.215 | 22.4 | 0.616 |
| 119 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.113 | 0.237 | 0.313 | 0.185 | 0.217 | 0.217 | 22.4 | 0.616 |
| 120 | `k3_bm25_embedding_full_d0.65_b0.25_e0.10` | 0.107 | 0.257 | 0.313 | 0.193 | 0.217 | 0.210 |  |  |
| 121 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.103 | 0.253 | 0.313 | 0.191 | 0.216 | 0.214 | 22.4 | 0.616 |
| 122 | `source_ge3_plus_embedding_only_top20_rerank_k3bm25_ratio60_10` | 0.113 | 0.253 | 0.313 | 0.192 | 0.216 | 0.211 | 18.6 | 0.528 |
| 123 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.127 | 0.257 | 0.310 | 0.202 | 0.224 | 0.227 | 22.4 | 0.616 |
| 124 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.123 | 0.253 | 0.310 | 0.198 | 0.222 | 0.225 | 22.4 | 0.616 |
| 125 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.120 | 0.257 | 0.310 | 0.199 | 0.221 | 0.222 | 22.4 | 0.616 |
| 126 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.123 | 0.250 | 0.310 | 0.196 | 0.221 | 0.223 | 22.4 | 0.616 |
| 127 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.123 | 0.237 | 0.310 | 0.189 | 0.219 | 0.221 | 22.4 | 0.616 |
| 128 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.123 | 0.243 | 0.310 | 0.191 | 0.219 | 0.220 | 22.4 | 0.616 |
| 129 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.117 | 0.253 | 0.310 | 0.195 | 0.218 | 0.218 | 22.4 | 0.616 |
| 130 | `k3_bm25_embedding_full_d0.75_b0.20_e0.05` | 0.117 | 0.257 | 0.310 | 0.196 | 0.218 | 0.212 |  |  |
| 131 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.117 | 0.240 | 0.310 | 0.187 | 0.216 | 0.217 | 22.4 | 0.616 |
| 132 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.117 | 0.230 | 0.310 | 0.183 | 0.216 | 0.216 | 22.4 | 0.616 |
| 133 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.120 | 0.227 | 0.310 | 0.181 | 0.215 | 0.215 | 22.4 | 0.616 |
| 134 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.110 | 0.250 | 0.310 | 0.190 | 0.214 | 0.214 | 22.4 | 0.616 |
| 135 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.100 | 0.260 | 0.310 | 0.193 | 0.214 | 0.212 | 22.4 | 0.616 |
| 136 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.100 | 0.253 | 0.310 | 0.188 | 0.212 | 0.210 | 22.4 | 0.616 |
| 137 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.127 | 0.253 | 0.307 | 0.199 | 0.221 | 0.224 | 22.4 | 0.616 |
| 138 | `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05` | 0.123 | 0.257 | 0.307 | 0.199 | 0.219 | 0.216 | 20.3 | 0.596 |
| 139 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.117 | 0.257 | 0.307 | 0.198 | 0.219 | 0.221 | 22.4 | 0.616 |
| 140 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.117 | 0.253 | 0.307 | 0.195 | 0.217 | 0.219 | 22.4 | 0.616 |
| 141 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.107 | 0.257 | 0.307 | 0.193 | 0.213 | 0.214 | 22.4 | 0.616 |
| 142 | `result_fusion_k3bm25_075_025_slots_1_2_4_5_embedding_slot3` | 0.110 | 0.237 | 0.307 | 0.184 | 0.213 | 0.205 |  |  |
| 143 | `source_ge3_plus_embedding_only_top20_rerank_k3bm25_075_025` | 0.107 | 0.247 | 0.307 | 0.188 | 0.212 | 0.209 | 18.6 | 0.528 |
| 144 | `five_source_top10_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.117 | 0.247 | 0.303 | 0.193 | 0.216 | 0.217 | 33.1 | 0.613 |
| 145 | `k3_bm25_full_d0.75_b0.25` | 0.110 | 0.243 | 0.303 | 0.187 | 0.212 | 0.206 |  |  |
| 146 | `four_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.107 | 0.243 | 0.303 | 0.186 | 0.210 | 0.205 | 16.4 | 0.508 |
| 147 | `result_fusion_k3bm25_ratio60_10_slots_1_2_4_5_embedding_slot3` | 0.113 | 0.233 | 0.300 | 0.182 | 0.210 | 0.206 |  |  |
| 148 | `five_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.110 | 0.243 | 0.300 | 0.187 | 0.210 | 0.207 | 20.3 | 0.596 |
| 149 | `k3_custom_vector_average` | 0.113 | 0.223 | 0.300 | 0.177 | 0.208 | 0.202 |  |  |
| 150 | `k3_bm25_dense_top20_d0.75_b0.25` | 0.110 | 0.247 | 0.290 | 0.187 | 0.205 | 0.204 |  |  |
| 151 | `external_embedding` | 0.087 | 0.203 | 0.277 | 0.155 | 0.185 | 0.187 |  |  |
| 152 | `bm25` | 0.033 | 0.080 | 0.117 | 0.061 | 0.075 | 0.069 |  |  |
| 153 | `embedding_only_top20_rerank_k3bm25_ratio60_10` | 0.007 | 0.030 | 0.070 | 0.020 | 0.037 | 0.071 | 8.6 | 0.078 |
| 154 | `embedding_only_top20_rerank_k3bm25_075_025` | 0.007 | 0.030 | 0.067 | 0.021 | 0.036 | 0.072 | 8.6 | 0.078 |

## Configs

- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.35 + BM25 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.35 + BM25 0.00.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.35 + BM25 0.20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.25 + BM25 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.30 + BM25 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.40 + embedding 0.35 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.30 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.35 + BM25 0.15.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.30 + BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.35 + BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.70_b0.20_e0.10`: Full-corpus z-score fusion: K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.25 + BM25 0.25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.85 + embedding 0.10 + BM25 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.60_b0.10_e0.30`: Full-corpus z-score fusion: K3 dense 0.60 + BM25 0.10 + embedding 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.25 + BM25 0.15.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.30 + BM25 0.20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.30 + BM25 0.00.
- `five_source_top3_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top3 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.85 + embedding 0.15 + BM25 0.00.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.50_b0.25_e0.25`: Full-corpus z-score fusion: K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.30 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.40 + embedding 0.30 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.15 + BM25 0.30.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.35 + embedding 0.35 + BM25 0.30.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.20 + BM25 0.15.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.25 + BM25 0.20.
- `five_source_top20_source_ge2_rerank_d0.60_b0.10_e0.30`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.60 + BM25 0.10 + embedding 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.25 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.20 + BM25 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.20 + BM25 0.20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.25 + BM25 0.00.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.60_b0.25_e0.15`: Full-corpus z-score fusion: K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top5_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top5 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.15 + BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.15 + BM25 0.05.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.10 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.15 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.25 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.20 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.20 + BM25 0.30.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.20 + BM25 0.00.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.90 + embedding 0.10 + BM25 0.00.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.10 + BM25 0.20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.65_b0.25_e0.10`: Full-corpus z-score fusion: K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `source_ge3_plus_embedding_only_top20_rerank_k3bm25_ratio60_10`: Candidate set=top20 source_count>=3 plus embedding-only top20; rerank by K3+BM25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.15 + BM25 0.20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.20 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.75_b0.20_e0.05`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.10 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.10 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.10 + BM25 0.15.
- `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.15 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `result_fusion_k3bm25_075_025_slots_1_2_4_5_embedding_slot3`: Result-level fusion: K3+BM25 supplies slots 1/2/4/5, external embedding supplies slot 3 using its first non-duplicate candidate.
- `source_ge3_plus_embedding_only_top20_rerank_k3bm25_075_025`: Candidate set=top20 source_count>=3 plus embedding-only top20; rerank by K3+BM25.
- `five_source_top10_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top10 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_bm25_full_d0.75_b0.25`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.25.
- `four_source_top20_source_ge2_rerank_d0.75_b0.25`: Four-source candidate screening: 3 prompt sources + BM25, source_count>=2, rerank=K3/BM25.
- `result_fusion_k3bm25_ratio60_10_slots_1_2_4_5_embedding_slot3`: Result-level fusion: K3+BM25 supplies slots 1/2/4/5, external embedding supplies slot 3 using its first non-duplicate candidate.
- `five_source_top20_source_ge2_rerank_d0.75_b0.25`: Five-source candidate screening: 3 prompt sources + BM25 + external embedding, source_count>=2, rerank=K3/BM25.
- `k3_custom_vector_average`: K3 dense baseline: 2-3-1 + 2-5_token + 2-8_emoji, vector_average_component_norm.
- `k3_bm25_dense_top20_d0.75_b0.25`: Dense top-20 shortlist reranked by K3 dense 0.75 + BM25 0.25.
- `external_embedding`: External Qwen embedding standalone reference loaded from cache.
- `bm25`: BM25 standalone reference.
- `embedding_only_top20_rerank_k3bm25_ratio60_10`: Only candidates that appear in embedding top20 and no other source top20; rerank by K3+BM25.
- `embedding_only_top20_rerank_k3bm25_075_025`: Only candidates that appear in embedding top20 and no other source top20; rerank by K3+BM25.
