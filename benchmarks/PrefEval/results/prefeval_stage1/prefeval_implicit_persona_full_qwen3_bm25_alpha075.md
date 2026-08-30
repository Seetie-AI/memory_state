# PrefEval Qwen3-Embedding + BM25

- Created UTC: `2026-05-12T01:40:37.467404+00:00`
- Dataset: `siyanzhao/prefeval_implicit_persona`
- Items: `1000`
- Alpha: `0.75`
- Elapsed: `22m23s`

| rank | retriever | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `qwen3_embedding` | 0.093 | 0.216 | 0.281 | 0.191 | 0.200 |
| 2 | `qwen3_embedding_bm25_alpha0.75` | 0.096 | 0.212 | 0.273 | 0.189 | 0.195 |
| 3 | `bm25` | 0.035 | 0.074 | 0.094 | 0.066 | 0.067 |
