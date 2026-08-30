# GGUF final embedding eval

This is a llama.cpp approximation: Base model, final embedding, P0 last-token pooling.

| Mode | Recall@5 | NDCG@5 | Scored |
|---|---:|---:|---:|
| cosine | 1.000 | 0.431 | 1 |
| centered_cosine | 1.000 | 0.431 | 1 |

Limits:
- Base model rather than the Stage 2 Instruct model.
- Final model embedding rather than internal layer-30 hidden state.
- llama.cpp GGUF path rather than the MLX hidden-state extractor.
