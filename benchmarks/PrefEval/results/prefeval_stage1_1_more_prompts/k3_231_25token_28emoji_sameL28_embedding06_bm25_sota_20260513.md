# PrefEval External Embedding Fusion

- Created UTC: `2026-05-13T16:31:26.165444+00:00`
- Items: `1000`
- Hidden tensor dir: `benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- K3 combo: `2-3-1 + 2-5_token + 2-8_emoji`
- Embedding cache dir: `benchmarks/PrefEval/tensors/qwen3_embedding_implicit_persona_n1000_d19e54c734`
- Embedding model: `models/Qwen3-Embedding-0.6B-4bit-DWQ`
- Source rule: `top20 source_count>=2`
- Elapsed: `1m48s`

## Notes

- External embeddings are used only as a score matrix/source, not concatenated with 9B hidden vectors.
- Primary K3 dense baseline is 2-3-1 + 2-5_token + 2-8_emoji with vector_average_component_norm.
- source_count>=2 experiments use per-source top-k lists, with prompt components kept as separate sources.
- Concat experiments use source_count>=concat_source_min plus embedding top-k candidates, then rerank only that candidate set.

## Results

| rank | config | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR | avg shortlist | oracle@shortlist |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.118 | 0.252 | 0.335 | 0.194 | 0.228 | 0.227 | 22.9 | 0.625 |
| 2 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.117 | 0.247 | 0.335 | 0.192 | 0.228 | 0.226 | 22.9 | 0.625 |
| 3 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.114 | 0.248 | 0.334 | 0.192 | 0.227 | 0.225 | 22.9 | 0.625 |
| 4 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.112 | 0.247 | 0.334 | 0.190 | 0.226 | 0.224 | 22.9 | 0.625 |
| 5 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.121 | 0.249 | 0.333 | 0.195 | 0.229 | 0.231 | 22.9 | 0.625 |
| 6 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.116 | 0.251 | 0.333 | 0.194 | 0.228 | 0.228 | 22.9 | 0.625 |
| 7 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.117 | 0.253 | 0.333 | 0.195 | 0.227 | 0.227 | 22.9 | 0.625 |
| 8 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.118 | 0.251 | 0.333 | 0.194 | 0.227 | 0.227 | 22.9 | 0.625 |
| 9 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.119 | 0.248 | 0.332 | 0.194 | 0.228 | 0.229 | 22.9 | 0.625 |
| 10 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.115 | 0.245 | 0.332 | 0.191 | 0.226 | 0.225 | 22.9 | 0.625 |
| 11 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.115 | 0.251 | 0.332 | 0.192 | 0.225 | 0.224 | 22.9 | 0.625 |
| 12 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.110 | 0.247 | 0.332 | 0.189 | 0.224 | 0.222 | 22.9 | 0.625 |
| 13 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.124 | 0.249 | 0.331 | 0.196 | 0.229 | 0.231 | 22.9 | 0.625 |
| 14 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.116 | 0.256 | 0.331 | 0.197 | 0.228 | 0.230 | 22.9 | 0.625 |
| 15 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.119 | 0.252 | 0.331 | 0.195 | 0.228 | 0.228 | 22.9 | 0.625 |
| 16 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.115 | 0.246 | 0.331 | 0.191 | 0.226 | 0.225 | 22.9 | 0.625 |
| 17 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.109 | 0.249 | 0.331 | 0.191 | 0.224 | 0.223 | 22.9 | 0.625 |
| 18 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.112 | 0.243 | 0.331 | 0.188 | 0.224 | 0.222 | 22.9 | 0.625 |
| 19 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.112 | 0.242 | 0.331 | 0.187 | 0.224 | 0.221 | 22.9 | 0.625 |
| 20 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.112 | 0.243 | 0.331 | 0.187 | 0.223 | 0.220 | 22.9 | 0.625 |
| 21 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.111 | 0.241 | 0.331 | 0.186 | 0.223 | 0.221 | 22.9 | 0.625 |
| 22 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.122 | 0.253 | 0.330 | 0.197 | 0.229 | 0.231 | 22.9 | 0.625 |
| 23 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.118 | 0.252 | 0.330 | 0.195 | 0.226 | 0.227 | 22.9 | 0.625 |
| 24 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.113 | 0.246 | 0.330 | 0.190 | 0.224 | 0.223 | 22.9 | 0.625 |
| 25 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.112 | 0.245 | 0.330 | 0.189 | 0.224 | 0.222 | 22.9 | 0.625 |
| 26 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.113 | 0.245 | 0.330 | 0.189 | 0.223 | 0.221 | 22.9 | 0.625 |
| 27 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.114 | 0.240 | 0.330 | 0.187 | 0.223 | 0.221 | 22.9 | 0.625 |
| 28 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.118 | 0.251 | 0.329 | 0.195 | 0.228 | 0.229 | 22.9 | 0.625 |
| 29 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.121 | 0.246 | 0.329 | 0.193 | 0.227 | 0.229 | 22.9 | 0.625 |
| 30 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.117 | 0.251 | 0.329 | 0.194 | 0.226 | 0.228 | 22.9 | 0.625 |
| 31 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.116 | 0.252 | 0.329 | 0.194 | 0.226 | 0.227 | 22.9 | 0.625 |
| 32 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.115 | 0.250 | 0.329 | 0.193 | 0.225 | 0.226 | 22.9 | 0.625 |
| 33 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.117 | 0.246 | 0.329 | 0.191 | 0.225 | 0.226 | 22.9 | 0.625 |
| 34 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.115 | 0.249 | 0.329 | 0.192 | 0.225 | 0.225 | 22.9 | 0.625 |
| 35 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.114 | 0.245 | 0.329 | 0.190 | 0.225 | 0.225 | 22.9 | 0.625 |
| 36 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.114 | 0.251 | 0.329 | 0.192 | 0.224 | 0.224 | 22.9 | 0.625 |
| 37 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.115 | 0.244 | 0.329 | 0.190 | 0.224 | 0.224 | 22.9 | 0.625 |
| 38 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.114 | 0.244 | 0.329 | 0.189 | 0.224 | 0.224 | 22.9 | 0.625 |
| 39 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.114 | 0.241 | 0.329 | 0.187 | 0.223 | 0.221 | 22.9 | 0.625 |
| 40 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.111 | 0.246 | 0.329 | 0.189 | 0.223 | 0.221 | 22.9 | 0.625 |
| 41 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.110 | 0.246 | 0.329 | 0.189 | 0.222 | 0.220 | 22.9 | 0.625 |
| 42 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.119 | 0.253 | 0.328 | 0.197 | 0.228 | 0.230 | 22.9 | 0.625 |
| 43 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.119 | 0.253 | 0.328 | 0.196 | 0.227 | 0.229 | 22.9 | 0.625 |
| 44 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.120 | 0.253 | 0.328 | 0.196 | 0.227 | 0.230 | 22.9 | 0.625 |
| 45 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.119 | 0.253 | 0.328 | 0.196 | 0.227 | 0.229 | 22.9 | 0.625 |
| 46 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.117 | 0.254 | 0.328 | 0.195 | 0.226 | 0.227 | 22.9 | 0.625 |
| 47 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.116 | 0.250 | 0.328 | 0.193 | 0.225 | 0.226 | 22.9 | 0.625 |
| 48 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.118 | 0.247 | 0.328 | 0.192 | 0.225 | 0.225 | 22.9 | 0.625 |
| 49 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.112 | 0.253 | 0.328 | 0.193 | 0.224 | 0.224 | 22.9 | 0.625 |
| 50 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.111 | 0.249 | 0.328 | 0.191 | 0.222 | 0.221 | 22.9 | 0.625 |
| 51 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.112 | 0.241 | 0.328 | 0.186 | 0.222 | 0.220 | 22.9 | 0.625 |
| 52 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.107 | 0.243 | 0.328 | 0.185 | 0.220 | 0.218 | 22.9 | 0.625 |
| 53 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.118 | 0.251 | 0.327 | 0.195 | 0.226 | 0.228 | 22.9 | 0.625 |
| 54 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.118 | 0.250 | 0.327 | 0.193 | 0.225 | 0.226 | 22.9 | 0.625 |
| 55 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.112 | 0.249 | 0.327 | 0.191 | 0.223 | 0.223 | 22.9 | 0.625 |
| 56 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.112 | 0.248 | 0.327 | 0.191 | 0.223 | 0.222 | 22.9 | 0.625 |
| 57 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.113 | 0.243 | 0.327 | 0.188 | 0.223 | 0.223 | 22.9 | 0.625 |
| 58 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.112 | 0.243 | 0.327 | 0.188 | 0.223 | 0.222 | 22.9 | 0.625 |
| 59 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.112 | 0.240 | 0.327 | 0.186 | 0.222 | 0.221 | 22.9 | 0.625 |
| 60 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.110 | 0.243 | 0.327 | 0.187 | 0.221 | 0.220 | 22.9 | 0.625 |
| 61 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.119 | 0.250 | 0.326 | 0.195 | 0.226 | 0.229 | 22.9 | 0.625 |
| 62 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.118 | 0.252 | 0.326 | 0.195 | 0.225 | 0.228 | 22.9 | 0.625 |
| 63 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.115 | 0.245 | 0.326 | 0.191 | 0.224 | 0.225 | 22.9 | 0.625 |
| 64 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.118 | 0.244 | 0.326 | 0.191 | 0.224 | 0.225 | 22.9 | 0.625 |
| 65 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.115 | 0.245 | 0.326 | 0.189 | 0.223 | 0.224 | 22.9 | 0.625 |
| 66 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.111 | 0.245 | 0.326 | 0.188 | 0.221 | 0.221 | 22.9 | 0.625 |
| 67 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.107 | 0.248 | 0.326 | 0.189 | 0.221 | 0.220 | 22.9 | 0.625 |
| 68 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.110 | 0.240 | 0.326 | 0.185 | 0.220 | 0.219 | 22.9 | 0.625 |
| 69 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.119 | 0.252 | 0.325 | 0.196 | 0.226 | 0.229 | 22.9 | 0.625 |
| 70 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.118 | 0.252 | 0.325 | 0.196 | 0.226 | 0.229 | 22.9 | 0.625 |
| 71 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.114 | 0.248 | 0.325 | 0.192 | 0.223 | 0.225 | 22.9 | 0.625 |
| 72 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.113 | 0.245 | 0.325 | 0.190 | 0.222 | 0.223 | 22.9 | 0.625 |
| 73 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.113 | 0.242 | 0.325 | 0.188 | 0.222 | 0.223 | 22.9 | 0.625 |
| 74 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.111 | 0.243 | 0.325 | 0.187 | 0.220 | 0.221 | 22.9 | 0.625 |
| 75 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.113 | 0.239 | 0.325 | 0.185 | 0.220 | 0.220 | 22.9 | 0.625 |
| 76 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.111 | 0.242 | 0.325 | 0.186 | 0.220 | 0.219 | 22.9 | 0.625 |
| 77 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.113 | 0.251 | 0.324 | 0.192 | 0.222 | 0.224 | 22.9 | 0.625 |
| 78 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.114 | 0.244 | 0.324 | 0.190 | 0.222 | 0.223 | 22.9 | 0.625 |
| 79 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.115 | 0.247 | 0.324 | 0.191 | 0.222 | 0.222 | 22.9 | 0.625 |
| 80 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.111 | 0.251 | 0.324 | 0.192 | 0.222 | 0.223 | 22.9 | 0.625 |
| 81 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.113 | 0.244 | 0.324 | 0.189 | 0.222 | 0.222 | 22.9 | 0.625 |
| 82 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.112 | 0.247 | 0.324 | 0.190 | 0.222 | 0.222 | 22.9 | 0.625 |
| 83 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.111 | 0.243 | 0.324 | 0.188 | 0.221 | 0.221 | 22.9 | 0.625 |
| 84 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.116 | 0.248 | 0.323 | 0.192 | 0.222 | 0.224 | 22.9 | 0.625 |
| 85 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.116 | 0.249 | 0.323 | 0.192 | 0.222 | 0.225 | 22.9 | 0.625 |
| 86 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.119 | 0.241 | 0.323 | 0.189 | 0.222 | 0.225 | 22.9 | 0.625 |
| 87 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.115 | 0.241 | 0.323 | 0.187 | 0.221 | 0.221 | 22.9 | 0.625 |
| 88 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.106 | 0.239 | 0.323 | 0.183 | 0.217 | 0.216 | 22.9 | 0.625 |
| 89 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.120 | 0.247 | 0.322 | 0.193 | 0.223 | 0.226 | 22.9 | 0.625 |
| 90 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.111 | 0.249 | 0.322 | 0.191 | 0.221 | 0.222 | 22.9 | 0.625 |
| 91 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.117 | 0.249 | 0.321 | 0.193 | 0.223 | 0.226 | 22.9 | 0.625 |
| 92 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.115 | 0.249 | 0.321 | 0.192 | 0.221 | 0.224 | 22.9 | 0.625 |
| 93 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.110 | 0.242 | 0.321 | 0.186 | 0.218 | 0.219 | 22.9 | 0.625 |
| 94 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.108 | 0.238 | 0.321 | 0.183 | 0.217 | 0.217 | 22.9 | 0.625 |
| 95 | `five_source_top10_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.124 | 0.250 | 0.320 | 0.197 | 0.225 | 0.228 | 32.1 | 0.616 |
| 96 | `five_source_top5_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.121 | 0.255 | 0.320 | 0.199 | 0.225 | 0.227 | 16.8 | 0.488 |
| 97 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.116 | 0.245 | 0.320 | 0.191 | 0.221 | 0.224 | 22.9 | 0.625 |
| 98 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.112 | 0.248 | 0.320 | 0.191 | 0.220 | 0.222 | 22.9 | 0.625 |
| 99 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.118 | 0.245 | 0.319 | 0.191 | 0.221 | 0.225 | 22.9 | 0.625 |
| 100 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.112 | 0.251 | 0.319 | 0.193 | 0.220 | 0.223 | 22.9 | 0.625 |
| 101 | `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25` | 0.112 | 0.243 | 0.319 | 0.188 | 0.219 | 0.219 | 20.8 | 0.605 |
| 102 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.113 | 0.239 | 0.319 | 0.185 | 0.218 | 0.220 | 22.9 | 0.625 |
| 103 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.109 | 0.241 | 0.319 | 0.185 | 0.216 | 0.217 | 22.9 | 0.625 |
| 104 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.114 | 0.248 | 0.318 | 0.191 | 0.220 | 0.223 | 22.9 | 0.625 |
| 105 | `result_fusion_k3bm25_ratio60_10_slots_1_2_4_5_embedding_slot3` | 0.111 | 0.248 | 0.318 | 0.190 | 0.219 | 0.216 |  |  |
| 106 | `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10` | 0.113 | 0.242 | 0.318 | 0.187 | 0.218 | 0.217 | 20.8 | 0.605 |
| 107 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.110 | 0.239 | 0.318 | 0.184 | 0.216 | 0.218 | 22.9 | 0.625 |
| 108 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.114 | 0.241 | 0.316 | 0.188 | 0.218 | 0.223 | 22.9 | 0.625 |
| 109 | `k3_bm25_embedding_full_d0.50_b0.25_e0.25` | 0.112 | 0.241 | 0.316 | 0.187 | 0.217 | 0.217 |  |  |
| 110 | `source_ge3_plus_embedding_only_top20_rerank_k3bm25_ratio60_10` | 0.110 | 0.249 | 0.316 | 0.190 | 0.217 | 0.216 | 19.1 | 0.542 |
| 111 | `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15` | 0.109 | 0.244 | 0.316 | 0.187 | 0.216 | 0.216 | 20.8 | 0.605 |
| 112 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.110 | 0.244 | 0.316 | 0.187 | 0.216 | 0.219 | 22.9 | 0.625 |
| 113 | `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10` | 0.109 | 0.246 | 0.316 | 0.188 | 0.216 | 0.214 | 20.8 | 0.605 |
| 114 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.108 | 0.237 | 0.316 | 0.183 | 0.215 | 0.217 | 22.9 | 0.625 |
| 115 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.113 | 0.243 | 0.315 | 0.187 | 0.217 | 0.220 | 22.9 | 0.625 |
| 116 | `k3_bm25_embedding_full_d0.70_b0.20_e0.10` | 0.112 | 0.243 | 0.315 | 0.187 | 0.217 | 0.215 |  |  |
| 117 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.110 | 0.241 | 0.315 | 0.186 | 0.216 | 0.219 | 22.9 | 0.625 |
| 118 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.109 | 0.242 | 0.315 | 0.185 | 0.215 | 0.218 | 22.9 | 0.625 |
| 119 | `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05` | 0.109 | 0.243 | 0.315 | 0.186 | 0.215 | 0.213 | 20.8 | 0.605 |
| 120 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.108 | 0.245 | 0.315 | 0.186 | 0.214 | 0.216 | 22.9 | 0.625 |
| 121 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.108 | 0.238 | 0.315 | 0.183 | 0.214 | 0.216 | 22.9 | 0.625 |
| 122 | `k3_bm25_embedding_full_d0.65_b0.25_e0.10` | 0.111 | 0.241 | 0.314 | 0.186 | 0.216 | 0.213 |  |  |
| 123 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.109 | 0.241 | 0.314 | 0.185 | 0.215 | 0.218 | 22.9 | 0.625 |
| 124 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.108 | 0.241 | 0.314 | 0.184 | 0.214 | 0.217 | 22.9 | 0.625 |
| 125 | `k3_custom_vector_average` | 0.106 | 0.240 | 0.314 | 0.183 | 0.213 | 0.208 |  |  |
| 126 | `k3_bm25_embedding_full_d0.75_b0.20_e0.05` | 0.112 | 0.244 | 0.313 | 0.188 | 0.216 | 0.214 |  |  |
| 127 | `k3_bm25_embedding_full_d0.60_b0.25_e0.15` | 0.109 | 0.243 | 0.313 | 0.186 | 0.215 | 0.213 |  |  |
| 128 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.110 | 0.242 | 0.313 | 0.186 | 0.215 | 0.218 | 22.9 | 0.625 |
| 129 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.110 | 0.244 | 0.313 | 0.186 | 0.214 | 0.218 | 22.9 | 0.625 |
| 130 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.111 | 0.238 | 0.313 | 0.184 | 0.214 | 0.217 | 22.9 | 0.625 |
| 131 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.109 | 0.239 | 0.313 | 0.184 | 0.214 | 0.217 | 22.9 | 0.625 |
| 132 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.109 | 0.243 | 0.312 | 0.186 | 0.214 | 0.218 | 22.9 | 0.625 |
| 133 | `source_ge3_plus_embedding_only_top20_rerank_k3bm25_075_025` | 0.112 | 0.238 | 0.312 | 0.184 | 0.214 | 0.214 | 19.1 | 0.542 |
| 134 | `result_fusion_k3bm25_075_025_slots_1_2_4_5_embedding_slot3` | 0.109 | 0.236 | 0.312 | 0.182 | 0.214 | 0.209 |  |  |
| 135 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.110 | 0.242 | 0.312 | 0.185 | 0.214 | 0.217 | 22.9 | 0.625 |
| 136 | `five_source_top3_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.119 | 0.245 | 0.311 | 0.193 | 0.220 | 0.223 | 10.2 | 0.382 |
| 137 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.115 | 0.240 | 0.311 | 0.187 | 0.216 | 0.221 | 22.9 | 0.625 |
| 138 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.110 | 0.242 | 0.311 | 0.186 | 0.214 | 0.219 | 22.9 | 0.625 |
| 139 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.107 | 0.240 | 0.311 | 0.184 | 0.213 | 0.217 | 22.9 | 0.625 |
| 140 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.110 | 0.240 | 0.310 | 0.185 | 0.213 | 0.217 | 22.9 | 0.625 |
| 141 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.107 | 0.232 | 0.310 | 0.179 | 0.211 | 0.214 | 22.9 | 0.625 |
| 142 | `four_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.111 | 0.236 | 0.308 | 0.183 | 0.212 | 0.209 | 17.1 | 0.522 |
| 143 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.105 | 0.235 | 0.308 | 0.180 | 0.210 | 0.213 | 22.9 | 0.625 |
| 144 | `five_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.109 | 0.237 | 0.307 | 0.183 | 0.211 | 0.211 | 20.8 | 0.605 |
| 145 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.106 | 0.235 | 0.307 | 0.180 | 0.209 | 0.213 | 22.9 | 0.625 |
| 146 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.104 | 0.230 | 0.307 | 0.176 | 0.207 | 0.210 | 22.9 | 0.625 |
| 147 | `k3_bm25_dense_top20_d0.75_b0.25` | 0.109 | 0.239 | 0.305 | 0.185 | 0.212 | 0.211 |  |  |
| 148 | `k3_bm25_full_d0.75_b0.25` | 0.109 | 0.237 | 0.305 | 0.183 | 0.211 | 0.208 |  |  |
| 149 | `external_embedding` | 0.084 | 0.207 | 0.287 | 0.155 | 0.187 | 0.189 |  |  |
| 150 | `bm25` | 0.035 | 0.074 | 0.094 | 0.058 | 0.066 | 0.067 |  |  |
| 151 | `embedding_only_top20_rerank_k3bm25_075_025` | 0.012 | 0.044 | 0.073 | 0.030 | 0.041 | 0.080 | 8.4 | 0.077 |
| 152 | `embedding_only_top20_rerank_k3bm25_ratio60_10` | 0.011 | 0.043 | 0.073 | 0.029 | 0.041 | 0.080 | 8.4 | 0.077 |

## Configs

- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.30 + BM25 0.00.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.30 + BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.85 + embedding 0.15 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.20 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.20 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.15 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.35 + BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.20 + BM25 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.25 + BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.25 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.10 + BM25 0.15.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.30 + BM25 0.05.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.35 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.35 + BM25 0.00.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.90 + embedding 0.10 + BM25 0.00.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.20 + BM25 0.20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.20 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.25 + BM25 0.20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.35 + BM25 0.20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.25 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.35 + BM25 0.05.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.15 + BM25 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.15 + BM25 0.20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.10 + BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.25 + BM25 0.05.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.85 + embedding 0.10 + BM25 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.30 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.10 + BM25 0.20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.10 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.15 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.30 + BM25 0.20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.30 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top10_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top10 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `five_source_top5_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top5 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `result_fusion_k3bm25_ratio60_10_slots_1_2_4_5_embedding_slot3`: Result-level fusion: K3+BM25 supplies slots 1/2/4/5, external embedding supplies slot 3 using its first non-duplicate candidate.
- `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.20 + BM25 0.25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.50_b0.25_e0.25`: Full-corpus z-score fusion: K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `source_ge3_plus_embedding_only_top20_rerank_k3bm25_ratio60_10`: Candidate set=top20 source_count>=3 plus embedding-only top20; rerank by K3+BM25.
- `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.15 + BM25 0.25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.70_b0.20_e0.10`: Full-corpus z-score fusion: K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.65_b0.25_e0.10`: Full-corpus z-score fusion: K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_custom_vector_average`: K3 dense baseline: 2-3-1 + 2-5_token + 2-8_emoji, vector_average_component_norm.
- `k3_bm25_embedding_full_d0.75_b0.20_e0.05`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_bm25_embedding_full_d0.60_b0.25_e0.15`: Full-corpus z-score fusion: K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.15 + BM25 0.30.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `source_ge3_plus_embedding_only_top20_rerank_k3bm25_075_025`: Candidate set=top20 source_count>=3 plus embedding-only top20; rerank by K3+BM25.
- `result_fusion_k3bm25_075_025_slots_1_2_4_5_embedding_slot3`: Result-level fusion: K3+BM25 supplies slots 1/2/4/5, external embedding supplies slot 3 using its first non-duplicate candidate.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top3_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top3 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.40 + embedding 0.35 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.25 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.10 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.20 + BM25 0.30.
- `four_source_top20_source_ge2_rerank_d0.75_b0.25`: Four-source candidate screening: 3 prompt sources + BM25, source_count>=2, rerank=K3/BM25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.25 + BM25 0.30.
- `five_source_top20_source_ge2_rerank_d0.75_b0.25`: Five-source candidate screening: 3 prompt sources + BM25 + external embedding, source_count>=2, rerank=K3/BM25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.40 + embedding 0.30 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.35 + embedding 0.35 + BM25 0.30.
- `k3_bm25_dense_top20_d0.75_b0.25`: Dense top-20 shortlist reranked by K3 dense 0.75 + BM25 0.25.
- `k3_bm25_full_d0.75_b0.25`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.25.
- `external_embedding`: External Qwen embedding standalone reference loaded from cache.
- `bm25`: BM25 standalone reference.
- `embedding_only_top20_rerank_k3bm25_075_025`: Only candidates that appear in embedding top20 and no other source top20; rerank by K3+BM25.
- `embedding_only_top20_rerank_k3bm25_ratio60_10`: Only candidates that appear in embedding top20 and no other source top20; rerank by K3+BM25.
