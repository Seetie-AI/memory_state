# Stage 2 Plan

## TL;DR

- Stage 2 tests three research-facing upgrades: 4-bit model viability, prompt-template sensitivity, and a conditional 9B-4bit scale-up.
- Model-forward work must run serially on the 16GB Mac; do not run two MLX jobs at once.
- Prompt sweeps must dump all-layer last-token Tier A tensors, because changing the suffix may move the best layer away from layer 22.

## Current Assets

- `MVP_Plan.md`: original v0 plan.
- `notes/results_log.md`: compact record of Stage 1 / Phase 2-deep findings.
- `tensors/dump_v1/tier_a/`: 2B bf16 Tier A dump, 100 LongMemEval-S/round instances, all-layer last-token vectors.
- `tensors/dump_v1/tier_b/`: Tier B all-position dump, about 29GB. It is useful historically but mostly redundant after the position/pooling analyses.
- `results/`: full generated JSON/markdown analysis outputs, gitignored.
- `models/Qwen3.5-2B-bf16/`: current main MLX model.

Stage 1 conclusion to preserve:

- Best hidden-only turn R@5: about `0.681`.
- Best fusion turn R@5: about `0.713`.
- Best hidden-only session_hit@5: about `0.947`.
- The method is best framed as a strong session-level memory router with weaker turn-level disambiguation.

## Storage Budget

Target practical free-space budget: about 30GB after deleting Tier B.

| Asset | Estimated size | Keep during Stage 2? | Note |
|---|---:|---|---|
| Current Tier A dump | ~2.4GB | Yes | Needed for Stage 1 comparisons |
| Current Tier B dump | ~29GB | No, after approval | Position result already summarized |
| Qwen3.5-2B bf16 | ~4.5GB | Yes | Current anchor model |
| Qwen3.5-2B 4bit | ~1.6-1.8GB | Yes, if validation proceeds | 4-bit sanity |
| Qwen3.5-9B 4bit | ~6GB | Conditional | Only after 2B 4-bit validation |
| 2B prompt Tier A dump | ~2.4GB each at 100 instances | Keep only top 1-2 long term | Use 50 subset first |
| 9B Tier A dump | ~5-7GB each at 100 instances | Conditional | Depends on hidden size / layer count |

Storage rule:

- Do not keep every prompt variant dump indefinitely.
- Keep metrics JSON/markdown for every run.
- Keep only the current anchor dump plus the best prompt/model dump unless the user explicitly asks otherwise.

## Execution Order

### Step 0: Storage Cleanup

Input:

- Existing `tensors/dump_v1/tier_b/`.
- Existing `results/analysis_*` and `notes/results_log.md`.

Action:

- After human approval, delete only Tier B all-position tensor files.
- Preserve Tier A chunks, `manifest.json`, all result summaries, and `notes/results_log.md`.

Output:

- About 29GB freed.

Go/No-Go:

- Go only if `notes/results_log.md` contains the Tier B conclusions: last/minus2 position findings, mean/max pooling failure, and diagonal/pooling negative results.
- No-go if any planned Stage 2 experiment still needs full-position Tier B tensors.

Estimated time:

- Minutes.

Human approval checkpoint:

- Required before deletion.

### Step 1: 2B 4-bit Sanity Validation

Input:

- `Qwen3.5-2B-bf16` as reference.
- `mlx-community/Qwen3.5-2B-MLX-4bit` or equivalent MLX 4-bit model.

Action:

- Run a Phase-0-style hidden-state sanity check on 10-20 prompts.
- Compare bf16 model hidden vectors against 4-bit model hidden vectors.
- Run a small retrieval smoke test on a limited subset if hidden cosine passes.

Output:

- Hidden cosine summary: mean/min.
- Top-token overlap summary.
- Small retrieval delta vs bf16.

Go/No-Go:

- Go if hidden cosine mean `> 0.99` and min `> 0.98`.
- Go if small retrieval R@5 degradation is `<= 2pp`.
- No-go if hidden cosine is unstable or retrieval drops more than `2pp`.
- If no-go, keep Stage 2 prompt sweeps on 2B bf16 and do not use 4-bit for 9B conclusions.

Estimated time:

- About 30 minutes, excluding model download.

Human approval checkpoint:

- Required before any 9B-4bit work.

### Step 2: 2B bf16 Prompt Sweep, 50-Instance Exploration

Input:

- 2B bf16 model.
- LongMemEval-S/round subset of 50 instances.
- Prompt variants P0/P1/P4/P5 from this document.

Action:

- For each prompt variant, dump Tier A all-layer last-token vectors.
- Evaluate layer scan, anti-PCA/query-only anti-PCA, session metrics, and turn metrics.
- Do not hardcode layer 22; prompt changes may move the best layer.

Output:

- Prompt comparison table on 50 instances.
- Best prompt candidate(s) for 100-instance confirmation.

Go/No-Go:

- Go to 100-instance confirmation if a prompt improves turn R@5 by `>= 3pp`, session_hit@5 by `>= 1pp`, or materially improves NDCG@5.
- If no prompt clearly improves over P0, retain P0 and document prompt robustness.

Estimated time:

- About 2-4 hours depending on forward speed and number of variants.

Human approval checkpoint:

- Required before confirming a prompt on 100 instances.

### Step 3: 2B Prompt Confirmation, 100 Instances

Input:

- Best prompt from Step 2.
- P0 current prompt as anchor.

Action:

- Run the best prompt on the same 100-instance Tier A setting as Stage 1.
- Compare against P0 with the same metrics and analysis pipeline.

Output:

- Confirmed prompt result.
- Decision: update default prompt or keep P0.

Go/No-Go:

- Accept new prompt if it preserves or improves session_hit@5 and improves turn R@5 or NDCG@5 by at least `3pp`.
- Reject if improvement appears only on the 50-instance exploration subset and disappears at 100.

Estimated time:

- About 1-2 hours per confirmed prompt.

Human approval checkpoint:

- Required before any 9B full run uses the selected prompt.

### Step 4: 9B-4bit Wrapper Smoke + Layer Scan

Input:

- Selected prompt from Step 3.
- `mlx-community/Qwen3.5-9B-MLX-4bit` or `mlx-community/Qwen3.5-9B-OptiQ-4bit`.

Action:

- Load the 9B-4bit model.
- Verify wrapper compatibility: model layout, layer count, hidden dimension, one prompt extraction.
- Dump a 30-50 instance Tier A all-layer last-token subset.
- Run layer scan and anti-PCA/query-only anti-PCA.

Output:

- 9B model compatibility note.
- 9B subset layer sweet spot.
- 9B subset retrieval metrics.

Go/No-Go:

- Go if wrapper works and memory stays within a safe range.
- Go if any one of these conditions is met on subset:
  - turn R@5 `>= 0.731`;
  - session_hit@5 `>= 0.970`;
  - NDCG@5 `>= 0.60`.
- Stop if turn R@5 is at least `3pp` worse than the 2B best configuration.

Estimated time:

- Highly uncertain. Plan for several hours including model download and smoke debugging.

Human approval checkpoint:

- Required before running 9B on 100 instances.

### Step 5: 9B-4bit 100-Instance Evaluation

Input:

- 9B-4bit model that passed Step 4.
- Best prompt from Step 3.
- Best layer/transform discovered in Step 4.

Action:

- Run 100-instance Tier A all-layer dump or targeted all-layer evaluation if storage is constrained.
- Compare against 2B best, BM25, and Qwen3-Embedding baselines.

Output:

- Final Stage 2 9B comparison.

Go/No-Go:

- Keep 9B as a serious candidate only if it improves over 2B on turn R@5, session_hit@5, or NDCG@5 by the thresholds in Step 4.
- If 9B does not improve, document that larger model scale does not automatically improve hidden-state retrieval geometry.

Estimated time:

- Several hours.

Human approval checkpoint:

- Required before any 500-instance evaluation.

### Step 6: Stage 2 Summary

Input:

- Step 1-5 results.

Action:

- Update `notes/results_log.md`.
- Add a concise Stage 2 conclusion section.
- Decide whether a 500-instance run is justified.

Output:

- Human-readable Stage 2 summary.

Go/No-Go:

- Go to 500-instance validation only if Stage 2 finds a robust improvement over Stage 1 and storage/time are acceptable.

Human approval checkpoint:

- Required before 500-instance dump/evaluation.

## Prompt Variants

Batch 1 only:

| ID | Template | Hypothesis |
|---|---|---|
| P0 | current suffix: `\n请用一个词来summarize上面这段文字，这个词是：“` | Anchor |
| P1 | no suffix | Test whether the summary instruction is necessary |
| P4 | `\n用于记忆检索的关键词是：` | Retrieval-specific Chinese instruction |
| P5 | `\nMemory key:` | Minimal English deployment-friendly instruction |

Rules:

- P0/P4/P5 must use symmetric memory/query suffixes.
- P1 means raw text end; interpret carefully because the final token varies by input text.
- Dump all-layer last-token Tier A for each prompt variant.
- Do not run asymmetric prompts in Batch 1.

Conditional Batch 2:

| ID | Template | Trigger |
|---|---|---|
| P2 | `\n关键词：` | If P5 minimal prompt helps |
| P3 | `\nTopic:` | If P5 helps and language choice matters |
| P6 | asymmetric memory/query prompts | Only after symmetric prompts are understood |

## 9B Upgrade Plan

Candidate models:

- `mlx-community/Qwen3.5-9B-MLX-4bit`.
- `mlx-community/Qwen3.5-9B-OptiQ-4bit`.

9B-specific requirements:

- Do not assume layer 22 remains best.
- Record actual layer count and hidden dimension.
- Run all-layer last-token scans before selecting a layer.
- Stop early if wrapper layout differs and extraction is ambiguous.

Primary comparison:

- 2B best from Stage 1/Stage 2 vs 9B-4bit best on the same subset.

## Go/No-Go Criteria Summary

| Decision | Go criteria | No-go criteria |
|---|---|---|
| Delete Tier B | Tier B conclusions already summarized | Any upcoming analysis still needs full positions |
| 2B 4-bit model | cosine mean >0.99, min >0.98, retrieval drop <=2pp | geometry unstable or retrieval drop >2pp |
| Prompt replacement | 100-instance improvement >=3pp turn R@5 or meaningful NDCG/session gain | 50-subset gain disappears on 100 |
| 9B subset | turn R@5 >=0.731 or session_hit@5 >=0.970 or NDCG@5 >=0.60 | turn R@5 >=3pp below 2B best |
| 500-instance validation | Stage 2 finds robust improvement | no robust improvement or storage/time unacceptable |

## Risk Register

| Risk | Mitigation |
|---|---|
| Disk full from multiple dumps | Delete Tier B first; keep only top prompt dumps |
| Two MLX jobs contend for GPU/unified memory | Run all model-forward tasks serially |
| 9B quantized model layout differs from 2B | Wrapper smoke test before any dump |
| Prompt sweep changes best layer | Dump all-layer last-token vectors, not layer 22 only |
| P1 no-suffix final token varies | Treat P1 as an exploratory stress test |
| 100-instance prompt tuning overfits | Explore on 50, confirm on 100 |
| 9B is slower than expected | Start with 30-50 subset and require approval before 100 |
| 4-bit weights change hidden geometry | Require bf16-vs-4bit sanity before 9B conclusions |
| Quantized hidden vector storage distracts from research | Keep int4 vector storage as backburner |

## Backburner / Not in Stage 2

- Hidden-vector int4 storage quantization.
- TurboQuant / KV-cache quantization.
- Prompt variants P2/P3/P6 unless Batch 1 creates a reason to run them.
- 500-instance validation before Stage 2 go/no-go is satisfied.
- Multi-key memory summaries.
- New benchmark migration.

## Human Approval Checkpoints

1. Before deleting Tier B.
2. After 2B 4-bit sanity, before 9B-related work.
3. After 50-instance prompt sweep, before 100-instance prompt confirmation.
4. After 100-instance prompt confirmation, before selecting prompt for 9B.
5. After 9B wrapper smoke and 30-50 subset layer scan, before 9B 100-instance run.
6. After 9B 100-instance result, before any 500-instance validation.
7. Before deleting any non-Tier-B tensors or model files.
