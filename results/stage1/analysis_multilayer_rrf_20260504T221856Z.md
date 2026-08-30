# Analysis: multilayer_rrf

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_multilayer_rrf_20260504T221856Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "rrf_k": 60.0,
  "configs": {
    "rrf_layer21_22_23_final_center_instance": {
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
            "low": 0.24414893617021277,
            "high": 0.44680851063829785
          }
        },
        "ndcg_any@1": {
          "mean": 0.46808510638297873,
          "ci95": {
            "low": 0.3617021276595745,
            "high": 0.5851063829787234
          }
        },
        "recall_all@3": {
          "mean": 0.5106382978723404,
          "ci95": {
            "low": 0.41462765957446807,
            "high": 0.6066489361702129
          }
        },
        "ndcg_any@3": {
          "mean": 0.546757708344133,
          "ci95": {
            "low": 0.44737786045252154,
            "high": 0.6359477500679991
          }
        },
        "recall_all@5": {
          "mean": 0.6170212765957447,
          "ci95": {
            "low": 0.4997340425531915,
            "high": 0.7127659574468085
          }
        },
        "ndcg_any@5": {
          "mean": 0.5951407277716888,
          "ci95": {
            "low": 0.4979041298563668,
            "high": 0.6782297061771629
          }
        },
        "recall_all@10": {
          "mean": 0.7127659574468085,
          "ci95": {
            "low": 0.6063829787234043,
            "high": 0.7981382978723405
          }
        },
        "ndcg_any@10": {
          "mean": 0.6315340643740063,
          "ci95": {
            "low": 0.5401360119756625,
            "high": 0.7096141582471693
          }
        },
        "recall_all@30": {
          "mean": 0.8617021276595744,
          "ci95": {
            "low": 0.7872340425531915,
            "high": 0.9151595744680852
          }
        },
        "ndcg_any@30": {
          "mean": 0.6682526210816757,
          "ci95": {
            "low": 0.5944288108954681,
            "high": 0.7368426385246329
          }
        },
        "recall_all@50": {
          "mean": 0.9361702127659575,
          "ci95": {
            "low": 0.8827127659574469,
            "high": 0.9787234042553191
          }
        },
        "ndcg_any@50": {
          "mean": 0.6805329851131443,
          "ci95": {
            "low": 0.6080783249643738,
            "high": 0.7494020202633104
          }
        }
      }
    }
  }
}
```
