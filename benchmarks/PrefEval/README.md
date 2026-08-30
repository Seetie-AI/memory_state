# PrefEval Automatic Retrieval Benchmark

This folder keeps the preference/persona memory experiment separate from Stage
3 LongMemEval runs. The first target is `implicit_persona`, because it is the
closest public benchmark shape for an entertainment/companionship chatbot:
preference is revealed indirectly, and evaluation can be fully automatic.

## Task Definition

- Candidate memories: one stored `preference` string per PrefEval row.
- Query: the row's `question`.
- Gold: the same row's preference id. Identical preference strings are treated
  as equivalent gold memories by default.
- Metrics: R@1/R@3/R@5, NDCG@3/NDCG@5, MRR.
- No LLM judge is used.

When duplicate preference strings exist, the benchmark keeps all equivalent
gold ids in the prepared JSONL for auditability, then collapses them to one
canonical id during scoring so any equivalent memory counts as a hit. Tensor
and embedding cache manifests include a data fingerprint over item ids,
preference/question text, query ids, and gold ids; newer runs reject caches
whose fingerprint does not match the prepared JSONL instead of trusting
position-only ids.

## Compared Retrievers

- `single_1-3`: Stage 3 strong tag-style single prompt.
- `k3_concat_selected`: current best K=3 concat, selected layers/transforms.
  This remains available as a legacy evaluator, but it is not part of the
  n=1000 tensor-generation command because K3-style prompt fusion is an
  offline composition over saved prompt/layer tensors.
- `k3_concat_uniform_l31_both_k15`: same three prompts, all L31 and
  `anti_pca_both_k15`, retained as an optional evaluator for over-tuning
  checks.
- `qwen3_embedding_bm25`: Qwen3-Embedding-8B + BM25 z-score fusion,
  `alpha=0.75`.
- `bm25`: lexical baseline.
- `prompt_sweep_l28_l29_l30_l31_both_k15`: single-prompt sweep over the pruned
  Stage 3 prompt matrix at L28/L29/L30/L31 + `anti_pca_both_k15`. Layer labels
  are zero-based in the script, so L31 is the model's 32nd/final layer. After
  the n=100 pass this sweep is pruned to keep the stronger preference/topic
  prompts, K3 component diagnostics, three new preference-oriented prompts,
  and two "一个token" wording treatments.

The Stage 3 historical scripts are unchanged. The PrefEval sweep intentionally
drops duplicate and low-value controls from the n=100 run: `1-1_CN` duplicates
`1-3`, `1-1_CN_ASCII` and `1-1_EN` already served as punctuation/language
controls, the four `代表` treatment prompts are retired, and `2-6`/`2-7`/`2-8`
are not run by default after weak PrefEval and LongMemEval results.

Decision note: `2-1` ("话题") led the n=100 PrefEval sweep by R@3, but the word
"话题" may partially fit PrefEval's topic-structured rows. This is still close
to the AI companion target use case, so `2-1` remains in the sweep and a
paired `2-1_token` treatment tests whether "一个token" wording changes the
signal.

New preference-oriented prompts:

- `user_preference`: `用一个词标记上面这段对话中用户的偏好，这个词是：“`
- `user_avoidance`: `用一个词标记上面这段对话中用户不喜欢或应避免的内容，这个词是：“`
- `personalization_need`: `用一个词标记下次回答这个用户时最需要记住的个性化信息，这个词是：“`
- Token treatments: `2-1_token` and `user_preference_token`.

The n=1000 tensor-generation command stores sparse next-token logit
distributions with `--store-topk-logits 256`: token ids plus logit values for
the top 256 next tokens for every prompt and every memory/query text. This
matches the Stage 3 sparse-logit audit style while avoiding full-vocabulary
logits, which would approach the local storage and memory budget for this run.
It also stores a second PromptReps-style sparse distribution with
`--store-promptreps-logits`: lowercase words from the source text are extracted,
English stopwords/punctuation are removed, the remaining words are tokenized,
only those token ids' logits are kept, ReLU + `log1p` saturation is applied,
the top 128 weights are retained, and weights are quantized by multiplying by
100 and converting to integers.

## Commands

BM25-only real data smoke:

```bash
.venv/bin/python benchmarks/PrefEval/prefeval_benchmark.py \
  --task implicit_persona \
  --limit 30 \
  --shuffle-seed 0 \
  --retrievers bm25 \
  --bootstrap-samples 200
```

Default pruned hidden-state tensor-generation pass:

```bash
.venv/bin/python benchmarks/PrefEval/prefeval_benchmark.py \
  --task implicit_persona \
  --limit 1000 \
  --shuffle-seed 0 \
  --retrievers bm25,prompt_sweep_l28_l29_l30_l31_both_k15 \
  --store-topk-logits 256 \
  --store-promptreps-logits \
  --promptreps-topk 128 \
  --bootstrap-samples 1000
```

Small hidden-state smoke with the same online workflow:

```bash
.venv/bin/python benchmarks/PrefEval/prefeval_benchmark.py \
  --task implicit_persona \
  --limit 100 \
  --shuffle-seed 0 \
  --retrievers bm25,prompt_sweep_l28_l29_l30_l31_both_k15 \
  --store-topk-logits 256 \
  --store-promptreps-logits \
  --promptreps-topk 128 \
  --bootstrap-samples 1000
```

Qwen3-Embedding + BM25 only:

```bash
.venv/bin/python benchmarks/PrefEval/prefeval_benchmark.py \
  --task implicit_persona \
  --limit 100 \
  --shuffle-seed 0 \
  --retrievers bm25,qwen3_embedding_bm25 \
  --embedding-alpha 0.75 \
  --bootstrap-samples 1000
```

Offline K3 combo sweep over saved n=1000 tensors. This does not run the 9B
model; it ranks systematic K3 dense combinations, then runs BM25/PromptReps
weight sweeps and logits shortlist screening on the top dense rows:

```bash
.venv/bin/python benchmarks/PrefEval/prefeval_stage1_offline.py \
  --phase combo_sweep \
  --output-prefix combo_sweep_$(date +%Y%m%d_%H%M%S) \
  --combo-top-n 8 \
  --combo-selection-split first500 \
  --shortlist-size 20 \
  --screen-alpha 0.80 \
  --bootstrap-samples 200
```

Prepare official multiple-choice classification prompts. This script only
prepares/scorers JSONL and does not run generation. `implicit_choice` is the
first supported task because it has official `options` and `aligned_op` fields:

```bash
.venv/bin/python benchmarks/PrefEval/prefeval_classification.py \
  --mode prepare \
  --task implicit_choice \
  --limit 0 \
  --reminder both \
  --turn-limit 300
```

The script prints progress during download, scoring, hidden-state encoding, and
embedding encoding. Outputs are written under:

- `benchmarks/PrefEval/data/`
- Official PrefEval distractor turns:
  `benchmarks/PrefEval/data/official/filtered_inter_turns.json`
- `benchmarks/PrefEval/tensors/`
- `benchmarks/PrefEval/results/`
