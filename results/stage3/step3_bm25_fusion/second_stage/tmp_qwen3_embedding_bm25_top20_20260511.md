# Temporary embedding + BM25 sweep

BM25 scope: `vector_top20`

| rank | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.70 | 0.681 | 0.789 | 0.745 | 0.809 | 0.856 | 0.989 | 94 |
| 2 | 0.75 | 0.681 | 0.785 | 0.745 | 0.802 | 0.852 | 0.989 | 94 |
| 3 | 0.80 | 0.681 | 0.785 | 0.745 | 0.801 | 0.848 | 0.989 | 94 |

## Inputs

- embedding_dir: `/Users/gordonxiong/Desktop/Repos/memory_state/tensors/stage3/embedding_eval/qwen3_embedding_8b_dwq_subset0-100`
- model_path: `models/Qwen3-Embedding-8B-4bit-DWQ`
- elapsed_seconds: 3.3
