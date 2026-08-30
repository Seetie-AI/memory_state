# PrefEval Automatic Retrieval

- Created UTC: `2026-05-12T00:50:45.773363+00:00`
- Task: `implicit_persona`
- Dataset: `siyanzhao/prefeval_implicit_persona`
- Items: `30`
- Gold policy: `same_preference_text`
- Elapsed: `2s`

## Results

| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `bm25` | 0.033 | 0.167 | 0.300 | 0.113 | 0.168 | 0.179 |

## Configs

- `bm25`: BM25 over preference memory strings

## Prompt Notes

- `2-7`: `
用一个词标记上面这段对话的互动模式，这个词是：“`
- `2-8`: `
用一个词标记回答上面这段对话中的对方时最该采用的策略，这个词是：“`
