# Stage 2 Plan

## TL;DR

- Stage 2 no longer uses full Tier B-style tensor dumps. It uses **online evaluation plus compact vector storage**: stream one LongMemEval instance at a time, compute retrieval metrics, write JSON outputs, retain suffix/end Tier A-plus vectors, then release KV cache.
- Main upgrades: 2B 4-bit validation, prompt-template sweep, KV-cache reuse for suffix variants, and conditional Qwen3.5-9B-4bit scale-up.
- Stage 1 best practices carry forward: suffix-end vectors, late-layer scan, centered cosine / anti-PCA, query-only transform checks, and optional BM25 fusion.

## Current Assets

- `notes/results_log.md`: compact record of Stage 1 / Phase 2-deep / Tier B findings.
- `notes/stage_2_plan.md`: this online-eval Stage 2 plan.
- `scripts/analyze_hidden_states.py`: archived Stage 1 analysis code, including Tier B lean/multi-slice helpers.
- `tensors/dump_v1/tier_a/`: Stage 1 2B bf16 Tier A dump, retained as comparison anchor.
- `tensors/dump_v1/tier_b/`: Stage 1 all-position dump, approved for deletion after this plan review.
- `results/`: full generated JSON/markdown analysis outputs, gitignored.
- `models/Qwen3.5-2B-bf16/`: Stage 1 anchor model.
- `models/Qwen3.5-9B-MLX-4bit/`: user-provided 9B 4-bit MLX model.

Stage 1 conclusions to preserve:

- Best hidden-only turn R@5: about `0.681`.
- Best fusion turn R@5: about `0.713`.
- Best hidden-only session_hit@5: about `0.947`.
- Method is best framed as a strong session-level memory router with weaker turn-level turn disambiguation.
- Useful hidden states are suffix-end / prompt-final vectors; content positions are weak.
- Layer 22 for 2B is useful because it sits before the largest final-block drift at 22->23.

## Verified 9B Model Facts

Verified from local `models/Qwen3.5-9B-MLX-4bit/config.json` and the public Qwen config:

- `num_hidden_layers`: `32`
- `hidden_size`: `4096`
- `full_attention_interval`: `4`
- layer pattern: hybrid Qwen3.5 text model, with three `linear_attention` layers followed by one `full_attention` layer repeatedly.
- `model_type`: `qwen3_5_text` inside `text_config`.

Implication:

- Do **not** assume 2B layer 22 transfers directly.
- Use 2B priors only as scan anchors:
  - 75% layer prior: around layer `24` of 32.
  - 92% layer prior: around layer `29` of 32.
  - last-8 scan: layers `24-31`.

Reference: Qwen/Qwen3.5-9B config on HuggingFace: https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/config.json

## Deprecated Dump-Based Plan

The first Stage 2 plan proposed dumping all-layer Tier A tensors for every prompt variant and for 9B subsets. That is now deprecated.

Why it changed:

- User wants to avoid another large dump.
- Stage 1 taught us which positions and layer ranges matter.
- Prompt variants share the same candidate prefix, so KV-cache reuse can avoid recomputing long prefixes.
- Full all-position tensors are not required for Stage 2 decisions, but compact suffix/end vectors are worth keeping because they are small enough and save future reruns.

Do not execute dump-based prompt sweeps unless online evaluation fails and human explicitly approves a fallback.

## Storage Budget

Target practical free-space budget: about 30GB after deleting Tier B. Stage 2 should not recreate Tier B-style all-position dumps, but it should keep compact Tier A-plus vectors so future analysis does not require rerunning the model.

### Stored Vector Policy

Store compact suffix/end vectors with this tensor layout:

```text
states: (n_prompts, n_layers, n_positions, hidden_dim) bf16
```

Positions to store:

| Position | Reason |
|---|---|
| `last` | Stage 1 robust default |
| `minus2` | Tier B showed possible R@5 edge |
| `minus3` | Cheap suffix-end continuity check |
| `suffix_start` | Prompt-template diagnostic |
| `content_end` | Negative control / no-suffix comparison |

Layer policy:

| Model / step | Layers to store | Reason |
|---|---|---|
| 2B Step 2 prompt sweep | all 24 layers | Cheap enough; prompt changes may move sweet spot |
| 2B Step 3 winning prompt 100-subset | all 24 layers | Long-term comparison artifact |
| 9B Step 4 30-subset layer scan | all 32 layers | Needed to find 9B-specific sweet spot |
| 9B Step 5 100-subset confirmation | selected late/useful layers only | Avoid 30GB+ output |

### Long-Term vs Temporary Dumps

Long-term keep:

| Artifact | Estimated size | Note |
|---|---:|---|
| Existing Stage 1 Tier A | ~2.4GB | Comparison anchor |
| 2B Step 3 winning prompt 100-subset | ~3.5GB | All layers × 5 positions |
| 9B Step 5 100-subset selected-layer dump | ~10GB | Selected late/useful layers |

Temporary / auto-cleanable after approval:

| Artifact | Estimated size | Cleanup rule |
|---|---:|---|
| 2B Step 2 prompt sweep, 30-subset, 4 prompts | ~14GB | Ask approval to delete after Step 3 succeeds |
| 9B Step 4 30-subset full-layer scan | ~10GB | Ask approval to delete after Step 5 succeeds |

Storage table:

| Asset / output | Estimated size | Keep during Stage 2? | Note |
|---|---:|---|---|
| Current Tier A dump | ~2.4GB | Yes | Stage 1 comparison anchor |
| Current Tier B dump | ~29GB | No, after approval | Findings archived in `notes/results_log.md` |
| Qwen3.5-2B bf16 | ~4.5GB | Yes | Anchor model |
| Qwen3.5-2B 4bit | ~1.6-1.8GB | Yes, if sanity passes | Download into `models/` |
| Qwen3.5-9B 4bit | ~6GB | Yes | Already in `models/` |
| Stage 2 compact vector chunks | varies | Yes / temp by rule above | Chunked safetensors |
| Stage 2 metrics JSON | <100KB/run | Yes | Gitignored results + summarized in log |
| Stage 2 prediction JSON | Usually <10MB/run | Yes | For metric recomputation |

Storage rules:

- Delete only `tensors/dump_v1/tier_b/`; preserve Tier A, `manifest.json`, results, and notes.
- Do not store full all-position tensors during Stage 2.
- Store compact Stage 2 vectors in chunked safetensors under `tensors/stage2/`.
- Chunk target size: about `512MB`, with dynamic prompt count per chunk.
- Metrics/predictions JSON are still required for every run.
- Before each run, estimate output size and current free space. If projected free space after completion is `<20GB`, stop and request approval.
- Step 3 success should trigger a human approval checkpoint to delete Step 2 temporary dumps.
- Step 5 success should trigger a human approval checkpoint to delete Step 4 temporary dumps.

Manifest schema for each Stage 2 vector set:

```json
{
  "created_utc": "...",
  "git_commit": "...",
  "model_path": "...",
  "tokenizer_path": "...",
  "prompt_variant": "P0|P1|P4|P5",
  "positions": ["last", "minus2", "minus3", "suffix_start", "content_end"],
  "layers": [0, 1, "..."],
  "score_modes_evaluated": ["cosine", "centered_cosine", "anti_pca_k10", "query_only_anti_pca_k10"],
  "chunks": [{"file": "chunk_0000.safetensors", "prompt_ids": ["..."]}],
  "prompts": {
    "prompt_id": {
      "instance_index": 0,
      "question_id": "...",
      "role": "query|candidate",
      "candidate_id": "...",
      "is_gold": false,
      "token_count": 0,
      "resolved_positions": {"last": -1},
      "chunk_file": "chunk_0000.safetensors",
      "chunk_index": 0
    }
  }
}
```

## Execution Order

### Step 0: Storage Cleanup

Input:

- `tensors/dump_v1/tier_b/`.
- `notes/results_log.md` with all Tier B findings.

Action:

- After human approval, delete only Tier B all-position tensor files.
- Preserve Tier A chunks, `manifest.json`, all result summaries, and notes.

Output:

- About 29GB freed.

Go/No-Go:

- Go: Tier B conclusions are in `notes/results_log.md`.
- No-go: any remaining planned experiment needs all-position Tier B tensors.

Human approval checkpoint:

- Required before deletion.

### Step 1: 2B 4-bit Sanity Validation

Input:

- `models/Qwen3.5-2B-bf16/`.
- 2B 4-bit MLX model downloaded into `models/`.

Action:

- Compare bf16 vs 4-bit hidden-state vectors on 10-20 prompts.
- Run a tiny retrieval smoke test if vector cosine passes.
- Use the same suffix-end position and late-layer settings as Stage 1.

Output:

- Hidden cosine mean/min.
- Top-token overlap.
- Small retrieval delta vs bf16.

Go/No-Go:

- Go if hidden cosine mean `> 0.98` and min `> 0.97`.
- Go if small retrieval R@5 degradation is `<= 3pp`.
- No-go if geometry is unstable or retrieval drops more than `3pp`.
- If no-go, keep 2B prompt sweeps on bf16 and treat 9B-4bit results as scale-only exploratory.

Estimated time:

- About 30 minutes, excluding model download.

Human approval checkpoint:

- Required before using 4-bit as a default Stage 2 path.

### Step 1.5: KV-Cache Correctness Smoke

Input:

- 2B model that passed Step 1, or 2B bf16 fallback.
- 10 prompts with several suffix variants.

Action:

For each `text + suffix`:

1. Run full forward over `text + suffix`.
2. Run prefix forward over `text`, keeping model cache.
3. Deep-copy the prefix cache.
4. Run suffix-only forward from the copied cache.
5. Compare suffix-end hidden vectors from full vs cached path.

Implementation requirement:

- Use `model.make_cache()` rather than hand-constructing KV cache. Qwen3.5 uses mixed cache types: `ArraysCache` for linear/SSM layers and `KVCache` for full-attention layers.
- Use `copy.deepcopy(prefix_cache)` per suffix variant.
- Never reuse a suffix-mutated cache for another suffix.

Output:

- Cosine mean/min between full-forward and cached-forward vectors.

Go/No-Go:

- Go if all prompt vector cosines are `> 0.998`.
- Warning if any are between `0.99` and `0.998`; inspect before continuing.
- No-go if any are `< 0.99`; fallback to full forward for smaller subsets.

Fallback:

- Do not do cache hacking.
- Use full forward with subset reduced to 20 instances.

Human approval checkpoint:

- Required before KV-cache path is used for prompt sweep.

### Step 2: 2B Online Prompt Sweep, 30-Instance Exploration

Input:

- LongMemEval-S/round 30-instance subset.
- 2B model selected by Step 1.
- Prompt variants P0/P1/P4/P5.

Action:

Stream by instance:

```text
for instance:
    for candidate:
        prefill candidate text once
        run P0/P4/P5 suffixes from copied prefix cache
        use prefix-final vector for P1 no-suffix
    encode query variants the same way
    compute rankings and metrics
    append compact vectors to chunk buffers
    flush chunks as needed
    release KV cache
```

For each prompt variant:

- Evaluate `last` and `minus2` suffix-end positions.
- Evaluate late-layer candidates, not full layer dump.
- Use Stage 1 score modes:
  - cosine;
  - centered cosine / per-instance mean removal;
  - anti-PCA k=10;
  - query-only anti-PCA k=10.
- Do not run mean/max pooling, concat, RRF, or diagonal slices.

Output:

- Prompt comparison table on 30 instances.
- Best prompt candidate(s) for 100-instance confirmation.
- Small JSON per run.
- Temporary compact vector chunks for all prompt variants.

Go/No-Go:

- Go to 100-instance confirmation if a prompt improves turn R@5 by `>= 3pp`, session_hit@5 by `>= 1pp`, or materially improves NDCG@5.
- If no prompt improves, keep P0 and document prompt robustness.

Estimated time:

- Target: about 30-60 minutes if KV cache works.
- If full-forward fallback is needed: reduce to 20 instances.

Human approval checkpoint:

- Required before 100-instance prompt confirmation.

### Step 3: 2B Prompt Confirmation, 100 Instances

Input:

- Best prompt from Step 2.
- P0 current prompt as anchor.

Action:

- Run online evaluation for best prompt and P0 on the same 100-instance Stage 1 subset.
- Evaluate the same late-layer / suffix-position / score-mode grid used in Step 2.
- Save compact suffix/end vectors for the winning prompt as a long-term reusable artifact.
- Do not save full all-position tensors.

Output:

- Confirmed 2B prompt result.
- Decision: update default prompt or keep P0.
- Long-term compact vector chunks for the winning prompt.

Go/No-Go:

- Accept new prompt if it preserves/improves session_hit@5 and improves turn R@5 or NDCG@5 by at least `3pp`.
- Reject if 30-instance gain disappears at 100.

Estimated time:

- About 1-2 hours with KV cache; longer with fallback.

Human approval checkpoint:

- Required before using selected prompt for 9B work.

### Step 4: 9B-4bit Smoke + Late-Layer Scan

Input:

- `models/Qwen3.5-9B-MLX-4bit/`.
- Selected prompt from Step 3.
- 30-instance subset.

Action:

- Load 9B model.
- Verify wrapper compatibility:
  - text model layout;
  - layer count = 32;
  - hidden dimension = 4096;
  - hybrid cache via `model.make_cache()`.
- Run KV-cache correctness smoke on 9B.
- Scan:
  - last-8 layers: `24-31`;
  - 75% prior: layer `24`;
  - 92% prior: layer `29`;
  - final post-norm if available.
- Evaluate both `last` and `minus2` suffix-end positions.
- Use centered cosine and anti-PCA / query-only anti-PCA.

Output:

- 9B compatibility note.
- 9B subset sweet-spot layer / position / score mode.
- Metrics JSON.
- Temporary compact vector chunks for layer/position analysis.

Go/No-Go:

- Go if wrapper and cache smoke work and memory remains near target.
- Go if any one is met:
  - turn R@5 `>= 0.731`;
  - session_hit@5 `>= 0.970`;
  - NDCG@5 `>= 0.60`.
- Stop if turn R@5 is at least `3pp` worse than the 2B best configuration.

Estimated time:

- About 1-2 hours if KV cache works.

Human approval checkpoint:

- Required before 9B 100-instance run.

### Step 5: 9B-4bit 100-Instance Evaluation

Input:

- 9B model that passed Step 4.
- Best prompt / layer / position / score mode from Step 4.

Action:

- Run online 100-instance evaluation.
- Compare against:
  - 2B best;
  - BM25;
  - Qwen3-Embedding-0.6B;
  - hidden+BM25 fusion if applicable.

Output:

- Final Stage 2 9B comparison.
- Long-term compact vector chunks for selected 9B layers.

Go/No-Go:

- Keep 9B as serious candidate only if it improves over 2B on turn R@5, session_hit@5, or NDCG@5 by Step 4 thresholds.
- If 9B does not improve, document that larger model scale does not automatically improve hidden-state retrieval geometry.

Estimated time:

- Several hours.

Human approval checkpoint:

- Required before any 500-instance validation.

### Step 6: Stage 2 Summary

Input:

- Step 1-5 results.

Action:

- Update `notes/results_log.md`.
- Add a concise Stage 2 conclusion.
- Decide whether a 500-instance run is justified.

Output:

- Human-readable Stage 2 summary.

Go/No-Go:

- Go to 500-instance validation only if Stage 2 finds a robust improvement over Stage 1 and storage/time are acceptable.

Human approval checkpoint:

- Required before 500-instance validation.

## Prompt Variants

Batch 1 only:

| ID | Template | Vector source | Hypothesis |
|---|---|---|---|
| P0 | `\n请用一个词来summarize上面这段文字，这个词是：“` | suffix-end | Stage 1 anchor |
| P1 | no suffix | prefix-final | Test whether summary instruction is necessary |
| P4 | `\n用于记忆检索的关键词是：` | suffix-end | Retrieval-specific Chinese instruction |
| P5 | `\nMemory key:` | suffix-end | Minimal English deployment-friendly instruction |

Rules:

- P0/P4/P5 must use symmetric memory/query suffixes.
- P1 is a stress test; final token varies by input text and should not be overinterpreted.
- For suffix variants, evaluate both `last` and `minus2`.
- Do not run asymmetric prompts in Batch 1.

Conditional Batch 2:

| ID | Template | Trigger |
|---|---|---|
| P2 | `\n关键词：` | If P5 minimal prompt helps |
| P3 | `\nTopic:` | If P5 helps and language choice matters |
| P6 | asymmetric memory/query prompts | Only after symmetric prompts are understood |

## Score Modes

Every prompt/model run should evaluate the small Stage 1 best-practice grid:

| Score mode | Reason |
|---|---|
| cosine | raw baseline |
| centered cosine | Stage 1 strong geometry fix |
| anti-PCA global k=10 | Stage 1 best hidden-only config |
| query-only anti-PCA global k=10 | Deployment-friendly, nearly as strong as both-sided |
| optional BM25 fusion α=0.5 | Orthogonal lexical signal, only after hidden-only result |

Do not repeat mean/max pooling, layer concat, RRF, z-score, whitening, or diagonal slice unless a new Stage 2 result specifically motivates them.

## Online Evaluator Design

The Stage 2 implementation should be a new online evaluator with a compact vector writer. It is **not** a Tier B-style full tensor dumper: it stores only suffix/end vectors for selected layers and positions.

Suggested modules:

- `src/hidden_state/cached_suffix_extractor.py`
  - `prefill_prefix(text_tokens) -> PrefixState`
  - `encode_suffix_variants(prefix_state, suffixes, target_layers, positions) -> vectors`
  - `encode_prompt_variants(text, variants, target_layers, positions) -> vectors`
- `scripts/stage2_online_eval.py`
  - loads data;
  - streams instance by instance;
  - writes predictions/metrics JSON;
  - appends compact suffix/end vectors to chunked safetensors;
  - never stores all-position hidden tensors.
- `src/stage2/vector_store.py`
  - `Stage2VectorWriter`
  - buffers `states: (n_prompts, n_layers, n_positions, hidden_dim)` in bf16;
  - flushes dynamic chunks near the `512MB` target;
  - writes manifest rows with tokenizer path, score modes, timestamp, and git commit.

Correctness invariant:

- Cached suffix vectors must match full-forward vectors before any metrics are trusted.
- The vector writer manifest row count must match the number of rows in written `states` chunks.
- Compact vector storage is a reusable artifact; retrieval metrics must be reproducible from the prediction JSON even if temporary vector chunks are later deleted.

## Memory Budget

Target peak: about `8GB`, hard caution above `10GB`.

Expected contributors:

- 9B-4bit weights: about `6GB`.
- One prefix cache: candidate-length dependent, expected tens to a few hundred MB.
- One instance vectors: a few MB to tens of MB.
- One vector chunk buffer: target `<=512MB`; lower to `256MB` if 9B memory pressure appears.
- Python/MLX overhead: leave 2GB margin.

Runtime rules:

- One MLX model-forward process at a time.
- No background diagnostic jobs while model inference is running.
- Clear MLX cache between large runs.
- Check projected disk free space before each run; stop before starting if completion would leave `<20GB` free.
- If memory exceeds 10GB or swap pressure appears, stop and reduce subset size.

## Go/No-Go Criteria Summary

| Decision | Go criteria | No-go criteria |
|---|---|---|
| Delete Tier B | Tier B conclusions summarized | Any upcoming analysis still needs full positions |
| 2B 4-bit model | cosine mean >0.98, min >0.97, retrieval drop <=3pp | geometry unstable or retrieval drop >3pp |
| KV cache path | all full-vs-cache cosines >0.998 | any cosine <0.99 |
| Prompt replacement | 100-instance improvement >=3pp turn R@5 or meaningful NDCG/session gain | 30-subset gain disappears at 100 |
| 9B subset | turn R@5 >=0.731 or session_hit@5 >=0.970 or NDCG@5 >=0.60 | turn R@5 >=3pp below 2B best |
| 500-instance validation | Stage 2 finds robust improvement | no robust improvement or storage/time unacceptable |

## Risk Register

| Risk | Mitigation |
|---|---|
| KV cache fork mutates shared state | Full-vs-cache smoke; `copy.deepcopy(prefix_cache)` per suffix |
| Qwen3.5 hybrid cache differs from simple KV | Use `model.make_cache()` only |
| KV cache path fails | Full-forward fallback on 20-instance subset |
| Two MLX jobs contend for unified memory | Run all model-forward tasks serially |
| 9B quantized model layout differs from 2B | Wrapper smoke before metrics |
| Prompt sweep changes best layer | Scan late layers; do not hardcode 2B layer 22 |
| P1 no-suffix final token varies | Treat P1 as exploratory stress test |
| 100-instance prompt tuning overfits | Explore on 30, confirm on 100 |
| 9B slower or memory-heavy | Start with 30 subset; require approval before 100 |
| 4-bit weights change hidden geometry | Require 2B bf16-vs-4bit sanity |
| Disk fills again | No full dumps; compact vector chunks only; require projected free space >=20GB |

## Backburner / Not in Stage 2

- Hidden-vector int4 storage quantization.
- TurboQuant / KV-cache quantization.
- Prompt variants P2/P3/P6 unless Batch 1 creates a reason to run them.
- Full tensor dumps for prompt variants.
- 500-instance validation before Stage 2 go/no-go is satisfied.
- Multi-key memory summaries.
- New benchmark migration.

## Human Approval Checkpoints

1. Before deleting Tier B.
2. After 2B 4-bit sanity, before using 4-bit as default.
3. After KV-cache smoke, before online prompt sweep.
4. After 30-instance prompt sweep, before 100-instance prompt confirmation.
5. After 100-instance prompt confirmation, before selecting prompt for 9B.
6. After 9B wrapper/cache smoke and 30-instance layer scan, before 9B 100-instance run.
7. After 9B 100-instance result, before any 500-instance validation.
8. Before deleting any non-Tier-B tensors or model files.
