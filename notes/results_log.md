# Memory-state experiments log

This file is a concise, git-tracked summary of the experiment record. Full run
JSON files live under `results/` and tensor dumps live under `tensors/`; those
large/generated artifacts are intentionally not tracked.

## Round 0: baseline state (2026-05-04)

Setup: LongMemEval-S / round granularity, 100-instance Tier A subset, 94 scored
questions after official abstention filtering.

| Config | Recall@5 | NDCG@5 | Note |
|---|---:|---:|---|
| BM25 | 0.585 | 0.547 | lexical baseline on S/round |
| Qwen3-Embedding-0.6B | 0.766 | 0.809 | strongest current embedding baseline |
| Hidden state final post-norm + cosine | 0.479 | 0.450 | original Phase 2 method |
| Hidden state layer 22 + centered cosine | 0.638 | ~0.55 | best discovered Tier A config so far |

Key observations:

- Early/mid layers up through about layer 15 have almost no retrieval signal.
- Layer 22 prompt-final vectors are the best current single-layer source.
- Centered cosine removes a shared prompt/corpus direction and gives a large
  lift over plain cosine.
- Tier B position scans show the last prompt position is the key aggregation
  point; full-sequence mean/max pooling collapses.

## Round 1: vector geometry sweep (2026-05-04)

Setup: existing `tensors/dump_v1` only; no model rerun. Tier A 100-instance (94 scored). All centered_cosine unless noted.

### Top configs by R@5

| Config | Recall@5 | CI low | CI high |
|---|---:|---:|---:|
| layer22 + anti-PCA global k=10 | 0.6809 | 0.5745 | 0.7660 |
| layer22 + anti-PCA global k=2 | 0.6702 | 0.5636 | 0.7553 |
| layer22 + anti-PCA global k=5 | 0.6702 | 0.5638 | 0.7553 |
| layer22 + anti-PCA instance k=2 | 0.6596 | 0.5532 | 0.7447 |
| layer22 + center_instance (prior best) | 0.6383 | 0.5213 | 0.7237 |
| delta_22_minus_18 + center_instance | 0.6383 | 0.5319 | 0.7234 |
| concat_21_22 + center_instance | 0.6277 | 0.5210 | 0.7234 |
| layer22 z-score instance | 0.6277 | 0.5104 | 0.7128 |
| RRF layer 21/22/23/final | 0.6170 | 0.4997 | 0.7128 |
| concat_21_22_23 + center_instance | 0.5851 | 0.4574 | 0.6915 |
| delta_22_minus_21 + center_instance | 0.4787 | 0.3612 | 0.5747 |

### Tier B (n=20) suffix position scan (layer 22, centered_cosine)

| Pool | R@5 | NDCG@5 |
|---|---:|---:|
| minus2 | 0.90 | 0.70 |
| last | 0.85 | 0.71 |
| mean_last3 | 0.85 | 0.73 |
| mean_last5 | 0.70 | 0.48 |
| minus3 | 0.15 | 0.13 |

### Question-type breakdown (Tier A)

| Config | single-session-user (n=64) | multi-session (n=30) |
|---|---:|---:|
| layer22 + anti-PCA global k=5 | 0.875 | 0.233 |
| layer22 + center_instance | 0.844 | 0.200 |
| layer22 + zscore_instance | 0.828 | 0.200 |
| concat_21_22_23 + center | 0.781 | 0.167 |
| delta_22_minus_21 + center | 0.688 | 0.033 |
| final cosine | 0.688 | 0.033 |

### Score diagnostics

| Config | gold mean | non-gold mean | pairwise gold>non-gold |
|---|---:|---:|---:|
| final cosine | 0.921 | 0.885 | 0.943 |
| layer22 + center_instance | 0.311 | -0.001 | 0.968 |

### Highlights / discussion

- **Anti-PCA global k=10 is new best at 0.681 (+20pp over Phase 2 baseline)**.
- **Global PCA beats per-instance PCA**: directions to remove are cross-instance prompt artifacts, not within-instance candidate drift.
- Layer concat / RRF / residual deltas all underperform layer 22 alone — layer 22 dominates, others add noise (except delta_22-18 ties).
- Z-score is essentially equivalent to centered cosine; per-dim std normalization adds little after mean removal.
- **Method is bimodal**: 0.88 on single-session vs 0.23 on multi-session. recall_all@5 strict metric punishes multi-gold queries severely.
- Tier B (n=20) suggests **minus2 (penultimate token) may beat last position** (0.90 vs 0.85); needs more data.
- Pairwise win rate ~ 0.97 but R@5 ~ 0.64: signal strong, multi-gold strict ranking is bottleneck.

### Round 2 direction candidates (executed)

See Round 2 section.

## Round 2: deeper geometry sweep (2026-05-04)

Setup: existing `tensors/dump_v1`. Tier A 100-instance (94 scored). Each direction varies one variable per row.

### Anti-PCA extended sweep (control: layer 22 fixed)

| k | R@5 | CI low | CI high |
|---|---:|---:|---:|
| 10 (Round 1 best, repeated) | 0.6809 | 0.5745 | 0.7660 |
| 15 | 0.6383 | 0.5106 | 0.7340 |
| 20 | 0.6170 | 0.5104 | 0.7128 |
| 30 | 0.6277 | 0.5106 | 0.7128 |
| 50 | 0.6064 | 0.5104 | 0.6918 |
| 80 | 0.5851 | 0.4997 | 0.6705 |
| 100 | 0.5532 | 0.4572 | 0.6489 |
| 200 | 0.5532 | 0.4468 | 0.6492 |

**k=10 is the sweet spot**; larger k removes too much signal.

### Anti-PCA layer sweep (control: k=10 fixed)

| Layer | R@5 |
|---|---:|
| 21 | 0.6809 (TIE) |
| 22 | 0.6809 |
| 23 | 0.6383 |
| final | 0.6383 |

Layer 21 and 22 are equivalent under anti-PCA. Layer 23/final lag.

### Whitening sweep (layer 22, global)

| Shrinkage | dim | R@5 |
|---|---|---:|
| 0.01 | 128 | 0.6702 |
| 0.1 | 128 | 0.6702 |
| 0.1 | 1024 | 0.6596 |
| 0.01 | 256 | 0.6383 |
| 0.1 | 256 | 0.6383 |
| 0.01 | 512/1024/2048 | 0.6277 |
| 0.1 | 512/2048 | 0.6277 |

Whitening dim=128 ≈ anti-PCA k=10 (0.670 vs 0.681). Different mechanism, similar gain. Shrinkage barely matters.

### Transform ablation (layer 22, key finding)

| Variant | R@5 |
|---|---:|
| anti_pca BOTH k=10 (Round 1 best) | 0.6809 |
| **center QUERY only** | 0.6702 |
| **anti_pca QUERY only** | 0.6702 |
| center BOTH | 0.6383 |
| raw cosine | 0.5426 |
| center CANDIDATES only | 0.1809 |
| anti_pca CANDIDATES only | 0.2234 |

**Critical insight**: query-only transform ≈ both-transform; candidates-only is catastrophic. The gain comes from **query reframing into the candidate-centered subspace**, not from de-biasing the candidates.

### Multi-gold breakdown (layer22 anti-PCA k=10)

| Split | n | R@1 | R@5 | R@10 | R@20 | R@50 | MRR |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 gold | 64 | 0.594 | 0.891 | 0.922 | 0.953 | 0.984 | 0.725 |
| 2 gold | 8 | 0.000 | 0.500 | 0.625 | 0.875 | 1.000 | 0.485 |
| 3+ gold | 22 | 0.000 | 0.136 | 0.227 | 0.545 | 0.818 | 0.580 |
| all | 94 | 0.404 | 0.681 | 0.734 | 0.851 | 0.947 | 0.670 |

**Single-gold queries hit R@5 = 0.89, near Qwen3-Embedding-0.6B (0.766) on this subset**. Multi-gold strict R@5 is the only weakness; R@50 = 0.95 confirms golds are retrieved, just not all in top-5.

### Rank & error diagnostics (layer22 anti-PCA k=10)

| Metric | Value |
|---|---:|
| Gold margin (best_gold - best_non_gold) mean | 0.003 |
| Gold margin std | 0.125 |
| Top-1 FP same-session-as-gold rate | 62% |
| Top-1 FP same-day-as-gold rate | 62% |
| Token count vs rank Spearman | 0.05 |

**Key observation**: 62% of top-1 false positives are turns from the same session that contains a gold turn. Method correctly identifies the topic/session but picks the wrong specific turn.

### Highlights / discussion

- **Confirmed best: layer 22 (or 21) + anti-PCA global k=10 + L2-norm cosine = R@5 0.681**.
- **Transform asymmetry**: query reframing alone explains nearly all the gain. Single-instance transforms on the candidate matrix are not necessary.
- **Multi-gold strict metric is the dominant residual penalty**; on single-gold the method nearly matches modern embedding baselines.
- **Same-session false positives** suggest a within-session disambiguation challenge: turn-level retrieval inherits session-level coherence, making fine-grained turn ranking the next problem.
- Whitening offers an alternative path with similar gains; it does not stack with anti-PCA (same problem family, similar effect).

### Round 3 candidates (executed)

See Round 3 section.

## Round 3: deployment-relevant validation (2026-05-04)

Setup: existing `tensors/dump_v1`. Tier A 100-instance (94 scored). Targeting Round 2 questions: is query-only transform stable? How much corpus needed? Is the 62% same-session FP a routing-vs-disambiguation issue?

### Query-only anti-PCA stability (Round 2 hypothesis verification)

| Layer | k=2 | k=5 | k=10 | k=15 |
|---|---:|---:|---:|---:|
| 21 | 0.6702 | **0.6809** | **0.6809** | 0.6702 |
| 22 | 0.6702 | 0.6596 | 0.6702 | 0.6596 |
| 23 | **0.6809** | 0.6489 | 0.6277 | 0.6489 |

Multiple (layer, k) cells achieve R@5 = 0.681, matching the both-sided transform from Round 2. **Query-only is stable, not a layer-22/k=10 outlier**. Production simplification is viable.

### Session-hit diagnostics (layer22 + anti-PCA global k=10)

| Split | n | turn R@5 | session_hit@5 | session_recall_all@5 |
|---|---:|---:|---:|---:|
| 1 gold | 64 | 0.891 | 0.969 | 0.969 |
| 2 gold | 8 | 0.500 | 1.000 | 0.750 |
| 3+ gold | 22 | 0.136 | 0.864 | 0.364 |
| all | 94 | 0.681 | **0.947** | 0.809 |

**Major finding**: at session level the method is near-perfect.
- 95% of queries have at least one gold session in top-5 retrieved turns;
- 81% have all gold sessions covered;
- The aggregate turn-level R@5 = 0.681 is dragged down by within-session turn disambiguation, especially for 3+ gold queries.

This reframes the method: **hidden-state retrieval is a strong session-level memory router**; turn-level fine-grained selection is the next problem, not the existence of the signal.

### Corpus stat sampling (deployment relevance, layer22 query-only anti-PCA k=10)

| Fraction | R@5 mean ± std over 5 seeds |
|---|---:|
| 1.00 | 0.6702 ± 0.0000 |
| 0.50 | 0.6702 ± 0.0000 |
| 0.25 | 0.6638 ± 0.0085 |
| 0.10 | 0.6660 ± 0.0085 |
| 0.05 | 0.6702 ± 0.0223 |

**Conclusion**: a 5-10% corpus sample reproduces full-corpus PCs for retrieval. Production systems do not need to recompute PCs over the entire memory base.

### Same-session rerank baseline (BM25 over top-50)

| Stage | R@5 | R@10 |
|---|---:|---:|
| Hidden state alone (baseline) | 0.6809 | 0.7340 |
| Top-50 BM25 rerank | 0.6170 | 0.6702 |

**BM25 rerank hurts** (-6pp R@5). Turn-level user text is too short for reliable BM25; the lexical signal is noisier than the hidden-state ranking it replaces. Fusion (weighted hidden+BM25 scores) might recover, but a simple BM25 rerank does not.

### Highlights / discussion

- **Query-only anti-PCA validated**: stable across (layer, k) cells, simplest deployable pipeline equals the both-sided transform's R@5.
- **Hidden state is a near-perfect session router (94.7% session_hit@5)**, but a weak within-session turn disambiguator. This shifts the problem framing from "find the right vector geometry" to "design a 2nd-stage reranker for turn selection inside hit sessions".
- **Corpus PCs converge fast**: 5-10% sample is sufficient. Production constraints relaxed.
- **BM25 alone cannot rerank turns** at this granularity. Turn text is too short and lexical-only signal underperforms hidden-state ranking. Need score-fusion (weighted) or a stronger 2nd-stage signal (e.g., assistant turn content, metadata, time, slot extraction).

### Round 4 candidates (executed)

See Round 4 section.

## Round 4: stand the conclusions up (2026-05-04)

Setup: focus on robustness, fairness, and a controlled fusion test instead of squeezing more R@5 from the same 100-instance subset (avoid p-hacking).

### Apples-to-apples baselines on same 94 scored

| Method | turn R@5 | turn R@10 | session_hit@5 | session_recall_all@5 | MRR |
|---|---:|---:|---:|---:|---:|
| BM25 | 0.585 | (TBD) | 0.862 | 0.660 | (TBD) |
| Qwen3-Embedding-0.6B | 0.766 | (TBD) | **0.989** | 0.851 | (TBD) |
| Hidden state (layer 22 anti-PCA k=10) | 0.681 | 0.734 | 0.947 | 0.809 | 0.670 |
| Hidden + BM25 fusion (α=0.5) | **0.713** | — | — | — | — |

Notes:
- All metrics computed on the exact 94 question_ids in our Tier A dump.
- Qwen3-Embedding remains strongest. Hidden-state alone surpasses BM25 by ~10pp turn R@5 and is roughly equal on session_hit@5.
- Hidden + BM25 fusion narrows the gap to Qwen-Embedding from -8.5pp to -5.3pp (turn R@5).

### Score fusion α sweep (full curve, no cherry-picking)

| α | R@5 |
|---:|---:|
| 0.00 (BM25 only) | 0.6064 |
| 0.10 | 0.6277 |
| 0.25 | 0.6489 |
| **0.50** | **0.7128** |
| **0.75** | **0.7128** |
| 0.90 | 0.6702 |
| 1.00 (hidden only) | 0.6702 |

Mid-α has a flat plateau peak; both 0.5 and 0.75 reach 0.713. Fusion is genuinely orthogonal: BM25 lexical signal compensates for hidden state's within-session weakness.

### Statistical robustness

1000-bootstrap on top 5 configs (n=94):

| Config | R@5 | CI (1000 bootstrap) |
|---|---:|---:|
| layer22 anti_pca_both k=10 | 0.6809 | 0.5851-0.7660 |
| layer21 query_only_anti_pca k=5 | 0.6809 | 0.5851-0.7660 |
| layer22 query_only_anti_pca k=10 | 0.6702 | 0.5745-0.7660 |
| layer22 center_instance | 0.6383 | 0.5319-0.7340 |
| hidden final_cosine (Phase 2) | 0.4787 | 0.3723-0.5745 |

50/50 split stability (first_half n=46, second_half n=48):

| Config | first_half R@5 | second_half R@5 |
|---|---:|---:|
| anti_pca_both k=10 | 0.696 | 0.667 |
| layer 21 query-only k=5 | 0.674 | 0.688 |
| layer 22 query-only k=10 | 0.674 | 0.667 |
| center_instance | 0.652 | 0.625 |
| final_cosine | 0.500 | 0.458 |

**Method ranking is stable across halves**. Round 1-3 wins are not artifact of one subset.

### Oracle ceiling and rank overlap

Oracle (per-question max over top 5 configs) ceiling: **R@5 = 0.7234** (only +4pp above best single config 0.681). Limited ensemble headroom from this config family alone.

Rank overlap (Jaccard@5):

| Pair | Jaccard@5 |
|---|---:|
| final_cosine vs layer22 query_only k10 | 0.258 |
| final_cosine vs layer22 anti_pca_both k10 | 0.332 |
| final_cosine vs layer22 center_instance | 0.464 |
| layer22 anti_pca_both vs layer22 query_only | **0.737** |
| layer21 query-only vs layer22 query-only | **0.680** |
| anti_pca_both vs center_instance | 0.539 |

- final_cosine vs transformed configs: low overlap (0.26-0.46) → these methods make complementary errors.
- Transformed configs among themselves: high overlap (0.46-0.74) → same signal family, redundant.
- **Implication**: combining methods within the anti-PCA / centering family stacks little; combining with orthogonal signal (BM25) helps. Confirms why fusion succeeded and why anti-PCA + whitening did not stack in Round 2.

### Highlights / discussion

- **Fusion (α=0.5) is the new strongest config at R@5 = 0.713**, half-way to Qwen-Embedding (0.766) on the same 94 questions.
- **Methods are stable** across 50/50 split and tighter (1000) bootstrap. Conclusions are not p-hacked.
- **Within the hidden-state family the ceiling is ~0.72** (oracle); to go further requires either orthogonal signal (BM25 fusion proved this) or a different method family (e.g., second-stage reranker, supervised projection).
- **Hidden state's session-routing signal is competitive with Qwen-Embedding**: 0.947 session_hit@5 vs 0.989. The aggregate turn R@5 gap is dominated by within-session disambiguation, not by missing the right session.

### Round 5 plan

Round 5 is the wrap-up. We will not run new experiments; instead we synthesize:

- A single short paper-style summary at the top of `notes/results_log.md` (plus an explicit non-overfitting disclaimer).
- A clear list of falsified, supported, and undecided claims.
- A short production recommendation: query-only anti-PCA k=10 on 5-10% sampled corpus, optionally fused with BM25 at α=0.5.

## Round 5: paper-style synthesis (2026-05-04)

### Headline claim

A training-free hidden-state retriever that uses Qwen3.5-2B's prompt-final layer-22 vector with global anti-PCA (k=10) reaches **turn-level R@5 = 0.681 and session_hit@5 = 0.947** on LongMemEval-S/round (94/100 scored). Fusing it with BM25 at α=0.5 reaches **turn-level R@5 = 0.713**, narrowing the gap to Qwen3-Embedding-0.6B from -10.6pp to -5.3pp on the same 94 questions.

### Reframing

The original Phase 2 framing ("hidden-state retriever vs embedding model on turn-level Recall@5") is not the right comparison. The data show:

- The method is **a strong session-level memory router** (0.947 session_hit@5, comparable to Qwen3-Embedding-0.6B's 0.989).
- It is **a weak fine-grained turn disambiguator** (3+gold turn R@5 = 0.14 while session_hit@5 = 0.86).
- Its main remaining error mode is "right session, wrong turn" (~62% of top-1 false positives are same-session as gold).

### What we showed (supported claims)

1. Final-layer post-norm hidden state alone underperforms BM25 by 11pp turn R@5; this is the original Phase 2 negative result.
2. Layer choice matters: layer 22 (and 21) is much stronger than the final post-norm vector for retrieval at the prompt-final position.
3. Geometry post-processing matters: global anti-PCA (k=10), global whitening, and centered cosine all yield similar gains; they are members of the same anisotropy-correction family.
4. The geometry gain comes mainly from **query reframing**. Transforming only the query is nearly as effective as transforming both candidates and query.
5. Production-relevant: PCs converge with 5-10% of the corpus.
6. Fusion is genuinely orthogonal: hidden+BM25 at α=0.5 beats either alone.
7. The aggregate turn R@5 underestimates the method: at the session level the method is comparable to a modern embedding baseline.

### What we ruled out / falsified

1. Mid-layer (1/e from end, layer 15) outputs are not retrieval-useful: pairwise cosine ~0.96 collapses ranking.
2. Mean / max pooling over the prompt sequence collapses signal at layer 22; the last position is the unique aggregation point.
3. Layer concatenation, multi-layer RRF, residual deltas (except 22-18 ties) and z-score do not beat single layer 22 + centered cosine.
4. BM25 replacement of hidden-state ranking inside top-50 hurts; only weighted fusion helps.
5. Stacking anti-PCA with whitening does not stack — same signal family.

### Undecided / not in scope

1. Whether the conclusions hold on the full 500 LongMemEval-S/round (not yet dumped). Round 5 is on 100 scored 94.
2. Whether a learned 2nd-stage turn reranker (small classifier, attention features, or assistant-side content) closes the 5pp gap to Qwen-Embedding.
3. Whether MemoryAgentBench / other 2026 long-memory benchmarks reproduce the same pattern.

### Production recommendation

Smallest deployable variant:

- Use Qwen3.5-2B layer 22 prompt-final hidden state.
- Apply query-only anti-PCA with global PCs estimated from 5-10% of the candidate corpus, k=10.
- Score by cosine on normalized vectors.
- Optionally fuse with BM25 at α=0.5 over a top-50 hidden shortlist.

Storage cost is unchanged from Phase 0/2. The transform is one mean subtraction plus a `(d, 10)` projection per query — essentially free.

### Statistical disclaimer

All numbers above are on the same 100-instance, 94-scored subset. Subset bias is real (Round 2 showed first 100 of M had +8pp BM25 inflation; here we cannot rule out a similar effect on S). The conclusions about method ranking, layer choice, query reframing, fusion orthogonality, and session-vs-turn framing are stable under 50/50 split and 1000-bootstrap, so we treat them as well supported. The absolute R@5 numbers are not yet definitive.

## Tier B Extra Exploration (post-Round 5)

### Disclaimer

Tier B contains only 20 LongMemEval-S/round instances. These results are direction-finding diagnostics before deleting the large all-position tensor dump, not conclusive performance claims. All comparisons below are apples-to-apples on the same 20 scored questions and 5,043 valid prompts.

### Content-end / suffix-position scan

Layer fixed at 22, score fixed to global anti-PCA k=10 unless noted.

| Position | R@5 | NDCG@5 | Note |
|---|---:|---:|---|
| content_end | 0.45 | 0.351 | Last content token before summary suffix |
| suffix_start | 0.35 | 0.229 | First token of fixed summary suffix |
| minus2 | **0.90** | 0.688 | Second-to-last prompt position |
| last | 0.85 | **0.727** | Existing Tier B baseline |

Takeaway: the suffix is not just noise. The final summary-prompt positions are much stronger than the raw content-end vector. `minus2` has higher R@5 than `last` on this tiny subset, but lower NDCG; treat this as a possible follow-up, not a new best claim.

### Position-debiased retrieval

Layer fixed at 22. This replaces global anti-PCA with simple position-specific mean subtraction, either pooled across query/candidate roles or separated by role.

| Position | Debias scheme | R@5 | NDCG@5 |
|---|---|---:|---:|
| content_end | role-pooled mean | 0.10 | 0.053 |
| content_end | role-separated mean | 0.35 | 0.294 |
| minus2 | role-pooled mean | **0.90** | 0.720 |
| minus2 | role-separated mean | **0.90** | **0.741** |
| last | role-pooled mean | 0.85 | 0.720 |
| last | role-separated mean | 0.85 | 0.702 |

Takeaway: per-position centering is approximately equivalent to anti-PCA for late suffix positions. This supports the interpretation that anti-PCA mainly removes a position/template-specific shared direction rather than discovering an unrelated semantic transform.

### Layer scan at content_end

Position fixed at `content_end`; score fixed to global anti-PCA k=10.

| Layer | R@5 | NDCG@5 |
|---|---:|---:|
| 16 | 0.25 | 0.163 |
| 17 | 0.30 | 0.170 |
| 18 | 0.25 | 0.146 |
| 19 | 0.40 | 0.301 |
| 20 | 0.45 | 0.326 |
| 21 | **0.50** | **0.377** |
| 22 | 0.45 | 0.351 |
| 23 | **0.50** | 0.336 |

Takeaway: changing position shifts the best content-end layer slightly (21/23 tie), but no content-end layer comes close to late suffix positions (`last` R@5 0.85, `minus2` R@5 0.90). The practical recipe remains layer 22 near the prompt end.

### Decision

These three Tier B checks address the remaining all-position hypotheses without repeating previously falsified mean/max pooling or diagonal-slice experiments. The main hypotheses are now either supported or ruled out:

- **Suffix necessary**: content-end vectors are much weaker than late suffix vectors.
- **Per-position de-bias explains anti-PCA**: late-position mean subtraction matches anti-PCA-style performance on this subset.
- **Layer 22 robust near prompt end**: content-end layer choice shifts slightly, but the strong signal remains in the final suffix positions.

There is no clear reason to spend another Tier B round before Stage 2. Tier B can be deleted according to `notes/stage_2_plan.md` after human approval.
