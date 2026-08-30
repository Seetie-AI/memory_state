# PrefEval Stage 1 Offline Analysis

- Created UTC: `2026-05-12T18:46:52.579082+00:00`
- Analysis: `prefeval_stage1_promptreps`
- Items: `1000`
- Tensor dir: `/Users/gordonxiong/Desktop/Repos/memory_state/benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- Elapsed: `13s`

## Notes

- Stored hidden vectors are raw extractor outputs; this offline pass applies retrieval transforms after loading.
- The n=1000 prompt-sweep table previously reported anti_pca_both_k15 plus L2-normalized cosine, not untreated raw cosine.
- candidate_only k=10 is a sanity check because earlier LongMemEval stages found candidate-only transforms harmful.

## Results

| rank | split | config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | `all` | `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.90` | 0.116 | 0.256 | 0.347 | 0.233 | 0.226 |
| 2 | `all` | `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.80` | 0.112 | 0.236 | 0.332 | 0.222 | 0.217 |
| 3 | `all` | `promptreps_2-3-1_dense_sparse_alpha0.90` | 0.106 | 0.241 | 0.318 | 0.216 | 0.209 |
| 4 | `all` | `promptreps_2-5_dense_sparse_alpha0.90` | 0.099 | 0.228 | 0.315 | 0.210 | 0.202 |
| 5 | `all` | `promptreps_2-3-2_query_dense_sparse_alpha0.90` | 0.097 | 0.230 | 0.311 | 0.207 | 0.199 |
| 6 | `all` | `promptreps_2-3-1_dense_sparse_alpha0.80` | 0.101 | 0.226 | 0.309 | 0.208 | 0.202 |
| 7 | `all` | `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.70` | 0.101 | 0.214 | 0.304 | 0.202 | 0.200 |
| 8 | `all` | `promptreps_2-5_dense_sparse_alpha0.80` | 0.095 | 0.221 | 0.298 | 0.200 | 0.196 |
| 9 | `all` | `promptreps_2-3-2_query_dense_sparse_alpha0.80` | 0.089 | 0.215 | 0.296 | 0.195 | 0.189 |
| 10 | `all` | `promptreps_2-1_dense_sparse_alpha0.90` | 0.090 | 0.206 | 0.295 | 0.194 | 0.194 |
| 11 | `all` | `promptreps_2-3-1_dense_sparse_alpha0.70` | 0.091 | 0.206 | 0.284 | 0.190 | 0.187 |
| 12 | `all` | `promptreps_2-5_dense_sparse_alpha0.70` | 0.084 | 0.190 | 0.278 | 0.182 | 0.179 |
| 13 | `all` | `promptreps_2-3-2_query_dense_sparse_alpha0.70` | 0.084 | 0.194 | 0.274 | 0.180 | 0.175 |
| 14 | `all` | `promptreps_2-1_dense_sparse_alpha0.80` | 0.086 | 0.188 | 0.273 | 0.179 | 0.183 |
| 15 | `all` | `promptreps_2-1_dense_sparse_alpha0.70` | 0.078 | 0.169 | 0.237 | 0.158 | 0.167 |
| 16 | `all` | `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.50` | 0.079 | 0.155 | 0.212 | 0.145 | 0.153 |
| 17 | `all` | `promptreps_2-3-1_dense_sparse_alpha0.50` | 0.077 | 0.149 | 0.202 | 0.140 | 0.146 |
| 18 | `all` | `promptreps_2-3-2_query_dense_sparse_alpha0.50` | 0.076 | 0.139 | 0.195 | 0.134 | 0.139 |
| 19 | `all` | `promptreps_2-5_dense_sparse_alpha0.50` | 0.066 | 0.133 | 0.191 | 0.129 | 0.135 |
| 20 | `all` | `promptreps_2-1_dense_sparse_alpha0.50` | 0.071 | 0.140 | 0.190 | 0.131 | 0.140 |
| 21 | `all` | `promptreps_2-1_dense_sparse_alpha0.25` | 0.066 | 0.125 | 0.168 | 0.117 | 0.123 |
| 22 | `all` | `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.25` | 0.063 | 0.124 | 0.165 | 0.115 | 0.121 |
| 23 | `all` | `promptreps_2-3-1_dense_sparse_alpha0.25` | 0.062 | 0.117 | 0.163 | 0.113 | 0.116 |
| 24 | `all` | `promptreps_2-3-2_query_dense_sparse_alpha0.25` | 0.057 | 0.119 | 0.145 | 0.103 | 0.110 |
| 25 | `all` | `promptreps_2-5_dense_sparse_alpha0.25` | 0.054 | 0.108 | 0.138 | 0.098 | 0.106 |
| 26 | `all` | `promptreps_2-1_sparse_only` | 0.047 | 0.090 | 0.117 | 0.084 | 0.089 |
| 27 | `all` | `promptreps_k3_key_assoc_topic_sparse_zsum` | 0.043 | 0.082 | 0.107 | 0.077 | 0.081 |
| 28 | `all` | `promptreps_2-3-1_sparse_only` | 0.046 | 0.083 | 0.105 | 0.077 | 0.081 |
| 29 | `all` | `promptreps_2-3-2_query_sparse_only` | 0.041 | 0.078 | 0.104 | 0.073 | 0.077 |
| 30 | `all` | `promptreps_2-5_sparse_only` | 0.036 | 0.079 | 0.101 | 0.070 | 0.073 |

## Configs

- `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.90`: Winning dense K3 vector-average fused with K3 PromptReps sparse z-sum; alpha weights dense (dense_sparse_zfusion)
- `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.80`: Winning dense K3 vector-average fused with K3 PromptReps sparse z-sum; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-1_dense_sparse_alpha0.90`: Same-prompt dense/sparse PromptReps fusion for 2-3-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-5_dense_sparse_alpha0.90`: Same-prompt dense/sparse PromptReps fusion for 2-5; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-2_query_dense_sparse_alpha0.90`: Same-prompt dense/sparse PromptReps fusion for 2-3-2_query; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-1_dense_sparse_alpha0.80`: Same-prompt dense/sparse PromptReps fusion for 2-3-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.70`: Winning dense K3 vector-average fused with K3 PromptReps sparse z-sum; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-5_dense_sparse_alpha0.80`: Same-prompt dense/sparse PromptReps fusion for 2-5; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-2_query_dense_sparse_alpha0.80`: Same-prompt dense/sparse PromptReps fusion for 2-3-2_query; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-1_dense_sparse_alpha0.90`: Same-prompt dense/sparse PromptReps fusion for 2-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-1_dense_sparse_alpha0.70`: Same-prompt dense/sparse PromptReps fusion for 2-3-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-5_dense_sparse_alpha0.70`: Same-prompt dense/sparse PromptReps fusion for 2-5; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-2_query_dense_sparse_alpha0.70`: Same-prompt dense/sparse PromptReps fusion for 2-3-2_query; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-1_dense_sparse_alpha0.80`: Same-prompt dense/sparse PromptReps fusion for 2-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-1_dense_sparse_alpha0.70`: Same-prompt dense/sparse PromptReps fusion for 2-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.50`: Winning dense K3 vector-average fused with K3 PromptReps sparse z-sum; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-1_dense_sparse_alpha0.50`: Same-prompt dense/sparse PromptReps fusion for 2-3-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-2_query_dense_sparse_alpha0.50`: Same-prompt dense/sparse PromptReps fusion for 2-3-2_query; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-5_dense_sparse_alpha0.50`: Same-prompt dense/sparse PromptReps fusion for 2-5; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-1_dense_sparse_alpha0.50`: Same-prompt dense/sparse PromptReps fusion for 2-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-1_dense_sparse_alpha0.25`: Same-prompt dense/sparse PromptReps fusion for 2-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.25`: Winning dense K3 vector-average fused with K3 PromptReps sparse z-sum; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-1_dense_sparse_alpha0.25`: Same-prompt dense/sparse PromptReps fusion for 2-3-1; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-3-2_query_dense_sparse_alpha0.25`: Same-prompt dense/sparse PromptReps fusion for 2-3-2_query; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-5_dense_sparse_alpha0.25`: Same-prompt dense/sparse PromptReps fusion for 2-5; alpha weights dense (dense_sparse_zfusion)
- `promptreps_2-1_sparse_only`: PromptReps sparse-only score for 2-1 (sparse_dot)
- `promptreps_k3_key_assoc_topic_sparse_zsum`: PromptReps sparse z-sum for the winning K3 key+association+topic variants (sparse_zsum)
- `promptreps_2-3-1_sparse_only`: PromptReps sparse-only score for 2-3-1 (sparse_dot)
- `promptreps_2-3-2_query_sparse_only`: PromptReps sparse-only score for 2-3-2_query (sparse_dot)
- `promptreps_2-5_sparse_only`: PromptReps sparse-only score for 2-5 (sparse_dot)
