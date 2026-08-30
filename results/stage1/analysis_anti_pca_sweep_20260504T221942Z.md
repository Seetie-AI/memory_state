# Analysis: anti_pca_sweep

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_anti_pca_sweep_20260504T221942Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "configs": {
    "layer22_anti_pca_instance_k1": {
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
            "low": 0.2654255319148936,
            "high": 0.47898936170212775
          }
        },
        "ndcg_any@1": {
          "mean": 0.5106382978723404,
          "ci95": {
            "low": 0.3829787234042553,
            "high": 0.6170212765957447
          }
        },
        "recall_all@3": {
          "mean": 0.5425531914893617,
          "ci95": {
            "low": 0.43617021276595747,
            "high": 0.6382978723404256
          }
        },
        "ndcg_any@3": {
          "mean": 0.5846305766663822,
          "ci95": {
            "low": 0.4815461053499076,
            "high": 0.6593205285362219
          }
        },
        "recall_all@5": {
          "mean": 0.648936170212766,
          "ci95": {
            "low": 0.5319148936170213,
            "high": 0.7343085106382979
          }
        },
        "ndcg_any@5": {
          "mean": 0.6148220513724463,
          "ci95": {
            "low": 0.5153673320128506,
            "high": 0.6922746414583621
          }
        },
        "recall_all@10": {
          "mean": 0.7021276595744681,
          "ci95": {
            "low": 0.5957446808510638,
            "high": 0.7872340425531915
          }
        },
        "ndcg_any@10": {
          "mean": 0.6456021187155857,
          "ci95": {
            "low": 0.5608773032264548,
            "high": 0.7170994156424031
          }
        },
        "recall_all@30": {
          "mean": 0.8404255319148937,
          "ci95": {
            "low": 0.7659574468085106,
            "high": 0.9042553191489362
          }
        },
        "ndcg_any@30": {
          "mean": 0.6826657715709332,
          "ci95": {
            "low": 0.6030425658688549,
            "high": 0.7480485111235887
          }
        },
        "recall_all@50": {
          "mean": 0.8723404255319149,
          "ci95": {
            "low": 0.7978723404255319,
            "high": 0.9361702127659575
          }
        },
        "ndcg_any@50": {
          "mean": 0.6903202292140014,
          "ci95": {
            "low": 0.6168269338625662,
            "high": 0.7519137091589961
          }
        }
      }
    },
    "layer22_anti_pca_global_k1": {
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
          "mean": 0.39361702127659576,
          "ci95": {
            "low": 0.2765957446808511,
            "high": 0.48936170212765956
          }
        },
        "ndcg_any@1": {
          "mean": 0.5212765957446809,
          "ci95": {
            "low": 0.4039893617021276,
            "high": 0.6066489361702129
          }
        },
        "recall_all@3": {
          "mean": 0.5531914893617021,
          "ci95": {
            "low": 0.44680851063829785,
            "high": 0.648936170212766
          }
        },
        "ndcg_any@3": {
          "mean": 0.5961717782253461,
          "ci95": {
            "low": 0.5056057701888682,
            "high": 0.6689223814813453
          }
        },
        "recall_all@5": {
          "mean": 0.6276595744680851,
          "ci95": {
            "low": 0.5,
            "high": 0.7130319148936171
          }
        },
        "ndcg_any@5": {
          "mean": 0.62272868264915
```
