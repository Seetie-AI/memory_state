# PrefEval Stage 2 Retrieval-Only Design

## Goal

Stage 1 converted PrefEval into a global retrieval task: each query searched
across 1000 preference rows. That was useful for prompt/fusion discovery, but
it can over-penalize near-miss memories and can mix independent users into the
same candidate pool.

Stage 2 switches to a cleaner product-shaped retrieval setup:

- each example has its own user memory store;
- official PrefEval distractor turns provide long-context noise;
- retrieval is evaluated directly, without MCQ answer generation.

The core question is whether our memory retrieval stack can find the target
preference from a per-user memory pool containing many irrelevant turns. This
keeps Stage 2 focused on the memory layer instead of mixing in answer-generation
behavior.

## Data

- Target rows: PrefEval preference/question rows already used in Stage 1.
- Official distractors:
  `benchmarks/PrefEval/data/official/filtered_inter_turns.json`.
- The distractor file contains conversation streams. For a 300-turn setting,
  use the first 600 user/assistant messages.

This avoids the Stage 1 global-pool issue: distractors are not other benchmark
users' target preferences.

## Candidate Construction

For each query:

1. Add the row's target preference as one positive memory.
2. Build distractor memories from official inter-turn messages.
3. Rank the positive memory against distractor memories.

Initial chunking plan:

| setting | value |
|---|---:|
| distractor messages | 600 |
| messages per chunk | 10 |
| overlap | 5 |
| distractor chunks | 119 |
| target memories | 1 |
| total candidates/query | 120 |

The 10-message chunk is a product-oriented memory chunk, not a strict official
message-level unit. A later pass can compare message-level, exchange-level, and
chunk-level memory units.

## Experimental Risks And Controls

Stage 2's biggest risk is experiment construction, not model capacity. The
official distractor setup is clean because distractors are designed to be
unrelated to the target preference, but it may also be too easy or too artificial
if target memories are short preference sentences while distractors are long
dialogue chunks.

Priority controls:

| control | priority | reason |
|---|---|---|
| stronger cache manifest | must do | bind `prepared_jsonl_sha1`, target count, distractor hash, chunking, model path, and prompt cells to avoid silent tensor reuse |
| length-prior ablation | must do | target preference sentences and distractor chunks have different length/style; retrieval may learn short-vs-long shortcuts |
| anti-PCA fit corpus ablation | should do | compare fitting anti-PCA on target-only vs target+distractors, because mixing distractors can change the geometry |
| distractor slice ablation | should do | compare first/middle/random 600 messages so one distractor slice does not define the conclusion |
| per-distractor error distribution | should do | find whether a few distractor chunks act as high-score sinks across many queries |
| Stage 1 vs Stage 2 warning | must do | Stage 1 global preference retrieval and Stage 2 per-query target+distractor retrieval are not numerically comparable |
| same-topic preference hard negatives | later | useful product stress test, but it reintroduces near-gold ambiguity and should not be mixed into the official-distractor baseline |

Classification remains out of scope for Stage 2.

## Retrieval Variants

Start with the current best no-embedding mainline and a few controls:

| variant | purpose |
|---|---|
| BM25 | lexical baseline |
| `2-3-1` single prompt | strongest shared single prompt |
| `2-5` single prompt | association/diversity check |
| `2-1-2` single prompt | topic preference check, replacing `2-1` after Stage 1.1 |
| K3 vector average: `2-3-1 + 2-5 + 2-1-2` | current practical dense mainline |
| K3 + BM25 small-weight fusion | current production-like retrieval stack |
| optional 0.6B embedding | diagnostic only, not mainline unless it wins clearly |

Do not use a global 1000-row candidate pool in Stage 2.

## Metrics

Retrieval-only metrics:

- target rank distribution;
- R@1, R@3, R@5;
- MRR;
- target score margin over best distractor;
- failure examples where distractor outranks target.

Out of scope for Stage 2:

- Classification-RAG / MCQ accuracy.
- 10-turn vs 300-turn generation with and without official reminder.
- Any LLM judge or generation-model comparison.

Those can be a separate Stage 3 once retrieval behavior is understood.

## Guardrails

- No gold leakage in reminder prompts. Official reminder is a generic reminder
  to consider prior discussion, not the preference text.
- Cache manifests must bind item ids, target text, query text, distractor file
  hash, prepared JSONL SHA1, target count, chunk size, overlap, model path, and
  retrieval variant.
- Stage 2 results should be written under
  `benchmarks/PrefEval/results/prefeval_stage2/`.
- Tensor/cache outputs should be written under `benchmarks/PrefEval/tensors/`
  with explicit `stage2` names.

## Interpretation

If target retrieval is strong in this setting, Stage 1's modest gains were
partly caused by an artificially hard global candidate pool.

If target retrieval is weak even against official distractors, the issue is not
global-pool contamination; the prompt/vector strategy is failing to isolate the
preference from ordinary long-context noise.

Stage 1 and Stage 2 scores should not be compared as if they were the same
benchmark. Stage 1 asks each query to search a global pool of 1000 target
preference memories. Stage 2 asks each query to rank one target preference
against per-query distractors. The absolute scores answer different questions;
only directional lessons about prompts or fusion should transfer.

Initial BM25-only baseline:

| run | R@1 | R@3 | R@5 | MRR | mean rank |
|---|---:|---:|---:|---:|---:|
| n=30 smoke, 300 turns, 10/5 chunks | 0.000 | 0.000 | 0.000 | 0.009 | 115.5 |
| n=1000, 300 turns, 10/5 chunks | 0.044 | 0.064 | 0.077 | 0.069 | 94.2 |

This baseline suggests lexical matching alone is weak in the official-distractor
retrieval-only setup.
