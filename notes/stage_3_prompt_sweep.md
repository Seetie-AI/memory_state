# Stage 3 Prompt Sweep Notes

Stage 3 is a prompt-variant sweep for chatbot memory retrieval. It keeps the
Stage 2 encoder path but writes new artifacts under Stage 3 locations:

- script: `scripts/stage3_prompt_sweep.py`
- vectors: `tensors/stage3/prompt_sweep/<run_label>/`
- online sanity metrics: `results/stage3/prompt_sweep/<run_label>.json`

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

Optional sparse logits can be stored with `--store-topk-logits K`. When enabled,
each chunk also contains:

```text
top_logit_token_ids: (n_prompts, n_variants, n_positions, K)
top_logit_values:    (n_prompts, n_variants, n_positions, K)
```

These are final-layer next-token logits at the same prompt positions as the
hidden vectors. They do not repeat across the layer axis. The option defaults to
`0` because full-vocab distributions would be too large, while top-K logits are
only a lightweight sparse audit signal.

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

## Runtime Safety

Stage 3 writes under `tensors/stage3/prompt_sweep/` and flushes a chunk after
each instance. If the process receives SIGINT or SIGTERM, the writer is closed in
the cleanup path so completed rows are preserved.

The default runtime knobs are conservative for the 16GB Mac target:

- `--metal-cache-limit-gb 2`: keep a bounded MLX/Metal reusable allocation cache.
- `--clear-cache-every row`: reuse Metal buffers across all suffix prompts for
  one text row, then clear them. This does not delete the live prefix KV cache;
  it only controls reusable temporary buffers.
- `--profile-timing`: optional coarse timing profiler. It persists aggregate
  prefix prefill, suffix encode, vector writing, chunk flush, and online scoring
  timings in the result JSON without storing per-row traces.

## Multi-Machine Splits

Use `--subset-start S --subset N` to encode a disjoint global instance slice.
The script preserves original LongMemEval `instance_index` values in prompt IDs
and metadata so two machines can be merged later without label collisions.

Machine B can run from the prepared `airdrop_machineB/` folder. After its
`output/` folder returns, merge the two vector stores with:

```bash
python scripts/stage3_merge_stores.py \
  --store-a tensors/stage3/prompt_sweep/<machineA_vectors> \
  --store-b tensors/stage3/prompt_sweep/<imported_machineB_vectors> \
  --output-dir tensors/stage3/prompt_sweep/<merged_vectors>
```

Final anti-PCA/retrieval analysis should run on the merged store. Split metrics
are only smoke checks because PCA components depend on the full candidate
corpus.

Current local merged store:

```text
tensors/stage3/prompt_sweep/merged_subset0-100_cache2gb_logits256/
```

This store was created after machine A and B completed disjoint slices. The
current local merge used a CPU byte-preserving chunk-copy fallback because MLX
was unavailable in the maintenance session; see the store-local
`MERGE_NOTES.md` for audit details and differences from the canonical rechunking
merge script.

## Multi-Token Follow-Up

TODO, separate research track: generate N tokens with greedy decoding and store
hidden states across the trajectory. Combination methods include concat, stack
matrix, and diff/relative-motion vectors. Approximate storage tiers for 30
instances are 0.57 GiB for 1 prompt x 1 layer x 1 state, 3.4 GiB for 1 x 3 x 2,
and 24 GiB for 7 x 3 x 2. PromptReps found first-token representations strongest
on BEIR, but chatbot memory may differ.
