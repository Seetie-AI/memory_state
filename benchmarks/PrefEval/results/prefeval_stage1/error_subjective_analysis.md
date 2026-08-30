# PrefEval Error Subjective Analysis

Date: 2026-05-12

## Setup

- Benchmark: PrefEval `implicit_persona`, n=1000
- Retriever: `k3_key_assoc_topic_vector_average_component_norm_dense_bm25_d0.75_b0.25`
- K3 prompts: `2-3-1 + 2-5 + 2-1`
- Scoring: component-normalized vector average, then `0.75 * z(dense) + 0.25 * z(BM25)`
- Error set: cases where gold memory is not in top5
- Error count: 665 / 1000
- Subjective sample: 100 errors, random seed 13
- Raw sampled cases: `error_subjective_analysis_cases.json`

## Label Scheme

The two target labels are useful but not quite enough, so I used one middle
bucket:

| Label | Meaning |
|---|---|
| Reasonable same-topic candidate | Top1 is semantically plausible for the query, often same topic / same user-preference axis, but not the benchmark gold. This suggests benchmark ceiling or multi-answer ambiguity. |
| Same topic, wrong constraint | Top1 is in the right broad topic but misses the key constraint: allergy vs style, vegan vs halal, no VR vs no sports, etc. This is method headroom. |
| Clearly unrelated | Top1 is from a different domain or triggered by superficial lexical/topic overlap. This is clear method headroom. |

## Subjective Counts

| Bucket | Count / 100 | Interpretation |
|---|---:|---|
| Reasonable same-topic candidate | 58 | A large fraction of misses are not nonsense; top1 would often be useful in a product setting. |
| Same topic, wrong constraint | 28 | Retrieval finds the right neighborhood but cannot select the exact preference axis. |
| Clearly unrelated | 14 | There is still clear retrieval space, but this is not the dominant error mode. |

If forced into the original binary framing:

| Binary view | Count / 100 |
|---|---:|
| Same-topic / plausible / ceiling pressure | 58 |
| Method headroom: wrong constraint or unrelated | 42 |

## Representative Cases

### Near-Ceiling / Reasonable Same-Topic

| Case | Query | Gold | Top1 | Note |
|---:|---|---|---|---|
| 27 | Sofa upholstery fabrics | Dislikes synthetic fabrics, prefers natural fibers | Dislikes synthetic fabrics, prefers natural fibers in home textiles | Essentially equivalent; benchmark false negative / duplicate wording issue. |
| 75 | NY to LA transportation | Fear of flying; avoid air travel | Strong aversion to flying; ground transportation | Essentially equivalent. |
| 89 | Hotels in Paris | Dislikes chain hotels; prefers independent properties | Avoids chain hotels; prefers boutique accommodations | Essentially equivalent. |
| 93 | Low-maintenance pet | Only wants hypoallergenic pets | Allergic to pet dander; only hypoallergenic animals | Essentially equivalent. |
| 40 | Pleasant-scent body lotions | Avoids synthetic fragrances | Dislikes citrus/fruity fragrances | Same product axis; not exact but still plausible. |
| 17 | Outdoor adventures in Costa Rica | Fear of heights / no ziplining | Dislikes adventure sports | Broader but still useful. |

### Same Topic, Wrong Constraint

| Case | Query | Gold | Top1 | Why it matters |
|---:|---|---|---|---|
| 5 | New Orleans cuisine | Severe shellfish allergy | Avoids molecular gastronomy | Same food/travel domain, but misses a hard safety constraint. |
| 45 | Thailand street food | Severe peanut/tree nut allergy | Avoids street food hygiene risk | Same query setting, wrong reason. |
| 52 | Bangkok restaurants | Severe peanut allergy | Avoids spicy food | Same cuisine domain, misses critical allergy. |
| 31 | Istanbul restaurants | Vegan-only dedicated vegan menu | Halal options | Same dietary category, wrong constraint. |
| 30 | Smartphone recommendation | Needs physical buttons | Removable batteries | Same device domain, wrong hardware constraint. |
| 60 | Recent TV series | Avoid supernatural elements | Avoid shows over three seasons | Same entertainment domain, wrong preference axis. |
| 70 | Immersive RPGs | Avoid crafting/resource systems | Likes character customization | Same game genre, wrong feature dimension. |

### Clearly Unrelated / Lexical Leakage

| Case | Query | Gold | Top1 | Failure pattern |
|---:|---|---|---|---|
| 15 | Keep up with AI developments | Dislikes long articles / papers | Prefers driver-assist car tech | Cross-domain technology leakage. |
| 32 | Apps for environmental science | Avoids in-app purchases | Uses eco-friendly appliances | Keyword `environmental` pulled home appliance memory. |
| 33 | Creative writing course resources | Prefers logical step-by-step learning | Avoids books without music composition focus | Cross-domain resource/book leakage. |
| 68 | Graphic design learning platforms | Needs scheduled interactive classes | Avoids games with graphic violence | Lexical `graphic` collision. |
| 97 | Hawaii activities | Avoids water activities because cannot swim | Dislikes cold-weather activities | Travel/activity topic, wrong environment. |

## Observations

1. PrefEval is not purely fact retrieval. Many misses are actually reasonable
   alternate memories for the same user query. This creates a real ceiling for
   retrieval-style evaluation with a single gold memory.

2. The largest useful improvement target is not broad topic matching. The
   retriever already often finds the right topic. The missing skill is selecting
   the exact constraint axis: allergy, material, modality, format, safety,
   aversion target, or diet rule.

3. Safety / hard-constraint misses are important. Food allergy, vegan diet,
   fear of heights, motion sickness, and medical constraints appear repeatedly.
   In product terms, these errors matter more than benign style misses.

4. BM25 does not solve this by itself. It helps lexical overlap, but many
   failures are same-topic alternatives where lexical overlap can be misleading.

5. The benchmark likely underestimates product usefulness for companion memory:
   a retrieved top1 can be non-gold but still useful personalization context.
   However, it still exposes a real ranking problem for hard constraints.

## Recommendation

Keep PrefEval as a stress test, but do not treat R@5 as a pure product ceiling.
For product-facing validation, add a classification-style eval where the model
chooses whether a candidate memory is applicable to the query. That can separate:

- genuinely applicable alternate memories,
- same-topic but wrong-constraint memories,
- unrelated memories.

For retrieval improvement, the most promising second stage is a lightweight
constraint-aware reranker over top20/top50 candidates, not more broad prompt
fusion.
