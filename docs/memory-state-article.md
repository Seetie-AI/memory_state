# Can an LLM Leave Its Own Memory Index Behind?

_Memory State_

Code and results: [github.com/Seetie-AI/memory_state](https://github.com/Seetie-AI/memory_state)

We did not expect an emoji to make a general LLM competitive with an 8B embedding model at retrieving agent memory. Yet in a 1,000-item PrefEval prompt sweep, a generic emoji prompt with Qwen3.5-9B put the right memory in its top five about 28.5% of the time, beside 28.1% for Qwen3-Embedding-8B. The emoji was not the best prompt. It was a clue that the reasoning model might already contain a useful memory index in a place we had not thought to look.

The more important result is broader. At roughly comparable parameter scale, hidden states from a general Qwen3.5-9B model, with no trained retriever, reached overall parity with a dedicated Qwen3-Embedding-8B model on two derived memory-retrieval tasks. This is not an apples-to-apples comparison: the generative model comes from the newer Qwen3.5 family, while the embedding model is built on Qwen3, so the generation difference favors Memory State.

## The memory you do not know to search for

File-based agent memory often starts with plain text and keyword search. It is cheap, transparent, and easy to inspect. It also has a blind spot: you need to know what to search for. A relevant memory may use none of the words in the current query. This is the unknown unknown problem.

Semantic RAG fixes the unknown unknown problem, but it adds another model to the harness. That retriever is usually smaller and theoretically less intelligent than the reasoning model. It can also be benchmaxxed for a task that does not match the agent's real use case. If it misses, the smarter model never sees the memory.

When an LLM reads, it continually turns the text into internal numbers called hidden states. You can think of one as a thin slice of the LLM's brain while it is reading, before it says anything.

The ingredients are not new. [PromptEOL](https://aclanthology.org/2024.findings-emnlp.181/) showed that a one-word prompt can turn a hidden state into a sentence embedding. [MetaEOL](https://aclanthology.org/2024.acl-long.546/) used several prompted views. [PromptReps](https://aclanthology.org/2024.emnlp-main.250/) applied prompted representations to full-corpus retrieval. [All-but-the-Top](https://openreview.net/pdf?id=HkuGJ3kCb) showed how removing shared dominant directions can improve sentence representations.

Memory State combines these ideas for agent memory. Depending on the configuration, two or three short prompts turn each memory and query into different search vectors. The views are combined before the system searches for the closest stored memories. The same reasoning model creates the vectors directly, with no separately trained retriever.

## LongMemEval: finding a workable retrieval recipe

We did not run the full [LongMemEval-S](https://arxiv.org/abs/2410.10813) question-answering benchmark. For each question, we only ranked user turns from its own history, using the benchmark's labels for where the answer appeared. Recall@5 is strict here: every labeled turn must appear in the top 5.

The sample was also biased. The file is ordered by question type, so its first 100 entries contained 70 single-session user questions and 30 multi-session questions, with four other question types missing. After six abstention cases were removed, 94 remained. These numbers describe this slice, not LongMemEval as a whole.

| Method | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|
| BM25 | 0.585 | 0.547 | 0.559 |
| Qwen3-Embedding-8B, 4-bit | 0.755 | 0.789 | 0.826 |
| Memory State, two views, 4-bit | 0.777 | 0.788 | 0.820 |

*Metric guide, for this and every table below. R@k (Recall@k) measures how much
relevant memory evidence appears within the first k results; LongMemEval uses a
strict version requiring every gold turn in the top five. NDCG@5 rewards
relevant evidence appearing nearer the top. MRR measures how early the first
relevant result appears. Higher is better throughout.*

The Memory State row is the compact two-view version. It uses hidden states alone, with no BM25 or embedding score. It scores higher on strict recall and is roughly tied on ranking quality. Its 0.022 recall margin over the 8B baseline equals two questions in this sample.

## PrefEval: the more relevant agent memory test

We used [PrefEval](https://arxiv.org/abs/2502.09597) data, but not its official evaluation. PrefEval normally asks a model to read a full conversation, then generate an answer or choose one of four options. We instead put 1,000 labeled preference statements in one shared pool and asked each final question to retrieve its paired statement. This tests preference-memory retrieval, not whether the model gives the right final answer.

It is still closer to the kind of memory an agent needs, because the right past interaction may share no obvious words with the present query.

| Method | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---|---:|---:|---:|---:|---:|
| BM25 | 0.035 | 0.074 | 0.094 | 0.066 | 0.067 |
| Qwen3-Embedding-8B, 4-bit | 0.093 | 0.216 | 0.281 | 0.191 | 0.200 |
| Memory State, three transferred views, 4-bit | 0.093 | 0.212 | 0.299 | 0.197 | 0.188 |

On this derived retrieval task, the hidden-state system uses no BM25 and no embedding score. Its Recall@5 is 0.299 versus 0.281 for the 8B embedding model, a margin of 1.8 percentage points. It is slightly lower on R@3 and MRR.

Only three prompt ideas carried over from LongMemEval: user, conversation tag, and association. The exact wording, layers, and vector settings changed on PrefEval. This configuration placed last among four three-view candidates there, but still reached 0.299. The ideas may cross memory domains; the exact recipe does not.

## Why this matters for agents

The techniques are not new. The interesting part is what happens to the economics and architecture of agent memory when they are combined this way.

There is no hand-built memory schema, labeled training set, or separately trained retriever. The reasoning model can create the memory vectors inside its existing inference path, using about 24 KB per memory page for three views. No one will ever use a 2-trillion-parameter embedding model, but a future reasoning model may already carry a better memory representation in the same brain it uses to answer.

## Limits worth stating plainly

The LongMem result comes from the biased 94-question slice described above, where one question moves the metric by about 1.1 percentage points. Prompt and fusion choices were explored on the evaluated data, not a clean held-out set.

The PrefEval-derived task also has imperfect labels: only the paired preference and exact duplicates count as correct. In 100 reviewed misses, 58 found plausible same-topic statements, 28 found the topic but the wrong constraint, and 14 were unrelated. The score can miss useful alternatives, but same-topic does not always mean correct.

Results may change with another model, quantization, language, or prompt template. The work supports feasibility, not a decisive universal win over embedding models.

What it suggests is more specific and more useful: the memory an agent needs may already be present in the act of understanding, waiting to be read out rather than rebuilt by another model.
