# Data availability

This repository contains code, experiment notes, the results overview, and the
result files produced by our runs. It does **not** redistribute the benchmark
datasets themselves, the downloaded HuggingFace caches, the model weights, or
the hidden-state tensor dumps.

The benchmark data belongs to its original authors. We do not republish it here
so that anyone using it goes to the original source and accepts the terms that
apply there. Please check the license and usage terms at each source below
before using the data.

## What is excluded, and where it lives locally

| Excluded path | What it holds | Why it is excluded |
|---|---|---|
| `data/` | LongMemEval cleaned JSON files | Third-party dataset |
| `benchmarks/PrefEval/data/` | Files derived from the PrefEval dataset | Derived from a third-party dataset |
| `benchmarks/PrefEval/.hf_home/` | HuggingFace dataset and hub cache | Third-party dataset cache |
| `models/` | Local MLX model weights | Large, and belongs to the model publishers |
| `tensors/`, `benchmarks/PrefEval/tensors/` | Hidden-state dumps | Large and regenerable from the scripts |

## LongMemEval

Used for the evidence-retrieval experiments at round granularity.

The cleaned files this project reads are `longmemeval_s_cleaned.json` and
`longmemeval_m_cleaned.json`. `scripts/download_data.py` fetches them from:

```
https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned
```

To download:

```bash
python scripts/download_data.py
```

The files land in `data/`, which is gitignored.

Benchmark paper: *LongMemEval: Benchmarking Chat Assistants on Long-Term
Interactive Memory*, <https://arxiv.org/abs/2410.10813>.

## PrefEval

Used for the implicit preference and persona memory experiments.

The dataset id is `siyanzhao/prefeval_implicit_persona`, loaded through the
HuggingFace `datasets` library. See `benchmarks/PrefEval/prefeval_benchmark.py`,
which reads the cache directory from the `HF_DATASETS_CACHE` environment
variable.

```bash
export HF_DATASETS_CACHE=benchmarks/PrefEval/.hf_home
python -c "from datasets import load_dataset; load_dataset('siyanzhao/prefeval_implicit_persona')"
```

Dataset page: <https://huggingface.co/datasets/siyanzhao/prefeval_implicit_persona>.

## Models

The reported runs use local 4-bit MLX conversions:

- `Qwen3.5-9B-MLX-4bit` for hidden-state extraction
- `Qwen3.5-2B-MLX-4bit` for the model-size check
- `Qwen3-Embedding-0.6B-4bit-DWQ` and `Qwen3-Embedding-8B-4bit-DWQ` as
  embedding baselines

Weights are not included. Obtain them from their publishers and place them
under `models/`, then follow the run instructions in `README.md`.
