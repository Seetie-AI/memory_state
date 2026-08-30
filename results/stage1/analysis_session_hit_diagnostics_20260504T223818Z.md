# Analysis: session_hit_diagnostics

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_session_hit_diagnostics_20260504T223818Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "config": "layer22_anti_pca_global_k10",
  "groups": {
    "1_gold": {
      "n": 64,
      "turn_metrics": {
        "n_total": 64,
        "n_scored": 64,
        "ignored_abstention_count": 0,
        "ignored_abstention_ids": [],
        "ignored_no_target_count": 0,
        "ignored_no_target_ids": [],
        "metrics": {
          "recall_all@1": {
            "mean": 0.59375,
            "ci95": {
              "low": 0.46875,
              "high": 0.734375
            }
          },
          "ndcg_any@1": {
            "mean": 0.59375,
            "ci95": {
              "low": 0.46875,
              "high": 0.734375
            }
          },
          "recall_all@3": {
            "mean": 0.84375,
            "ci95": {
              "low": 0.75,
              "high": 0.9375
            }
          },
          "ndcg_any@3": {
            "mean": 0.7412535513950943,
            "ci95": {
              "low": 0.641727563554693,
              "high": 0.8276872985784108
            }
          },
          "recall_all@5": {
            "mean": 0.890625,
            "ci95": {
              "low": 0.812109375,
              "high": 0.953125
            }
          },
          "ndcg_any@5": {
            "mean": 0.7607567689479275,
            "ci95": {
              "low": 0.6780984447138306,
              "high": 0.8392243967533105
            }
          },
          "recall_all@10": {
            "mean": 0.921875,
            "ci95": {
              "low": 0.84375,
              "high": 0.96875
            }
          },
          "ndcg_any@10": {
            "mean": 0.7712516449462674,
            "ci95": {
              "low": 0.6944876706590122,
              "high": 0.8459978426118767
            }
          },
          "recall_all@20": {
            "mean": 0.953125,
            "ci95": {
              "low": 0.90625,
              "high": 1.0
            }
          },
          "ndcg_any@20": {
            "mean": 0.7794327931926637,
            "ci95": {
              "low": 0.7078062523170676,
              "high": 0.8524338241950584
            }
          },
          "recall_all@30": {
            "mean": 0.96875,
            "ci95": {
              "low": 0.921875,
              "high": 1.0
            }
          },
          "ndcg_any@30": {
            "mean": 0.782886929590437,
            "ci95": {
              "low": 0.7113467421247854,
              "high": 0.8524471466515203
            }
          },
          "recall_all@50": {
            "mean": 0.984375,
            "ci95": {
              "low": 0.953125,
              "high": 1.0
            }
          },
          "ndcg_any@50": {
            "mean": 0.7859844274524771,
            "ci95": {
              "low": 0.7174643004023145,
              "high": 0.8554672070670093
            }
          }
        }
      },
      "session_metrics": {
        "session_hit@1": 0.859375,
        "session_recall_all@1": 0.859375,
        "session_hit@3": 0.953125,
        "session_recall_all@3": 0.953125,
        "session_hit@5": 0.96875,
        "session_recall_all@5": 0.96875,
        "session_hit@10": 0.984375,
        "session_recall_all@10": 0.984375,
        "session_hit@20": 0.984375,
        "session_recall_all@20": 0.984375,
        "session_hit@30": 0.984375,
        "session_recall_all@30": 0.984375,
        "session_hit@50": 1.0,
        "session_recall_all@50": 1.0
      }
    },
    "2_gold": {
      "n": 8,
      "turn_metrics": {
        "n_total": 8,
        "n_scored": 8,
        "ignored_abstention_count": 0,
        "ignored_abstention_ids": [],
        "ignored_no_target_count": 0,
        "ignored_no_target_ids": [],
        "metrics": {
          "recall_all@1": {
            "mean": 0.0,
            "ci95": {
              "low": 0.0,
              "high": 0.0
            }
          },
          "ndcg_any@1": {
            "mean": 0.25,
            "ci95": {
              "low": 0.0,
              "high": 0.5
         
```
