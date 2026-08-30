# Analysis: score_fusion_alpha_sweep

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_score_fusion_alpha_sweep_20260504T224542Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "score_normalization": "zscore within hidden top-50",
  "alphas": {
    "0.0": {
      "n_predictions": 100,
      "turn_metrics": {
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
            "mean": 0.3404255319148936,
            "ci95": {
              "low": 0.2553191489361702,
              "high": 0.425531914893617
            }
          },
          "ndcg_any@1": {
            "mean": 0.43617021276595747,
            "ci95": {
              "low": 0.35106382978723405,
              "high": 0.5319148936170213
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
            "mean": 0.5330471654124656,
            "ci95": {
              "low": 0.4550604716991863,
              "high": 0.6101907052801208
            }
          },
          "recall_all@5": {
            "mean": 0.6063829787234043,
            "ci95": {
              "low": 0.5106382978723404,
              "high": 0.7021276595744681
            }
          },
          "ndcg_any@5": {
            "mean": 0.5604405215702234,
            "ci95": {
              "low": 0.4863666433136439,
              "high": 0.6335777848275205
            }
          },
          "recall_all@10": {
            "mean": 0.6702127659574468,
            "ci95": {
              "low": 0.574468085106383,
              "high": 0.7659574468085106
            }
          },
          "ndcg_any@10": {
            "mean": 0.5936581911281649,
            "ci95": {
              "low": 0.5223009207385365,
              "high": 0.664228183993603
            }
          },
          "recall_all@20": {
            "mean": 0.7446808510638298,
            "ci95": {
              "low": 0.6595744680851063,
              "high": 0.8297872340425532
            }
          },
          "ndcg_any@20": {
            "mean": 0.6266596516100543,
            "ci95": {
              "low": 0.5596231064506176,
              "high": 0.6915855890687532
            }
          },
          "recall_all@30": {
            "mean": 0.8297872340425532,
            "ci95": {
              "low": 0.7553191489361702,
              "high": 0.9042553191489362
            }
          },
          "ndcg_any@30": {
            "mean": 0.6414595252332247,
            "ci95": {
              "low": 0.5795280809922023,
              "high": 0.7031724412262045
            }
          },
          "recall_all@50": {
            "mean": 0.9468085106382979,
            "ci95": {
              "low": 0.8936170212765957,
              "high": 0.9893617021276596
            }
          },
          "ndcg_any@50": {
            "mean": 0.6588027848453466,
            "ci95": {
              "low": 0.6022216012599426,
              "high": 0.7158536561620764
            }
          }
        }
      },
      "session_metrics": {
        "session_hit@1": 0.6063829787234043,
        "session_recall_all@1": 0.4148936170212766,
        "session_hit@3": 0.851063829787234,
        "session_recall_all@3": 0.6276595744680851,
        "session_hit@5": 0.925531914893617,
        "session_recall_all@5": 0.7127659574468085,
        "session_hit@10": 0.9574468085106383,
        "session_recall_all@10": 0.7553191489361702,
        "session_hit@20": 0.9893617021276596,
        "session_recall_all@20": 0.9042553191489362,
        "session_hit@30": 0.9893617021276596,
        "session_recall_all@30": 0.9361702127659575,
        "session_hit@50": 0.9893617021276596,
        "session_reca
```
