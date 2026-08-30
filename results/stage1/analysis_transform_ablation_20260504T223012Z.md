# Analysis: transform_ablation

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_transform_ablation_20260504T223012Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "configs": {
    "layer22_raw_cosine": {
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
          "mean": 0.2765957446808511,
          "ci95": {
            "low": 0.19122340425531914,
            "high": 0.3723404255319149
          }
        },
        "ndcg_any@1": {
          "mean": 0.3723404255319149,
          "ci95": {
            "low": 0.27632978723404256,
            "high": 0.4683510638297873
          }
        },
        "recall_all@3": {
          "mean": 0.44680851063829785,
          "ci95": {
            "low": 0.3191489361702128,
            "high": 0.5425531914893617
          }
        },
        "ndcg_any@3": {
          "mean": 0.44274499515057414,
          "ci95": {
            "low": 0.35478181727635333,
            "high": 0.5350284890164055
          }
        },
        "recall_all@5": {
          "mean": 0.5425531914893617,
          "ci95": {
            "low": 0.425531914893617,
            "high": 0.648936170212766
          }
        },
        "ndcg_any@5": {
          "mean": 0.4809628696967674,
          "ci95": {
            "low": 0.39419689450176504,
            "high": 0.56506921795749
          }
        },
        "recall_all@10": {
          "mean": 0.5957446808510638,
          "ci95": {
            "low": 0.47845744680851066,
            "high": 0.6808510638297872
          }
        },
        "ndcg_any@10": {
          "mean": 0.5150318800156444,
          "ci95": {
            "low": 0.43218499741081184,
            "high": 0.5930237002825487
          }
        },
        "recall_all@30": {
          "mean": 0.7446808510638298,
          "ci95": {
            "low": 0.648936170212766,
            "high": 0.8297872340425532
          }
        },
        "ndcg_any@30": {
          "mean": 0.5587888260674766,
          "ci95": {
            "low": 0.48736304324192614,
            "high": 0.6336940193917024
          }
        },
        "recall_all@50": {
          "mean": 0.8297872340425532,
          "ci95": {
            "low": 0.7446808510638298,
            "high": 0.8936170212765957
          }
        },
        "ndcg_any@50": {
          "mean": 0.5754925904558049,
          "ci95": {
            "low": 0.5096433277629122,
            "high": 0.64944928035534
          }
        }
      }
    },
    "layer22_center_both": {
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
          "mean": 0.3829787234042553,
          "ci95": {
            "low": 0.26595744680851063,
            "high": 0.48936170212765956
          }
        },
        "ndcg_any@1": {
          "mean": 0.5212765957446809,
          "ci95": {
            "low": 0.40425531914893614,
            "high": 0.6170212765957447
          }
        },
        "recall_all@3": {
          "mean": 0.5425531914893617,
          "ci95": {
            "low": 0.425531914893617,
            "high": 0.6382978723404256
          }
        },
        "ndcg_any@3": {
          "mean": 0.5825728489683262,
          "ci95": {
            "low": 0.49110968750206097,
            "high": 0.6645536330222814
          }
        },
        "recall_all@5": {
          "mean": 0.6382978723404256,
          "ci95": {
            "low": 0.5212765957446809,
            "high": 0.7236702127659576
          }
        },
        "ndcg_any@5": {
          "mean": 0.62554713154256
```
