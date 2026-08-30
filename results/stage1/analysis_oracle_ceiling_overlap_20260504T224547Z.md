# Analysis: oracle_ceiling_overlap

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_oracle_ceiling_overlap_20260504T224547Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "warning": "Oracle ceiling is diagnostic only, not a real method.",
  "oracle": {
    "selected_config_counts": {
      "hidden_layer22_query_only_anti_pca_k10": 11,
      "hidden_final_cosine": 42,
      "hidden_layer22_center_instance": 29,
      "hidden_layer22_anti_pca_both_k10": 12,
      "hidden_layer21_query_only_anti_pca_k5": 6
    },
    "metrics": {
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
            "mean": 0.44680851063829785,
            "ci95": {
              "low": 0.35079787234042553,
              "high": 0.5425531914893617
            }
          },
          "ndcg_any@1": {
            "mean": 0.7021276595744681,
            "ci95": {
              "low": 0.6061170212765958,
              "high": 0.7872340425531915
            }
          },
          "recall_all@3": {
            "mean": 0.6276595744680851,
            "ci95": {
              "low": 0.5319148936170213,
              "high": 0.723404255319149
            }
          },
          "ndcg_any@3": {
            "mean": 0.7164220540656906,
            "ci95": {
              "low": 0.6456672385360515,
              "high": 0.7787897617086373
            }
          },
          "recall_all@5": {
            "mean": 0.723404255319149,
            "ci95": {
              "low": 0.6276595744680851,
              "high": 0.8085106382978723
            }
          },
          "ndcg_any@5": {
            "mean": 0.7392308895765405,
            "ci95": {
              "low": 0.6721423137177139,
              "high": 0.8026268013079821
            }
          },
          "recall_all@10": {
            "mean": 0.8085106382978723,
            "ci95": {
              "low": 0.7340425531914894,
              "high": 0.8829787234042553
            }
          },
          "ndcg_any@10": {
            "mean": 0.769350043505953,
            "ci95": {
              "low": 0.7075216056185865,
              "high": 0.8232007307407776
            }
          },
          "recall_all@20": {
            "mean": 0.8404255319148937,
            "ci95": {
              "low": 0.7659574468085106,
              "high": 0.9045212765957444
            }
          },
          "ndcg_any@20": {
            "mean": 0.783522204559339,
            "ci95": {
              "low": 0.723797433816141,
              "high": 0.83377432307401
            }
          },
          "recall_all@30": {
            "mean": 0.8936170212765957,
            "ci95": {
              "low": 0.8297872340425532,
              "high": 0.9468085106382979
            }
          },
          "ndcg_any@30": {
            "mean": 0.7920615694116946,
            "ci95": {
              "low": 0.73502295263383,
              "high": 0.8418879566043014
            }
          },
          "recall_all@50": {
            "mean": 0.9574468085106383,
            "ci95": {
              "low": 0.9148936170212766,
              "high": 0.9893617021276596
            }
          },
          "ndcg_any@50": {
            "mean": 0.8001741207482552,
            "ci95": {
              "low": 0.746415445941138,
              "high": 0.8465337741741299
            }
          }
        }
      },
      "session_metrics": {
        "session_hit@1": 0.8617021276595744,
        "session_recall_all@1": 0.5638297872340425,
        "session_hit@3": 0.9361702127659575,
        "session_recall_all@3": 0.7021276595744681,
        "session_hit@5": 0.9574468085106383,
        "session_recall_all@5": 0.8297872340425532,
        "session_hit@10": 0.9787234042553191,
        "session_recall_all@10": 0.88297872
```
