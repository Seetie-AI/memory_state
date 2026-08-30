# PrefEval Final Retrieval Configs

Created: 2026-05-13

Updated: 2026-05-13 after the K3 contrast runs.

This document records the final PrefEval retrieval baselines after Stage 1.1.
There are two different goals, so the result should not be collapsed into a
single "best" row:

- `prefeval_best_retrieval`: maximize PrefEval retrieval metrics.
- `companion_balanced_retrieval`: keep a companion-relevant interaction or
  affect signal even when it is not the PrefEval leaderboard optimum.

The distinction matters because PrefEval `implicit_persona` rewards preference
matching more directly than companion-style affect and relationship dynamics.

## Named Configs

### `prefeval_best_retrieval`

This is the strongest clean full-corpus PrefEval baseline from the contrast
table.

- K3 prompts: `2-3-1_L30 + 2-5_L29 + 2-1_L30`
- Dense scorer: `vector_average_component_norm`
- Final full-corpus score:

```text
final_score =
  0.60 * row_zscore(K3_vector_average_score)
+ 0.30 * row_zscore(Qwen3-Embedding-0.6B_score)
+ 0.10 * row_zscore(BM25_score)
```

Use this when reporting the best PrefEval Stage 1.1 retrieval score.

### `companion_balanced_retrieval_dynamics`

This is the preferred companion-balanced candidate when the third K3 slot is
allowed to represent interaction dynamics rather than a pure topic/fact axis.

- K3 prompts: `2-3-1_L30 + 2-5_token_L30 + 2-7_emoji_L30`
- Dense scorer: `vector_average_component_norm`
- Final full-corpus score: same 60/30/10 K3 / embedding / BM25 z-score fusion.

This config is not the PrefEval maximum, but it keeps an interaction-pattern
axis and still recovers most of the retrieval score. In the contrast run it
outperformed the emotion-anchor alternative on R@1 and R@5.

### `companion_balanced_retrieval_emotion`

This is the earlier emotion-anchor candidate.

- K3 prompts: `2-3-1_L30 + 2-5_token_L30 + 2-8_emoji_L30`
- Dense scorer: `vector_average_component_norm`
- Final full-corpus score: same 60/30/10 K3 / embedding / BM25 z-score fusion.

Keep this as a product hypothesis if the third slot must explicitly encode
emotion. Otherwise, `2-7_emoji` is the stronger balanced default on PrefEval and
is closer to the companion "interaction dynamics" motivation.

## Prompt Id Caveat

`2-8` has changed meaning across Stage 1 experiments:

- Earlier Stage 1 `2-8` referred to answer strategy.
- Stage 1.1 `2-8_emoji` refers to conversation emotion:
  `用一个emoji标记上面这段对话的情绪，这个emoji是：“`

Do not reproduce `2-8_emoji` from an old Stage 1 tensor or prompt dictionary
without checking the suffix text.

## K3 Contrast Table

All rows below use full-corpus scoring with the same 60/30/10 K3 /
Qwen3-Embedding-0.6B / BM25 z-score fusion. The hidden-only columns use only
the K3 vector-average score.

| K3 config | interpretation | hidden-only R@3 | hidden-only R@5 | final R@1 | final R@3 | final R@5 | final NDCG@5 | final MRR |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `2-3-1 + 2-5 + 2-1` | PrefEval-best topic baseline | 0.265 | 0.339 | 0.119 | 0.265 | **0.355** | **0.240** | **0.235** |
| `2-3-1 + 2-5_token + 2-7_emoji` | companion dynamics anchor | 0.246 | 0.317 | **0.125** | 0.259 | 0.341 | 0.236 | 0.234 |
| `2-3-1_summarize + 2-5_token + 2-1-2` | post-1.1 treated topic | 0.250 | 0.329 | 0.110 | 0.247 | 0.338 | 0.226 | 0.224 |
| `2-3-1 + 2-5_token + 2-8_emoji` | companion emotion anchor | 0.245 | 0.314 | 0.122 | **0.265** | 0.332 | 0.232 | 0.233 |

Main observations:

- The old topic K3 remains the best PrefEval retrieval config.
- The emotion-anchor config preserves R@3 but gives up about 2.3 pp R@5 versus
  the topic baseline under the same 60/30/10 full-corpus fusion.
- The dynamics-anchor config is a stronger balanced candidate than the
  emotion-anchor config on R@1 and R@5, while giving up only 0.6 pp R@3.
- Single-prompt treatment gains do not add linearly: the treated topic K3 is
  weaker than the old topic K3 after fusion.

## Selected Scores

| named config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| `prefeval_best_retrieval` | 0.119 | 0.265 | 0.355 | 0.240 | 0.235 |
| `companion_balanced_retrieval_dynamics` | 0.125 | 0.259 | 0.341 | 0.236 | 0.234 |
| `companion_balanced_retrieval_emotion` | 0.122 | 0.265 | 0.332 | 0.232 | 0.233 |

The earlier highest observed R@3 row remains:

| config | prompt set | rerank / screening | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---|---|---:|---:|---:|---:|---:|
| highest observed R@3 | `2-3-1_L30 + 2-5_L29 + 2-1_L30` | source_ge3 + embedding top20, score z-fusion `K3=0.90 / emb=0.10 / BM25=0.00` | 0.127 | 0.270 | 0.344 | 0.239 | 0.238 |

That row is useful as a tuning ceiling, but it is not the clean final config:
it came from a broader sweep over source screening and fusion weights, removes
BM25, and uses a K3-heavy 90/10/0 mix.

## Holdout Caveat

The deterministic `holdout300_seed0` result for the emotion-anchor config is a
split robustness check, not a blind validation:

| split | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| all1000, emotion anchor | 0.122 | 0.265 | 0.332 | 0.232 | 0.233 |
| holdout300_seed0, emotion anchor | 0.127 | 0.263 | 0.320 | 0.228 | 0.228 |

The prompt set and fusion family had already been explored on all 1000 queries
before this split was made. Therefore this holdout cannot prove absence of
hyperparameter overfit; it only shows that the chosen row is not obviously
localized to one deterministic slice.

## Product Interpretation

- Use `prefeval_best_retrieval` for benchmark reporting.
- Use `companion_balanced_retrieval_dynamics` as the current balanced companion
  candidate if a single K3 retriever must carry a dynamics signal.
- Keep `companion_balanced_retrieval_emotion` as an explicit emotion-anchor
  alternative, not as the default benchmark winner.
- Do not lock the third K3 slot permanently. In the companion eval, compare
  "topic third slot", "dynamics third slot", "emotion third slot", and an
  emotion/dynamics side-channel design.
- Do not add source-count shortlist to the default full-corpus z-score reranker
  unless retrieve-1 quality becomes the priority. Some shortlist rows have
  slightly better R@1, but they add another tuning knob.

## Reproduction Pointers

PrefEval-best topic baseline:

- Result file:
  `benchmarks/PrefEval/results/prefeval_stage1_1_more_prompts/k3_compare_old_topic_full_k060_e030_b010_20260513.json`
- Use row:
  `k3_bm25_embedding_full_d0.60_b0.10_e0.30`

Companion dynamics-anchor baseline:

- Result file:
  `benchmarks/PrefEval/results/prefeval_stage1_1_more_prompts/k3_compare_dynamics_27emoji_full_k060_e030_b010_20260513.json`
- Use row:
  `k3_bm25_embedding_full_d0.60_b0.10_e0.30`

Companion emotion-anchor baseline:

- Result file:
  `benchmarks/PrefEval/results/prefeval_stage1_1_more_prompts/k3_231_25token_28emoji_sameL30_sourcege2_k060_e030_b010_20260513.json`
- Use row:
  `k3_bm25_embedding_full_d0.60_b0.10_e0.30`

Emotion-anchor holdout sanity check:

- Result file:
  `benchmarks/PrefEval/results/prefeval_stage1_1_more_prompts/k3_231_25token_28emoji_sameL30_full_k060_e030_b010_holdout300_seed0_20260513.json`
- Use row:
  `k3_bm25_embedding_full_d0.60_b0.10_e0.30`

Highest observed R@3 row:

- Result file:
  `benchmarks/PrefEval/results/prefeval_stage1/prefeval_embedding06_k3_concat_source_ge3_plus_embedding_top20_bm25_broad_sweep_20260512.json`
