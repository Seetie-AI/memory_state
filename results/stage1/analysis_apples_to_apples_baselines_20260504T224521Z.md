# Analysis: apples_to_apples_baselines

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_apples_to_apples_baselines_20260504T224521Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "bm25": {
    "n_predictions": 94,
    "turn_metrics": {
      "n_total": 94,
      "n_scored": 94,
      "ignored_abstention_count": 0,
      "ignored_abstention_ids": [],
      "ignored_no_target_count": 0,
      "ignored_no_target_ids": [],
      "metrics": {
        "recall_all@1": {
          "mean": 0.3404255319148936,
          "ci95": {
            "low": 0.2553191489361702,
            "high": 0.43617021276595747
          }
        },
        "ndcg_any@1": {
          "mean": 0.43617021276595747,
          "ci95": {
            "low": 0.3404255319148936,
            "high": 0.5319148936170213
          }
        },
        "recall_all@3": {
          "mean": 0.5212765957446809,
          "ci95": {
            "low": 0.425531914893617,
            "high": 0.6170212765957447
          }
        },
        "ndcg_any@3": {
          "mean": 0.5154071483717928,
          "ci95": {
            "low": 0.43480045038082044,
            "high": 0.594321869806234
          }
        },
        "recall_all@5": {
          "mean": 0.5851063829787234,
          "ci95": {
            "low": 0.5,
            "high": 0.6808510638297872
          }
        },
        "ndcg_any@5": {
          "mean": 0.5467524987056783,
          "ci95": {
            "low": 0.4711226852225942,
            "high": 0.6243835389366676
          }
        },
        "recall_all@10": {
          "mean": 0.6170212765957447,
          "ci95": {
            "low": 0.5212765957446809,
            "high": 0.7127659574468085
          }
        },
        "ndcg_any@10": {
          "mean": 0.5673710359542363,
          "ci95": {
            "low": 0.49225283826616195,
            "high": 0.6409234425906165
          }
        },
        "recall_all@20": {
          "mean": 0.6808510638297872,
          "ci95": {
            "low": 0.5954787234042553,
            "high": 0.776595744680851
          }
        },
        "ndcg_any@20": {
          "mean": 0.5891990917806748,
          "ci95": {
            "low": 0.5186173430752917,
            "high": 0.6591393115916618
          }
        },
        "recall_all@30": {
          "mean": 0.7021276595744681,
          "ci95": {
            "low": 0.6170212765957447,
            "high": 0.7978723404255319
          }
        },
        "ndcg_any@30": {
          "mean": 0.5947454850090209,
          "ci95": {
            "low": 0.5259490683366199,
            "high": 0.6635794272043606
          }
        },
        "recall_all@50": {
          "mean": 0.7340425531914894,
          "ci95": {
            "low": 0.648936170212766,
            "high": 0.8191489361702128
          }
        },
        "ndcg_any@50": {
          "mean": 0.6041732423899077,
          "ci95": {
            "low": 0.5365492252865988,
            "high": 0.6717143851899525
          }
        }
      }
    },
    "session_metrics": {
      "session_hit@1": 0.5957446808510638,
      "session_recall_all@1": 0.43617021276595747,
      "session_hit@3": 0.776595744680851,
      "session_recall_all@3": 0.5957446808510638,
      "session_hit@5": 0.8617021276595744,
      "session_recall_all@5": 0.6595744680851063,
      "session_hit@10": 0.925531914893617,
      "session_recall_all@10": 0.7446808510638298,
      "session_hit@20": 0.9574468085106383,
      "session_recall_all@20": 0.8191489361702128,
      "session_hit@30": 0.9574468085106383,
      "session_recall_all@30": 0.8191489361702128,
      "session_hit@50": 0.9787234042553191,
      "session_recall_all@50": 0.9042553191489362
    },
    "rank_metrics": {
      "mrr": 0.5588446860657277,
      "first_hit_position_histogram": {
        "1": 41,
        "2": 13,
        "3": 6,
        "4": 2,
        "5": 5,
        "6": 2,
        "7": 1,
        "8": 4,
        "11": 1,
        "17": 2,
        "19": 3,
        "26": 1,
        "29": 1,
        "31": 2,
        "35": 1,
        "44": 1,
        ">50": 8
      }
    },
    "summary": {
      "turn_recall_all@5": 0.5851063829787234,
    
```
