# Inference-Native Memory State

This repository tests whether an LLM's own inference-time hidden states can act
as long-term memory retrieval vectors, without training a separate embedding
model.

## Start here

- [docs/memory-state-article.md](docs/memory-state-article.md): short write-up
  for a general reader.
- [paper/memory-state-paper.md](paper/memory-state-paper.md): the academic
  write-up, with related work, negative results, and limitations.
- [docs/DATA.md](docs/DATA.md): which benchmark data is not redistributed here,
  and how to obtain it.

Those two write-ups carry the current headline numbers. The Stage 2 summary
below and the rest of this README are the May 2026 working state, kept as a
log. Where they disagree with the write-ups above, the write-ups are current.

---

The final Stage 2 result is:

> Qwen3.5-9B-4bit, using the prompt-final hidden state from layer 30, anti-PCA
> post-processing, and light BM25 fusion, reaches **Recall@5 = 0.766** on the
> LongMemEval-S / round-level 100-instance subset. This matches the
> Qwen3-Embedding-0.6B baseline on the same 94 scored questions.

This README is the entry point for a new reader. Detailed experiment logs live
in [notes/results_log.md](notes/results_log.md), and the Stage 2 execution plan
lives in [notes/stage_2_plan.md](notes/stage_2_plan.md).

## Headline Results

Setup: LongMemEval-S, round-level retrieval, 100 instances, 94 scored after the
official abstention filter.

| Method | Recall@5 | NDCG@5 | Session hit@5 | Note |
|---|---:|---:|---:|---|
| BM25 | 0.585 | 0.547 | 0.862 | lexical baseline |
| Qwen3-Embedding-0.6B | 0.766 | 0.809 | 0.989 | lightweight modern embedding baseline |
| 2B hidden-state baseline | 0.479 | 0.450 | - | final post-norm + cosine |
| 2B Stage 1 best | 0.713 | - | 0.947 | anti-PCA + BM25 fusion |
| 9B hidden-only | 0.755 | 0.779 | 0.968 | layer 30 + anti-PCA |
| **9B final** | **0.766** | **0.791** | - | anti-PCA + BM25 fusion alpha=0.75 |

Important caveat: the parity claim is against **Qwen3-Embedding-0.6B**, not
Qwen3-Embedding-4B or Qwen3-Embedding-8B. Stronger embedding baselines remain to
be tested.

## What Was Tested

The benchmark is LongMemEval-S at **round** granularity:

- Each question has roughly 200-300 candidate user turns.
- The retriever ranks candidate turns.
- A gold turn is a turn that contains evidence needed to answer the question.
- Some questions have multiple gold turns; the main Recall@5 metric is strict.

The method encodes each memory candidate and query with a prompt suffix, then
uses a selected hidden state as the retrieval vector:

```text
<text>
请用一个词来summarize上面这段文字，这个词是：“
```

The best discovered production-style configuration is:

1. Qwen3.5-9B-MLX-4bit.
2. Layer 30 of 32, roughly 94% model depth.
3. The final suffix token position (`last`).
4. L2-normalized cosine over hidden states.
5. Anti-PCA over the candidate corpus, best at k=15 for 9B.
6. Optional BM25 score fusion, best alpha=0.75 in Stage 2.

## Key Mechanism Findings

- **Late but not final layer**: 2B works best around layer 22/24; 9B works best
  around layer 30/32. Both are near 92-94% model depth.
- **Suffix-end position matters**: the useful vector is at the prompt/suffix
  end. Content-end positions are much weaker.
- **Anti-PCA removes shared prompt/corpus directions**: the candidate vectors
  share a strong common direction induced by prompt structure and corpus
  geometry. Removing top principal components exposes semantic differences.
- **Session routing is easier than turn disambiguation**: hidden states are very
  strong at finding the correct conversation/session, but strict turn-level
  Recall@5 penalizes multi-gold questions.
- **KV cache reuse is valid**: cached-prefix suffix encoding matched full
  forward hidden states with cosine above 0.9998 in Stage 2 sanity tests.

## Glossary

**Turn / round**: one user message in a conversation. In round-level retrieval,
each candidate is one user turn.

**Session**: a multi-turn conversation block. A session contains many turns.

**Gold**: an evidence turn marked as containing information needed to answer the
question.

**Recall@5 / recall_all@5**: strict metric. A question scores 1 only if **all**
gold turns are in the top 5 retrieved turns; otherwise it scores 0.

**NDCG@5**: ranking-quality metric. It rewards putting gold turns higher in the
top 5, and is less all-or-nothing than recall_all@5.

**Session hit@5**: maps the top retrieved turns back to sessions. It scores 1 if
at least one correct gold session appears in the top 5 retrieved turns.

**Centered cosine**: subtracts the per-instance candidate mean vector before
computing cosine similarity. This removes a shared direction within the local
candidate set.

**Anti-PCA**: computes principal components over candidate vectors and removes
the top-k shared directions before retrieval. It is similar in spirit to
"all-but-the-top" post-processing for anisotropic embeddings.

**BM25 fusion**: combines hidden-state similarity with a cheap lexical BM25
score. In Stage 2, alpha=0.75 means 75% hidden-state score and 25% BM25 score.

## Reproducibility Paths

There are three ways to reproduce or inspect the project, depending on how much
compute and storage you want to spend.

### Path A: Read-Only Review

No compute required.

Read:

- [notes/results_log.md](notes/results_log.md): concise experiment log and all
  headline numbers.
- [notes/stage_2_plan.md](notes/stage_2_plan.md): Stage 2 online-evaluation and
  storage plan.
- `results/*.json` and `results/*.md`: full generated analysis outputs, if
  present locally. These are intentionally gitignored.

This path is enough to understand the main result and the reasoning behind it.

### Path B: Reproduce Stage 2 Metrics From Saved Vectors

This is the fastest useful reproduction path. It does not rerun Qwen. It reads
saved compact vectors from `tensors/stage2/9b_4bit_100_p0/` and recomputes
offline analyses.

```bash
cd /path/to/memory_state
source .venv/bin/activate

python scripts/stage2_offline_analyze.py \
  --dump-dir tensors/stage2/9b_4bit_100_p0 \
  --analysis anti_pca_bm25_fusion_combo \
  --layer 30 \
  --position last
```

To rerun all Stage 2 offline analyses over the saved 9B vectors:

```bash
python scripts/stage2_offline_analyze.py \
  --dump-dir tensors/stage2/9b_4bit_100_p0 \
  --analysis all \
  --layer 30 \
  --position last
```

Expected final result for the combo analysis:

```text
anti-PCA k=15 + BM25 fusion alpha=0.75
Recall@5 = 0.766
NDCG@5   = 0.791
```

### Path C: Full Rerun From Data and Models

This reruns model inference. It is slower and requires Apple Silicon + MLX.

Environment setup:

```bash
cd /path/to/memory_state
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Download data and standard models:

```bash
python scripts/download_data.py
python scripts/download_models.py
```

Note: the 9B 4-bit model used in Stage 2 was placed under
`models/Qwen3.5-9B-MLX-4bit/`. If that directory is missing, provide an
equivalent MLX-converted Qwen3.5-9B 4-bit model before running Stage 2 9B
experiments.

Run the Stage 2 sanity checks:

```bash
python scripts/stage2_step1_4bit_sanity.py
python scripts/stage2_step1_5_kv_cache_smoke.py
```

Rerun the 9B 100-subset online evaluation:

```bash
python scripts/stage2_online_eval.py \
  --model-path models/Qwen3.5-9B-MLX-4bit \
  --data data/longmemeval_s_cleaned.json \
  --subset 100 \
  --variants P0 \
  --layers 24-31 \
  --positions last,minus2,minus3,suffix_start,content_end \
  --output-dir tensors/stage2/9b_4bit_100_p0 \
  --result-path results/stage2/stage2_step5_9b_4bit_100_p0.json
```

Then run Path B's offline analysis commands to reproduce the final anti-PCA and
fusion metrics.

### GGUF Base Final-Embedding Probe

`scripts/gguf_final_embedding_eval.py` runs the lightweight llama.cpp probe for
`models/Qwen3.5-9B-Base.i1-Q4_K_M.gguf`. This is a diagnostic for whether the
Base model's final embedding has retrieval signal; it is not equivalent to the
main Stage 2 method, which uses the Instruct model, an internal late layer, and
the suffix-final token.

Local tests found unexpectedly high `llama-embedding` memory usage for unclear reasons, so the GGUF route may be infeasible; also, `Qwen3.5-9B-Base` is already a mid-trained model.

```bash
python scripts/gguf_final_embedding_eval.py \
  --subset 30 \
  --gpu
```

The script first tokenizes all prompts to choose a non-truncating context size,
spot-checks that tokenizer against `llama-tokenize`, estimates memory, and
refuses to start llama.cpp if the estimate exceeds the 8GB target. Its GGUF
defaults use `--parallel 1`, `--no-repack`, `--fit on`, and medium-sized prompt
batches that are split by token budget so llama.cpp never decodes more than
`-b` tokens in one call. The runtime watchdog monitors the llama.cpp child
process's physical footprint/private memory and kills it above 10GB; it does
not use process RSS because macOS can count reclaimable mmap-backed GGUF pages
there. Each batch prints elapsed time, throughput, and ETA so a subset-1 smoke
run can be scaled to the planned 30-instance probe before committing to it.

## Setup Requirements

- macOS on Apple Silicon.
- Python 3.13.
- Plain `venv` + `pip`; the project intentionally does not require `uv`.
- MLX / mlx-lm installed from `requirements.txt`.
- 16GB unified memory was enough for the project, but do not run multiple large
  model jobs at once.
- Keep at least 30GB free disk before running Stage 2 style experiments.
- All data, models, vectors, and results should live inside this repository
  directory.

## Repository Map

| Path | Purpose |
|---|---|
| `MVP_Plan.md` | Original v0 feasibility plan. Useful background, not the final result summary. |
| `Original_Research_Plan.md` | Early research-plan snapshot. |
| `notes/results_log.md` | Main tracked experiment log. Read this for final numbers. |
| `notes/stage_2_plan.md` | Stage 2 execution and storage plan. |
| `scripts/download_data.py` | Downloads LongMemEval cleaned data. |
| `scripts/download_models.py` | Downloads standard local model assets. |
| `scripts/phase1a_eval.py` | Stage 1 / baseline retrieval evaluator. |
| `scripts/analyze_hidden_states.py` | Stage 1 geometry and Tier B analysis toolkit. |
| `scripts/stage2_online_eval.py` | Stage 2 online model runner and compact vector writer. |
| `scripts/stage2_offline_analyze.py` | Stage 2 offline analyzer over saved vectors. |
| `scripts/select_stage2_layers.py` | Copies selected Stage 2 layers into a smaller verified vector store. |
| `scripts/stage3_prompt_sweep.py` | Stage 3 prompt-variant encoder/evaluator. |
| `scripts/stage3_offline_analyze.py` | Stage 3 offline prompt-sweep leaderboard over merged vectors. |
| `scripts/stage3_merge_stores.py` | Stage 3 multi-machine vector-store merge utility. |
| `scripts/stage3_merged_store_check.py` | Stage 3 merged-store self-consistency checker. |
| `scripts/stage3_embedding_eval.py` | Stage 3 embedding-model counterpart evaluator. |
| `scripts/gguf_final_embedding_eval.py` | Runs the GGUF Base-model final-embedding approximation with llama.cpp. |
| `src/hidden_state/` | MLX / transformers hidden-state extraction utilities. |
| `src/stage2/vector_store.py` | Compact Stage 2 vector storage. |
| `src/eval/longmemeval_metrics.py` | Recall@k / NDCG / bootstrap metrics. |
| `data/` | Local LongMemEval cleaned JSON files. Gitignored. |
| `models/` | Local model weights. Gitignored. |
| `tensors/stage1/`, `tensors/stage2/`, `tensors/stage3/` | Saved hidden-state/vector artifacts, organized by stage. Gitignored. |
| `results/stage1/`, `results/stage2/`, `results/stage3/` | Per-run JSON/markdown outputs, organized by stage. Gitignored. |

## Current Local Artifacts

The key local tensor artifacts are listed below. The original Stage 1 dump
archive now lives at `tensors/stage1/dump_v1/`.

| Artifact | Role |
|---|---|
| `tensors/stage1/dump_v1/` | Stage 1 2B bf16 Tier A archive. |
| `tensors/stage2/2b_4bit_100_p0_selected/` | Stage 2 2B 4-bit comparison vectors, reduced to layers 20-23 after exact verification. |
| `tensors/stage2/9b_4bit_100_p0/` | Stage 2 final 9B 4-bit vectors used by offline analyses. |
| `tensors/stage3/prompt_sweep/merged_subset0-100_cache2gb_logits256/` | Stage 3 merged prompt-sweep vectors for instances 0-99. |
| `tensors/stage3/embedding_eval/qwen3_embedding_8b_dwq_subset0-100/` | Stage 3 Qwen3 embedding-eval stored outputs. |

The selected 2B store keeps the late layers that carried the useful retrieval
signal while dropping earlier layers from the larger confirmation dump. It was
created as a new directory, verified chunk-by-chunk against the source bf16
slices, sanity-checked with `stage2_offline_analyze.py`, and only then replaced
the old local `2b_4bit_100_p0_confirm` artifact.

The temporary `tensors/stage2/9b_4bit_30_layer_scan/`,
`tensors/dump_preview/`, and `models/Qwen3.5-2B-hf/` artifacts were cleanup
candidates after their results had been summarized. They were removed after
human approval; the logged results remain in `notes/results_log.md` and
`results/stage1/` and `results/stage2/`.

## Known Limitations

- The headline parity is with **Qwen3-Embedding-0.6B**. Qwen3-Embedding-4B and
  Qwen3-Embedding-8B have not been evaluated here.
- The main reported subset is 100 LongMemEval-S instances, with 94 scored
  questions after abstention filtering. Full 500-instance validation remains a
  stronger future check.
- LongMemEval mostly tests explicit long-term memory retrieval: facts,
  multi-session aggregation, temporal reasoning, and knowledge updates. It is
  not primarily a preference-reasoning or recommender benchmark.
- Stage 3 prompt-sweep scores should be read with that chatbot-memory caveat:
  persona/preference-style prompts can be useful even when this evidence-heavy
  benchmark ranks them below fact/topic prompts.
- The final best R@5 uses BM25 fusion. The best 9B hidden-only result is
  Recall@5 = 0.755.
- NDCG@5 still trails Qwen3-Embedding-0.6B: final Stage 2 is 0.791 vs 0.809.
- 4-bit quantization changes geometry slightly. Stage 2 sanity checks passed,
  but the 2B 4-bit result was several points below the 2B bf16 result.
- KV cache is used as a short-term inference acceleration mechanism. It is not
  stored as the long-term memory index because it is too large and
  model-specific.

## FAQ

### Why is the best layer not the final layer?

The useful layer is just before the model's largest final task-specific
transformation. For 2B, this is around layer 22/24; for 9B, it is around layer
30/32. Tier B drift analysis showed the largest representation change happens
in the final block, and the pre-change vector is more useful for retrieval than
the final token-prediction-calibrated state.

### Why does anti-PCA help?

Prompt-final hidden states share a large common direction caused by the fixed
suffix and corpus geometry. Anti-PCA removes the top shared components, exposing
the smaller semantic differences that matter for retrieval.

### Why use BM25 fusion if the goal is LLM-native memory?

BM25 is cheap and complementary: it contributes exact lexical evidence while
the hidden state contributes semantic/session routing. In Stage 2, alpha=0.75
fusion matched Qwen3-Embedding-0.6B on Recall@5.

### Why is Recall@5 strict?

LongMemEval's `recall_all@5` requires **all** gold evidence turns to appear in
the top 5. Multi-gold questions are therefore much harder than single-gold
questions, even if the retriever finds the correct session.

### Can I delete tensors and still reproduce the result?

If you delete `tensors/stage2/9b_4bit_100_p0/`, you can still read the logged
result, but you cannot cheaply rerun the Stage 2 offline analyses. You would
need to rerun Qwen3.5-9B inference.

### Is this ready as a production memory system?

Not yet. It is a feasibility result for memory retrieval. A product system
would still need indexing, update policy, privacy controls, stronger embedding
baselines, and evaluation on preference/recommendation-style memory tasks.
