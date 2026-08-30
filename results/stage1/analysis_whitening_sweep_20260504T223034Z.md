# Analysis: whitening_sweep

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_whitening_sweep_20260504T223034Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "configs": {
    "layer22_whitening_global_lambda0.01_dim128": {
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
          "mean": 0.35106382978723405,
          "ci95": {
            "low": 0.2656914893617021,
            "high": 0.4574468085106383
          }
        },
        "ndcg_any@1": {
          "mean": 0.4787234042553192,
          "ci95": {
            "low": 0.3723404255319149,
            "high": 0.574468085106383
          }
        },
        "recall_all@3": {
          "mean": 0.5638297872340425,
          "ci95": {
            "low": 0.4574468085106383,
            "high": 0.6595744680851063
          }
        },
        "ndcg_any@3": {
          "mean": 0.592984724599691,
          "ci95": {
            "low": 0.5105462895531853,
            "high": 0.6612468906319965
          }
        },
        "recall_all@5": {
          "mean": 0.6702127659574468,
          "ci95": {
            "low": 0.584840425531915,
            "high": 0.7659574468085106
          }
        },
        "ndcg_any@5": {
          "mean": 0.6246029989377967,
          "ci95": {
            "low": 0.5450128338125653,
            "high": 0.6869298911860452
          }
        },
        "recall_all@10": {
          "mean": 0.7553191489361702,
          "ci95": {
            "low": 0.6702127659574468,
            "high": 0.8404255319148937
          }
        },
        "ndcg_any@10": {
          "mean": 0.66524002268213,
          "ci95": {
            "low": 0.5975518428382981,
            "high": 0.7153730726579457
          }
        },
        "recall_all@30": {
          "mean": 0.9042553191489362,
          "ci95": {
            "low": 0.8297872340425532,
            "high": 0.9574468085106383
          }
        },
        "ndcg_any@30": {
          "mean": 0.6963756617794568,
          "ci95": {
            "low": 0.6329786518058157,
            "high": 0.7474283649029135
          }
        },
        "recall_all@50": {
          "mean": 0.9468085106382979,
          "ci95": {
            "low": 0.9042553191489362,
            "high": 0.9893617021276596
          }
        },
        "ndcg_any@50": {
          "mean": 0.702628064531816,
          "ci95": {
            "low": 0.6428062962778597,
            "high": 0.7508588871058425
          }
        }
      }
    },
    "layer22_whitening_global_lambda0.01_dim256": {
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
          "mean": 0.3723404255319149,
          "ci95": {
            "low": 0.26595744680851063,
            "high": 0.4787234042553192
          }
        },
        "ndcg_any@1": {
          "mean": 0.46808510638297873,
          "ci95": {
            "low": 0.3827127659574468,
            "high": 0.5638297872340425
          }
        },
        "recall_all@3": {
          "mean": 0.5638297872340425,
          "ci95": {
            "low": 0.4678191489361702,
            "high": 0.6595744680851063
          }
        },
        "ndcg_any@3": {
          "mean": 0.5994909950288905,
          "ci95": {
            "low": 0.5127572780899614,
            "high": 0.6619291351239522
          }
        },
        "recall_all@5": {
          "mean": 0.6382978723404256,
          "ci95": {
            "low": 0.5316489361702128,
            "high": 0.723404255319149
          }
        },
        "ndcg_any@5"
```
