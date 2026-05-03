# MVP Plan: Inference-Native Memory State

## 1. Scope

This document defines the v0 plan for testing whether a generative LLM's own final hidden state can work as a retrieval vector for long-term conversational memory.

The original research idea is: after reading a memory source, ask the same LLM to produce a very short memory key, then save the model's internal hidden state at that key-generation point. At query time, ask the model to produce the same kind of one-word key and retrieve by cosine similarity between hidden states.

Narrowed claim: this MVP only tests **training-free native hidden-state retrieval feasibility**. It does not claim to replace production RAG, external embedding models, or long-context full attention.

*Why*: The core uncertainty is not whether this can be engineered, but whether hidden states from different contexts are stable and comparable enough for direct retrieval.

## 2. Core Hypothesis

The hypothesis to falsify:

> Final-layer hidden states produced at the one-word summary position preserve enough context-specific information to rank relevant memory sessions above irrelevant sessions by cosine similarity.

This means the test is about retrieval quality, not answer generation quality.

*Why*: If retrieval fails, downstream QA can still look good for unrelated reasons. Retrieval-only metrics isolate whether the vector representation itself works.

## 3. Method Definition

### 3.1 Prompt Template

For memory/session indexing:

```text
<context>
请用一个词来summarize上面这段文字，这个词是：“
```

For query encoding:

```text
<query>
请用一个词来summarize上面这段文字，这个词是：“
```

The query is treated as the text to summarize into a one-word retrieval key.

*Why*: Keeping the suffix identical reduces prompt-template artifacts between memory vectors and query vectors.

### 3.2 Hidden State Position

Use option **A**:

- run one forward pass over the prompt;
- take the final-layer, post-norm hidden state at the prompt's last position;
- this is the state that predicts the next token, i.e. the first one-word summary token;
- do not feed the generated token back into the model to get a second hidden state.

*Why*: This is the simplest and cheapest definition. It captures the model state immediately before the summary token is emitted, and avoids mixing in the model's later observation of its own generated token.

### 3.3 Vector Normalization and Retrieval

Default vector:

- final-layer post-norm hidden state;
- last prompt position only;
- convert to float32 for storage/scoring;
- L2 normalize;
- cosine similarity for retrieval.

*Why*: L2-normalized cosine is the standard first-pass choice for dense retrieval and avoids raw hidden-state norm dominating ranking.

### 3.4 Pooling

v0 uses only last-position pooling.

Mean pooling over prompt positions is a later ablation, not part of v0.

*Why*: The research question is about the one-word summary generation point. Adding pooling now would make the first experiment harder to interpret.

## 4. Benchmark Strategy

### 4.1 Main Benchmark: LongMemEval

Use LongMemEval as the main benchmark.

Relevant settings:

- LongMemEval-M, session-level: official BM25/Contriever anchor numbers exist.
- LongMemEval-S, session-level: feasible for Qwen3.5-2B hidden-state evaluation on a 16GB Mac.
- LongMemEval-S, round-level: fallback if S/session is too easy.

*Why*: LongMemEval has evidence labels and retrieval-only metrics. This is required for testing vector retrieval directly. LoCoMo, MemoryAgentBench, EngramaBench, and similar newer memory benchmarks are useful later, but they do not give the same combination of retrieval-only labels and official BM25/Contriever anchors for this MVP.

### 4.2 Official Metrics

Use the LongMemEval retrieval metrics:

- `recall_all@5`;
- `ndcg_any@5`;
- optionally `recall_all@10` and `ndcg_any@10`.

Do not report MRR as an official LongMemEval replication metric.

*Why*: The official LongMemEval retrieval scripts report recall and NDCG variants, not MRR. Matching the official metric definition is necessary for pipeline validation.

### 4.3 Why Not Start With 2026 Benchmarks

MemoryAgentBench, EngramaBench, RAGRouter-Bench, MTRAG-UN, and related 2026 benchmarks are backburner for v1+.

*Why*: The current MVP needs a retrieval-only benchmark with evidence labels and reproducible public retrieval baselines. More recent benchmarks may be harder or more agentic, but if they measure end-to-end QA accuracy, they cannot cleanly test whether hidden-state vectors retrieve the right memory.

## 5. Baselines

### 5.1 Pipeline Anchor Baselines

Use BM25 and `facebook/contriever` to replicate official LongMemEval-M/session-level numbers:

- BM25: Recall@5 about `0.634`, NDCG@5 about `0.516`;
- Contriever: Recall@5 about `0.723`, NDCG@5 about `0.634`.

The expected tolerance for full-run replication is about +/- 2 percentage points.

*Why*: These baselines validate that local data loading, candidate construction, evidence labels, abstention handling, and metric code are correct before testing the proposed method.

### 5.2 Fair Modern Embedding Baseline

Add `Qwen3-Embedding-0.6B` as a modern long-context embedding baseline for LongMemEval-S.

*Why*: Official Contriever uses BERT-length truncation and is mainly a replication anchor. A longer-context Qwen embedding model is a fairer comparison when the hidden-state method reads longer session text.

### 5.3 Contriever Input Caveat

The official LongMemEval Contriever baseline:

- uses user turns from each session;
- tokenizes with truncation;
- effectively uses the model's BERT-style maximum length, around 512 tokens;
- does not chunk full 3k-token sessions.

*Why*: If our method reads fuller sessions, a direct win over Contriever may reflect input-length advantage rather than hidden-state quality. This caveat must be visible in all result summaries.

## 6. Model and Framework

### 6.1 Main LLM

Use `Qwen/Qwen3.5-2B` as the v0 LLM.

Run fp16 first.

*Why*: Qwen3.5-2B is small enough for a 16GB Apple Silicon Mac while still being a current Qwen3.5-family model. Larger models are not practical for session-level indexing on this machine.

Fallback: if Qwen3.5-2B is unavailable, gated, or not loadable through the selected MLX path, use `Qwen/Qwen3-1.7B` with the same fp16 and hidden-state wrapper approach.

*Why*: The experiment should continue with a smaller Qwen-family model rather than blocking on a packaging or architecture issue unrelated to the core retrieval hypothesis.

### 6.2 Main Framework: mlx-lm

Use `mlx-lm` as the primary inference path.

Do not fork mlx-lm and do not monkey-patch it in v0. Implement a local wrapper that directly calls the internal base model to obtain the final post-norm hidden state.

Expected Qwen3.5 MLX path:

```python
hidden = model.language_model.model(input_ids)
vec = hidden[:, -1, :]
logits = model.language_model.lm_head(hidden)[:, -1, :]
```

If weights are tied, use the model's tied embedding projection path instead of `lm_head`.

The wrapper should auto-detect the model layout, including multimodal-style wrappers such as `model.language_model.model` and text-only layouts such as `model.model`.

*Why*: The project needs to learn how to use mlx-lm for future software development. A wrapper is simpler and safer than modifying package internals, while still exposing the hidden state we need.

### 6.3 Sanity Check Framework: Transformers + MPS

Use HuggingFace Transformers + MPS only for a small sanity check.

Procedure:

- run 10-20 prompts through both mlx-lm and Transformers;
- compare next-token top predictions;
- compare final hidden-state cosine similarity;
- target cosine: greater than `0.99` for fp16-vs-fp16 runs.

*Why*: Hidden-state extraction is easy to get subtly wrong. A second implementation catches wrong layer, wrong norm position, tokenizer mismatch, or tied-head mistakes before expensive runs.

### 6.4 Precision Policy

Default: fp16.

Backburner fallback: 4-bit quantized MLX weights only if fp16 does not fit.

Do not use fp8 for v0 on Mac.

*Why*: This study measures hidden-state geometry. Quantization can change hidden-state distributions, so fp16 is the clean first measurement. fp8 support on Mac/MLX is not the practical path for this experiment.

## 7. Environment Strategy

Use a local Python virtual environment with plain pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Do not use `uv` for v0.

*Why*: The user prefers the simplest dependency setup even if installation is slower.

Keep all downloaded models and datasets inside the repo directory:

```bash
export HF_HOME="$PWD/.hf_cache"
```

Recommended ignored paths:

```gitignore
.venv/
.hf_cache/
data/raw/
results/
__pycache__/
*.pyc
.DS_Store
```

*Why*: The machine environment should stay clean. Removing the repo-local virtual environment, model cache, raw data, and results should fully clean up local artifacts.

## 8. Phased Execution Plan

### Phase 0: Hidden-State Extraction Sanity Check

Goal:

- create the local environment;
- install mlx-lm and Transformers in `.venv`;
- implement the mlx-lm hidden-state wrapper;
- compare against Transformers + MPS on 10-20 prompts.

Go/no-go:

- next-token predictions should broadly match;
- hidden-state cosine should be greater than `0.99` for fp16-vs-fp16;
- if this fails, stop and debug before any benchmark work.

*Why*: If the hidden vector is extracted from the wrong location, all retrieval results are meaningless.

### Phase 1a: Official Pipeline Replication

Dataset:

- LongMemEval-M;
- session-level retrieval.

Scale:

- 500 questions/instances;
- about 500 candidate sessions per question;
- about 250k candidate session evaluations in total.

Methods:

- BM25;
- Contriever.

Execution:

- start with a 100-instance subset for development;
- run full 500-instance evaluation once the subset pipeline is stable.

Go/no-go:

- full-run BM25 and Contriever should land near official LongMemEval-M/session anchor numbers, within about +/- 2 percentage points for Recall@5;
- if not, stop and inspect data parsing, candidate construction, abstention skipping, and metric implementation.

*Why*: This phase proves the local retrieval evaluation setup is trustworthy before testing the proposed method.

### Phase 1b: Local Baselines for the Final Setting

Dataset:

- LongMemEval-S;
- session-level retrieval.

Methods:

- BM25;
- Contriever;
- Qwen3-Embedding-0.6B.

Goal:

- establish local baseline numbers for the same dataset where the Qwen3.5-2B hidden-state method will run.

Trigger:

- if Qwen3-Embedding-0.6B exceeds Recall@5 `0.90` on S/session, consider S/session too easy and move Phase 2 to S/round.

*Why*: LongMemEval-S is computationally feasible for Qwen hidden-state indexing, but it lacks official BM25/Contriever anchor numbers. Local baselines tell us whether there is enough headroom.

### Phase 2: Proposed Method v0

Dataset:

- LongMemEval-S/session by default;
- LongMemEval-S/round if S/session is too easy.

Method:

- Qwen3.5-2B with mlx-lm;
- one forward pass per candidate memory text and per query;
- prompt-last-position final hidden state;
- L2 normalize and cosine retrieve.

Execution:

- start with a 50-instance subset;
- scale to the full 500 instances only after output format, caching, and metrics are stable.

Comparison:

- compare against Phase 1b baselines;
- treat Contriever as a pipeline anchor, not the fairest long-context comparison;
- treat Qwen3-Embedding-0.6B as the primary embedding comparison.

*Why*: The method is expensive because every candidate session needs an LLM forward pass. S/session or S/round is the practical Mac-scale testbed.

### Phase 3: Difficulty Escalation

Trigger:

- S/session is too saturated, especially if strong embedding retrieval is above Recall@5 `0.90`.

Next setting:

- LongMemEval-S/round.

Do not move the proposed method to LongMemEval-M in v0.

*Why*: Round-level retrieval is harder and still computationally feasible. LongMemEval-M would require too many Qwen3.5-2B forwards on a 16GB Mac.

## 9. Expected Time Budget

Rough estimates for a 16GB Apple Silicon Mac:

- LongMemEval-M/session BM25 full run: about 20-90 minutes;
- LongMemEval-M/session Contriever full run: about 3-10 hours;
- LongMemEval-S/session Qwen3.5-2B hidden-state full run: potentially many hours to around a day;
- Qwen method development should always start with 50-instance subsets.

*Why*: Baseline replication is hours-level and feasible. Qwen hidden-state indexing is the expensive step, so subset-first development is mandatory.

## 10. Backburner Items

The following are intentionally out of v0:

- multi-key memory, including 100-token summary hidden states;
- multi-view key generation;
- collision-key stress tests;
- raw input-embedding diagnostic baseline;
- shuffled hidden-state negative control;
- fp16 vs q4 hidden-state distribution ablation;
- sentinel-token pooling;
- mean-pooling ablations;
- Qwen3.5-27B or other large-model experiments;
- evaluating the proposed method on LongMemEval-M;
- MemoryAgentBench;
- EngramaBench;
- RAGRouter-Bench;
- MTRAG-UN;
- end-to-end QA generation after retrieval.

*Why*: Each item may be useful later, but adding them now would blur the first question: can one training-free prompt-position hidden state work as a retrieval vector at all?

## 11. Decision Log

Decision: use LongMemEval as the main benchmark.  
*Why*: It has retrieval-only evidence labels and official BM25/Contriever anchor numbers.

Decision: use LongMemEval-M/session for official baseline replication, but LongMemEval-S/session or S/round for the proposed method.  
*Why*: M/session has public anchors; S settings are computationally feasible for Qwen3.5-2B hidden-state indexing.

Decision: use Qwen3.5-2B as the LLM.  
*Why*: It is current enough for the research direction and small enough for a 16GB Mac.

Decision: use mlx-lm as the main path.  
*Why*: The user's future software work is expected to use mlx-lm, so this project should learn that path.

Decision: keep Transformers + MPS as a sanity-check path.  
*Why*: It provides an independent way to detect incorrect MLX hidden-state extraction.

Decision: use fp16 first.  
*Why*: The target object is hidden-state geometry, and quantization could change it.

Decision: use plain pip in `.venv`.  
*Why*: The user requested a simple, non-global environment and does not mind slower installation.

Decision: keep model cache and data under the repo, ignored by git.  
*Why*: The computer environment should remain clean and easy to delete.

Decision: treat Contriever as an official anchor, not the fairest final comparator.  
*Why*: Official Contriever uses user-turn-only text and 512-token truncation; Qwen3-Embedding-0.6B is a fairer modern embedding comparator for longer inputs.

Decision: no document or code changes beyond this plan until the plan is reviewed.  
*Why*: The project should lock the experiment design before creating environment files, scripts, or benchmark outputs.
