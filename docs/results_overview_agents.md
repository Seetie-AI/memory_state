# Inference-Native Memory State: Results Overview for Agents

Internal agent-facing companion to the Chinese HTML report and the LaTeX
technical report.

## Executive Thesis

The project tests whether a generative LLM can reuse its own inference-time
hidden states as long-term memory retrieval vectors. The result is positive,
but conditional: the useful vector is a late suffix-final hidden state extracted
under a retrieval-oriented prompt, then debiased and fused at score level when
the domain benefits from lexical or embedding signals.

The clean project story is:

- LongMemEval establishes the method on evidence retrieval.
- PrefEval adapts the same method pattern to preference/persona memory.
- The final companion-memory retriever is one PrefEval-selected K3 config:
  `2-3-1 + 2-5_token + 2-8_emoji`.

## Motivation and Systems Thesis

The point is not to beat every embedding model on every benchmark. The point is
to test whether the model that reads and reasons over memory can also provide
the memory representation. If this works, memory construction can reuse the
same inference path, same tokenizer, and same semantic space as downstream
reasoning, instead of depending entirely on a separate embedding stack.

This matters for a companion-memory system:

- The memory key is model-native: query and candidate are represented by the
  same 4bit LLM hidden-state geometry.
- The approach is training-free: no contrastive finetuning or labeled retriever
  training is required for the reported configs.
- External embeddings remain useful, but only as score-level signals. They do
  not replace the hidden-state memory representation.

## Models

Hidden-state extraction uses `models/Qwen3.5-9B-MLX-4bit`. The PrefEval final
fusion uses `models/Qwen3-Embedding-0.6B-4bit-DWQ` as an external score source.
LongMemEval also reports a local `Qwen3-Embedding-8B-4bit-DWQ` baseline.

All model references above are 4bit local models. Embedding vectors are used as
score matrices / rerank sources; they are not concatenated into the 9B hidden
vectors.

## Term Definitions

- `suffix-final`: the hidden state at the final token position of the retrieval
  suffix, after the model has been asked to compress the page/query into a key.
- `anti_pca_both_k15`: remove the top 15 shared principal directions from both
  query and candidate vectors before cosine scoring.
- `component-normalized vector average`: normalize each prompt component before
  averaging the K prompt scores/vectors, so one prompt view does not dominate
  only by scale.
- `z-score fusion`: row-wise score normalization before weighted score fusion.
- `oracle union`: label-aware union of hits from multiple prompt rankings. It is
  used only for prompt-complementarity diagnosis, not as a deployable scorer.
- `source_ge3`: a source-count agreement filter; useful as a tuning ceiling,
  but not part of the final default.

## LongMemEval Method Result

LongMemEval-S/round is the evidence-retrieval benchmark. On subset 0-100, after
the official abstention filter, there are 94 scored questions.

| Method | R@5 | NDCG@5 | MRR | Role |
|---|---:|---:|---:|---|
| BM25 | 0.585 | 0.547 | 0.559 | lexical baseline |
| Qwen3-Embedding-0.6B local baseline | 0.766 | 0.809 | - | embedding reference |
| Qwen3-Embedding-8B-4bit-DWQ | 0.755 | 0.789 | 0.826 | local 4bit embedding baseline |
| Stage 3 compact K2 hidden-only (`2-4-1_user_word + 1-3`) | 0.777 | 0.788 | 0.820 | no BM25, 8 KB/page |
| **Stage 3 LongMem K3 + BM25 top20** | **0.777** | **0.822** | **0.851** | evidence-retrieval method result |

LongMem K3:

| Prompt id | Suffix intent | Layer | Transform |
|---|---|---:|---|
| `2-4-1_user_word` | user/product wording | 31 | `anti_pca_both_k15` |
| `1-3` | generic tag / marker | 31 | `anti_pca_both_k15` |
| `2-5` | association | 31 | `anti_pca_both_k15` |

Scoring: concatenate the three 4096-d vectors, rank by cosine, keep vector
top20, then rerank with `0.75*z(vector) + 0.25*z(BM25)`.

This is not a decisive embedding-model win. It is parity-scale evidence on a
small 94-question subset.

## PrefEval Final Companion-Memory Configuration

PrefEval implicit-persona n=1000 is the preference/persona memory benchmark.
The final retriever is a single K3 configuration, not a menu of alternatives.
The canonical prompt text is more important than the implementation id.

| Role | Implementation id | Full suffix | Layer | Transform |
|---|---|---|---:|---|
| Recall-keyword marker | PrefEval `2-3-1`; LongMem replay `2-3-1_mark` | `用一个词标记上面这段对话最该让我想起的关键词，这个词是：“` | 30 | `anti_pca_both_k15` |
| Association token | `2-5_token` | `用一个token标记上面这段对话让我产生的联想，这个token是：“` | 30 | `anti_pca_both_k15` |
| Emotion emoji | `2-8_emoji` | `用一个emoji标记上面这段对话的情绪，这个emoji是：“` | 30 | `anti_pca_both_k15` |

Dense scorer: `vector_average_component_norm`.

Full-corpus score fusion:

```text
final_score =
  0.60 * row_zscore(K3_vector_average_score)
+ 0.30 * row_zscore(Qwen3-Embedding-0.6B-4bit-DWQ_score)
+ 0.10 * row_zscore(BM25_score)
```

PrefEval all1000 result with baselines:

| Config | R@1 | R@3 | R@5 | NDCG@5 | MRR | Role |
|---|---:|---:|---:|---:|---:|---|
| BM25 | 0.035 | 0.074 | 0.094 | 0.066 | 0.067 | lexical floor |
| Qwen3-Embedding-8B-4bit-DWQ | 0.093 | 0.216 | 0.281 | 0.191 | 0.200 | 4bit embedding baseline |
| **Final companion K3 + 0.6B embedding + BM25** | **0.122** | **0.265** | **0.332** | **0.232** | **0.233** | final config |
| Topic metric ceiling control | 0.119 | 0.265 | 0.355 | 0.240 | 0.235 | higher R@5, less aligned with companion objective |

Holdout300 sanity split for the final config: R@1 0.127, R@3 0.263, R@5
0.320, NDCG@5 0.228, MRR 0.228. The split was created after exploration, so it
is a robustness check, not blind validation.

## Why This Final K3 Is Not Benchmark Maxxing

The topic metric ceiling control is useful because it shows the benchmark-only
upper direction, but it is not the final product choice:

| Config | K3 prompts | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---|---:|---:|---:|---:|---:|
| Topic metric ceiling control | `2-3-1 + 2-5 + 2-1` | 0.119 | 0.265 | 0.355 | 0.240 | 0.235 |
| **Final companion config** | `2-3-1 + 2-5_token + 2-8_emoji` | **0.122** | 0.265 | 0.332 | 0.232 | 0.233 |

The 0.355 vs 0.332 contrast is not a clean single-factor ablation because both
the association prompt and the third prompt differ. The clean third-slot
contrast fixes the first two slots as `2-3-1 + 2-5_token`:

| Third slot | K3 prompts | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---|---:|---:|---:|---:|---:|
| Dynamics emoji | `2-3-1 + 2-5_token + 2-7_emoji` | 0.125 | 0.259 | 0.341 | 0.236 | 0.234 |
| **Emotion emoji** | `2-3-1 + 2-5_token + 2-8_emoji` | 0.122 | **0.265** | 0.332 | 0.232 | 0.233 |

So the final choice is a product-objective tradeoff, not an accidental
benchmark maximum: emotion is slightly worse on R@5 than the dynamics variant,
but it preserves R@3 and directly represents affective interaction state.

There are also source-screened rows above clean defaults, such as `source_ge3 +
embedding top20`. Those are treated as tuning ceilings, not defaults, because
they introduce another same-set candidate-selection knob.

## PrefEval Prompt Sweep

PrefEval tested 25 prompt variants. The sweep covered:

- object axis: generic tag, topic, recall keyword, association, user/counterparty,
  need, interaction pattern, emotion;
- verb axis: represent, tag, summarize;
- language axis: Chinese, English, Russian, Japanese;
- output-form axis: word, token, emoji;
- deictic wording: with or without "上面";
- product-specific wording: user/counterparty variants.

Representative non-winners and what they taught:

| Prompt / treatment | Result | Interpretation |
|---|---|---|
| `2-1-2` topic without "上面" | R@5 0.321 as a single prompt | strong topic single prompt, but its gain does not compose linearly in final K3 |
| `2-5-2` association without "上面" | weaker than `2-5` | removing "上面" is not generally helpful |
| `2-3-3` / `2-5-3` direct-token wording | do not beat originals | forcing unreadable token keys does not improve retrieval |
| `1-1_RU_explicit` | R@5 0.107 | language mismatch collapses |
| `1-1_EMOJI` | about R@5 0.285 | surprising generic emoji signal, but not the final K3 third slot |
| `2-7` interaction-pattern word prompt | R@5 0.229 alone | weak as a single retriever; dynamics variants remain product hypotheses |

The final emoji prompt is not `1-1_EMOJI`. It is `2-8_emoji`, which explicitly
asks for conversation emotion.

## Prompt Complementarity

Prompt overlap was judged with oracle union hit@k and pairwise Jaccard@k.
Oracle union is label-aware and is used only to generate hypotheses.

Fixed base pair `2-3-1 + 2-5`:

| Prompt set | union@3 | union@5 | Takeaway |
|---|---:|---:|---|
| `2-3-1 + 2-5` | 0.300 | 0.369 | base pair |
| `+ 2-1_token` | 0.339 | 0.415 | best union@3 third |
| `+ 2-1-2` | 0.332 | 0.417 | best union@5 among top thirds |
| `+ 1-1_EMOJI` | 0.322 | 0.399 | useful but not exceptional |
| `+ 2-1` | 0.326 | 0.410 | strong topic control after fusion |

Single-prompt quality and prompt complementarity do not directly determine the
final product config. Final selection also requires an interpretable memory
axis.

## Shortlist Policy

There are two different shortlist questions:

- Source-count agreement shortlist: not part of the final default on either
  benchmark. It can raise some early-rank rows, but it adds a tuned
  candidate-selection stage.
- BM25 fusion scope: benchmark-specific. LongMemEval uses BM25 only inside
  vector top20; PrefEval final uses full-corpus z-score fusion.

This difference is informative rather than contradictory: lexical signal is
stronger as a local evidence reranker on LongMemEval, while PrefEval benefits
from a small global lexical prior.

## Embedding Policy

PrefEval final uses `Qwen3-Embedding-0.6B-4bit-DWQ` at weight 0.30. Its role is
to improve early-rank precision and MRR as a score-level signal. It is not the
stored memory representation and does not replace the K3 hidden-state vectors.

LongMemEval keeps the hidden-state result as the product-clean default and uses
embedding mainly as a baseline/reranker. The asymmetry is intentional: PrefEval
needs the extra ranking signal, while LongMem already reaches parity-scale R@5
with the hidden-state K3/BM25 setup.

## Deployment Cost

For Qwen3.5-9B hidden size 4096, bf16 storage costs about 8 KB per prompt view
per memory page. Therefore:

- K2 hidden-only: about 16 KB/page if both prompt vectors are stored in bf16;
  the compact score path reported above is summarized as 8 KB/page when using a
  single averaged vector.
- K3 hidden-state storage: `3 * 4096 * 2 bytes = 24 KB/page`.
- About 20k memory pages require roughly 500 MB for K3 bf16 vectors, before
  metadata and index overhead.

This is small enough to be plausible for local companion memory, especially
because no separate high-dimensional trained retriever state is required for
the primary representation.

## LongMem Replay of PrefEval Final K3

The final PrefEval K3 was replayed on LongMemEval-S/round using the same
final-style fusion:

| Config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| PrefEval final-style 0.60 K3 + 0.30 emb + 0.10 BM25 | 0.532 | 0.745 | 0.766 | 0.805 | 0.831 |
| K3 hidden-only vector average | 0.468 | 0.723 | 0.745 | 0.752 | 0.767 |
| embedding-only | 0.511 | 0.681 | 0.755 | 0.789 | 0.826 |

This is strong transfer, but still below the LongMem-specific K3 result of
R@5 0.777 / NDCG@5 0.822.

## What Works

- Late suffix-final hidden states.
- Anti-PCA / centering to remove shared prompt and corpus directions.
- Multi-prompt views chosen for the memory domain.
- Vector averaging with component normalization for PrefEval K3.
- Small score-level fusion with BM25 and 4bit Qwen embedding when it improves
  the target domain.

## What Does Not Work

- Final post-norm cosine.
- Early/mid-layer vectors.
- Sequence mean/max pooling.
- Direct-token prompt wording as a general fix.
- Removing "上面" as a general prompt improvement.
- Russian explicit prompt for this dataset/model setup.
- Source-count screening as the final clean default.
- Assuming the LongMem K3 prompt set transfers unchanged to PrefEval.

## Limitations

- LongMemEval main numbers are on 94 scored questions; one question moves the
  metric by about 1.1 percentage points.
- Prompt and fusion choices were tuned on the explored benchmark subsets.
- PrefEval holdout300 is a sanity check created after exploration, not a blind
  benchmark.
- The geometry is tied to Qwen3.5-9B-MLX-4bit and may change under another
  model, quantization, or prompt template.
- The final system still uses an external 4bit embedding score on PrefEval.
  Removing it is possible, but the reported final config includes it because it
  improves early-rank quality.

## Primary Sources

- `notes/stage_3_prompt_sweep_findings.md`
- `benchmarks/PrefEval/prefeval_benchmark.py`
- `scripts/stage3_prompt_sweep.py`
- `scripts/stage3_longmem_prefeval_final_fusion.py`
- `benchmarks/PrefEval/results/prefeval_stage1_1_more_prompts/findings.md`
- `benchmarks/PrefEval/results/prefeval_stage1_1_more_prompts/k3_231_25token_28emoji_sameL30_fixed_all1000_20260514.md`
- K3 dynamics/emotion third-slot comparison output under `benchmarks/PrefEval/results/prefeval_stage1_1_more_prompts/`
- K3 topic-control comparison output under `benchmarks/PrefEval/results/prefeval_stage1_1_more_prompts/`
- `results/stage3/prompt_fusion_prefeval_replay/prefeval_l30_k3_longmemeval100.md`
