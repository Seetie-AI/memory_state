# Analysis: rank_and_error_diagnostics

Full JSON: `/Users/gordonxiong/Desktop/Repos/memory_state/results/analysis_rank_and_error_diagnostics_20260504T223020Z.json`

This summary is intentionally brief; inspect the JSON for full metrics.

```json
{
  "layer22_center_instance": {
    "gold_margin_best_gold_minus_best_non_gold": {
      "mean": -0.010285432826965413,
      "std": 0.12859655337349157,
      "min": -0.4014938697218895,
      "max": 0.3496443033218384
    },
    "same_session_top1_false_positive_rate": 0.4666666666666667,
    "same_day_top1_false_positive_rate": 0.4666666666666667,
    "token_count_vs_rank_spearman": 0.14939294019154067,
    "top_false_positive_examples": [
      {
        "question_id": "e47becba",
        "top_candidate_id": "sharegpt_8dJs7Ai_0_5",
        "top_candidate_text": "What math problem do they solve?",
        "top_score": 0.4153182804584503,
        "gold_candidate_ids": [
          "answer_280352e9_5"
        ],
        "gold_texts": [
          "I graduated with a degree in Business Administration, which has definitely helped me in my new role."
        ],
        "best_gold_score": 0.12583956122398376,
        "same_session_as_any_gold": false,
        "same_day_as_any_gold": false
      },
      {
        "question_id": "58ef2f1c",
        "top_candidate_id": "ultrachat_246324_11",
        "top_candidate_text": "I think I'm going to start by volunteering with the Dayton Foodbank. Do you know if they have any up",
        "top_score": 0.603365421295166,
        "gold_candidate_ids": [
          "answer_59547700_9"
        ],
        "gold_texts": [
          "I'm really looking forward to the silent auction and raffles at \"Strut Your Mutt\". I've had a great "
        ],
        "best_gold_score": 0.25758877396583557,
        "same_session_as_any_gold": false,
        "same_day_as_any_gold": false
      },
      {
        "question_id": "f8c5f88b",
        "top_candidate_id": "noans_c3567066_7",
        "top_candidate_text": "I'm planning to buy new tennis balls this weekend. Do you know any good brands or types of tennis ba",
        "top_score": 0.5642112493515015,
        "gold_candidate_ids": [
          "answer_c3567066_5"
        ],
        "gold_texts": [
          "I'll definitely do those exercises before playing tennis. By the way, I'm really happy with my new t"
        ],
        "best_gold_score": 0.49333125352859497,
        "same_session_as_any_gold": true,
        "same_day_as_any_gold": true
      },
      {
        "question_id": "5d3d2817",
        "top_candidate_id": "sharegpt_0OYTYWn_15_4",
        "top_candidate_text": "Use the grid model please",
        "top_score": 0.3360444903373718,
        "gold_candidate_ids": [
          "answer_235eb6fb_5"
        ],
        "gold_texts": [
          "I've used Trello in my previous role as a marketing specialist at a small startup and I'm familiar w"
        ],
        "best_gold_score": -0.06544937938451767,
        "same_session_as_any_gold": false,
        "same_day_as_any_gold": false
      },
      {
        "question_id": "c960da58",
        "top_candidate_id": "noans_e05e4612_7",
        "top_candidate_text": "That's a great idea about using emojis or keywords in playlist names. I think I'll start doing that ",
        "top_score": 0.5232947468757629,
        "gold_candidate_ids": [
          "answer_e05e4612_3"
        ],
        "gold_texts": [
          "I've been listening to a mix of Lo-Fi hip hop beats and Tameca Jones' album on repeat lately, and I "
        ],
        "best_gold_score": 0.38094353675842285,
        "same_session_as_any_gold": true,
        "same_day_as_any_gold": true
      },
      {
        "question_id": "3b6f954b",
        "top_candidate_id": "ultrachat_294369_5",
        "top_candidate_text": "Can students from other faculties, who are not involved in varsity sports, still use the athletic fa",
        "top_score": 0.271218866109848,
        "gold_candidate_ids": [
          "answer_94030872_9"
        ],
        "gold_texts": [
          "That sounds amazing! I've been to the Great Ocean Road before, and it's definitely a must-see in Aus"
        ],
        "best_gold_score": 0.22659200429916382,
        "same_session_as
```
