# Stage 3 Prompt Sweep Notes

Stage 3 is a prompt-variant sweep for chatbot memory retrieval. It keeps the
Stage 2 encoder path but writes new artifacts under Stage 3 locations:

- script: `scripts/stage3_prompt_sweep.py`
- vectors: `tensors/stage3_prompt_sweep/<run_label>/`
- online sanity metrics: `results/stage3_prompt_sweep/<run_label>.json`

The original Stage 2 scripts and vectors are left untouched.

## What Gets Stored

The vector store uses the existing chunked safetensors schema:

```text
states: (n_prompts, n_variants, n_layers, n_positions, hidden_dim)
```

For the approved Stage 3 defaults this means:

- variants: the Stage 3 prompt matrix plus inherited `P0`
- layers: `29,30,31`
- positions: `last`
- dtype: bf16 on disk

The manifest keeps `role`, `instance_index`, `question_id`, `candidate_id`, and
`is_gold`, so offline analysis can split candidates and queries and recover the
gold labels.

## Does This Support Later Vector-Combination Search?

Yes. The Stage 3 encoder stores raw vectors before anti-PCA, BM25 fusion, or any
retrieval-specific transformation. That means later offline scripts can combine
saved vectors without rerunning the model.

Useful combinations include:

- concatenating several prompt vectors into one larger vector;
- stacking several prompt vectors into a matrix and using a late-interaction or
  max-sim score;
- weighted score fusion across prompt variants, layers, or positions;
- asymmetric memory/query pairing, such as `2-3-2_mem` with `2-3-2_query`.

The current script does not implement those combination scorers. It only ensures
the raw material is preserved. A later offline evaluator can load the same
candidate/query rows and build combined representations from the variant/layer
axes.

## Multi-Token Follow-Up

TODO, separate research track: generate N tokens with greedy decoding and store
hidden states across the trajectory. Combination methods include concat, stack
matrix, and diff/relative-motion vectors. Approximate storage tiers for 30
instances are 0.57 GiB for 1 prompt x 1 layer x 1 state, 3.4 GiB for 1 x 3 x 2,
and 24 GiB for 7 x 3 x 2. PromptReps found first-token representations strongest
on BEIR, but chatbot memory may differ.
