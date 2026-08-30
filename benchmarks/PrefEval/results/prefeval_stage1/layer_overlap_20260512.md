# PrefEval Stage 1 Offline Analysis

- Created UTC: `2026-05-12T18:52:06.278006+00:00`
- Analysis: `prefeval_stage1_layer_overlap`
- Items: `1000`
- Tensor dir: `/Users/gordonxiong/Desktop/Repos/memory_state/benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128`
- Elapsed: `4s`

## Notes

- Stored hidden vectors are raw extractor outputs; this offline pass applies retrieval transforms after loading.
- The n=1000 prompt-sweep table previously reported anti_pca_both_k15 plus L2-normalized cosine, not untreated raw cosine.
- candidate_only k=10 is a sanity check because earlier LongMemEval stages found candidate-only transforms harmful.

## Results

| rank | split | config | R@1 | R@3 | R@5 | NDCG@5 | MRR |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | `all` | `layer_overlap_2-3-1_L29_L30_zsum` | 0.111 | 0.245 | 0.311 | 0.217 | 0.214 |
| 2 | `all` | `layer_overlap_2-3-1_L28_L29_L30_L31_zsum` | 0.107 | 0.248 | 0.307 | 0.214 | 0.210 |
| 3 | `all` | `layer_overlap_2-3-1_L28_L29_L30_zsum` | 0.107 | 0.243 | 0.306 | 0.212 | 0.210 |

## Oracle Union Diagnostics

| combo | split | any_hit@5 | recall_all@5 | best_component_any@5 | gain | mean_jaccard@5 |
|---|---|---:|---:|---:|---:|---:|
| `2-3-1_L29_L30` | `all` | 0.327 | 0.327 | 0.312 | 0.015 | 0.815 |
| `2-3-1_L28_L29_L30` | `all` | 0.337 | 0.337 | 0.312 | 0.025 | 0.790 |
| `2-3-1_L28_L29_L30_L31` | `all` | 0.357 | 0.356 | 0.312 | 0.045 | 0.689 |

## Configs

- `layer_overlap_2-3-1_L29_L30_zsum`: Layer z-sum diagnostic for 2-3-1_L29_L30 (zsum)
- `layer_overlap_2-3-1_L28_L29_L30_L31_zsum`: Layer z-sum diagnostic for 2-3-1_L28_L29_L30_L31 (zsum)
- `layer_overlap_2-3-1_L28_L29_L30_zsum`: Layer z-sum diagnostic for 2-3-1_L28_L29_L30 (zsum)
