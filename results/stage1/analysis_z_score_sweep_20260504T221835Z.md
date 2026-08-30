# Analysis: z_score_sweep

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_z_score_sweep_20260504T221835Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "configs": {
    "layer18_zscore_instance": {
      "n_total": 100,
      "n_scored": 94,
      "ignored_abstention_count": 6,
      "ignored_abstention_ids": [
        "0862e8bf_abs",
        "15745da0_abs",
        "bc8a6e93_abs",
        "19b5f2b3_abs",
        "29f2956b_abs",
        "f4f1d8a4_abs"
      ],
      "ignored_no_target_count": 0,
      "ignored_no_target_ids": [],
      "metrics": {
        "recall_all@1": {
          "mean": 0.0425531914893617,
          "ci95": {
            "low": 0.010638297872340425,
            "high": 0.0851063829787234
          }
        },
        "ndcg_any@1": {
          "mean": 0.09574468085106383,
          "ci95": {
            "low": 0.0425531914893617,
            "high": 0.14893617021276595
          }
        },
        "recall_all@3": {
          "mean": 0.11702127659574468,
          "ci95": {
            "low": 0.06382978723404255,
            "high": 0.18111702127659582
          }
        },
        "ndcg_any@3": {
          "mean": 0.12435771227610197,
          "ci95": {
            "low": 0.07267602822898946,
            "high": 0.17014694359867866
          }
        },
        "recall_all@5": {
          "mean": 0.2127659574468085,
          "ci95": {
            "low": 0.1276595744680851,
            "high": 0.2872340425531915
          }
        },
        "ndcg_any@5": {
          "mean": 0.16594767842980143,
          "ci95": {
            "low": 0.11554539539943559,
            "high": 0.21022773731788347
          }
        },
        "recall_all@10": {
          "mean": 0.40425531914893614,
          "ci95": {
            "low": 0.2978723404255319,
            "high": 0.5111702127659575
          }
        },
        "ndcg_any@10": {
          "mean": 0.2363558861088255,
          "ci95": {
            "low": 0.18163823049205452,
            "high": 0.28527573264960554
          }
        },
        "recall_all@30": {
          "mean": 0.6170212765957447,
          "ci95": {
            "low": 0.4997340425531915,
            "high": 0.7130319148936171
          }
        },
        "ndcg_any@30": {
          "mean": 0.30676265830964766,
          "ci95": {
            "low": 0.25576581581264174,
            "high": 0.34991604407500615
          }
        },
        "recall_all@50": {
          "mean": 0.723404255319149,
          "ci95": {
            "low": 0.6276595744680851,
            "high": 0.8085106382978723
          }
        },
        "ndcg_any@50": {
          "mean": 0.33359947846219246,
          "ci95": {
            "low": 0.28387512641976853,
            "high": 0.37493227370759713
          }
        }
      }
    },
    "layer18_zscore_global": {
      "n_total": 100,
      "n_scored": 94,
      "ignored_abstention_count": 6,
      "ignored_abstention_ids": [
        "0862e8bf_abs",
        "15745da0_abs",
        "bc8a6e93_abs",
        "19b5f2b3_abs",
        "29f2956b_abs",
        "f4f1d8a4_abs"
      ],
      "ignored_no_target_count": 0,
      "ignored_no_target_ids": [],
      "metrics": {
        "recall_all@1": {
          "mean": 0.0425531914893617,
          "ci95": {
            "low": 0.010638297872340425,
            "high": 0.0851063829787234
          }
        },
        "ndcg_any@1": {
          "mean": 0.10638297872340426,
          "ci95": {
            "low": 0.0425531914893617,
            "high": 0.1702127659574468
          }
        },
        "recall_all@3": {
          "mean": 0.1276595744680851,
          "ci95": {
            "low": 0.06382978723404255,
            "high": 0.19148936170212766
          }
        },
        "ndcg_any@3": {
          "mean": 0.13907421948236615,
          "ci95": {
            "low": 0.09243253342934053,
            "high": 0.19047573005538315
          }
        },
        "recall_all@5": {
          "mean": 0.23404255319148937,
          "ci95": {
            "low": 0.14867021276595743,
            "high": 0.3087765957446809
          }
        },
        "ndcg_any@5": {
 
```
