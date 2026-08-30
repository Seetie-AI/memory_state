# Stage 3 Step 3: BM25 Fusion and Second-Stage Rerank

This folder isolates the BM25 and second-stage rerank work from the earlier
prompt-vector fusion experiments.

## Scope

- Base vector config: `concat_k3_norm_weighted_userword_tag_assoc`
  - `2-4-1_user_word|L30|anti_pca_both_k15`
  - `1-3|L31|anti_pca_both_k15`
  - `2-5|L29|query_only_anti_pca_k2`
- Dataset: saved Stage 3 subset `0-100`, `94` scored questions.
- BM25 is treated as a score/source overlay, not as prompt-vector fusion.

## Artifacts

- `bm25_sweeps/`: BM25 score fusion over existing vector configs.
- `union_shortlist/`: top20 source-union and source-overlap analysis.
- `second_stage/`: agreement-filter and Qwen3-Embedding-8B second-stage tests.

Main scripts:

- `scripts/stage3_prompt_fusion_bm25_sweep.py`
- `scripts/tmp_union_top20_prompt_bm25_fusion.py`
- `scripts/tmp_agreement_second_stage_rerank.py`
- `scripts/tmp_qwen3_second_stage_rerank.py`

## BM25 Fusion Findings

## Current Product Default

Use the K=3 prompt-vector concat retriever with a light BM25 rerank inside the
vector top20 shortlist.

Stored vector config:

| component | variant | layer | transform | role |
|---:|---|---:|---|---|
| 1 | `2-4-1_user_word` | 30 | `anti_pca_both_k15` | product/user wording |
| 2 | `1-3` | 31 | `anti_pca_both_k15` | tag / marker prompt |
| 3 | `2-5` | 29 | `query_only_anti_pca_k2` | association prompt |

Vector scorer:

- scorer: `vertical_concat_norm_weighted`
- per component: apply that component's transform first
- concat: concatenate the three 4096-d vectors into one 12288-d vector
- similarity: L2-normalized cosine over the concatenated vector
- storage: bf16 K=3, about 24 KB per memory page

Retrieval/rerank:

1. score all memory pages with concat cosine
2. keep `vector_top20`
3. compute BM25 only inside that top20 shortlist
4. rerank by `0.75 * z(concat_score) + 0.25 * z(BM25_score)`
5. return top5; append the rest by vector rank only if a full ranking is needed

Metrics on Stage 3 subset 0-100:

| config | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|
| product default: concat K3 + BM25 `vector_top20`, alpha=0.75 | 0.766 | 0.826 | 0.853 |
| close alternative: concat K3 + BM25 `vector_top50`, alpha=0.75 | 0.766 | 0.824 | 0.856 |

Do not include Qwen3-Embedding-8B in the product default. It improves NDCG/MRR
as a research reranker, but it requires running and storing another embedding
model for only a small product-experience gain and no R@5 improvement here.

Best BM25 overlays on the K=3 concat vector:

| config | R@5 | NDCG@5 | MRR | note |
|---|---:|---:|---:|---|
| concat K3 + BM25 `vector_top20`, alpha=0.75 | 0.766 | 0.826 | 0.853 | best NDCG among simple BM25 overlays |
| concat K3 + BM25 `vector_top50`, alpha=0.75 | 0.766 | 0.824 | 0.856 | best MRR among simple BM25 overlays |
| concat K3 + BM25 `full`, alpha=0.65 | 0.777 | 0.810 | 0.834 | best R@5 balanced full-scope row |
| concat K3 vector-only | 0.766 | 0.806 | 0.839 | baseline for BM25 overlay |

BM25 improves ranking quality more than raw recall. It is useful as a lexical
tie-breaker, but too much BM25 weight hurts.

## Source Union Findings

Candidate set:

- top20 from `2-4-1_user_word`
- top20 from `1-3`
- top20 from `2-5`
- top20 from BM25

Summary:

| candidate rule | avg candidates | oracle recall_all |
|---|---:|---:|
| any source, source_count >= 1 | 49.8 | 0.968 |
| agreement filter, source_count >= 2 | 17.4 | 0.915 |
| source_count >= 3 | 9.5 | 0.862 |
| source_count >= 4 | 3.3 | 0.660 |

Gold coverage by number of sources:

| source count | questions | fraction |
|---:|---:|---:|
| 0 | 4 | 0.043 |
| 1 | 4 | 0.043 |
| 2 | 6 | 0.064 |
| 3 | 18 | 0.191 |
| 4 | 62 | 0.660 |

Agreement is a good shortlist filter: gold candidates are much more likely to
appear in 3-4 sources than non-gold candidates. However, using source_count as
the primary sort key hurts; source_count should filter, not dominate ranking.

## Agreement Second Stage

Keeping `source_count >= 2` and reranking with concat+BM25:

| strategy | avg candidates | oracle | best R@5 | best NDCG@5 | best MRR |
|---|---:|---:|---:|---:|---:|
| 3 prompts top20 + BM25 top20 | 17.4 | 0.915 | 0.777 | 0.819 | 0.854 |
| concat top20 + BM25 top20 | 5.1 | 0.670 | 0.660 | 0.713 | 0.742 |
| concat top50 + BM25 top50 | 14.8 | 0.723 | 0.702 | 0.743 | 0.780 |

Important conclusion: do not collapse the three prompt sources into concat
before source agreement. The individual prompt sources preserve useful
diversity that concat+BMM25 two-source agreement loses.

## Qwen3-Embedding-8B Second Stage

Existing Qwen3-Embedding-8B subset `0-100` tensors were reused; no re-encoding.

Two tests:

1. Qwen3 as a rerank score only, over the existing `source_count >= 2` shortlist.
2. Qwen3 top20 as a fifth source, then `source_count >= 2`.

Oracle impact:

| source set | avg candidates at source>=2 | oracle recall_all |
|---|---:|---:|
| 3 prompts + BM25 | 17.4 | 0.915 |
| 3 prompts + BM25 + Qwen3 top20 | 21.4 | 0.957 |

Best Qwen3 rerank rows:

| setup | base alpha | base weight | qwen weight | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3 score only, not source | 0.75 | 0.50 | 0.50 | 0.766 | 0.834 | 0.888 |
| Qwen3 as fifth source + score | 0.75 | 0.50 | 0.50 | 0.766 | 0.834 | 0.888 |
| Qwen3 as fifth source + light score | 0.75 | 0.75 | 0.25 | 0.766 | 0.833 | 0.869 |

Qwen3 improves ranking quality (NDCG/MRR) substantially, but does not improve
R@5 in this small subset. Adding Qwen3 as a fifth source improves oracle
coverage, but the current score fusion still does not fully exploit that extra
coverage.

## Current Recommendation

- Product default: `concat K3 + BM25 vector_top20 alpha=0.75`.
- Product alternative if MRR is preferred over NDCG: `vector_top50 alpha=0.75`.
- Keep Qwen3-Embedding-8B as research-only for now. It is not worth the extra
  product/device cost given the small gain and unchanged R@5.
- If pursuing further gains, the next likely bottleneck is evidence judgment,
  not vector fusion. A pointwise LLM evidence judge over the 17-21 candidate
  shortlist is the next high-upside experiment.
