# PrefEval Stage 1 Offline Analysis

- Created UTC: `2026-05-13T00:21:11.084138+00:00`
- Analysis: `prefeval_stage1_logits_k3`
- Items: `1000`
- Tensor dir: `/Users/gordonxiong/Desktop/Repos/memory_state/benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- Elapsed: `1m43s`

## Notes

- Stored hidden vectors are raw extractor outputs; this offline pass applies retrieval transforms after loading.
- The n=1000 prompt-sweep table previously reported anti_pca_both_k15 plus L2-normalized cosine, not untreated raw cosine.
- candidate_only k=10 is a sanity check because earlier LongMemEval stages found candidate-only transforms harmful.

## Results

| rank | split | config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | `second500` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.120 | 0.260 | 0.356 | 0.238 | 0.230 |
| 2 | `second500` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.114 | 0.258 | 0.352 | 0.235 | 0.227 |
| 3 | `second500` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.118 | 0.254 | 0.350 | 0.235 | 0.227 |
| 4 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05` | 0.112 | 0.256 | 0.350 | 0.234 | 0.224 |
| 5 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10` | 0.114 | 0.250 | 0.349 | 0.233 | 0.224 |
| 6 | `second500` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.118 | 0.250 | 0.348 | 0.234 | 0.226 |
| 7 | `second500` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.120 | 0.254 | 0.346 | 0.234 | 0.227 |
| 8 | `second500` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.122 | 0.248 | 0.346 | 0.234 | 0.226 |
| 9 | `second500` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.102 | 0.252 | 0.344 | 0.225 | 0.212 |
| 10 | `second500` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.116 | 0.250 | 0.342 | 0.230 | 0.224 |
| 11 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.75_b0.20_l0.05` | 0.116 | 0.250 | 0.341 | 0.230 | 0.223 |
| 12 | `second500` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.116 | 0.244 | 0.340 | 0.229 | 0.223 |
| 13 | `all` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10` | 0.110 | 0.249 | 0.340 | 0.227 | 0.219 |
| 14 | `second500` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.104 | 0.244 | 0.340 | 0.223 | 0.211 |
| 15 | `second500` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.102 | 0.242 | 0.340 | 0.223 | 0.210 |
| 16 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_dense_only` | 0.124 | 0.263 | 0.339 | 0.235 | 0.231 |
| 17 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25` | 0.117 | 0.253 | 0.339 | 0.230 | 0.223 |
| 18 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25` | 0.117 | 0.254 | 0.338 | 0.230 | 0.224 |
| 19 | `second500` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.110 | 0.252 | 0.338 | 0.229 | 0.220 |
| 20 | `second500` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.120 | 0.240 | 0.338 | 0.228 | 0.224 |
| 21 | `all` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05` | 0.110 | 0.248 | 0.337 | 0.226 | 0.219 |
| 22 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10` | 0.120 | 0.246 | 0.336 | 0.229 | 0.224 |
| 23 | `second500` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.124 | 0.240 | 0.336 | 0.229 | 0.226 |
| 24 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25` | 0.115 | 0.253 | 0.336 | 0.229 | 0.223 |
| 25 | `second500` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.108 | 0.262 | 0.336 | 0.229 | 0.221 |
| 26 | `second500` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.120 | 0.234 | 0.336 | 0.227 | 0.224 |
| 27 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.70_b0.20_l0.10` | 0.115 | 0.242 | 0.336 | 0.226 | 0.219 |
| 28 | `second500` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.104 | 0.248 | 0.336 | 0.223 | 0.211 |
| 29 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25` | 0.119 | 0.251 | 0.335 | 0.229 | 0.223 |
| 30 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_dense_bm25_d0.75_b0.25` | 0.117 | 0.250 | 0.335 | 0.228 | 0.222 |
| 31 | `second500` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.108 | 0.260 | 0.334 | 0.228 | 0.220 |
| 32 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15` | 0.115 | 0.246 | 0.334 | 0.227 | 0.222 |
| 33 | `second500` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.108 | 0.250 | 0.334 | 0.226 | 0.218 |
| 34 | `all` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.75_b0.20_l0.05` | 0.114 | 0.245 | 0.334 | 0.226 | 0.219 |
| 35 | `second500` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.104 | 0.250 | 0.334 | 0.221 | 0.211 |
| 36 | `second500` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.100 | 0.242 | 0.334 | 0.219 | 0.207 |
| 37 | `all` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25` | 0.121 | 0.244 | 0.333 | 0.228 | 0.221 |
| 38 | `second500` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.122 | 0.242 | 0.332 | 0.226 | 0.223 |
| 39 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05` | 0.114 | 0.252 | 0.332 | 0.226 | 0.221 |
| 40 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10` | 0.108 | 0.247 | 0.332 | 0.222 | 0.217 |
| 41 | `second500` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500` | 0.108 | 0.244 | 0.332 | 0.221 | 0.211 |
| 42 | `second500` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500` | 0.108 | 0.238 | 0.332 | 0.221 | 0.210 |
| 43 | `all` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25` | 0.117 | 0.244 | 0.331 | 0.226 | 0.221 |
| 44 | `all` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25` | 0.117 | 0.241 | 0.331 | 0.226 | 0.219 |
| 45 | `all` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25` | 0.116 | 0.244 | 0.331 | 0.225 | 0.220 |
| 46 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05` | 0.108 | 0.247 | 0.330 | 0.223 | 0.215 |
| 47 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10` | 0.107 | 0.240 | 0.330 | 0.222 | 0.214 |
| 48 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.75_b0.20_l0.05` | 0.112 | 0.244 | 0.329 | 0.224 | 0.216 |
| 49 | `first500` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.116 | 0.252 | 0.328 | 0.225 | 0.218 |
| 50 | `all` | `logits_k3_k3_key_assoc_topic_zsum_dense_bm25_d0.75_b0.25` | 0.116 | 0.244 | 0.328 | 0.224 | 0.220 |
| 51 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25` | 0.116 | 0.244 | 0.328 | 0.223 | 0.219 |
| 52 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_dense_bm25_d0.75_b0.25` | 0.114 | 0.246 | 0.328 | 0.223 | 0.218 |
| 53 | `all` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15` | 0.111 | 0.241 | 0.328 | 0.221 | 0.216 |
| 54 | `all` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10` | 0.109 | 0.241 | 0.328 | 0.221 | 0.215 |
| 55 | `all` | `logits_k3_k3_key_assoc_topic_zsum_dense_only` | 0.117 | 0.254 | 0.327 | 0.226 | 0.224 |
| 56 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_dense_only` | 0.112 | 0.251 | 0.327 | 0.223 | 0.222 |
| 57 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.75_b0.20_l0.05` | 0.115 | 0.243 | 0.327 | 0.222 | 0.219 |
| 58 | `all` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.70_b0.20_l0.10` | 0.115 | 0.231 | 0.327 | 0.221 | 0.216 |
| 59 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25` | 0.115 | 0.240 | 0.326 | 0.222 | 0.219 |
| 60 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_dense_only` | 0.099 | 0.235 | 0.326 | 0.215 | 0.203 |
| 61 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25` | 0.116 | 0.243 | 0.325 | 0.223 | 0.219 |
| 62 | `all` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25` | 0.104 | 0.242 | 0.325 | 0.218 | 0.208 |
| 63 | `first500` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.118 | 0.248 | 0.324 | 0.225 | 0.219 |
| 64 | `all` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.75_b0.20_l0.05` | 0.106 | 0.239 | 0.324 | 0.217 | 0.208 |
| 65 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25` | 0.112 | 0.243 | 0.323 | 0.222 | 0.215 |
| 66 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25` | 0.116 | 0.245 | 0.323 | 0.221 | 0.218 |
| 67 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25` | 0.108 | 0.246 | 0.323 | 0.218 | 0.216 |
| 68 | `first500` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.118 | 0.238 | 0.322 | 0.223 | 0.216 |
| 69 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25` | 0.111 | 0.248 | 0.322 | 0.222 | 0.216 |
| 70 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25` | 0.110 | 0.248 | 0.322 | 0.221 | 0.215 |
| 71 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_dense_bm25_d0.75_b0.25` | 0.110 | 0.242 | 0.322 | 0.220 | 0.213 |
| 72 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_paper_alpha0.50` | 0.107 | 0.236 | 0.322 | 0.218 | 0.218 |
| 73 | `all` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25` | 0.106 | 0.236 | 0.322 | 0.217 | 0.208 |
| 74 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.65_b0.25_l0.10` | 0.113 | 0.234 | 0.321 | 0.218 | 0.214 |
| 75 | `all` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25` | 0.107 | 0.238 | 0.321 | 0.217 | 0.208 |
| 76 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10` | 0.108 | 0.239 | 0.321 | 0.216 | 0.213 |
| 77 | `first500` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.116 | 0.248 | 0.320 | 0.223 | 0.219 |
| 78 | `first500` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.120 | 0.240 | 0.320 | 0.222 | 0.216 |
| 79 | `first500` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.114 | 0.248 | 0.320 | 0.222 | 0.219 |
| 80 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_dense_only` | 0.113 | 0.248 | 0.320 | 0.221 | 0.217 |
| 81 | `first500` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.116 | 0.238 | 0.320 | 0.221 | 0.216 |
| 82 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25` | 0.110 | 0.243 | 0.320 | 0.220 | 0.213 |
| 83 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.70_b0.20_l0.10` | 0.112 | 0.236 | 0.320 | 0.219 | 0.213 |
| 84 | `all` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05` | 0.105 | 0.238 | 0.320 | 0.217 | 0.210 |
| 85 | `all` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25` | 0.106 | 0.238 | 0.320 | 0.217 | 0.208 |
| 86 | `all` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10` | 0.106 | 0.235 | 0.320 | 0.216 | 0.210 |
| 87 | `all` | `logits_k3_k3_key_assoc_tag_zsum_dense_bm25_d0.75_b0.25` | 0.106 | 0.235 | 0.320 | 0.216 | 0.207 |
| 88 | `all` | `logits_k3_k3_key_assoc_tag_zsum_dense_only` | 0.102 | 0.243 | 0.320 | 0.216 | 0.207 |
| 89 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15` | 0.109 | 0.235 | 0.320 | 0.215 | 0.213 |
| 90 | `first500` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.112 | 0.248 | 0.318 | 0.218 | 0.214 |
| 91 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.70_b0.20_l0.10` | 0.113 | 0.232 | 0.317 | 0.216 | 0.214 |
| 92 | `all` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25` | 0.108 | 0.236 | 0.317 | 0.214 | 0.212 |
| 93 | `first500` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.110 | 0.246 | 0.316 | 0.217 | 0.213 |
| 94 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25` | 0.103 | 0.234 | 0.316 | 0.213 | 0.204 |
| 95 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10` | 0.108 | 0.239 | 0.315 | 0.216 | 0.212 |
| 96 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10` | 0.109 | 0.233 | 0.315 | 0.215 | 0.210 |
| 97 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25` | 0.102 | 0.240 | 0.315 | 0.213 | 0.206 |
| 98 | `all` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.65_b0.25_l0.10` | 0.107 | 0.230 | 0.315 | 0.212 | 0.208 |
| 99 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25` | 0.101 | 0.235 | 0.315 | 0.212 | 0.203 |
| 100 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.75_b0.20_l0.05` | 0.101 | 0.234 | 0.315 | 0.212 | 0.204 |
| 101 | `first500` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.116 | 0.238 | 0.314 | 0.218 | 0.216 |
| 102 | `first500` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.110 | 0.248 | 0.314 | 0.217 | 0.212 |
| 103 | `first500` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.108 | 0.246 | 0.314 | 0.216 | 0.211 |
| 104 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05` | 0.107 | 0.236 | 0.314 | 0.214 | 0.208 |
| 105 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_dense_bm25_d0.75_b0.25` | 0.101 | 0.237 | 0.314 | 0.212 | 0.203 |
| 106 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_paper_alpha0.50` | 0.102 | 0.228 | 0.313 | 0.210 | 0.211 |
| 107 | `all` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15` | 0.102 | 0.228 | 0.312 | 0.210 | 0.204 |
| 108 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15` | 0.108 | 0.232 | 0.311 | 0.213 | 0.210 |
| 109 | `all` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.70_b0.20_l0.10` | 0.107 | 0.228 | 0.311 | 0.212 | 0.206 |
| 110 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25` | 0.103 | 0.237 | 0.311 | 0.211 | 0.205 |
| 111 | `all` | `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_paper_alpha0.50` | 0.104 | 0.227 | 0.311 | 0.211 | 0.213 |
| 112 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10` | 0.101 | 0.227 | 0.311 | 0.209 | 0.203 |
| 113 | `first500` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.112 | 0.236 | 0.310 | 0.215 | 0.209 |
| 114 | `all` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10` | 0.104 | 0.231 | 0.310 | 0.211 | 0.207 |
| 115 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.65_b0.25_l0.10` | 0.108 | 0.224 | 0.309 | 0.210 | 0.208 |
| 116 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15` | 0.096 | 0.220 | 0.309 | 0.205 | 0.199 |
| 117 | `first500` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.114 | 0.234 | 0.308 | 0.215 | 0.210 |
| 118 | `first500` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.114 | 0.234 | 0.308 | 0.215 | 0.211 |
| 119 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25` | 0.103 | 0.229 | 0.307 | 0.207 | 0.208 |
| 120 | `first500` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.112 | 0.236 | 0.306 | 0.213 | 0.208 |
| 121 | `first500` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.106 | 0.232 | 0.306 | 0.210 | 0.205 |
| 122 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.70_b0.20_l0.10` | 0.103 | 0.223 | 0.305 | 0.206 | 0.200 |
| 123 | `first500` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.110 | 0.230 | 0.304 | 0.211 | 0.205 |
| 124 | `first500` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.108 | 0.228 | 0.304 | 0.211 | 0.204 |
| 125 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25` | 0.108 | 0.224 | 0.303 | 0.208 | 0.207 |
| 126 | `first500` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.110 | 0.232 | 0.302 | 0.210 | 0.205 |
| 127 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.65_b0.25_l0.10` | 0.105 | 0.229 | 0.302 | 0.207 | 0.203 |
| 128 | `first500` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.098 | 0.230 | 0.300 | 0.205 | 0.197 |
| 129 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.60_b0.25_l0.15` | 0.103 | 0.223 | 0.299 | 0.203 | 0.202 |
| 130 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_paper_alpha0.50` | 0.098 | 0.220 | 0.297 | 0.201 | 0.202 |
| 131 | `first500` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500` | 0.102 | 0.228 | 0.296 | 0.206 | 0.200 |
| 132 | `first500` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.100 | 0.230 | 0.296 | 0.204 | 0.201 |
| 133 | `all` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25` | 0.105 | 0.220 | 0.296 | 0.203 | 0.203 |
| 134 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25` | 0.098 | 0.219 | 0.294 | 0.199 | 0.198 |
| 135 | `all` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.60_b0.25_l0.15` | 0.099 | 0.209 | 0.293 | 0.197 | 0.196 |
| 136 | `all` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.65_b0.25_l0.10` | 0.103 | 0.213 | 0.292 | 0.200 | 0.197 |
| 137 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.60_b0.25_l0.15` | 0.098 | 0.209 | 0.291 | 0.196 | 0.195 |
| 138 | `first500` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500` | 0.098 | 0.230 | 0.290 | 0.201 | 0.198 |
| 139 | `all` | `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_paper_alpha0.50` | 0.093 | 0.210 | 0.289 | 0.194 | 0.195 |
| 140 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_paper_alpha0.50` | 0.090 | 0.206 | 0.288 | 0.191 | 0.192 |
| 141 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.60_b0.25_l0.15` | 0.100 | 0.211 | 0.285 | 0.194 | 0.193 |
| 142 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.65_b0.25_l0.10` | 0.101 | 0.206 | 0.281 | 0.193 | 0.193 |
| 143 | `all` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.60_b0.25_l0.15` | 0.098 | 0.198 | 0.278 | 0.189 | 0.188 |
| 144 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.60_b0.25_l0.15` | 0.099 | 0.195 | 0.267 | 0.184 | 0.185 |
| 145 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.50_b0.25_l0.25` | 0.088 | 0.189 | 0.250 | 0.171 | 0.177 |
| 146 | `all` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.50_b0.25_l0.25` | 0.084 | 0.184 | 0.246 | 0.167 | 0.172 |
| 147 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.50_b0.25_l0.25` | 0.086 | 0.183 | 0.243 | 0.165 | 0.168 |
| 148 | `all` | `logits_k3_k3_key_assoc_topic_toplogits_sparse_only` | 0.076 | 0.166 | 0.243 | 0.159 | 0.165 |
| 149 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.50_b0.25_l0.25` | 0.083 | 0.184 | 0.241 | 0.164 | 0.171 |
| 150 | `all` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.50_b0.25_l0.25` | 0.083 | 0.175 | 0.238 | 0.161 | 0.163 |
| 151 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.50_b0.25_l0.25` | 0.083 | 0.172 | 0.227 | 0.156 | 0.161 |
| 152 | `all` | `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_paper_alpha0.50` | 0.079 | 0.153 | 0.213 | 0.145 | 0.151 |
| 153 | `all` | `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_paper_alpha0.50` | 0.079 | 0.155 | 0.212 | 0.145 | 0.153 |
| 154 | `all` | `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_paper_alpha0.50` | 0.076 | 0.153 | 0.211 | 0.144 | 0.150 |
| 155 | `all` | `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_paper_alpha0.50` | 0.078 | 0.153 | 0.204 | 0.141 | 0.147 |
| 156 | `all` | `logits_k3_k3_key_assoc_tag_toplogits_sparse_only` | 0.060 | 0.146 | 0.204 | 0.134 | 0.139 |
| 157 | `all` | `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_paper_alpha0.50` | 0.077 | 0.144 | 0.194 | 0.136 | 0.143 |
| 158 | `all` | `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_paper_alpha0.50` | 0.075 | 0.144 | 0.190 | 0.133 | 0.141 |
| 159 | `all` | `logits_k3_k3_key_assoc_topic_promptreps_sparse_only` | 0.043 | 0.082 | 0.107 | 0.077 | 0.081 |
| 160 | `all` | `logits_k3_k3_key_assoc_tag_promptreps_sparse_only` | 0.041 | 0.083 | 0.104 | 0.075 | 0.079 |
| 161 | `all` | `bm25` | 0.035 | 0.074 | 0.094 | 0.066 | 0.067 |

## Configs

- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_dense_only`: K3 dense baseline for k3_key_assoc_topic, scorer=vector_average_component_norm (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_dense_bm25_d0.75_b0.25`: K3 dense + BM25 z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_second500`: Second-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_dense_bm25_d0.75_b0.25`: K3 dense + BM25 z-fusion for k3_key_assoc_topic, scorer=zsum (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_dense_bm25_d0.75_b0.25`: K3 dense + BM25 z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_topic_zsum_dense_only`: K3 dense baseline for k3_key_assoc_topic, scorer=zsum (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_dense_only`: K3 dense baseline for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_dense_only`: K3 dense baseline for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_dense_bm25_d0.75_b0.25`: K3 dense + BM25 z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_topic, scorer=vector_average_component_norm, alpha=0.50 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_dense_only`: K3 dense baseline for k3_key_assoc_tag, scorer=vector_average_component_norm (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_dense_bm25_d0.75_b0.25`: K3 dense + BM25 z-fusion for k3_key_assoc_tag, scorer=zsum (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_dense_only`: K3 dense baseline for k3_key_assoc_tag, scorer=zsum (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_topic: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.75_b0.20_l0.05`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_dense_bm25_d0.75_b0.25`: K3 dense + BM25 z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, alpha=0.50 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25`: Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_unfiltered_top256_log1p_relu_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_topic, scorer=zsum, alpha=0.50 (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.70_b0.20_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=unfiltered_top256_log1p_relu (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_unfiltered_top256_log1p_relu_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_tag, scorer=vector_average_component_norm, alpha=0.50 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge1_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge1, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=unfiltered_top256_log1p_relu (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=unfiltered_top256_log1p_relu (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_source_ge2_top20_rerank_d0.75_b0.25_first500`: First-half validation for Top-20 source screening for k3_key_assoc_tag: 3 dense prompt sources + BM25 + logits, source_ge2, rerank=dense/BM25 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_zsum_unfiltered_top256_log1p_relu_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_tag, scorer=zsum, alpha=0.50 (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_unfiltered_top256_log1p_relu_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, alpha=0.50 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.65_b0.25_l0.10`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.60_b0.25_l0.15`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vector_average_component_norm, logits=promptreps_text_token_filtered (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_toplogits_sparse_only`: Unfiltered top-256 sparse logits only for k3_key_assoc_topic (sparse_zsum)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=zsum, logits=promptreps_text_token_filtered (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_d0.50_b0.25_l0.25`: K3 dense + BM25 + logits z-fusion for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, logits=promptreps_text_token_filtered (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vertical_concat_norm_weighted_promptreps_text_token_filtered_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_topic, scorer=vertical_concat_norm_weighted, alpha=0.50 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_vector_average_component_norm_promptreps_text_token_filtered_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_topic, scorer=vector_average_component_norm, alpha=0.50 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_topic_zsum_promptreps_text_token_filtered_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_topic, scorer=zsum, alpha=0.50 (zsum)
- `logits_k3_k3_key_assoc_tag_vector_average_component_norm_promptreps_text_token_filtered_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_tag, scorer=vector_average_component_norm, alpha=0.50 (vector_average_component_norm)
- `logits_k3_k3_key_assoc_tag_toplogits_sparse_only`: Unfiltered top-256 sparse logits only for k3_key_assoc_tag (sparse_zsum)
- `logits_k3_k3_key_assoc_tag_zsum_promptreps_text_token_filtered_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_tag, scorer=zsum, alpha=0.50 (zsum)
- `logits_k3_k3_key_assoc_tag_vertical_concat_norm_weighted_promptreps_text_token_filtered_paper_alpha0.50`: PromptReps-style dense+sparse hybrid for k3_key_assoc_tag, scorer=vertical_concat_norm_weighted, alpha=0.50 (vertical_concat_norm_weighted)
- `logits_k3_k3_key_assoc_topic_promptreps_sparse_only`: PromptReps paper-style filtered sparse logits only for k3_key_assoc_topic (sparse_zsum)
- `logits_k3_k3_key_assoc_tag_promptreps_sparse_only`: PromptReps paper-style filtered sparse logits only for k3_key_assoc_tag (sparse_zsum)
- `bm25`: BM25 over preference memory strings (bm25)
