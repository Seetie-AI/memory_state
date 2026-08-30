# Analysis: multi_gold_breakdown

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_multi_gold_breakdown_20260504T223007Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "layer22_center_instance": {
    "1_gold": {
      "official_metrics": {
        "n_total": 64,
        "n_scored": 64,
        "ignored_abstention_count": 0,
        "ignored_abstention_ids": [],
        "ignored_no_target_count": 0,
        "ignored_no_target_ids": [],
        "metrics": {
          "recall_all@1": {
            "mean": 0.5625,
            "ci95": {
              "low": 0.4375,
              "high": 0.6722656250000001
            }
          },
          "ndcg_any@1": {
            "mean": 0.5625,
            "ci95": {
              "low": 0.4375,
              "high": 0.6722656250000001
            }
          },
          "recall_all@3": {
            "mean": 0.78125,
            "ci95": {
              "low": 0.671484375,
              "high": 0.8597656250000001
            }
          },
          "ndcg_any@3": {
            "mean": 0.6882412191964322,
            "ci95": {
              "low": 0.579227563554693,
              "high": 0.7758538869977701
            }
          },
          "recall_all@5": {
            "mean": 0.84375,
            "ci95": {
              "low": 0.749609375,
              "high": 0.921875
            }
          },
          "ndcg_any@5": {
            "mean": 0.7144737579691622,
            "ci95": {
              "low": 0.6163992603367489,
              "high": 0.8005310945242872
            }
          },
          "recall_all@10": {
            "mean": 0.890625,
            "ci95": {
              "low": 0.8125,
              "high": 0.953125
            }
          },
          "ndcg_any@10": {
            "mean": 0.7292597268611918,
            "ci95": {
              "low": 0.6385980626264204,
              "high": 0.8097255991222911
            }
          },
          "recall_all@20": {
            "mean": 0.953125,
            "ci95": {
              "low": 0.905859375,
              "high": 0.984375
            }
          },
          "ndcg_any@20": {
            "mean": 0.7450030767423932,
            "ci95": {
              "low": 0.6632320396799742,
              "high": 0.8197449883944631
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
            "mean": 0.7481569687202385,
            "ci95": {
              "low": 0.6659439870116957,
              "high": 0.8219006433692594
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
            "mean": 0.7512819687202386,
            "ci95": {
              "low": 0.6694827619794205,
              "high": 0.8219006433692594
            }
          }
        }
      },
      "rank_metrics": {
        "mrr": 0.6823035832187997,
        "first_hit_position_histogram": {
          "1": 36,
          "2": 8,
          "3": 6,
          "4": 3,
          "5": 1,
          "6": 1,
          "9": 1,
          "10": 1,
          "12": 1,
          "14": 1,
          "15": 1,
          "19": 1,
          "30": 1,
          "31": 1,
          ">50": 1
        }
      }
    },
    "2_gold": {
      "official_metrics": {
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
            "mean": 0.375,
            "ci95": {
              "low": 0.0,
              "high": 0.75
            }
          },
          "recall_all@3": {
            "mean": 0.125,
            "ci95": {
              "low": 0.0,
              "high": 0.375
            }
         
```
