# Stage 3 Prompt Sweep Temporary Observations

Status: preliminary notes from machine A subset 0-39 only. Do not treat as final
until machine B 40-99 is merged and offline query-only anti-PCA / asymmetric
cells are evaluated.

## Current Benchmark Anchors

Historical Stage 2 / baseline numbers on the 100-instance, 94-scored subset:

| Method | R@5 | NDCG@5 | Note |
|---|---:|---:|---|
| BM25 baseline | 0.585 | 0.547 | lexical baseline |
| Qwen3-Embedding-0.6B | 0.766 | 0.809 | embedding model baseline |
| Stage 2 9B P0 layer30 centered | 0.691 | 0.689 | online centered cosine |
| Stage 2 9B P0 layer30 query-only anti-PCA k=2 | 0.755 | 0.754 | deployment-friendly hidden-only |
| Stage 2 9B P0 layer30 anti-PCA both k=15 | 0.755 | 0.779 | best hidden-only |
| Stage 2 9B P0 layer30 anti-PCA k=15 + BM25 alpha=0.75 | 0.766 | 0.791 | final Stage 2 |

Public LongMemEval numbers found on 2026-05-10 are not apples-to-apples with
our setup. They usually report session-level `recall_any@5` on the full
LongMemEval-S 500 questions, while this repo currently reports stricter
turn/evidence retrieval metrics on a 100-instance cleaned subset. Keep them as
orientation only:

| Public system | Reported number | Method / caveat |
|---|---:|---|
| MemPalace raw | R@5 96.6% | ChromaDB/default embedding, zero API; session-level retrieval |
| MemPalace hybrid held-out | R@5 98.4% | keyword/temporal/preference heuristics; held-out claim |
| agentmemory BM25+Vector | R@5 95.2%, NDCG@10 87.9% | all-MiniLM-L6-v2, `recall_any@K`, 500 questions |
| agentmemory BM25-only | R@5 86.2%, NDCG@10 73.0% | same public setup |
| Schift vector | R@5 96%, NDCG@10 0.904 | sampled 100 balanced questions, schift-embed-1 |
| Schift L# Cache | R@5 96%, NDCG@10 0.923 | L0/L1/L2 multi-vector weighted merge |

No direct public Qwen3-Embedding-8B LongMemEval number was found. Public Qwen
sources report Qwen3-Embedding-8B as a strong general embedding model
(MTEB multilingual mean 70.58, retrieval type score around 70.88), but not on
LongMemEval specifically.

## Human Observations To Revisit After Full Merge

- `1-1_CN` is much stronger than `1-1_EN`; the language effect appears large.
- `2-1` (`代表话题`) currently looks like the strongest prompt and may be a
  clear leader.
- `1-3` (`标记`) is close on NDCG, but `2-1` has clearly stronger R@5.
- ASCII punctuation appears to reduce ranking quality relative to the full-width
  Chinese punctuation variant.
- As a verb, `代表` does not obviously beat `标记`; `标记` has strong NDCG.
- `代表对方` / `用户` / `对方需求` / `互动模式` / `回答策略` are all weak in this
  benchmark, possibly because LongMemEval is evidence-retrieval-heavy rather
  than preference/style/strategy-heavy.
- `回答策略` nearly collapses, suggesting little evidence-retrieval signal under
  this metric.
- Layer 29 looks better in many cases; it is unfortunate layer 28 was not kept.

## Codex Observations From A 0-39

- `2-1` is the current best online centered-cosine row:
  L29 R@5=0.975 / NDCG@5=0.808; L30 R@5=0.975 / NDCG@5=0.798.
- `1-1_CN` and `1-3` are strong, suggesting the broad content/topic labeling
  family is better aligned with this benchmark than persona/strategy prompts.
- `1-1_CN` vs `1-1_CN_ASCII`: R@5 can tie, but full-width punctuation currently
  has better NDCG, so punctuation may affect ordering even when recall survives.
- Layer 29 and 30 are the real contest; layer 31 is usually weaker. It is not
  true that layer 29 always beats layer 30.
- The online result evaluates only same-variant memory/query cells. The intended
  asymmetric cell `(2-3-2_mem, 2-3-2_query)` still needs an offline evaluator.
- These online numbers are centered-cosine only. Final comparison should use
  merged corpus query-only anti-PCA k=2, and optionally compare to Stage 2
  anti-PCA/BM25 anchors above.
- Because A 0-39 reaches very high R@5 for several prompts, subset bias or
  early-slice easiness is possible. The B 40-99 merge is necessary before making
  strong claims.
