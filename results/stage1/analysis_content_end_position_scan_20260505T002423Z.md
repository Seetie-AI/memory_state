# Analysis: content_end_position_scan

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_content_end_position_scan_20260505T002423Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "disclaimer": "Tier B contains only 20 LongMemEval-S/round instances. Treat these results as direction-finding diagnostics, not final performance claims.",
  "memory_plan": "Lean per-prompt slice loading: each safetensors file is opened, one small set of (layer, position, 2048) vectors is materialized as fp32, then the file object and MLX cache are released. Target peak memory for TB extra analyses is below the 8GB budget.",
  "layer": 22,
  "suffix_token_count": 15,
  "valid_prompt_count": 5043,
  "baseline": {
    "config": "layer22_last_anti_pca_global_k10",
    "valid_prompt_count": 5043,
    "skipped_prompt_count": 0,
    "metrics": {
      "n_total": 20,
      "n_scored": 20,
      "ignored_abstention_count": 0,
      "ignored_abstention_ids": [],
      "ignored_no_target_count": 0,
      "ignored_no_target_ids": [],
      "metrics": {
        "recall_all@1": {
          "mean": 0.55,
          "ci95": {
            "low": 0.29875,
            "high": 0.7512500000000003
          }
        },
        "ndcg_any@1": {
          "mean": 0.55,
          "ci95": {
            "low": 0.29875,
            "high": 0.7512500000000003
          }
        },
        "recall_all@3": {
          "mean": 0.8,
          "ci95": {
            "low": 0.65,
            "high": 0.95
          }
        },
        "ndcg_any@3": {
          "mean": 0.7077324383928645,
          "ci95": {
            "low": 0.5391449126473303,
            "high": 0.8709594271741172
          }
        },
        "recall_all@5": {
          "mean": 0.85,
          "ci95": {
            "low": 0.7,
            "high": 0.95
          }
        },
        "ndcg_any@5": {
          "mean": 0.7270750787545915,
          "ci95": {
            "low": 0.5704980893660815,
            "high": 0.8709594271741172
          }
        },
        "recall_all@10": {
          "mean": 0.85,
          "ci95": {
            "low": 0.7,
            "high": 0.95
          }
        },
        "ndcg_any@10": {
          "mean": 0.7270750787545915,
          "ci95": {
            "low": 0.5704980893660815,
            "high": 0.8709594271741172
          }
        },
        "recall_all@30": {
          "mean": 0.95,
          "ci95": {
            "low": 0.85,
            "high": 1.0
          }
        },
        "ndcg_any@30": {
          "mean": 0.7509585911894392,
          "ci95": {
            "low": 0.6078410626822189,
            "high": 0.8869913121759221
          }
        },
        "recall_all@50": {
          "mean": 0.95,
          "ci95": {
            "low": 0.85,
            "high": 1.0
          }
        },
        "ndcg_any@50": {
          "mean": 0.7509585911894392,
          "ci95": {
            "low": 0.6078410626822189,
            "high": 0.8869913121759221
          }
        }
      }
    }
  },
  "positions": {
    "content_end": {
      "skipped_prompt_count": 0,
      "metrics": {
        "n_total": 20,
        "n_scored": 20,
        "ignored_abstention_count": 0,
        "ignored_abstention_ids": [],
        "ignored_no_target_count": 0,
        "ignored_no_target_ids": [],
        "metrics": {
          "recall_all@1": {
            "mean": 0.2,
            "ci95": {
              "low": 0.0,
              "high": 0.35
            }
          },
          "ndcg_any@1": {
            "mean": 0.2,
            "ci95": {
              "low": 0.0,
              "high": 0.35
            }
          },
          "recall_all@3": {
            "mean": 0.45,
            "ci95": {
              "low": 0.25,
              "high": 0.7
            }
          },
          "ndcg_any@3": {
            "mean": 0.35118595071429154,
            "ci95": {
              "low": 0.16295896193303872,
              "high": 0.5211230893660816
            }
          },
          "recall_all@5": {
            "mean": 0.45,
            "ci95": {
              "low": 0.25,
              "high": 0.7
            }
          },
          "ndcg_any@5": {
            "mean": 
```
