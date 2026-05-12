# Stage 3 Findings: Prompt Sweep, Prompt Fusion, and BM25 Fusion

Date: 2026-05-11  
Dataset: LongMemEval-S cleaned subset 0-100, 94 scored questions.  
Vector store:
`tensors/stage3/prompt_sweep/merged_subset0-100_cache2gb_logits256/`.

This note supersedes:

- `notes/stage_3_prompt_sweep_observations_tmp.md` (A 0-39 only)
- the deleted `notes/stage_3_step_2_prompt_fusion_findings.md`

It records the Stage 3 "what works / what does not" conclusions and points to
the result files that produced them.

## Executive Summary

Stage 3 validates the core idea: Qwen hidden states can be turned into strong
memory retrieval vectors by choosing retrieval-oriented prompts, lightweight
geometry, and a small lexical rerank signal.

| Product candidate | Storage/page | R@5 | NDCG@5 | MRR | Notes |
|---|---:|---:|---:|---:|---|
| **Current SOTA / product default**: all-L31 concat K=3 + BM25 top20 alpha=0.75 | 24 KB | **0.777** | 0.822 | 0.851 | cleanest product-facing default; same layer and same transform across prompts |
| **Mixed-layer ranking alternative**: concat K=3 + BM25 top20 alpha=0.75 | 24 KB | 0.766 | **0.826** | 0.853 | tiny NDCG upside, but more same-set selection / overturn risk |
| **Close MRR alternative**: concat K=3 + BM25 top50 alpha=0.75 | 24 KB | 0.766 | 0.824 | **0.856** | slightly better MRR, larger rerank set |
| **Balanced, tuned**: concat K=3 + BM25 full alpha=0.65 | 24 KB | **0.777** | 0.810 | 0.834 | same-set alpha tuning; useful hypothesis, not a clean held-out estimate |
| **Compact**: avg K=2 component-normalized L30 | **8 KB** | **0.777** | 0.788 | 0.820 | single-vector page; no BM25 dependency |
| Single prompt best NDCG: `1-3` L31 both-k15 | 8 KB | 0.755 | 0.784 | 0.805 | best single prompt ranking |
| Qwen3-Embedding-8B-4bit-DWQ | model baseline | 0.755 | 0.789 | 0.826 | local embedding baseline |

The current SOTA / product default beats the local 8B embedding baseline on R@5, NDCG@5, and
MRR on this subset. The absolute differences are still within a small
94-question eval, so treat the result as a strong direction, not a held-out
claim.

## Current Product Default Config

Use the K=3 prompt-vector concat retriever with a light BM25 rerank inside the
vector top20 shortlist.

Stored vector components:

| component | variant | layer | transform | role |
|---:|---|---:|---|---|
| 1 | `2-4-1_user_word` | 31 | `anti_pca_both_k15` | product/user wording |
| 2 | `1-3` | 31 | `anti_pca_both_k15` | tag / marker prompt |
| 3 | `2-5` | 31 | `anti_pca_both_k15` | association prompt |

Scoring:

- vector scorer: `vertical_concat_norm_weighted`
- per component: apply `anti_pca_both_k15` first
- concat: concatenate the three 4096-d vectors into one 12288-d vector
- similarity: L2-normalized cosine over the concatenated vector
- storage: bf16 K=3, about 24 KB per memory page

Rerank:

1. score all memory pages with concat cosine
2. keep `vector_top20`
3. compute BM25 only inside that top20 shortlist
4. rerank by `0.75 * z(concat_score) + 0.25 * z(BM25_score)`
5. return top5; append the rest by vector rank only if a full ranking is needed

Stage 3 subset 0-100 metrics: R@5=0.777, NDCG@5=0.822, MRR=0.851.

The earlier mixed-layer version (`2-4-1_user_word` L30 both-k15, `1-3` L31
both-k15, `2-5` L29 query-only k2) reaches slightly higher ranking metrics
in some BM25 shortlist runs, up to NDCG@5=0.826 / MRR=0.856. Treat that as
remaining headroom rather than the default: it chooses different layers and
transforms per prompt on the same 94 scored questions, so it has higher
same-set selection and overturn risk.

Qwen3-Embedding-8B is not part of the product default. It improves NDCG/MRR as
a research reranker, but requires running another embedding model and did not
improve R@5 on this subset.

## Step 1: Single-Prompt Sweep

### Headline

| System | R@5 | NDCG@5 | session_hit@5 | Note |
|---|---:|---:|---:|---|
| **Stage 3 hidden best R@5** | **0.766** | 0.757 | 0.979 | `2-3-2_mem|L31|both_k15` and `2-4-1_user_word|L30|both_k15` |
| **Stage 3 hidden best NDCG@5** | 0.755 | **0.784** | **1.000** | `1-3|L31|both_k15` (the `标记` tag prompt) |
| Stage 2 P0 anchor reproduced | 0.755 | 0.779 | 0.989 | `P0|L30|both_k15` |
| Qwen3-Embedding-8B-4bit-DWQ | 0.755 | 0.789 | - | `results/stage3/embedding_eval/` |
| Qwen3-Embedding-0.6B historic | 0.766 | 0.809 | - | `results/stage1/phase1a_qwen_embedding_longmemeval_s_cleaned_round_100.json` |

Hidden-state retrieval is at embedding-baseline scale without training an
embedding model. Confidence intervals overlap; this is parity-level evidence,
not a statistically significant win.

### What Works

- **`anti_pca_both_k15` dominates**: it wins R@5 for 13 of 17 symmetric prompt
  variants. Query-only anti-PCA wins 3 variants; centered cosine wins only
  `1-1_CN`.
- **There is no universal best layer**: L29/L30/L31 win 6/6/5 variants. Layer
  choice depends on prompt semantics.
- **Two prompt families matter most**:
  - `2-3-2_mem` ("what should be saved to memory") is the recall-oriented
    winner.
  - `1-3` ("标记" tag prompt) is the ranking-oriented winner.
- **Product-native wording matters**: `2-4-1_user_word` (using "用户") beats
  `2-4-1` (using "对方") by 0.043 R@5. The model appears better aligned to
  product vocabulary than neutral wording.

### What Does Not Work

- **`2-8` answer-strategy prompt collapses**: R@5=0.574, NDCG@5=0.510.
- **English summary prompt is weaker than Chinese**: `1-1_EN` R@5=0.713 vs
  `1-1_CN` R@5=0.755.
- **Asymmetric `2-3-2_mem -> 2-3-2_query` does not beat symmetric memory-key
  encoding**: best R@5=0.755 vs `2-3-2_mem` symmetric R@5=0.766.
- **Early A0-39 observations were subset-biased**: `2-1` looked like a clear
  leader on A only, but fell to the middle of the full-100 leaderboard.

### Per-Variant Snapshot

Each row uses the variant's best layer and score mode.

| Variant | Best layer | Score mode | R@5 | NDCG@5 | session_hit@5 |
|---|---:|---|---:|---:|---:|
| 2-3-2_mem | 31 | both_k15 | 0.766 | 0.757 | 0.979 |
| 2-4-1_user_word | 30 | both_k15 | 0.766 | 0.751 | 0.979 |
| 1-3 | 31 | both_k15 | 0.755 | 0.784 | 1.000 |
| P0 | 30 | both_k15 | 0.755 | 0.779 | 0.989 |
| 1-1_CN | 29 | centered_cosine | 0.755 | 0.756 | 0.979 |
| 2-3-2_query | 29 | both_k15 | 0.745 | 0.764 | 0.989 |
| 2-5 | 29 | qpca_k2 | 0.723 | 0.747 | 0.968 |
| 2-7 | 31 | both_k15 | 0.702 | 0.672 | 0.968 |
| **2-8** | 31 | both_k15 | **0.574** | 0.510 | 0.915 |

Note: the all-L31 product default does not mean every component is individually
best at L31. `2-4-1_user_word|L31|both_k15` alone reaches only
R@5=0.723 / NDCG@5=0.728, below its L30 single-cell result. The all-L31 choice
is justified by the fused concat+BM25 result and by product simplicity, not by
per-prompt single-cell optimality.

Full table: `results/stage3/offline_prompt_sweep/merged_subset0-100_hidden_only.md`.

## Step 2: Prompt-Vector Fusion

Stage 3 Step 2 tested whether multiple saved prompt views improve retrieval
without rerunning the model.

### Complementarity

Single prompts are correlated, but a few pairs make different mistakes.
`phase1_union_r3_combo_sweep` is an oracle diagnostic: it uses gold labels to
find prompt pairs with complementary top-3 hits, so any downstream pair selected
from it has same-set overfit risk.

Best oracle union@3 pairs:

| Pair | Union@3 | Gain | Interpretation |
|---|---:|---:|---|
| `2-3-2_query + 2-4-1` | 0.745 | 0.074 | highest oracle complementarity; high-risk |
| `2-4-1_user_word + 2-5` | 0.745 | 0.053 | strong user wording + association |
| `1-3 + 2-5` | 0.745 | 0.043 | ranking prompt + association |

### Fusion Results

| Method | Combo | Storage | R@5 | NDCG@5 | MRR | Takeaway |
|---|---|---:|---:|---:|---:|---|
| `vertical_concat_norm_weighted` | `2-4-1_user_word + 1-3 + 2-5` | 3x4096 | 0.766 | **0.806** | 0.839 | best vector-only quality |
| `zsum` score fusion | same K=3 | 3 score passes | 0.777 | 0.789 | 0.815 | useful upper bound; not a stored vector |
| `vertical_concat_component_norm` | same K=3 | 3x4096 | 0.766 | 0.786 | 0.816 | cleaner equal-weight ablation, weaker here |
| `vector_average_component_norm_uniform_l30` | `2-4-1_user_word + 1-3` | 1x4096 | **0.777** | 0.788 | 0.820 | compact product candidate |
| `vector_average_norm_weighted` | `2-3-2_query + 2-4-1` | 1x4096 | **0.787** | 0.786 | 0.823 | oracle-selected; do not headline |
| `maxsim_sum` / late interaction | varies | K vectors | <=0.766 | <=0.789 | <=0.809 | did not justify complexity |
| `row_aligned_weighted` | K=3 selected layers | 3x4096 | 0.766 | 0.800 | 0.827 | interesting, not a winner |

### What Works

- **Raw/norm-weighted concat works better than equal component normalization**
  for the K=3 quality candidate. Component norms appear to carry useful prompt
  weighting signal on this benchmark.
- **Vector average is a strong compact representation**: K=2 averaged back to
  one 4096-d vector reaches R@5=0.777 with only 8 KB/page in bf16.
- **K=3 is not automatically better than K=2**: K=3 helps quality via concat;
  K=2 average is better for compact recall.

### What Does Not Work

- **Late interaction / max-sim was not a winner**.
- **Row-aligned profile scoring is plausible but not best**. Same-layer L30 did
  not consistently beat selected best layers.
- **Oracle-selected pairs must be treated as hypotheses**, not clean estimates.

## Step 3: BM25 Score Fusion

BM25 is a score-level lexical overlay. It is not part of the stored vector
representation. The script tests two scopes:

- `full`: vector and BM25 scores fused over the full per-instance candidate set.
- `vector_top20` / `vector_top50`: first shortlist by vector score, then fuse
  BM25 inside that shortlist and append the remaining candidates by vector rank.

### BM25 Findings

| Config | Scope | Alpha | R@5 | NDCG@5 | MRR | Interpretation |
|---|---|---:|---:|---:|---:|---|
| all-L31 concat K=3 + BM25 | vector_top20 | 0.75 | **0.777** | 0.822 | 0.851 | current SOTA / product default |
| mixed-layer concat K=3 + BM25 | vector_top20 | 0.75 | 0.766 | **0.826** | 0.853 | tiny NDCG upside, higher same-set selection risk |
| mixed-layer concat K=3 + BM25 | vector_top50 | 0.75 | 0.766 | 0.824 | **0.856** | highest MRR, larger rerank set |
| concat K=3 + BM25 | full | 0.80 | 0.766 | 0.820 | 0.853 | best full-scope NDCG |
| concat K=3 + BM25 | full | 0.65 | **0.777** | 0.810 | 0.834 | same-set tuned balanced point |
| avg K=2 | vector-only | 1.00 | **0.777** | 0.788 | 0.820 | compact clean point |
| avg K=2 + BM25 | vector_top20 | 0.75 | **0.777** | 0.791 | 0.818 | tiny NDCG gain, MRR neutral/slightly down |
| P0 + BM25 | vector_top50 | 0.75 | 0.766 | 0.791 | 0.819 | reproduces Stage 2 anchor |

### What Works

- **BM25 is useful as a small lexical vote inside a vector shortlist**.
  `vector_top20` and `vector_top50` both beat full-scope BM25 for ranking.
- **Current product default**: all-L31 concat K=3 + BM25 top20 alpha=0.75
  gives the best clean balance: R@5=0.777, NDCG@5=0.822, MRR=0.851.
- **Mixed prompt-specific layers leave small ranking headroom**: the old
  mixed-layer concat setup reaches NDCG@5 up to 0.826 / MRR up to 0.856, but
  has higher same-set overturn risk because layer and transform choices are
  tuned per prompt on this eval.
- **Stage 2 anchor is reproduced**: P0 + BM25 vector_top50 alpha=0.75 gives
  R@5=0.766 / NDCG@5=0.791, matching the historical Stage 2 result.

### What Does Not Work

- **BM25 should not dominate**. Alpha=0.25 collapses across configs because
  lexical matching is too noisy at turn level.
- **Full-scope BM25 can pull lexical false positives from the whole candidate
  set**. Shortlist fusion is safer.
- **More alpha tuning is not worth it on this same 94-question set**.
  alpha=0.75-0.85 differences are tiny and within same-set tuning noise.

## Step 4: Second-Stage Rerank Exploration

Beyond Step 3's BM25 lexical overlay, we tested heavier rerank ideas inside the
vector_top20 shortlist. These are research ceilings, not product defaults.

### Qwen3-Embedding-8B Rerank

`tmp_qwen3_second_stage_20260511.md` blends the concat+BM25 score with a
Qwen3-Embedding-8B score:

`final = base_weight * base_score + (1 - base_weight) * qwen3_score`

Best observed row on this subset:

| Strategy | Base alpha | Base weight | Qwen weight | R@5 | NDCG@5 | MRR | Note |
|---|---:|---:|---:|---:|---:|---:|---|
| `prompt3_bm25_top20` | 0.75 | 0.50 | 0.50 | 0.766 | **0.834** | **0.888** | research ranking ceiling |

This improves ranking over the current product default
(NDCG@5 0.822 / MRR 0.851), but it does not improve R@5 and it re-introduces a
separate embedding model dependency. Keep it as a ceiling / ablation, not a
default product path.

### Agreement Filtering

`tmp_agreement_second_stage_20260511.md` tests source-count agreement filtering:
keep candidates with `source_count >= 2`, then rerank with concat+BM25.

What happened:

- Source-count agreement has useful diagnostic value: gold candidates are much
  more likely than non-gold candidates to appear in multiple sources.
- But `agreement_first` sorting did not beat `score_only` on any tested alpha.
- Treat source count as a possible diagnostic or filter, not as the primary
  ranking signal.

## Product Interpretation

The current paged-memory plan is storage-feasible without quantization:
K=3 bf16 is 24 KB/page. With roughly 20k pages, this is about 500 MB.

Recommended product tiers:

| Tier | Representation | Retrieval | Storage/page | Why |
|---|---|---|---:|---|
| Current SOTA / default | concat K=3 (`2-4-1_user_word`, `1-3`, `2-5`), all L31, all both-k15 | vector top20 + BM25 alpha=0.75 | 24 KB | best clean product-facing balance |
| Mixed-layer ranking alternative | concat K=3 (`2-4-1_user_word`, `1-3`, `2-5`) with prompt-specific layers/transforms | vector top20/top50 + BM25 alpha=0.75 | 24 KB | tiny ranking upside, higher same-set overturn risk |
| Compact | avg K=2 (`2-4-1_user_word`, `1-3`) | vector-only | 8 KB | best compact recall, no lexical dependency |
| Experimental | concat K=3 | full BM25 alpha=0.65 | 24 KB | best same-set R@5/NDCG tradeoff, needs held-out validation |

Best current config, written explicitly:

1. Encode each memory page with prompts `2-4-1_user_word`, `1-3`, and `2-5`.
2. Use layer 31 and `anti_pca_both_k15` for all three prompt vectors.
3. Store the three bf16 4096-d vectors as a K=3 page representation
   (~24 KB/page).
4. At retrieval time, score pages with `vertical_concat_norm_weighted`.
5. Keep the vector top20 shortlist.
6. Rerank that shortlist with `0.75 * z(vector_score) + 0.25 * z(BM25_score)`.
7. Return top5.

## Caveats

- All Stage 3 conclusions use the same 100-instance / 94-scored subset.
  Differences of one question are not statistically meaningful.
- LongMemEval is evidence-retrieval biased. Persona / preference / style prompt
  variants may still matter in chatbot memory even when they score poorly here.
- BM25 alpha choices are same-set tuned. Prefer stable defaults (`0.75` in
  shortlist scope) over fine-grained optimum claims.
- Oracle union results use labels to select combinations and should be treated
  only as hypothesis generation.

## Result Files

Single prompt:

- `results/stage3/offline_prompt_sweep/merged_subset0-100_hidden_only.json`
- `results/stage3/offline_prompt_sweep/merged_subset0-100_hidden_only.md`

Prompt fusion:

- `results/stage3/prompt_fusion/audit_full.{json,md}`
- `results/stage3/prompt_fusion/phase1_union_r3_combo_sweep.{json,md}`
- `results/stage3/prompt_fusion/fusion_userword_tag_25_k23_v2.{json,md}`
- `results/stage3/prompt_fusion/fusion_userword_tag_25_vector_average_only.{json,md}`
- `results/stage3/prompt_fusion/fusion_query_persona_highrisk_pair_v2_20260511_162810.{json,md}`

BM25 fusion:

- `results/stage3/step3_bm25_fusion/second_stage/tmp_agreement_second_stage_20260511.{json,md}`
- `results/stage3/step3_bm25_fusion/second_stage/tmp_qwen3_embedding_bm25_top20_20260511.{json,md}`
- `results/stage3/step3_bm25_fusion/second_stage/tmp_qwen3_second_stage_20260511.{json,md}`
- `results/stage3/step3_bm25_fusion/second_stage/tmp_uniform_l29_bm25_20260511.{json,md}`
- `results/stage3/step3_bm25_fusion/second_stage/tmp_uniform_l30_bm25_20260511.{json,md}`
- `results/stage3/step3_bm25_fusion/second_stage/tmp_uniform_l31_bm25_20260511.{json,md}`
- `results/stage3/step3_bm25_fusion/second_stage/tmp_uniform_l31_top20_alpha_sweep_20260511.{json,md}`
- `results/stage3/prompt_fusion_bm25/findings_20260511_175509.{json,md}`
- `results/stage3/prompt_fusion_bm25/findings_top50_20260511_180146.{json,md}`
- `results/stage3/prompt_fusion_bm25/findings_top20_20260511_183522.{json,md}`
- `results/stage3/prompt_fusion_bm25/findings_alpha_fine_20260511_180420.{json,md}`

Scripts:

- `scripts/stage3_offline_analyze.py`
- `scripts/stage3_prompt_fusion_analyze.py`
- `scripts/stage3_prompt_fusion_oracle_union_sweep.py`
- `scripts/stage3_prompt_fusion_bm25_sweep.py`

Second-stage rerank and exploration scripts:

- `scripts/agreement_second_stage_rerank.py`
- `scripts/embedding_bm25_sweep.py`
- `scripts/qwen3_second_stage_rerank.py`
- `scripts/uniform_l30_bm25_check.py`
- `scripts/union_top20_prompt_bm25_fusion.py`
