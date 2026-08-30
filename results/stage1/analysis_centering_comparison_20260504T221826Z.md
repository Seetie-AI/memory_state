# Analysis: centering_comparison

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_centering_comparison_20260504T221826Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "configs": {
    "layer18_cosine": {
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
          "mean": 0.0851063829787234,
          "ci95": {
            "low": 0.0425531914893617,
            "high": 0.13829787234042554
          }
        },
        "ndcg_any@1": {
          "mean": 0.1276595744680851,
          "ci95": {
            "low": 0.06382978723404255,
            "high": 0.18085106382978725
          }
        },
        "recall_all@3": {
          "mean": 0.1595744680851064,
          "ci95": {
            "low": 0.09574468085106383,
            "high": 0.22340425531914893
          }
        },
        "ndcg_any@3": {
          "mean": 0.16336351103203242,
          "ci95": {
            "low": 0.10608321889078687,
            "high": 0.2147501287105265
          }
        },
        "recall_all@5": {
          "mean": 0.24468085106382978,
          "ci95": {
            "low": 0.14893617021276595,
            "high": 0.3404255319148936
          }
        },
        "ndcg_any@5": {
          "mean": 0.19988100790748128,
          "ci95": {
            "low": 0.13956711641698719,
            "high": 0.2585533342205306
          }
        },
        "recall_all@10": {
          "mean": 0.32978723404255317,
          "ci95": {
            "low": 0.23351063829787236,
            "high": 0.4148936170212766
          }
        },
        "ndcg_any@10": {
          "mean": 0.2323606674585355,
          "ci95": {
            "low": 0.16924923997246066,
            "high": 0.2864901113916964
          }
        },
        "recall_all@30": {
          "mean": 0.5212765957446809,
          "ci95": {
            "low": 0.41462765957446807,
            "high": 0.6276595744680851
          }
        },
        "ndcg_any@30": {
          "mean": 0.29541497488557794,
          "ci95": {
            "low": 0.23512353582880086,
            "high": 0.34664028287142523
          }
        },
        "recall_all@50": {
          "mean": 0.6170212765957447,
          "ci95": {
            "low": 0.5,
            "high": 0.7130319148936171
          }
        },
        "ndcg_any@50": {
          "mean": 0.3161121017824245,
          "ci95": {
            "low": 0.2582232287880794,
            "high": 0.366600762920979
          }
        }
      }
    },
    "layer18_center_instance": {
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
          "mean": 0.0851063829787234,
          "ci95": {
            "low": 0.031914893617021274,
            "high": 0.13829787234042554
          }
        },
        "recall_all@3": {
          "mean": 0.09574468085106383,
          "ci95": {
            "low": 0.05319148936170213,
            "high": 0.14893617021276595
          }
        },
        "ndcg_any@3": {
          "mean": 0.11088840994352783,
          "ci95": {
            "low": 0.06439446043677124,
            "high": 0.15330765645910863
          }
        },
        "recall_all@5": {
          "mean": 0.1702127659574468,
          "ci95": {
            "low": 0.09574468085106383,
            "high": 0.2553191489361702
          }
        },
        "ndcg_any@5": {
          "mean": 0.15090
```
