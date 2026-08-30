# PrefEval Stage 2 Retrieval-Only

- Created UTC: `2026-05-13T04:44:28.976694+00:00`
- Items: `1000`
- Distractor chunks/query: `119`
- Candidate pool/query: `120`
- Turns: `300`
- Chunk size / stride: `10` / `5`
- Elapsed: `1s`

| rank | retriever | R@1 | R@3 | R@5 | R@10 | R@20 | MRR | mean_rank | margin |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `bm25` | 0.044 | 0.064 | 0.077 | 0.090 | 0.120 | 0.069 | 94.2 | -11.770 |

## Rank Histograms

### `bm25`

| bucket | count |
|---|---:|
| `1` | 44 |
| `2-3` | 20 |
| `4-5` | 13 |
| `6-10` | 13 |
| `11-20` | 30 |
| `>20` | 880 |

