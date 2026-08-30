# PrefEval n=1000 Stage 1 Findings

This note tracks offline analysis over the PrefEval implicit_persona n=1000
run. The benchmark is separate from the LongMemEval Stage 1-3 line, so
conclusions are recorded here instead of in `notes/results_log.md`.

## Setup

- Data: `benchmarks/PrefEval/data/implicit_persona_n1000_pruned_hidden_l28_l29_l30_l31_logits256_promptreps128_20260512.jsonl`
- Tensor store: `benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128/`
- Stored vectors are raw extractor outputs. The original n=1000 prompt-sweep
  results applied `anti_pca_both_k15` and L2-normalized cosine at scoring time.
- PrefEval Stage 1 is an offline analysis stage: no 9B hidden encoding should
  run unless explicitly approved.

## Current Headline

Best current PrefEval Stage 1 row:

| Config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| `bm25_k3_key_assoc_topic_vector_average_full_alpha0.80` | 0.114 | 0.258 | **0.356** | **0.237** | 0.225 |

Compared with baselines:

| Method | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| BM25 | 0.035 | 0.074 | 0.094 | 0.066 | 0.067 |
| Qwen3-Embedding-8B | 0.093 | 0.216 | 0.281 | 0.191 | 0.200 |
| Best single hidden prompt (`2-3-1_L30_both_k15`) | 0.110 | 0.254 | 0.311 | 0.218 | 0.214 |
| Best dense K3 | 0.124 | 0.263 | 0.339 | 0.235 | 0.231 |
| Best K3 + PromptReps | 0.116 | 0.256 | 0.347 | 0.233 | 0.226 |
| Best K3 + BM25 | 0.114 | 0.258 | **0.356** | **0.237** | 0.225 |

Interpretation: PrefEval Stage 1 mostly rewards prompt diversity plus a light
lexical signal. The strongest dense representation is `2-3-1 + 2-5 + 2-1`;
BM25 currently beats PromptReps as the auxiliary signal.

## Anti-PCA Calibration

Result files:

- `benchmarks/PrefEval/results/prefeval_stage1/anti_pca_calibration_20260512.json`
- `benchmarks/PrefEval/results/prefeval_stage1/anti_pca_calibration_20260512.md`

The stored tensor cache contains raw extractor outputs. The original n=1000
prompt-sweep table was not raw cosine: it applied `anti_pca_both_k15` and
L2-normalized cosine at scoring time. This calibration compares that default
against raw cosine, centered cosine, alternate anti-PCA strengths, query-only
anti-PCA, and a candidate-only sanity check.

Best per prompt by R@5:

| Prompt/layer | Best transform | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---|---:|---:|---:|---:|---:|
| `2-3-1_L30` | `anti_pca_both_k15` | 0.110 | 0.254 | 0.311 | 0.218 | 0.214 |
| `2-3-2_query_L30` | `anti_pca_both_k15` | 0.097 | 0.241 | 0.310 | 0.208 | 0.198 |
| `2-1_L30` | `anti_pca_both_k5` | 0.097 | 0.215 | 0.305 | 0.203 | 0.201 |
| `2-5_L29` | `anti_pca_both_k15` | 0.096 | 0.233 | 0.301 | 0.204 | 0.199 |

Findings:

- `anti_pca_both_k15` remains the best dense single-prompt setting for
  `2-3-1`, `2-3-2_query`, and `2-5`. PrefEval does not currently justify
  replacing the default k for the main retrieval-key prompts.
- `2-1` prefers a lighter transform (`both_k5`/`both_k10`) over `both_k15`,
  which fits the earlier concern that the topic prompt behaves differently from
  the retrieval-key prompts.
- Raw cosine is usable but consistently lower than tuned anti-PCA. For
  `2-3-1_L30`, raw R@5 is 0.278 vs 0.311 for `both_k15`.
- Query-only anti-PCA is close only for `2-3-1` (`query_only_k15` R@5=0.309)
  but materially weaker for `2-3-2_query`, `2-5`, and `2-1`. Unlike
  LongMemEval, PrefEval Stage 1 should keep both-sided anti-PCA as the dense
  default unless later K3 fusion overturns this.
- Candidate-only anti-PCA remains bad across prompts, confirming the
  LongMemEval failure mode transfers to PrefEval.

## Dense K3 Fusion

Result files:

- `benchmarks/PrefEval/results/prefeval_stage1/dense_k3_20260512.json`
- `benchmarks/PrefEval/results/prefeval_stage1/dense_k3_20260512.md`

K3 candidates were selected from the Stage 1 discussion:

- `k3_key_query_assoc`: `2-3-1_L30_both_k15 + 2-3-2_query_L30_both_k15 + 2-5_L29_both_k15`
- `k3_key_assoc_topic`: `2-3-1_L30_both_k15 + 2-5_L29_both_k15 + 2-1_L30_both_k5`
- `k3_key_assoc_summary`: `2-3-1_L30_both_k15 + 2-5_L29_both_k15 + 1-2_L30_both_k15`
- `k3_longmemeval_legacy`: `2-4-1_user_word_L30_both_k15 + 1-3_L31_both_k15 + 2-5_L29_query_only_k2`

Best full-split dense K3 rows:

| Config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| `k3_key_assoc_topic_vector_average_component_norm` | 0.124 | 0.263 | 0.339 | 0.235 | 0.231 |
| `k3_key_assoc_topic_zsum` | 0.117 | 0.254 | 0.327 | 0.226 | 0.224 |
| `k3_key_assoc_topic_vertical_concat_norm_weighted` | 0.112 | 0.251 | 0.327 | 0.223 | 0.222 |
| `k3_key_assoc_summary_zsum` | 0.103 | 0.246 | 0.320 | 0.217 | 0.210 |
| `k3_key_query_assoc_vector_average_component_norm` | 0.113 | 0.257 | 0.316 | 0.222 | 0.220 |
| `k3_longmemeval_legacy_vector_average_component_norm` | 0.093 | 0.212 | 0.299 | 0.197 | 0.188 |

Findings:

- Dense K3 improves over the best single prompt (`2-3-1_L30_both_k15`,
  R@5=0.311) to R@5=0.339. The best row uses component-normalized vector
  average, not vertical concat.
- The best K3 is `key + association + topic`. This validates keeping the topic
  prompt as a complementary product-relevant facet even though it was not the
  best single prompt at n=1000.
- The first/second half split is directionally stable for the winning K3:
  R@5=0.314 on first500 and 0.364 on second500. The absolute second-half lift
  suggests the full-set value may still move with dataset composition, but the
  ranking over tested K3 candidates is stable.
- Oracle union diagnostics show real complementarity. `k3_key_assoc_topic`
  has any-hit@5=0.425 vs best component any-hit@5=0.312, a +0.113 oracle
  headroom with mean pairwise Jaccard@5=0.381.
- The LongMemEval legacy K3 transfers poorly to PrefEval (best R@5=0.299),
  confirming that PrefEval needs preference/query-oriented prompt selection
  rather than the evidence-retrieval K3 from Stage 3.

## PromptReps Logit Fusion

Result files:

- `benchmarks/PrefEval/results/prefeval_stage1/promptreps_20260512.json`
- `benchmarks/PrefEval/results/prefeval_stage1/promptreps_20260512.md`

PromptReps sparse scores use the text-token-filtered top128 logits saved during
the n=1000 run. The current tensor store uses `floor(value*100)` quantization;
the PromptReps reference code uses rounding, so this is a close recipe but not
byte-identical.

Best rows:

| Config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.90` | 0.116 | 0.256 | 0.347 | 0.233 | 0.226 |
| `promptreps_k3_key_assoc_topic_dense_sparse_alpha0.80` | 0.112 | 0.236 | 0.332 | 0.222 | 0.217 |
| `promptreps_2-3-1_dense_sparse_alpha0.90` | 0.106 | 0.241 | 0.318 | 0.216 | 0.209 |
| `promptreps_2-5_dense_sparse_alpha0.90` | 0.099 | 0.228 | 0.315 | 0.210 | 0.202 |
| `promptreps_2-1_sparse_only` | 0.047 | 0.090 | 0.117 | 0.084 | 0.089 |

Findings:

- Sparse-only PromptReps is weak on PrefEval, only slightly above BM25. It is
  not a standalone retriever in this setup.
- Dense+sparse hybrid helps only when dense dominates. The best K3 hybrid uses
  alpha=0.90 and improves R@5 from the dense K3 best 0.339 to 0.347, while
  NDCG@5 slightly decreases from 0.235 to 0.233.
- The best single-prompt hybrid (`2-3-1`, alpha=0.90) improves R@5 from 0.311
  to 0.318, again a small recall-side gain rather than a ranking breakthrough.
- Treat PromptReps as a weak auxiliary recall signal for now. It is not the
  main Stage 1 lever unless a later BM25/PromptReps combined fusion shows
  stronger complementarity.

## BM25 Fusion

Result files:

- `benchmarks/PrefEval/results/prefeval_stage1/bm25_fusion_20260512.json`
- `benchmarks/PrefEval/results/prefeval_stage1/bm25_fusion_20260512.md`

BM25 fusion uses alpha values from 0.70 to 0.90 in 0.05 increments. Alpha
weights the dense score. Two scopes were tested:

- `full`: fuse dense and BM25 over all candidates.
- `vector_top20`: keep dense top20, fuse only inside that shortlist, then
  append the rest by dense rank.

Best rows:

| Config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| `bm25_k3_key_assoc_topic_vector_average_full_alpha0.80` | 0.114 | 0.258 | 0.356 | 0.237 | 0.225 |
| `bm25_k3_key_assoc_topic_vector_average_full_alpha0.85` | 0.116 | 0.255 | 0.352 | 0.236 | 0.226 |
| `bm25_k3_key_assoc_topic_vector_average_full_alpha0.90` | 0.120 | 0.260 | 0.350 | 0.237 | 0.229 |
| `bm25_k3_key_assoc_topic_vector_average_top20_alpha0.85` | 0.120 | 0.261 | 0.346 | 0.237 | 0.230 |
| `bm25_single_2-3-1_full_alpha0.85` | 0.105 | 0.246 | 0.319 | 0.217 | 0.210 |

Findings:

- BM25 is the strongest auxiliary signal so far. K3 dense R@5=0.339 improves
  to 0.356 with full BM25 fusion at alpha=0.80.
- The best full-scope row improves recall more than PromptReps hybrid
  (0.356 vs 0.347 R@5). PromptReps remains a secondary auxiliary signal.
- `vector_top20` is safer and has similar NDCG/MRR, but full fusion gives the
  best R@5 on PrefEval Stage 1. This differs from LongMemEval Stage 3, where
  shortlist fusion was the cleaner default.
- Single-prompt BM25 fusion improves `2-3-1` only modestly (best R@5=0.319 vs
  0.311), so most of the gain comes from combining BM25 with the stronger K3
  dense base.

## Split Stability

The dense K3 phase evaluates all tested K3 configs on first500 and second500.
The winning dense K3 (`key + association + topic`, component-normalized vector
average) is stable directionally:

| Split | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| first500 | 0.136 | 0.256 | 0.314 | 0.230 | 0.235 |
| second500 | 0.112 | 0.270 | 0.364 | 0.241 | 0.228 |
| all | 0.124 | 0.263 | 0.339 | 0.235 | 0.231 |

The same K3 also wins the oracle union diagnostic on both halves:

| Split | any_hit@5 | best_component_any@5 | gain | mean_jaccard@5 |
|---|---:|---:|---:|---:|
| first500 | 0.400 | 0.300 | +0.100 | 0.381 |
| second500 | 0.450 | 0.330 | +0.120 | 0.380 |
| all | 0.425 | 0.312 | +0.113 | 0.381 |

## Layer Overlap Diagnostic

Result files:

- `benchmarks/PrefEval/results/prefeval_stage1/layer_overlap_20260512.json`
- `benchmarks/PrefEval/results/prefeval_stage1/layer_overlap_20260512.md`

Fixed prompt: `2-3-1`, transform: `anti_pca_both_k15`.

| Layer set | z-sum R@1 | z-sum R@3 | z-sum R@5 | Oracle any@5 | Gain vs best layer | Jaccard@5 |
|---|---:|---:|---:|---:|---:|---:|
| L29+L30 | 0.111 | 0.245 | 0.311 | 0.327 | +0.015 | 0.815 |
| L28+L29+L30 | 0.107 | 0.243 | 0.306 | 0.337 | +0.025 | 0.790 |
| L28+L29+L30+L31 | 0.107 | 0.248 | 0.307 | 0.357 | +0.045 | 0.689 |

Findings:

- Adjacent useful layers are highly overlapping. L29+L30 Jaccard@5 is 0.815
  and z-sum does not improve over best single layer.
- Adding L31 increases oracle union headroom but lowers realized z-sum quality,
  so the extra layer is probably adding noisy alternate candidates rather than
  a directly useful scoring signal.
- Cross-layer fusion is not a priority for PrefEval Stage 1. Prompt diversity
  is a better use of extra vectors than same-prompt layer diversity.
