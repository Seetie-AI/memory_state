# Stage 3 Step 2: Sparse Logits Fusion

This folder contains the Stage 3 step 2 sparse-logits fusion probe.

Unlike `logits_screening/`, this earlier probe used saved top-256 logits
directly, without filtering to tokens appearing in the original text. It showed
that sparse logits contain retrieval signal and can help rerank in a small
second stage, but they are not strong enough to replace hidden-state vectors.

Main script: `scripts/stage3_logits_sparse_fusion.py`

