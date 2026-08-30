# Memory State: Inference-Native Retrieval for Long-Term Agent Memory

**Gordon Xiong, Seetie Inc.**

Code and results: https://github.com/Seetie-AI/memory_state

## Abstract

Agent memory systems typically pair a reasoning model with a separate, smaller
embedding model that indexes what the agent should remember. We ask whether the
reasoning model can supply its own retrieval keys. Memory State prompts a
generative LLM to compress a memory page into a short key, then stores the
hidden state at the final key token, taken from a late-layer band near the output, as the
retrieval vector. No retriever is trained, distilled, or adapted.

On LongMemEval-S at round granularity, a compact two-view configuration using
Qwen3.5-9B-MLX-4bit reaches strict Recall@5 of 0.777 using hidden states alone,
at 8 KB per page, against 0.755 for a Qwen3-Embedding-8B-4bit-DWQ baseline on
the same 94 scored questions. The margin is two questions on this subset, so we
report it as parity-level evidence and make no significance claim.

To test whether the recipe transfers rather than fits one benchmark, we carry
the three prompt identities selected on LongMemEval over to PrefEval
implicit-persona, a preference and persona memory task, and evaluate them over
all 1,000 examples. Per-view layer and geometry settings were assigned on the
PrefEval side, so this is prompt-identity transfer rather than a frozen
configuration. As pure dense hidden-state retrieval with no lexical or
embedding signal it reaches Recall@5 of 0.299 against 0.281 for the same 8B
embedding baseline, while ranking last among the four K3 candidates evaluated
there. A model-size check under matched conditions gives 0.596 for
Qwen3.5-2B-MLX-4bit and 0.691 for Qwen3.5-9B-MLX-4bit, so the memory
representation improves with the reasoning model rather than being capped by a
smaller retriever.

## 1. Introduction

File-based agent memory usually begins with plain text and keyword search. It
is cheap, transparent, and easy to inspect. It also has a blind spot: the agent
must know what to search for. A memory that matters to the current situation
may share none of the words in the current query. This is the unknown unknown
problem.

Semantic retrieval addresses it, but it adds a second model. That retriever is
usually smaller than the reasoning model, and it was trained for some general
retrieval objective rather than for the agent that will read the result. If it
misses, the more capable model never sees the memory.

This work tests a third arrangement. The model that reads and reasons over a
memory also produces the vector that finds it later. If that works, the memory
index shares an inference path, a tokenizer, and a semantic space with
downstream reasoning, and it needs no separately trained component.

The question came from an anomaly. While sweeping prompt suffixes on PrefEval,
a generic prompt asking the model for a single emoji reached Recall@5 of about
0.285, next to 0.281 for an 8B embedding model on the same 1,000 examples. That
prompt was not the best in the sweep and it is not part of any system reported
here. We record it as the observation that motivated the work: a reasoning
model appears to carry a usable memory representation in places we do not
normally treat as an index.

We report three things. First, hidden-state keys reach embedding-baseline scale
on evidence retrieval. Second, a prompt combination selected on one memory
benchmark carries over to a different memory task. Third, the representation
improves with model size under matched conditions.

## 2. Related Work

**PromptEOL** [1] showed that a one-word prompt can turn the hidden state of
the final prompt token into a sentence embedding without fine-tuning.

**MetaEOL** [2] extended this with multiple meta-task prompt views over the same
text, and reported that the final layer is not always the best choice, with a
proportional layer-selection strategy giving improvements.

**PromptReps** [3] brought prompted LLM representations to training-free
full-corpus document retrieval, combining the last layer's last-token hidden
state with next-token logits into a dense and sparse hybrid, and reported
stronger retrieval with larger LLMs.

**All-but-the-Top** [4] established that removing the common mean and the top
principal components from a set of embeddings exposes semantic differences that
a shared dominant direction otherwise masks.

Memory State does not claim the mechanism. Prompted final-token hidden states,
multiple prompt views, layer selection below the output layer, and
dominant-direction removal
all come from this line of work. Our contribution is the application: treating
these representations as persistent retrieval keys for long-term agent memory,
designing memory-specific prompt suffixes, and evaluating the result on two
memory benchmarks.

We evaluate on **LongMemEval** [5] and **PrefEval** [6].

## 3. Method

For each memory page and each query, the model is run over the text plus a
retrieval suffix that asks it to compress the text into a short key. The
retrieval vector is the hidden state at the final token of that suffix.

The pattern is:

1. choose prompt views that match the memory domain;
2. extract the suffix-final hidden state from a late-layer band near the output;
3. apply dominant-direction removal to strip shared prompt and corpus geometry;
4. combine views by concatenation or component-normalized vector averaging;
5. optionally add a lexical score as a shortlist rerank signal.

Queries are encoded with the same recipe as memory pages. We tested the
asymmetric alternative, encoding memory and query with different prompts, and
it did not help: the best asymmetric configuration reached Recall@5 of 0.755
against 0.766 for symmetric encoding of the same prompt.

The reported configurations use hidden states as the dense representation.
Next-token logits were also collected, and a PromptReps-style sparse path was
reproduced, but it is not part of the reported systems.

### 3.1 Prompt views

Suffixes are written in Chinese and ask the model to emit a single token. One
of the PrefEval views, translated, reads: *Use one emoji to mark the emotion of
the conversation above. The emoji is: "*. The other two ask for one keyword the
conversation should recall and one token for the association it creates. The
originals and the full configuration are in the repository.

### 3.2 Geometry

Dominant-direction removal is applied symmetrically to query and candidate
vectors with rank 15. Across 17 symmetric prompt variants, symmetric removal
won Recall@5 for 13, query-only removal for 3, and plain centered cosine for 1.

## 4. Experimental Setup

Hidden-state extraction uses `Qwen3.5-9B-MLX-4bit`, with `Qwen3.5-2B-MLX-4bit`
for the model-size check. Embedding baselines are
`Qwen3-Embedding-8B-4bit-DWQ` and `Qwen3-Embedding-0.6B-4bit-DWQ`. All models
are local 4-bit conversions. Embedding scores are never concatenated
into the hidden vectors; they appear only as baselines or as score-level
signals.

LongMemEval-S is evaluated at round granularity on a 100-instance subset, of
which 94 questions score after the official abstention filter. Recall@5 is
strict: a question scores 1 only if every gold turn appears in the top 5. One
question moves the metric by about 1.1 percentage points. PrefEval
implicit-persona is evaluated over all 1,000 examples.

Benchmark data is not redistributed with the repository. Sources and download
instructions are documented there.

## 5. Results

### 5.1 LongMemEval

| Method | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|
| BM25 | 0.585 | 0.547 | 0.559 |
| Qwen3-Embedding-8B-4bit-DWQ | 0.755 | 0.789 | 0.826 |
| Memory State, compact K2, hidden only, 8 KB/page | 0.777 | 0.788 | 0.820 |
| Memory State, K3 concat plus BM25 top 20, 24 KB/page | 0.777 | 0.822 | 0.851 |

The compact two-view configuration matches the three-view hybrid on strict
recall while using no lexical signal and one third of the storage. Its 0.022
margin over the 8B embedding baseline equals two questions in this sample. At
that resolution we make no significance claim. This is parity-level evidence at
embedding-baseline scale without training an embedding model, not a decisive
held-out win.

### 5.2 Cross-task transfer to PrefEval

The three prompt identities were selected on LongMemEval. They were then
evaluated on PrefEval as pure dense hidden-state retrieval over all 1,000
examples. Per-view layer and dominant-direction settings were assigned when the
PrefEval K3 candidates were constructed, so what transfers is the prompt
combination, not a frozen extraction configuration.

| Method | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| BM25 | 0.035 | 0.074 | 0.094 | 0.066 | 0.067 |
| Qwen3-Embedding-8B-4bit-DWQ | 0.093 | 0.216 | 0.281 | 0.191 | 0.200 |
| Memory State, LongMem prompt transfer, hidden only | 0.093 | 0.212 | 0.299 | 0.197 | 0.188 |

The transferred combination exceeds the 8B embedding baseline on strict
Recall@5 using no lexical signal and no embedding score. It is slightly lower
on R@3 and MRR. The LongMemEval shortlist and fusion weights were not carried
over.

Two things make this the most informative PrefEval row we have. It was not
selected to win here: of the four K3 candidates evaluated on PrefEval it placed
last, below combinations whose prompts were chosen on PrefEval itself. And its
prompt identities were fixed by a different benchmark. So it is the weakest
candidate in its own sweep and still clears the 8B embedding baseline on strict
recall. This supports the claim that a prompt combination can cross memory
domains, not that every low-level parameter is universal.

A separate configuration tuned directly on PrefEval, fusing the hidden-state
score with an embedding score and BM25, reaches Recall@5 of 0.332. Because its
prompts and fusion weights were selected on the same data it is reported on, we
treat it as a domain-tuned exploratory result and not as the headline.

### 5.3 Model size

Both models were run with the same prompt suffix, the same centered transform,
the same 4-bit precision, and the same 100 instances.

| Model | Layer | R@5 | NDCG@5 |
|---|---:|---:|---:|
| Qwen3.5-2B-MLX-4bit | 22 | 0.596 | 0.547 |
| Qwen3.5-9B-MLX-4bit | 30 | 0.691 | 0.689 |

The larger model gains 9.5 percentage points on Recall@5. On a smaller
30-instance tuning slice both models scored 0.833, so the gap appears only at
the larger sample. Each model uses its own best late layer rather than a fixed
absolute index. The direction is consistent with earlier retrieval results
reported for prompted representations at larger model scale [3].

## 6. Analysis and Negative Results

**There is no universal best layer.** Across the prompt sweep, layers 29, 30,
and 31 each won for 6, 6, and 5 variants respectively. The useful region is a
band below the output layer whose exact position depends on prompt semantics,
not a single layer.

**Prompt wording matters more than expected.** Changing one word in an
otherwise identical suffix, from a neutral term for the other party to the
product-native term for the user, moved Recall@5 by 0.043. The model appears
better aligned to product vocabulary than to neutral phrasing.

**Prompt language is not neutral.** In the sweep, the best cell for an English
variant of one suffix reached Recall@5 of 0.713 while the best cell for its
Chinese original reached 0.755, on English memory content. The two best cells
do not share a layer and transform, so this is a sweep observation rather than
a single-variable comparison. Cross-language prompting worked here; we make no
general multilingual claim.

**Not every retrieval-shaped prompt works.** An answer-strategy prompt
collapsed to Recall@5 of 0.574, well below the lexical baseline's neighbours in
the sweep.

**Lexical fusion helps only as a small vote inside a shortlist.** Fusing BM25
inside the vector top 20 or top 50 beat full-corpus fusion for ranking, and
weighting BM25 heavily collapsed performance across configurations, because
turn-level lexical matching is noisy.

**Late interaction did not justify its cost.** Max-sim style scoring over
multiple stored vectors did not beat the simpler concatenation and averaging
candidates.

**Agreement filtering is a diagnostic, not a default.** Gold candidates were
much more likely than non-gold candidates to appear in multiple prompt
rankings, but sorting by agreement never beat sorting by score.

**A stronger reranker buys ranking, not recall.** Blending an 8B embedding
score into the hybrid raised NDCG@5 to 0.834 and MRR to 0.888 without improving
Recall@5, while reintroducing the separate model dependency the method exists
to avoid. We keep it as a ceiling, not a default.

**Small subsets misled us.** An early prompt that led a 40-instance slice fell
to mid-pack on the full 100 instances. Oracle union diagnostics, which use gold
labels to find complementary prompt pairs, were likewise treated as hypothesis
generators rather than estimates.

## 7. Deployment Considerations

The vector comes from the final token of a prompted key-generation pass. In an
online setting the reasoning model has already processed the conversation and
its context is in the KV cache, so capturing a memory key means decoding one
additional token per prompt view and keeping its hidden state. Memory capture
then happens inside the inference path rather than as a second encoding job by
another model. We did not measure end-to-end latency or cost, so this is a
deployment argument, not a measured result.

Storage is straightforward. Qwen3.5-9B has a hidden size of 4096, so one view
in bf16 costs 8 KB per page and three views cost 24 KB. Around 20,000 memory
pages need roughly 500 MB before index overhead. The compact configuration in
Section 5.1 reaches the same strict recall as the three-view hybrid at 8 KB.

## 8. Limitations

The LongMemEval numbers rest on 94 scored questions, where one question moves
the metric by about 1.1 percentage points, and confidence intervals between the
reported systems and the embedding baselines overlap.

Prompt and fusion choices were selected on explored benchmark subsets. The
LongMemEval results are therefore exploratory rather than a clean held-out
evaluation. The PrefEval result in Section 5.2 is the closest we come to an
independent estimate, because its prompt identities were fixed by a different
benchmark and it was not the configuration selected to perform best there.
Its per-view layer and geometry settings were still assigned on the PrefEval
side, so it is not a held-out evaluation either.

The geometry is tied to `Qwen3.5-9B-MLX-4bit` and may change under another
model, another quantization, another language, or another prompt template. Both
models tested come from one family, so we cannot say whether the effect holds
across model families.

The work supports feasibility at embedding-baseline scale. It does not
establish a general win over embedding models.

## 9. Reproducibility

Code, experiment logs, the earlier internal results overview, and the result
files for all reported numbers are public at
https://github.com/Seetie-AI/memory_state.

Benchmark datasets and model weights are not redistributed. The repository
documents the original sources for LongMemEval and PrefEval, the download
commands, and the model identifiers, so that users obtain them under the
original terms.

## 10. Conclusion

A generative model, in the course of reading a page, leaves behind a
representation that can be used to find that page again. On two different
memory benchmarks this representation performed at the scale of embedding
models built for the job, without training a retriever, and it improved with
model size under matched conditions.

The claim is not that hidden states beat embedding models. It is that an agent's
memory index may not require a second model at all, and that the memory an
agent needs may already be present in the act of understanding, waiting to be
read out rather than rebuilt.

## References

[1] Jiang et al. Scaling Sentence Embeddings with Large Language Models.
Findings of EMNLP 2024. https://aclanthology.org/2024.findings-emnlp.181/

[2] Lei et al. Meta-Task Prompting Elicits Embeddings from Large Language
Models. ACL 2024. https://aclanthology.org/2024.acl-long.546/

[3] Zhuang et al. PromptReps: Prompting Large Language Models to Generate Dense
and Sparse Representations for Zero-Shot Document Retrieval. EMNLP 2024.
https://aclanthology.org/2024.emnlp-main.250/

[4] Mu and Viswanath. All-but-the-Top: Simple and Effective Postprocessing for
Word Representations. ICLR 2018. https://openreview.net/pdf?id=HkuGJ3kCb

[5] Wu et al. LongMemEval: Benchmarking Chat Assistants on Long-Term
Interactive Memory. https://arxiv.org/abs/2410.10813

[6] Zhao, Hong, Liu, Hazarika, and Lin. Do LLMs Recognize Your Preferences?
Evaluating Personalized Preference Following in LLMs. 2025.
https://arxiv.org/abs/2502.09597
