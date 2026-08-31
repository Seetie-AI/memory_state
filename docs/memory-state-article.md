# Can an LLM Leave Its Own Memory Index Behind?

_Memory State_

Code and results: [github.com/Seetie-AI/memory_state](https://github.com/Seetie-AI/memory_state)

We did not expect an LLM with an emoji to come close to an 8B embedding model at retrieving agent memory. In a 1,000-item PrefEval prompt sweep, a generic emoji prompt with Qwen3.5-9B reached Recall@5 of about 0.285. The Qwen3-Embedding-8B baseline reached 0.281.

The emoji was not the best prompt. That is not the point. The strange result suggested that a reasoning model may already contain a useful memory representation in places we do not normally treat as an index.

## The memory you do not know to search for

File-based agent memory often starts with plain text and keyword search. It is cheap, transparent, and easy to inspect. It also has a blind spot: you need to know what to search for. A relevant memory may use none of the words in the current query. This is the unknown unknown problem.

Semantic RAG fixes the unknown unknown problem, but it adds another model to the harness. That retriever is usually smaller and theoretically less intelligent than the reasoning model. It can also be benchmaxxed for a task that does not match the agent's real use case. If it misses, the smarter model never sees the memory.

[PromptEOL](https://aclanthology.org/2024.findings-emnlp.181/) showed that a one-word prompt can turn the final prompt token's hidden state into a sentence embedding without fine-tuning. [MetaEOL](https://aclanthology.org/2024.acl-long.546/) extended this idea with multiple prompt views and found that late, non-final layers can work better. [PromptReps](https://aclanthology.org/2024.emnlp-main.250/) brought prompted hidden states and next-token logits to training-free full-corpus document retrieval.

Building on this line of work, we tested whether prompted hidden states could serve as persistent retrieval keys for agent memory. We call the resulting system _Memory State_. It reads the last-token position from a late non-final layer around 94% of model depth, applies dominant-direction removal following [All-but-the-Top](https://openreview.net/pdf?id=HkuGJ3kCb), and uses several hardcoded, memory-specific prompt suffixes as different views of the same memory. The configurations reported here use hidden states as the dense representation.

| | File and keyword search | Embedding RAG | Memory State |
|---|---|---|---|
| Finds unknown unknowns | Limited | Yes | Yes |
| Separate retrieval model | No | Yes | No |
| Retriever training | None | Trained separately | None |
| Scales with reasoning model | Yes | No, it scales separately | Yes |
| Main weakness | Unknown unknowns | Smaller model; can be benchmaxxed for the wrong use case | Hardcoded prompt suffixes |

Following the same basic recipe, the implementation is one sentence: give the memory text to the LLM, append a short instruction, decode the answer token, and store that token's hidden state from a late non-final layer as the retrieval vector.

At retrieval time, Memory State applies the same encoding recipe to the query and looks up the closest stored vectors.

The three views in the configuration reported below ask, translated from Chinese, for one word to represent the user in the conversation, one word to mark the conversation, and one word to represent the association it creates. The trailing quotation mark in each suffix opens the model's answer, so the next decoded token is the key.

## LongMemEval: finding a workable retrieval recipe

We did not run the full [LongMemEval-S](https://arxiv.org/abs/2410.10813) question-answering benchmark. For each question, we only ranked user turns from its own history, using the benchmark's labels for where the answer appeared. Recall@5 is strict here: every labeled turn must appear in the top 5.

The sample was also biased. The file is ordered by question type, so its first 100 entries contained 70 single-session user questions and 30 multi-session questions, with four other question types missing. After six abstention cases were removed, 94 remained. These numbers describe this slice, not LongMemEval as a whole.

| Method | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|
| BM25 | 0.585 | 0.547 | 0.559 |
| Qwen3-Embedding-8B-4bit-DWQ | 0.755 | 0.789 | 0.826 |
| Qwen3.5-9B-MLX-4bit K2, hidden only | 0.777 | 0.788 | 0.820 |

*Metric guide, for this and every table below. R@k (Recall@k) measures how much
relevant memory evidence appears within the first k results; LongMemEval uses a
strict version requiring every gold turn in the top five. NDCG@5 rewards
relevant evidence appearing nearer the top. MRR measures how early the first
relevant result appears. Higher is better throughout.*

The hidden state path scores higher on strict recall and is roughly tied on ranking quality. Its 0.022 recall margin over the 8B baseline equals two questions in this sample.

An earlier model-size check used the same P0 suffix, last-centered transformation, 4-bit precision, and 100 instances for both models:

| Model | Layer | R@5 | NDCG@5 |
|---|---:|---:|---:|
| Qwen3.5-2B-MLX-4bit | 22 | 0.596 | 0.547 |
| Qwen3.5-9B-MLX-4bit | 30 | 0.691 | 0.689 |

The 9B model gained 9.5 percentage points on Recall@5 under the matched setup. On the smaller 30-instance tuning slice, both models scored 0.833, so the gain appeared only in the 100-instance run. The direction will surprise no one: the larger model did better, consistent with PromptReps' earlier retrieval results.

The best LongMem hybrid used three hidden state views plus BM25 top 20 and reached 0.777 R@5, 0.822 NDCG@5, and 0.851 MRR. There is no 8B embedding plus BM25 run in the report, so I do not present that comparison.

The prompt suffixes were Chinese while the memory content was English. This is evidence that a cross-language setup can work, not proof of general multilingual performance. Another prompt language performed poorly, potentially due to Qwen's training data.

## PrefEval: the more relevant agent memory test

We used [PrefEval](https://arxiv.org/abs/2502.09597) data, but not its official evaluation. PrefEval normally asks a model to read a full conversation, then generate an answer or choose one of four options. We instead put 1,000 labeled preference statements in one shared pool and asked each final question to retrieve its paired statement. This tests preference-memory retrieval, not whether the model gives the right final answer.

It is still closer to the kind of memory an agent needs, because the right past interaction may share no obvious words with the present query.

| Method | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| BM25 | 0.035 | 0.074 | 0.094 | 0.066 | 0.067 |
| Qwen3-Embedding-8B-4bit-DWQ | 0.093 | 0.216 | 0.281 | 0.191 | 0.200 |
| Qwen3.5-9B-MLX-4bit, LongMem K3 prompt transfer, hidden only | 0.093 | 0.212 | 0.299 | 0.197 | 0.188 |

On this derived retrieval task, the hidden-state system uses no BM25 and no embedding score. Its Recall@5 is 0.299 versus 0.281 for the 8B embedding model, a margin of 1.8 percentage points. It is slightly lower on R@3 and MRR.

Only three prompt ideas carried over from LongMemEval: user, conversation tag, and association. The exact wording, layers, and vector settings changed on PrefEval. This configuration placed last among four three-view candidates there, but still reached 0.299. The ideas may cross memory domains; the exact recipe does not.

## Why this matters for agents

This approach has three practical advantages.

First, the manual encoding burden is small. Each view is one short prompt suffix. There is no hand-built memory schema and no labeled training set.

Second, there is no separate retriever training. The inference model produces the memory vector directly.

Third, the memory capability can scale with the reasoning model instead of remaining capped by a smaller retriever. No one will ever use a 2-trillion-parameter embedding model, but you enjoy similar capability if you incorporate this memory system into your inference workflow.

The intended online path is also simple. Once the reasoning model has processed the conversation, its context is already in the KV cache. Decode one additional answer token per prompt view, capture its hidden state, and store the vector. Memory capture happens inside the inference path rather than as a second encoding job performed by another model.

Storage is easier to quantify. One 4096-dimensional bf16 view costs 8 KB per page, while three views cost 24 KB.

## Limits worth stating plainly

The LongMem result comes from the biased 94-question slice described above, where one question moves the metric by about 1.1 percentage points. Prompt and fusion choices were explored on the evaluated data, not a clean held-out set.

The PrefEval-derived task also has imperfect labels: only the paired preference and exact duplicates count as correct. In 100 reviewed misses, 58 found plausible same-topic statements, 28 found the topic but the wrong constraint, and 14 were unrelated. The score can miss useful alternatives, but same-topic does not always mean correct.

Results may change with another model, quantization, language, or prompt template. The work supports feasibility, not a decisive universal win over embedding models.

What it suggests is more specific and more useful: the memory an agent needs may already be present in the act of understanding, waiting to be read out rather than rebuilt by another model.
