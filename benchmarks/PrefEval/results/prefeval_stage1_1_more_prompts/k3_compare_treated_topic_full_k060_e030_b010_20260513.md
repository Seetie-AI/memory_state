# PrefEval External Embedding Fusion

- Created UTC: `2026-05-13T18:27:07.148452+00:00`
- Items: `1000`
- Hidden tensor dir: `benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- K3 combo: `2-3-1_summarize + 2-5_token + 2-1-2`
- Embedding cache dir: `benchmarks/PrefEval/tensors/qwen3_embedding_implicit_persona_n1000_d19e54c734`
- Embedding model: `models/Qwen3-Embedding-0.6B-4bit-DWQ`
- Source rule: `top20 source_count>=2`
- Eval split: `all`
- Elapsed: `5m23s`

## Notes

- External embeddings are used only as a score matrix/source, not concatenated with 9B hidden vectors.
- Primary K3 dense baseline is 2-3-1_summarize + 2-5_token + 2-1-2 with vector_average_component_norm.
- source_count>=2 experiments use per-source top-k lists, with prompt components kept as separate sources.
- Concat experiments use source_count>=concat_source_min plus embedding top-k candidates, then rerank only that candidate set.

## Results

| rank | config | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR | avg shortlist | oracle@shortlist |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.123 | 0.257 | 0.346 | 0.199 | 0.236 | 0.233 | 24.5 | 0.639 |
| 2 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.121 | 0.254 | 0.344 | 0.197 | 0.234 | 0.231 | 24.5 | 0.639 |
| 3 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.120 | 0.247 | 0.344 | 0.192 | 0.232 | 0.227 | 24.5 | 0.639 |
| 4 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.116 | 0.248 | 0.343 | 0.192 | 0.231 | 0.228 | 24.5 | 0.639 |
| 5 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.123 | 0.257 | 0.342 | 0.200 | 0.235 | 0.233 | 24.5 | 0.639 |
| 6 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.120 | 0.251 | 0.342 | 0.196 | 0.232 | 0.229 | 24.5 | 0.639 |
| 7 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.121 | 0.250 | 0.342 | 0.195 | 0.232 | 0.229 | 24.5 | 0.639 |
| 8 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.121 | 0.249 | 0.342 | 0.194 | 0.232 | 0.230 | 24.5 | 0.639 |
| 9 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.118 | 0.252 | 0.342 | 0.195 | 0.232 | 0.230 | 24.5 | 0.639 |
| 10 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15` | 0.115 | 0.244 | 0.342 | 0.190 | 0.230 | 0.227 | 24.5 | 0.639 |
| 11 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.123 | 0.247 | 0.341 | 0.194 | 0.232 | 0.229 | 24.5 | 0.639 |
| 12 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.120 | 0.254 | 0.341 | 0.196 | 0.232 | 0.230 | 24.5 | 0.639 |
| 13 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.121 | 0.247 | 0.341 | 0.193 | 0.231 | 0.229 | 24.5 | 0.639 |
| 14 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.116 | 0.247 | 0.341 | 0.192 | 0.230 | 0.228 | 24.5 | 0.639 |
| 15 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10` | 0.116 | 0.252 | 0.341 | 0.194 | 0.230 | 0.226 | 24.5 | 0.639 |
| 16 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.116 | 0.248 | 0.341 | 0.192 | 0.230 | 0.227 | 24.5 | 0.639 |
| 17 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.112 | 0.250 | 0.341 | 0.191 | 0.228 | 0.224 | 24.5 | 0.639 |
| 18 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.121 | 0.256 | 0.340 | 0.198 | 0.233 | 0.230 | 24.5 | 0.639 |
| 19 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05` | 0.123 | 0.249 | 0.340 | 0.195 | 0.232 | 0.232 | 24.5 | 0.639 |
| 20 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.119 | 0.257 | 0.340 | 0.198 | 0.232 | 0.231 | 24.5 | 0.639 |
| 21 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.120 | 0.251 | 0.340 | 0.195 | 0.232 | 0.230 | 24.5 | 0.639 |
| 22 | `five_source_top20_source_ge2_rerank_d0.60_b0.10_e0.30` | 0.115 | 0.249 | 0.340 | 0.192 | 0.229 | 0.226 | 21.7 | 0.610 |
| 23 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.111 | 0.251 | 0.340 | 0.191 | 0.227 | 0.223 | 24.5 | 0.639 |
| 24 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.113 | 0.247 | 0.340 | 0.190 | 0.227 | 0.222 | 24.5 | 0.639 |
| 25 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.122 | 0.253 | 0.339 | 0.197 | 0.233 | 0.231 | 24.5 | 0.639 |
| 26 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.123 | 0.250 | 0.339 | 0.195 | 0.232 | 0.229 | 24.5 | 0.639 |
| 27 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.120 | 0.255 | 0.339 | 0.197 | 0.231 | 0.229 | 24.5 | 0.639 |
| 28 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.118 | 0.252 | 0.339 | 0.195 | 0.231 | 0.229 | 24.5 | 0.639 |
| 29 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.117 | 0.254 | 0.339 | 0.195 | 0.230 | 0.227 | 24.5 | 0.639 |
| 30 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.112 | 0.246 | 0.339 | 0.190 | 0.228 | 0.224 | 24.5 | 0.639 |
| 31 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.114 | 0.244 | 0.339 | 0.188 | 0.228 | 0.222 | 24.5 | 0.639 |
| 32 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15` | 0.111 | 0.244 | 0.339 | 0.188 | 0.227 | 0.224 | 24.5 | 0.639 |
| 33 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.120 | 0.253 | 0.338 | 0.197 | 0.232 | 0.230 | 24.5 | 0.639 |
| 34 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.118 | 0.251 | 0.338 | 0.194 | 0.230 | 0.227 | 24.5 | 0.639 |
| 35 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.115 | 0.250 | 0.338 | 0.192 | 0.228 | 0.226 | 24.5 | 0.639 |
| 36 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10` | 0.116 | 0.248 | 0.338 | 0.192 | 0.228 | 0.225 | 24.5 | 0.639 |
| 37 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.113 | 0.250 | 0.338 | 0.191 | 0.227 | 0.224 | 24.5 | 0.639 |
| 38 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.112 | 0.247 | 0.338 | 0.189 | 0.227 | 0.225 | 24.5 | 0.639 |
| 39 | `k3_bm25_embedding_full_d0.60_b0.10_e0.30` | 0.110 | 0.247 | 0.338 | 0.189 | 0.226 | 0.224 |  |  |
| 40 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00` | 0.120 | 0.257 | 0.337 | 0.199 | 0.232 | 0.231 | 24.5 | 0.639 |
| 41 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.119 | 0.250 | 0.337 | 0.194 | 0.230 | 0.228 | 24.5 | 0.639 |
| 42 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.118 | 0.250 | 0.337 | 0.194 | 0.229 | 0.226 | 24.5 | 0.639 |
| 43 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.120 | 0.252 | 0.337 | 0.195 | 0.229 | 0.229 | 24.5 | 0.639 |
| 44 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05` | 0.117 | 0.250 | 0.337 | 0.193 | 0.229 | 0.227 | 24.5 | 0.639 |
| 45 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.119 | 0.244 | 0.337 | 0.191 | 0.229 | 0.227 | 24.5 | 0.639 |
| 46 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.115 | 0.253 | 0.337 | 0.194 | 0.228 | 0.225 | 24.5 | 0.639 |
| 47 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.115 | 0.248 | 0.337 | 0.191 | 0.227 | 0.223 | 24.5 | 0.639 |
| 48 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.120 | 0.258 | 0.336 | 0.199 | 0.231 | 0.230 | 24.5 | 0.639 |
| 49 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00` | 0.118 | 0.254 | 0.336 | 0.196 | 0.230 | 0.229 | 24.5 | 0.639 |
| 50 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.120 | 0.253 | 0.336 | 0.196 | 0.230 | 0.229 | 24.5 | 0.639 |
| 51 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.121 | 0.248 | 0.336 | 0.194 | 0.230 | 0.229 | 24.5 | 0.639 |
| 52 | `five_source_top10_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.119 | 0.254 | 0.336 | 0.196 | 0.229 | 0.227 | 29.1 | 0.617 |
| 53 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.120 | 0.246 | 0.336 | 0.192 | 0.229 | 0.228 | 24.5 | 0.639 |
| 54 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10` | 0.117 | 0.248 | 0.336 | 0.192 | 0.229 | 0.228 | 24.5 | 0.639 |
| 55 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.119 | 0.247 | 0.336 | 0.192 | 0.228 | 0.226 | 24.5 | 0.639 |
| 56 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10` | 0.118 | 0.245 | 0.336 | 0.191 | 0.228 | 0.225 | 24.5 | 0.639 |
| 57 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.112 | 0.243 | 0.336 | 0.188 | 0.226 | 0.223 | 24.5 | 0.639 |
| 58 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15` | 0.113 | 0.248 | 0.336 | 0.190 | 0.226 | 0.223 | 24.5 | 0.639 |
| 59 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.119 | 0.252 | 0.335 | 0.195 | 0.229 | 0.227 | 24.5 | 0.639 |
| 60 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05` | 0.119 | 0.249 | 0.335 | 0.194 | 0.229 | 0.229 | 24.5 | 0.639 |
| 61 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.122 | 0.246 | 0.335 | 0.193 | 0.229 | 0.229 | 24.5 | 0.639 |
| 62 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.119 | 0.249 | 0.335 | 0.193 | 0.229 | 0.226 | 24.5 | 0.639 |
| 63 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.117 | 0.250 | 0.335 | 0.193 | 0.228 | 0.228 | 24.5 | 0.639 |
| 64 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.117 | 0.248 | 0.335 | 0.192 | 0.228 | 0.228 | 24.5 | 0.639 |
| 65 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05` | 0.116 | 0.252 | 0.335 | 0.194 | 0.228 | 0.226 | 24.5 | 0.639 |
| 66 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20` | 0.115 | 0.246 | 0.335 | 0.191 | 0.227 | 0.225 | 24.5 | 0.639 |
| 67 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.116 | 0.246 | 0.335 | 0.190 | 0.227 | 0.223 | 24.5 | 0.639 |
| 68 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10` | 0.113 | 0.248 | 0.335 | 0.191 | 0.226 | 0.225 | 24.5 | 0.639 |
| 69 | `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10` | 0.114 | 0.246 | 0.335 | 0.189 | 0.225 | 0.220 | 21.7 | 0.610 |
| 70 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.112 | 0.253 | 0.335 | 0.192 | 0.225 | 0.222 | 24.5 | 0.639 |
| 71 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.110 | 0.253 | 0.335 | 0.191 | 0.225 | 0.221 | 24.5 | 0.639 |
| 72 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.122 | 0.250 | 0.334 | 0.196 | 0.230 | 0.230 | 24.5 | 0.639 |
| 73 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00` | 0.120 | 0.253 | 0.334 | 0.197 | 0.230 | 0.230 | 24.5 | 0.639 |
| 74 | `five_source_top5_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.119 | 0.253 | 0.334 | 0.195 | 0.229 | 0.227 | 15.1 | 0.492 |
| 75 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00` | 0.117 | 0.255 | 0.334 | 0.196 | 0.228 | 0.226 | 24.5 | 0.639 |
| 76 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10` | 0.115 | 0.249 | 0.334 | 0.192 | 0.227 | 0.226 | 24.5 | 0.639 |
| 77 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.114 | 0.247 | 0.334 | 0.190 | 0.226 | 0.223 | 24.5 | 0.639 |
| 78 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15` | 0.112 | 0.250 | 0.334 | 0.191 | 0.225 | 0.222 | 24.5 | 0.639 |
| 79 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.110 | 0.254 | 0.334 | 0.191 | 0.224 | 0.220 | 24.5 | 0.639 |
| 80 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00` | 0.123 | 0.252 | 0.333 | 0.197 | 0.230 | 0.228 | 24.5 | 0.639 |
| 81 | `five_source_top3_union_ge1_score_fusion_k0.60_e0.30_b0.10` | 0.115 | 0.254 | 0.333 | 0.194 | 0.227 | 0.223 | 9.3 | 0.397 |
| 82 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.117 | 0.248 | 0.333 | 0.192 | 0.227 | 0.224 | 24.5 | 0.639 |
| 83 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05` | 0.116 | 0.249 | 0.333 | 0.192 | 0.226 | 0.224 | 24.5 | 0.639 |
| 84 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15` | 0.115 | 0.243 | 0.333 | 0.188 | 0.225 | 0.224 | 24.5 | 0.639 |
| 85 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20` | 0.114 | 0.245 | 0.333 | 0.189 | 0.225 | 0.223 | 24.5 | 0.639 |
| 86 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.109 | 0.254 | 0.333 | 0.191 | 0.223 | 0.219 | 24.5 | 0.639 |
| 87 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.119 | 0.246 | 0.332 | 0.191 | 0.226 | 0.225 | 24.5 | 0.639 |
| 88 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15` | 0.111 | 0.251 | 0.332 | 0.191 | 0.223 | 0.220 | 24.5 | 0.639 |
| 89 | `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05` | 0.114 | 0.245 | 0.332 | 0.188 | 0.223 | 0.217 | 21.7 | 0.610 |
| 90 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.118 | 0.252 | 0.331 | 0.195 | 0.227 | 0.225 | 24.5 | 0.639 |
| 91 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20` | 0.119 | 0.247 | 0.331 | 0.192 | 0.227 | 0.227 | 24.5 | 0.639 |
| 92 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.119 | 0.248 | 0.331 | 0.192 | 0.226 | 0.226 | 24.5 | 0.639 |
| 93 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05` | 0.115 | 0.251 | 0.331 | 0.193 | 0.226 | 0.224 | 24.5 | 0.639 |
| 94 | `source_ge3_plus_embedding_only_top20_rerank_k3bm25_ratio60_10` | 0.113 | 0.245 | 0.331 | 0.188 | 0.223 | 0.218 | 21.1 | 0.566 |
| 95 | `k3_bm25_embedding_full_d0.70_b0.20_e0.10` | 0.111 | 0.248 | 0.331 | 0.189 | 0.223 | 0.217 |  |  |
| 96 | `k3_bm25_embedding_full_d0.75_b0.20_e0.05` | 0.113 | 0.245 | 0.331 | 0.187 | 0.222 | 0.216 |  |  |
| 97 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.117 | 0.249 | 0.330 | 0.192 | 0.225 | 0.225 | 24.5 | 0.639 |
| 98 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.118 | 0.247 | 0.330 | 0.191 | 0.225 | 0.225 | 24.5 | 0.639 |
| 99 | `k3_custom_vector_average` | 0.120 | 0.250 | 0.329 | 0.194 | 0.226 | 0.220 |  |  |
| 100 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00` | 0.117 | 0.249 | 0.329 | 0.193 | 0.225 | 0.224 | 24.5 | 0.639 |
| 101 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.117 | 0.248 | 0.329 | 0.192 | 0.225 | 0.226 | 24.5 | 0.639 |
| 102 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.120 | 0.247 | 0.329 | 0.192 | 0.225 | 0.223 | 24.5 | 0.639 |
| 103 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.113 | 0.247 | 0.329 | 0.189 | 0.223 | 0.221 | 24.5 | 0.639 |
| 104 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.120 | 0.249 | 0.328 | 0.193 | 0.225 | 0.225 | 24.5 | 0.639 |
| 105 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.110 | 0.245 | 0.328 | 0.187 | 0.221 | 0.219 | 24.5 | 0.639 |
| 106 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20` | 0.121 | 0.249 | 0.327 | 0.194 | 0.225 | 0.227 | 24.5 | 0.639 |
| 107 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.119 | 0.247 | 0.327 | 0.192 | 0.224 | 0.224 | 24.5 | 0.639 |
| 108 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20` | 0.113 | 0.247 | 0.327 | 0.190 | 0.222 | 0.221 | 24.5 | 0.639 |
| 109 | `k3_bm25_embedding_full_d0.60_b0.25_e0.15` | 0.118 | 0.246 | 0.326 | 0.191 | 0.223 | 0.220 |  |  |
| 110 | `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10` | 0.117 | 0.250 | 0.326 | 0.192 | 0.223 | 0.219 | 21.7 | 0.610 |
| 111 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.116 | 0.247 | 0.326 | 0.190 | 0.223 | 0.222 | 24.5 | 0.639 |
| 112 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.121 | 0.248 | 0.325 | 0.193 | 0.224 | 0.227 | 24.5 | 0.639 |
| 113 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20` | 0.119 | 0.249 | 0.325 | 0.193 | 0.223 | 0.226 | 24.5 | 0.639 |
| 114 | `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15` | 0.118 | 0.245 | 0.324 | 0.190 | 0.222 | 0.221 | 21.7 | 0.610 |
| 115 | `k3_bm25_embedding_full_d0.65_b0.25_e0.10` | 0.118 | 0.247 | 0.324 | 0.191 | 0.222 | 0.218 |  |  |
| 116 | `source_ge3_plus_embedding_only_top20_rerank_k3bm25_075_025` | 0.117 | 0.239 | 0.324 | 0.187 | 0.221 | 0.218 | 21.1 | 0.566 |
| 117 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25` | 0.114 | 0.247 | 0.324 | 0.189 | 0.221 | 0.221 | 24.5 | 0.639 |
| 118 | `k3_bm25_dense_top20_d0.75_b0.25` | 0.113 | 0.239 | 0.324 | 0.185 | 0.220 | 0.214 |  |  |
| 119 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.119 | 0.249 | 0.323 | 0.193 | 0.223 | 0.226 | 24.5 | 0.639 |
| 120 | `result_fusion_k3bm25_ratio60_10_slots_1_2_4_5_embedding_slot3` | 0.112 | 0.235 | 0.323 | 0.183 | 0.219 | 0.215 |  |  |
| 121 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.117 | 0.242 | 0.322 | 0.189 | 0.221 | 0.222 | 24.5 | 0.639 |
| 122 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25` | 0.118 | 0.245 | 0.322 | 0.190 | 0.221 | 0.223 | 24.5 | 0.639 |
| 123 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.118 | 0.247 | 0.321 | 0.191 | 0.221 | 0.223 | 24.5 | 0.639 |
| 124 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25` | 0.116 | 0.244 | 0.321 | 0.189 | 0.221 | 0.222 | 24.5 | 0.639 |
| 125 | `five_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.116 | 0.238 | 0.321 | 0.185 | 0.219 | 0.215 | 21.7 | 0.610 |
| 126 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.119 | 0.248 | 0.320 | 0.193 | 0.223 | 0.226 | 24.5 | 0.639 |
| 127 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.121 | 0.248 | 0.319 | 0.193 | 0.221 | 0.226 | 24.5 | 0.639 |
| 128 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.117 | 0.247 | 0.319 | 0.191 | 0.221 | 0.223 | 24.5 | 0.639 |
| 129 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25` | 0.118 | 0.244 | 0.319 | 0.190 | 0.220 | 0.224 | 24.5 | 0.639 |
| 130 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.116 | 0.248 | 0.319 | 0.192 | 0.220 | 0.224 | 24.5 | 0.639 |
| 131 | `k3_bm25_embedding_full_d0.50_b0.25_e0.25` | 0.114 | 0.247 | 0.319 | 0.191 | 0.220 | 0.221 |  |  |
| 132 | `four_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.119 | 0.240 | 0.319 | 0.187 | 0.220 | 0.216 | 18.3 | 0.537 |
| 133 | `k3_bm25_full_d0.75_b0.25` | 0.117 | 0.239 | 0.318 | 0.186 | 0.219 | 0.214 |  |  |
| 134 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.111 | 0.238 | 0.318 | 0.184 | 0.216 | 0.217 | 24.5 | 0.639 |
| 135 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30` | 0.118 | 0.243 | 0.317 | 0.190 | 0.220 | 0.222 | 24.5 | 0.639 |
| 136 | `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25` | 0.119 | 0.246 | 0.316 | 0.192 | 0.220 | 0.224 | 21.7 | 0.610 |
| 137 | `result_fusion_k3bm25_075_025_slots_1_2_4_5_embedding_slot3` | 0.117 | 0.228 | 0.316 | 0.181 | 0.217 | 0.214 |  |  |
| 138 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.116 | 0.246 | 0.315 | 0.190 | 0.218 | 0.223 | 24.5 | 0.639 |
| 139 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.111 | 0.241 | 0.314 | 0.185 | 0.215 | 0.219 | 24.5 | 0.639 |
| 140 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25` | 0.114 | 0.245 | 0.313 | 0.189 | 0.217 | 0.223 | 24.5 | 0.639 |
| 141 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25` | 0.114 | 0.244 | 0.313 | 0.188 | 0.216 | 0.222 | 24.5 | 0.639 |
| 142 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30` | 0.113 | 0.243 | 0.313 | 0.187 | 0.216 | 0.219 | 24.5 | 0.639 |
| 143 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30` | 0.112 | 0.242 | 0.313 | 0.186 | 0.215 | 0.218 | 24.5 | 0.639 |
| 144 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.115 | 0.245 | 0.312 | 0.189 | 0.217 | 0.222 | 24.5 | 0.639 |
| 145 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.115 | 0.243 | 0.312 | 0.187 | 0.216 | 0.221 | 24.5 | 0.639 |
| 146 | `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.114 | 0.242 | 0.311 | 0.188 | 0.216 | 0.222 | 24.5 | 0.639 |
| 147 | `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.115 | 0.244 | 0.311 | 0.188 | 0.215 | 0.221 | 24.5 | 0.639 |
| 148 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30` | 0.108 | 0.242 | 0.306 | 0.185 | 0.211 | 0.217 | 24.5 | 0.639 |
| 149 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30` | 0.112 | 0.240 | 0.304 | 0.186 | 0.212 | 0.219 | 24.5 | 0.639 |
| 150 | `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30` | 0.105 | 0.236 | 0.303 | 0.180 | 0.208 | 0.214 | 24.5 | 0.639 |
| 151 | `external_embedding` | 0.084 | 0.207 | 0.287 | 0.155 | 0.187 | 0.189 |  |  |
| 152 | `bm25` | 0.035 | 0.074 | 0.094 | 0.058 | 0.066 | 0.067 |  |  |
| 153 | `embedding_only_top20_rerank_k3bm25_ratio60_10` | 0.020 | 0.037 | 0.068 | 0.029 | 0.042 | 0.083 | 8.2 | 0.070 |
| 154 | `embedding_only_top20_rerank_k3bm25_075_025` | 0.015 | 0.040 | 0.064 | 0.029 | 0.039 | 0.081 | 8.2 | 0.070 |

## Configs

- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.35 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.35_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.30 + BM25 0.15.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.35 + BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.20_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.20 + BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.35_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.35 + BM25 0.05.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.60_b0.10_e0.30`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.60 + BM25 0.10 + embedding 0.30.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.10 + BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.85 + embedding 0.15 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.30_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.25 + BM25 0.00.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.20 + BM25 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.15_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.15 + BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.60_b0.10_e0.30`: Full-corpus z-score fusion: K3 dense 0.60 + BM25 0.10 + embedding 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.35_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.35 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.25_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.25 + BM25 0.05.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.30 + BM25 0.00.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.25_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top10_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top10 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.35_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.20 + BM25 0.20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.10_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.15 + BM25 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.20_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.20 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.30_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.30 + BM25 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.20_b0.05`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.20_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.30_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.30 + BM25 0.10.
- `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.30_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top5_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top5 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.80_e0.20_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.80 + embedding 0.20 + BM25 0.00.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.25_b0.10`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.25 + BM25 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.15_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.15 + BM25 0.15.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.85_e0.15_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top3_union_ge1_score_fusion_k0.60_e0.30_b0.10`: Union of each source top3 with source_count>=1; rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.15 + BM25 0.20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.85_e0.10_b0.05`: Score-level z-fusion baseline for the same candidate set: K3 0.85 + embedding 0.10 + BM25 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.25_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.25 + BM25 0.15.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.15_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.75_e0.10_b0.15`: Score-level z-fusion baseline for the same candidate set: K3 0.75 + embedding 0.10 + BM25 0.15.
- `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: Score-level z-fusion baseline for the same candidate set: K3 0.90 + embedding 0.10 + BM25 0.00.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.25_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.25 + BM25 0.20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.80_e0.15_b0.05`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `source_ge3_plus_embedding_only_top20_rerank_k3bm25_ratio60_10`: Candidate set=top20 source_count>=3 plus embedding-only top20; rerank by K3+BM25.
- `k3_bm25_embedding_full_d0.70_b0.20_e0.10`: Full-corpus z-score fusion: K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_bm25_embedding_full_d0.75_b0.20_e0.05`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_custom_vector_average`: K3 dense baseline: 2-3-1_summarize + 2-5_token + 2-1-2, vector_average_component_norm.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.90_e0.10_b0.00`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.65 + embedding 0.10 + BM25 0.25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.30_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.30 + BM25 0.20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.70_e0.10_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.70 + embedding 0.10 + BM25 0.20.
- `k3_bm25_embedding_full_d0.60_b0.25_e0.15`: Full-corpus z-score fusion: K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.35_b0.20`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.35 + BM25 0.20.
- `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `k3_bm25_embedding_full_d0.65_b0.25_e0.10`: Full-corpus z-score fusion: K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `source_ge3_plus_embedding_only_top20_rerank_k3bm25_075_025`: Candidate set=top20 source_count>=3 plus embedding-only top20; rerank by K3+BM25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.65_e0.10_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_dense_top20_d0.75_b0.25`: Dense top-20 shortlist reranked by K3 dense 0.75 + BM25 0.25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `result_fusion_k3bm25_ratio60_10_slots_1_2_4_5_embedding_slot3`: Result-level fusion: K3+BM25 supplies slots 1/2/4/5, external embedding supplies slot 3 using its first non-duplicate candidate.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.20_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.20 + BM25 0.25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.15_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.15 + BM25 0.25.
- `five_source_top20_source_ge2_rerank_d0.75_b0.25`: Five-source candidate screening: 3 prompt sources + BM25 + external embedding, source_count>=2, rerank=K3/BM25.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.25_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.25 + BM25 0.25.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_bm25_embedding_full_d0.50_b0.25_e0.25`: Full-corpus z-score fusion: K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `four_source_top20_source_ge2_rerank_d0.75_b0.25`: Four-source candidate screening: 3 prompt sources + BM25, source_count>=2, rerank=K3/BM25.
- `k3_bm25_full_d0.75_b0.25`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.60 + embedding 0.10 + BM25 0.30.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.60_e0.10_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `result_fusion_k3bm25_075_025_slots_1_2_4_5_embedding_slot3`: Result-level fusion: K3+BM25 supplies slots 1/2/4/5, external embedding supplies slot 3 using its first non-duplicate candidate.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.30_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.30 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.35_b0.25`: Score-level z-fusion baseline for the same candidate set: K3 0.40 + embedding 0.35 + BM25 0.25.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.55_e0.15_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.55 + embedding 0.15 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.50_e0.20_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.50 + embedding 0.20 + BM25 0.30.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_concat_first_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: K3 vector average + external embedding weighted concat (concat_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_concat_norm_first_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: K3 vector average + external embedding weighted concat (norm_first), then BM25 score fusion; candidate set=top20 source_count>=3 plus embedding top20.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.40_e0.30_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.40 + embedding 0.30 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.45_e0.25_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.45 + embedding 0.25 + BM25 0.30.
- `k3_embedding_score_zfusion_bm25_source_ge3_plus_embedding_top20_k0.35_e0.35_b0.30`: Score-level z-fusion baseline for the same candidate set: K3 0.35 + embedding 0.35 + BM25 0.30.
- `external_embedding`: External Qwen embedding standalone reference loaded from cache.
- `bm25`: BM25 standalone reference.
- `embedding_only_top20_rerank_k3bm25_ratio60_10`: Only candidates that appear in embedding top20 and no other source top20; rerank by K3+BM25.
- `embedding_only_top20_rerank_k3bm25_075_025`: Only candidates that appear in embedding top20 and no other source top20; rerank by K3+BM25.
