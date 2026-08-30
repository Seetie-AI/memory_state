# PrefEval External Embedding Fusion

- Created UTC: `2026-05-13T02:02:35.194299+00:00`
- Items: `1000`
- Hidden tensor dir: `/Users/gordonxiong/Desktop/Repos/memory_state/benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- Embedding cache dir: `/Users/gordonxiong/Desktop/Repos/memory_state/benchmarks/PrefEval/tensors/qwen3_embedding_implicit_persona_n1000_d19e54c734`
- Embedding model: `models/Qwen3-Embedding-0.6B-4bit-DWQ`
- Source rule: `top20 source_count>=2`
- Elapsed: `24s`

## Notes

- External embeddings are used only as a score matrix/source, not concatenated with 9B hidden vectors.
- Primary K3 dense baseline is 2-3-1 + 2-5 + 2-1 with vector_average_component_norm.
- source_count>=2 experiments use per-source top-k lists, with prompt components kept as separate sources.

## Results

| rank | config | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR | avg shortlist | oracle@shortlist |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `k3_bm25_embedding_full_d0.75_b0.20_e0.05` | 0.114 | 0.257 | 0.352 | 0.196 | 0.235 | 0.225 |  |  |
| 2 | `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10` | 0.116 | 0.255 | 0.351 | 0.195 | 0.235 | 0.227 | 22.1 | 0.635 |
| 3 | `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05` | 0.117 | 0.258 | 0.348 | 0.197 | 0.234 | 0.227 | 22.1 | 0.635 |
| 4 | `k3_bm25_embedding_full_d0.70_b0.20_e0.10` | 0.116 | 0.257 | 0.348 | 0.196 | 0.234 | 0.227 |  |  |
| 5 | `k3_bm25_dense_top20_d0.75_b0.25` | 0.122 | 0.264 | 0.344 | 0.203 | 0.235 | 0.230 |  |  |
| 6 | `k3_key_assoc_topic_vector_average` | 0.126 | 0.265 | 0.339 | 0.205 | 0.235 | 0.231 |  |  |
| 7 | `five_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.119 | 0.255 | 0.339 | 0.196 | 0.231 | 0.226 | 22.1 | 0.635 |
| 8 | `four_source_top20_source_ge2_rerank_d0.75_b0.25` | 0.117 | 0.254 | 0.337 | 0.195 | 0.229 | 0.223 | 17.9 | 0.568 |
| 9 | `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10` | 0.123 | 0.254 | 0.336 | 0.198 | 0.231 | 0.229 | 22.1 | 0.635 |
| 10 | `k3_bm25_embedding_full_d0.65_b0.25_e0.10` | 0.121 | 0.254 | 0.336 | 0.197 | 0.230 | 0.227 |  |  |
| 11 | `k3_bm25_full_d0.75_b0.25` | 0.117 | 0.251 | 0.335 | 0.193 | 0.228 | 0.222 |  |  |
| 12 | `k3_bm25_embedding_full_d0.60_b0.25_e0.15` | 0.121 | 0.251 | 0.333 | 0.195 | 0.228 | 0.226 |  |  |
| 13 | `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15` | 0.119 | 0.254 | 0.333 | 0.196 | 0.228 | 0.227 | 22.1 | 0.635 |
| 14 | `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25` | 0.115 | 0.251 | 0.326 | 0.193 | 0.223 | 0.224 | 22.1 | 0.635 |
| 15 | `k3_bm25_embedding_full_d0.50_b0.25_e0.25` | 0.117 | 0.250 | 0.323 | 0.193 | 0.223 | 0.225 |  |  |
| 16 | `external_embedding` | 0.084 | 0.207 | 0.287 | 0.155 | 0.187 | 0.189 |  |  |
| 17 | `bm25` | 0.035 | 0.074 | 0.094 | 0.058 | 0.066 | 0.067 |  |  |

## Configs

- `k3_bm25_embedding_full_d0.75_b0.20_e0.05`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `five_source_top20_source_ge2_rerank_d0.70_b0.20_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `five_source_top20_source_ge2_rerank_d0.75_b0.20_e0.05`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.75 + BM25 0.20 + embedding 0.05.
- `k3_bm25_embedding_full_d0.70_b0.20_e0.10`: Full-corpus z-score fusion: K3 dense 0.70 + BM25 0.20 + embedding 0.10.
- `k3_bm25_dense_top20_d0.75_b0.25`: Dense top-20 shortlist reranked by K3 dense 0.75 + BM25 0.25.
- `k3_key_assoc_topic_vector_average`: Current clean K3 dense baseline: 2-3-1 + 2-5 + 2-1, vector_average_component_norm.
- `five_source_top20_source_ge2_rerank_d0.75_b0.25`: Five-source candidate screening: 3 prompt sources + BM25 + external embedding, source_count>=2, rerank=K3/BM25.
- `four_source_top20_source_ge2_rerank_d0.75_b0.25`: Four-source candidate screening: 3 prompt sources + BM25, source_count>=2, rerank=K3/BM25.
- `five_source_top20_source_ge2_rerank_d0.65_b0.25_e0.10`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_bm25_embedding_full_d0.65_b0.25_e0.10`: Full-corpus z-score fusion: K3 dense 0.65 + BM25 0.25 + embedding 0.10.
- `k3_bm25_full_d0.75_b0.25`: Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.25.
- `k3_bm25_embedding_full_d0.60_b0.25_e0.15`: Full-corpus z-score fusion: K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `five_source_top20_source_ge2_rerank_d0.60_b0.25_e0.15`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.60 + BM25 0.25 + embedding 0.15.
- `five_source_top20_source_ge2_rerank_d0.50_b0.25_e0.25`: Five-source candidate screening with same score rerank: source_count>=2, K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `k3_bm25_embedding_full_d0.50_b0.25_e0.25`: Full-corpus z-score fusion: K3 dense 0.50 + BM25 0.25 + embedding 0.25.
- `external_embedding`: External Qwen embedding standalone reference loaded from cache.
- `bm25`: BM25 standalone reference.
