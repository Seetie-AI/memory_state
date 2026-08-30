# Analysis: same_session_rerank_baseline

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_same_session_rerank_baseline_20260504T223822Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "baseline_hidden_state": {
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
        "mean": 0.40425531914893614,
        "ci95": {
          "low": 0.2978723404255319,
          "high": 0.5106382978723404
        }
      },
      "ndcg_any@1": {
        "mean": 0.5212765957446809,
        "ci95": {
          "low": 0.4148936170212766,
          "high": 0.6063829787234043
        }
      },
      "recall_all@3": {
        "mean": 0.5957446808510638,
        "ci95": {
          "low": 0.4997340425531915,
          "high": 0.6914893617021277
        }
      },
      "ndcg_any@3": {
        "mean": 0.6298466800667516,
        "ci95": {
          "low": 0.538749307321534,
          "high": 0.6907447154911885
        }
      },
      "recall_all@5": {
        "mean": 0.6808510638297872,
        "ci95": {
          "low": 0.574468085106383,
          "high": 0.7659574468085106
        }
      },
      "ndcg_any@5": {
        "mean": 0.6583166643251515,
        "ci95": {
          "low": 0.5695646926697949,
          "high": 0.7165764509305453
        }
      },
      "recall_all@10": {
        "mean": 0.7340425531914894,
        "ci95": {
          "low": 0.6486702127659575,
          "high": 0.8191489361702128
        }
      },
      "ndcg_any@10": {
        "mean": 0.6854976117187989,
        "ci95": {
          "low": 0.6040770423034901,
          "high": 0.7400793667637384
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
        "mean": 0.7240554552967258,
        "ci95": {
          "low": 0.6556856574928088,
          "high": 0.7738944857026706
        }
      },
      "recall_all@50": {
        "mean": 0.9468085106382979,
        "ci95": {
          "low": 0.9042553191489362,
          "high": 0.9789893617021277
        }
      },
      "ndcg_any@50": {
        "mean": 0.7298561820606597,
        "ci95": {
          "low": 0.6619642565381061,
          "high": 0.7774765031264711
        }
      }
    }
  },
  "top50_bm25_rerank": {
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
          "low": 0.2553191489361702,
          "high": 0.43643617021276604
        }
      },
      "ndcg_any@1": {
        "mean": 0.44680851063829785,
        "ci95": {
          "low": 0.35106382978723405,
          "high": 0.5425531914893617
        }
      },
      "recall_all@3": {
        "mean": 0.5319148936170213,
        "ci95": {
          "low": 0.43617021276595747,
          "high": 0.6276595744680851
        }
      },
      "ndcg_any@3": {
        "mean": 0.5330471654124656,
        "ci95": {
          "low": 0.44933666587563387,
          "high": 0.6186000740999319
        }
      },
      "recall_all@5": {
        "mean": 0.6170212765957447,
        "ci95": {
          "low": 0.5212765957446809,
          "high": 0.7023936170212767
        }
      },
      "ndcg_any@5": {
        "mean": 0.571935929875443,
        "ci95": {
          "low": 0.4973319311485655,
          "high": 0.6488215793838759
        }
      },
      "recall_all@10": {
        "mean": 0.6702127659574468,
        "ci95": {
          "low": 0.5638297872340425,
          "high": 0.7555851063829788
        }
      },
      "ndcg_any@10": {
        "me
```
