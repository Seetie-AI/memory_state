# Stage 3 Prompt Sweep Findings

Final results on the 100-instance / 94-scored LongMemEval-S round-level subset
using the merged Stage 3 store
(`tensors/stage3/prompt_sweep/merged_subset0-100_cache2gb_logits256/`).

Supersedes the preliminary observations in
`stage_3_prompt_sweep_observations_tmp.md`, which were based on A 0-39 only.

## Headline

| System | R@5 | NDCG@5 | session_hit@5 | Note |
|---|---:|---:|---:|---|
| **Stage 3 hidden best R@5** | **0.766** | 0.757 | 0.979 | `2-3-2_mem\|L31\|both_k15` and `2-4-1_user_word\|L30\|both_k15` |
| **Stage 3 hidden best NDCG@5** | 0.755 | **0.784** | **1.000** | `1-3\|L31\|both_k15` (the `标记` tag prompt) |
| Stage 2 P0 anchor reproduced | 0.755 | 0.779 | 0.989 | `P0\|L30\|both_k15` matches the historical Stage 2 number |
| Qwen3-Embedding-8B-4bit-DWQ | 0.755 | 0.789 | — | new baseline in `results/stage3/embedding_eval/` |
| Qwen3-Embedding-0.6B (historic) | 0.766 | 0.809 | — | from `results/stage1/phase1a_qwen_embedding_longmemeval_s_cleaned_round_100.json` |

**Hidden-state retrieval matches the 8B 4-bit embedding baseline on R@5
(+0.011) and is within 0.005 NDCG@5 of it.** Confidence intervals overlap
heavily, so this is parity-level evidence, not a significant win, but it does
mean Stage 3 prompt vectors carry retrieval signal comparable to a dedicated
embedding model **without training one**.

Note: 8B-4bit-DWQ trailing 0.6B fp16 by 1 question is consistent with
quantization-induced retrieval drop reported in the literature; it is not
evidence of corruption, and 100-sample CIs overlap.

## Best Score Mode

Across the 17 symmetric variants:

| Score mode | Variants where it wins R@5 |
|---|---:|
| `anti_pca_both_k15` | 13 |
| `query_only_anti_pca_k2` | 3 |
| `centered_cosine` | 1 (`1-1_CN`) |

Anti-PCA on both sides remains the dominant geometric post-processing under
Stage 3. The deployment-friendly query-only path that Stage 2 favored does not
win here for most prompts.

## Best Layer

`L29` / `L30` / `L31` win 6 / 6 / 5 variants. There is no single best layer; it
depends on the prompt. The earlier observation "layer 29 looks better" is a
myth driven by A-subset variance.

## Per-Variant Headline

Each cell uses its individually best score mode.

| Variant | Best layer | Score mode | R@5 | NDCG@5 | session_hit@5 |
|---|---:|---|---:|---:|---:|
| 2-3-2_mem | 31 | both_k15 | 0.766 | 0.757 | 0.979 |
| 2-4-1_user_word | 30 | both_k15 | 0.766 | 0.751 | 0.979 |
| 1-3 | 31 | both_k15 | 0.755 | 0.784 | 1.000 |
| P0 | 30 | both_k15 | 0.755 | 0.779 | 0.989 |
| 1-1_CN | 29 | centered_cosine | 0.755 | 0.756 | 0.979 |
| 2-3-2_mem -> 2-3-2_query | 31 | both_k15 | 0.755 | 0.751 | 0.957 |
| 2-1 | 30 | both_k15 | 0.755 | 0.730 | 0.968 |
| 1-1_CN_ASCII | 29 | qpca_k2 | 0.755 | 0.719 | 0.979 |
| 2-3-2_query | 29 | both_k15 | 0.745 | 0.764 | 0.989 |
| 2-3-1 | 30 | both_k15 | 0.745 | 0.762 | 0.968 |
| 1-2 | 29 | both_k15 | 0.745 | 0.762 | 0.979 |
| 2-5 | 29 | qpca_k2 | 0.723 | 0.747 | 0.968 |
| 2-4-1 | 30 | qpca_k2 | 0.723 | 0.718 | 0.989 |
| 2-6 | 30 | both_k15 | 0.723 | 0.700 | 0.989 |
| 1-1_EN | 31 | both_k15 | 0.713 | 0.689 | 0.979 |
| 2-4-2 | 29 | both_k15 | 0.713 | 0.648 | 0.968 |
| 2-7 | 31 | both_k15 | 0.702 | 0.672 | 0.968 |
| **2-8** | 31 | both_k15 | **0.574** | 0.510 | 0.915 |

## Two Different Kinds of Winners

- **Recall winners** (R@5 = 0.766): `2-3-2_mem` and `2-4-1_user_word`.
  `2-3-2_mem` is the "what should be saved to memory" prompt; high R@5, slightly
  lower NDCG. Useful when the memory layer is the gatekeeper and downstream
  re-ranking exists.
- **Ranking winner** (NDCG@5 = 0.784, session_hit = 1.000): `1-3` ("标记" tag
  prompt). Best ordering quality and never misses a session. Useful when no
  re-ranker follows.

These are two complementary objectives; fusing them is the natural next
experiment.

## Surprises and Counter-Observations

1. **`2-4-1_user_word` (control with "用户") beats `2-4-1` (with "对方")** in
   R@5 by 0.043. The wording control became the winner. Likely interpretation:
   "用户" is closer to the model's training distribution for chatbot context
   than "对方". This argues that prompt-engineering for retrieval may benefit
   from product-native vocabulary rather than neutral linguistic phrasing.
2. **`2-8` ("回答策略") collapses to R@5 = 0.574**, far below all other
   variants. Strategy/answer-style framings do not work on this evidence-heavy
   benchmark.
3. **`1-1_CN` substantially beats `1-1_EN` (0.755 vs 0.713)**. Language of the
   summary suffix matters; Chinese aligned with the bilingual model better
   here.
4. **`2-3-2_mem -> 2-3-2_query` asymmetric cell does not beat symmetric
   `2-3-2_mem`** (0.755 vs 0.766). `centered_cosine` on the asymmetric cell
   collapses to 0.553-0.638 because the candidate-corpus mean is geometrically
   incompatible with cross-prompt queries; this is a known anti-PCA caveat
   noted in the analysis script.

## Caveats

- 100-instance subset; 94 scored after abstention filter. CI is wide
  (~±0.04-0.08 on R@5). Single-question differences are within noise.
- LongMemEval is evidence-retrieval biased. The persona / preference / style
  variants (2-4-x, 2-7, 2-8) scoring lower here does **not** prove they are
  useless for chatbot memory in product; it proves they are not the right
  framing for fact-recall benchmarks.
- 8B-4bit-DWQ trailing 0.6B-fp is most likely quantization + `task_description`
  / pooling configuration differences, not data corruption. We did not rerun
  the 0.6B baseline with the same `task_description` to confirm.

## Open Directions Surfaced by Stage 3

- **Prompt vector fusion / late interaction**: combine multiple prompt cells
  (e.g. `1-3` + `2-3-2_mem` + `P0`) via vertical concat (one big vector) or
  side-by-side multi-vector (max-sim / ColBERT-style). This is the natural
  next step and is now Stage 4.
- **Preference-oriented benchmark**: revisit persona / strategy prompts on a
  preference or recommendation benchmark, not on LongMemEval.
- **Storage precision study**: bf16 per-vector is 8 KB; fp8 / int8 path to
  4 KB per vector for on-device chatbot memory storage budgets.

## Provenance

- Full leaderboard JSON:
  `results/stage3/offline_prompt_sweep/merged_subset0-100_hidden_only.json`
- Top-25 markdown:
  `results/stage3/offline_prompt_sweep/merged_subset0-100_hidden_only.md`
- Run log:
  `results/stage3/offline_prompt_sweep/merged_subset0-100_hidden_only.log`
- Embedding baseline:
  `results/stage3/embedding_eval/qwen3_embedding_8b_dwq_subset0-100.json`
- Analyzer: `scripts/stage3_offline_analyze.py` (MLX chunk-batched loader,
  commit `756a3ea`)
