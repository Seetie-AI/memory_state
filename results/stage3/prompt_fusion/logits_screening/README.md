# Stage 3 Step 2: PromptReps-Style Logits Screening

This folder contains the Stage 3 step 2 logits-screening experiments.

## Method

- Input store: `tensors/stage3/prompt_sweep/merged_subset0-100_cache2gb_logits256`
- No model rerun; this is an offline approximation.
- For each row, saved top-256 next-token logits are intersected with token ids
  from the original text.
- Sparse impact weight: `log1p(relu(logit))`.
- Main shortlist tests:
  - logits top20
  - BM25 top20
  - logits top20 union BM25 top20
  - logits/BM25 fused top20
  - hidden top20 reference
- Main rerank tests:
  - `0.50 * z(hidden concat) + 0.25 * z(BM25) + 0.25 * z(logits)`
  - logits only
  - `0.75 * z(hidden concat) + 0.25 * z(BM25)` reference

## Finding

The offline PromptReps approximation is too lossy with only saved top-256
logits. After filtering to original text tokens, each row keeps only about
1-2 logits tokens on average, so logits-only screening has low oracle recall.

Best logits/BM25 screening row:

| logit source | screen | score | R@5 | NDCG@5 | MRR |
|---|---|---|---:|---:|---:|
| `2-3-2_mem` | logits top20 union BM25 top20 | 0.50 hidden + 0.25 BM25 + 0.25 logits | 0.702 | 0.729 | 0.742 |

Best hidden-top20 reference with the same PromptReps-style logits score:

| logit source | screen | score | R@5 | NDCG@5 | MRR |
|---|---|---|---:|---:|---:|
| `2-5` | hidden top20 | 0.50 hidden + 0.25 BM25 + 0.25 logits | 0.777 | 0.816 | 0.848 |

No-logits hidden-top20 reference:

| screen | score | R@5 | NDCG@5 | MRR |
|---|---|---:|---:|---:|
| hidden top20 | 0.75 hidden + 0.25 BM25 | 0.766 | 0.826 | 0.853 |

Current implication: do not use approximate PromptReps logits as first-stage
screening. If this direction is worth pursuing, rerun encoding and extract
full-vocab logits for original text tokens online, instead of relying on saved
global top-256 logits.
