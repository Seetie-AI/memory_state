# PrefEval Stage 1.1 Findings: More Prompts

Stage 1.1 adds a focused prompt supplement on top of Stage 1:

- `2-1-2`: topic prompt without "上面".
- `2-5-2`: association prompt without "上面".
- `2-3-3` / `2-5-3`: token-oriented, "direct token, readability not required".
- `1-1-2`: generic tag prompt without "上面".
- explicit CN/EN/RU/JA 1-1 variants.
- `1-1_EMOJI`.
- `2-7` interaction-pattern prompt.

All single-prompt results use n=1000, L28-L31, `anti_pca_both_k15`; tables
below use each prompt's best layer.

## Single-Prompt Takeaways

| prompt | best layer | R@3 | R@5 | NDCG@5 | note |
|---|---:|---:|---:|---:|---|
| `2-1-2` | L30 | 0.228 | 0.321 | 0.215 | best R@5 single prompt; better than old `2-1` |
| `2-3-1` | L30 | 0.254 | 0.312 | 0.218 | still best early-rank / NDCG core prompt |
| `2-5` | L29 | 0.235 | 0.301 | 0.204 | association prompt remains strong |
| `1-1_EMOJI` | L30 | 0.227 | 0.285 | 0.200 | strongest 1-1-family supplement |
| `2-7` | L30 | 0.178 | 0.229 | 0.161 | full n=1000 does not revive it |
| `1-1_RU_explicit` | L30 | 0.074 | 0.107 | 0.071 | Russian prompt collapses |

`1-1_EMOJI` is surprisingly strong: it beats the ordinary 1-1 wording variants
and is competitive with weaker semantic prompts. It does not beat `2-3-1`,
`2-5`, or `2-1-2`.

## Hypotheses

| hypothesis | result |
|---|---|
| Removing "上面" helps `2-1` | Confirmed. `2-1-2` R@5 = 0.321 vs old `2-1` R@5 = 0.299. |
| Removing "上面" helps generally | Not confirmed. `2-5-2` underperforms old `2-5`; `1-1-2` is only mid-tier. |
| Token-oriented wording helps | Mostly rejected. `2-3-3` and `2-5-3` do not beat their originals. |
| `2-7` may revive on PrefEval | Rejected for retrieval. It remains weak on full n=1000. |
| Language choice matters | Partially confirmed. CN/EN/JA are close; RU fails hard; emoji is the outlier winner. |

## Oracle Union

New oracle union sweep:

- `oracle_union_more_prompts_20260513.{json,md}`
- prompts: 25
- metric: a query is covered if any prompt retrieves a gold memory within top-k.

Best pair by union@3:

| pair | union@3 | union@5 | note |
|---|---:|---:|---|
| `2-5 + 2-1-2` | 0.313 | 0.398 | new strongest pair oracle |
| `2-5 + 2-1_token` | 0.311 | 0.381 | previous strong diversity pair |
| `2-3-2_query + 2-5` | 0.306 | 0.376 | strong but more overlapping |
| `2-3-1 + 2-5` | 0.300 | 0.369 | current core base pair |
| `2-5 + 1-1_EMOJI` | 0.299 | 0.368 | emoji is good, but not a top diversity add |

Fixed base pair `2-3-1 + 2-5`, plus one prompt:

| third prompt | union@3 | union@5 | note |
|---|---:|---:|---|
| `2-1_token` | 0.339 | 0.415 | best union@3 third prompt |
| `1-1_EN_explicit` | 0.332 | 0.412 | surprisingly high diversity |
| `2-1-2` | 0.332 | 0.417 | best union@5 among top third prompts |
| `1-1_EMOJI` | 0.322 | 0.399 | useful but not exceptional as third prompt |
| old `2-1` | 0.326 | 0.410 | worse than `2-1-2` on union@5 |

## Current Decision

- Promote `2-1-2` as a strong single-prompt topic candidate, but do not assume
  single-prompt treatment gains add linearly inside K3. The later K3 contrast
  shows old `2-1` remains stronger than the treated topic stack after fusion.
- Keep `2-3-1` and `2-5` as core prompts.
- Test K3 variants that replace old `2-1` with `2-1-2`.
- Keep `1-1_EMOJI` as a diversity/diagnostic prompt, but do not promote it to
  default K3 without a real fusion win.
- Retire `2-5-2`, `2-3-3`, and `2-5-3` from the main retrieval path.
- Do not retire the dynamics axis for companion work. Later treatment runs show
  `2-7_emoji` is a viable interaction-dynamics third slot: it beats the
  emotion-anchor `2-8_emoji` on final R@1/R@5 under the same 60/30/10
  full-corpus fusion, while only slightly trailing on R@3.

## Final Config Update

The final Stage 1.1 retrieval document now separates benchmark and product
goals:

| named config | K3 third slot | final R@1 | final R@3 | final R@5 | interpretation |
|---|---|---:|---:|---:|---|
| `prefeval_best_retrieval` | old `2-1` topic | 0.119 | 0.265 | 0.355 | report this for PrefEval-best retrieval |
| `companion_balanced_retrieval_dynamics` | `2-7_emoji` dynamics | 0.125 | 0.259 | 0.341 | current balanced companion candidate |
| `companion_balanced_retrieval_emotion` | `2-8_emoji` emotion | 0.122 | 0.265 | 0.332 | explicit emotion-anchor alternative |

See `final_retrieval_config.md` for the full contrast table and reproduction
rows.
