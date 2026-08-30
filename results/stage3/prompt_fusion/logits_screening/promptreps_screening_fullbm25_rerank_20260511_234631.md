# Stage 3 PromptReps-Style Logits Screening

Offline approximation: saved top-k logits are intersected with original text tokens, then weighted with `log1p(relu(logit))`.

## Sparse Stats

| variant | avg kept logits | median kept logits | zero fraction | avg text tokens |
|---|---:|---:|---:|---:|
| `2-4-1_user_word` | 2.1 | 2.0 | 0.115 | 38.6 |
| `1-3` | 1.9 | 1.0 | 0.096 | 38.6 |
| `2-5` | 0.9 | 1.0 | 0.429 | 38.6 |
| `2-3-2_mem` | 2.4 | 2.0 | 0.131 | 38.6 |

## Shortlist Oracle

| logit source | screen mode | avg candidates | oracle R |
|---|---|---:|---:|
| `2-4-1_user_word` | `hidden_top20` | 20.0 | 0.936 |
| `1-3` | `hidden_top20` | 20.0 | 0.936 |
| `2-5` | `hidden_top20` | 20.0 | 0.936 |
| `2-3-2_mem` | `hidden_top20` | 20.0 | 0.936 |
| `fused_k3` | `hidden_top20` | 20.0 | 0.936 |
| `2-3-2_mem` | `logits_bm25_union20` | 37.1 | 0.745 |
| `2-4-1_user_word` | `logits_bm25_union20` | 37.7 | 0.723 |
| `fused_k3` | `logits_bm25_union20` | 35.9 | 0.713 |
| `2-5` | `logits_bm25_union20` | 38.2 | 0.713 |
| `2-4-1_user_word` | `logits_bm25_fused_top20` | 20.0 | 0.702 |
| `1-3` | `logits_bm25_union20` | 35.2 | 0.691 |
| `2-4-1_user_word` | `bm25_top20` | 20.0 | 0.681 |
| `1-3` | `bm25_top20` | 20.0 | 0.681 |
| `2-5` | `bm25_top20` | 20.0 | 0.681 |
| `2-3-2_mem` | `bm25_top20` | 20.0 | 0.681 |
| `fused_k3` | `bm25_top20` | 20.0 | 0.681 |
| `1-3` | `logits_bm25_fused_top20` | 20.0 | 0.670 |
| `fused_k3` | `logits_bm25_fused_top20` | 20.0 | 0.670 |
| `2-5` | `logits_bm25_fused_top20` | 20.0 | 0.660 |
| `2-3-2_mem` | `logits_bm25_fused_top20` | 20.0 | 0.660 |
| `2-3-2_mem` | `logits_top20` | 20.0 | 0.287 |
| `1-3` | `logits_top20` | 20.0 | 0.160 |
| `fused_k3` | `logits_top20` | 20.0 | 0.160 |
| `2-4-1_user_word` | `logits_top20` | 20.0 | 0.138 |
| `2-5` | `logits_top20` | 20.0 | 0.117 |

## Rerank Results

| rank | logit source | screen mode | score mode | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `2-3-2_mem` | `hidden_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.723 | 0.787 | 0.777 | 0.808 | 0.832 | 1.000 | 94 |
| 2 | `2-4-1_user_word` | `hidden_top20` | `hidden_bm25_75_25` | 0.723 | 0.803 | 0.766 | 0.817 | 0.847 | 1.000 | 94 |
| 3 | `1-3` | `hidden_top20` | `hidden_bm25_75_25` | 0.723 | 0.803 | 0.766 | 0.817 | 0.847 | 1.000 | 94 |
| 4 | `2-5` | `hidden_top20` | `hidden_bm25_75_25` | 0.723 | 0.803 | 0.766 | 0.817 | 0.847 | 1.000 | 94 |
| 5 | `2-3-2_mem` | `hidden_top20` | `hidden_bm25_75_25` | 0.723 | 0.803 | 0.766 | 0.817 | 0.847 | 1.000 | 94 |
| 6 | `fused_k3` | `hidden_top20` | `hidden_bm25_75_25` | 0.723 | 0.803 | 0.766 | 0.817 | 0.847 | 1.000 | 94 |
| 7 | `2-5` | `hidden_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.713 | 0.796 | 0.766 | 0.807 | 0.843 | 1.000 | 94 |
| 8 | `2-4-1_user_word` | `hidden_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.723 | 0.774 | 0.766 | 0.791 | 0.822 | 1.000 | 94 |
| 9 | `fused_k3` | `hidden_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.691 | 0.756 | 0.766 | 0.783 | 0.815 | 0.989 | 94 |
| 10 | `1-3` | `hidden_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.723 | 0.759 | 0.766 | 0.775 | 0.787 | 0.989 | 94 |
| 11 | `2-3-2_mem` | `logits_bm25_union20` | `mix_50_hidden_25_bm25_25_logits` | 0.660 | 0.714 | 0.702 | 0.733 | 0.751 | 0.979 | 94 |
| 12 | `2-3-2_mem` | `logits_bm25_union20` | `hidden_bm25_75_25` | 0.660 | 0.738 | 0.691 | 0.748 | 0.770 | 0.979 | 94 |
| 13 | `2-4-1_user_word` | `logits_bm25_union20` | `mix_50_hidden_25_bm25_25_logits` | 0.638 | 0.710 | 0.691 | 0.727 | 0.762 | 0.989 | 94 |
| 14 | `2-4-1_user_word` | `logits_bm25_union20` | `hidden_bm25_75_25` | 0.649 | 0.739 | 0.681 | 0.745 | 0.775 | 0.989 | 94 |
| 15 | `2-4-1_user_word` | `logits_bm25_fused_top20` | `hidden_bm25_75_25` | 0.638 | 0.703 | 0.681 | 0.709 | 0.751 | 0.947 | 94 |
| 16 | `2-4-1_user_word` | `logits_bm25_fused_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.617 | 0.679 | 0.681 | 0.692 | 0.728 | 0.947 | 94 |
| 17 | `fused_k3` | `logits_bm25_union20` | `hidden_bm25_75_25` | 0.638 | 0.736 | 0.670 | 0.742 | 0.775 | 0.979 | 94 |
| 18 | `2-5` | `logits_bm25_union20` | `hidden_bm25_75_25` | 0.638 | 0.727 | 0.670 | 0.734 | 0.763 | 0.947 | 94 |
| 19 | `2-5` | `logits_bm25_union20` | `mix_50_hidden_25_bm25_25_logits` | 0.628 | 0.725 | 0.670 | 0.734 | 0.771 | 0.947 | 94 |
| 20 | `fused_k3` | `logits_bm25_union20` | `mix_50_hidden_25_bm25_25_logits` | 0.606 | 0.698 | 0.670 | 0.716 | 0.757 | 0.979 | 94 |
| 21 | `1-3` | `logits_bm25_union20` | `hidden_bm25_75_25` | 0.628 | 0.716 | 0.660 | 0.725 | 0.752 | 0.968 | 94 |
| 22 | `2-4-1_user_word` | `bm25_top20` | `hidden_bm25_75_25` | 0.617 | 0.704 | 0.660 | 0.715 | 0.748 | 0.947 | 94 |
| 23 | `1-3` | `bm25_top20` | `hidden_bm25_75_25` | 0.617 | 0.704 | 0.660 | 0.715 | 0.748 | 0.947 | 94 |
| 24 | `2-5` | `bm25_top20` | `hidden_bm25_75_25` | 0.617 | 0.704 | 0.660 | 0.715 | 0.748 | 0.947 | 94 |
| 25 | `2-3-2_mem` | `bm25_top20` | `hidden_bm25_75_25` | 0.617 | 0.704 | 0.660 | 0.715 | 0.748 | 0.947 | 94 |
| 26 | `fused_k3` | `bm25_top20` | `hidden_bm25_75_25` | 0.617 | 0.704 | 0.660 | 0.715 | 0.748 | 0.947 | 94 |
| 27 | `2-3-2_mem` | `logits_bm25_fused_top20` | `hidden_bm25_75_25` | 0.628 | 0.696 | 0.660 | 0.705 | 0.746 | 0.957 | 94 |
| 28 | `1-3` | `logits_bm25_union20` | `mix_50_hidden_25_bm25_25_logits` | 0.606 | 0.677 | 0.660 | 0.694 | 0.724 | 0.968 | 94 |
| 29 | `2-4-1_user_word` | `bm25_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.606 | 0.672 | 0.660 | 0.693 | 0.729 | 0.947 | 94 |
| 30 | `2-3-2_mem` | `logits_bm25_fused_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.628 | 0.661 | 0.660 | 0.673 | 0.705 | 0.957 | 94 |
| 31 | `2-5` | `bm25_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.596 | 0.683 | 0.649 | 0.702 | 0.741 | 0.947 | 94 |
| 32 | `fused_k3` | `logits_bm25_fused_top20` | `hidden_bm25_75_25` | 0.617 | 0.693 | 0.649 | 0.699 | 0.733 | 0.947 | 94 |
| 33 | `1-3` | `logits_bm25_fused_top20` | `hidden_bm25_75_25` | 0.606 | 0.690 | 0.649 | 0.697 | 0.731 | 0.947 | 94 |
| 34 | `2-3-2_mem` | `bm25_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.638 | 0.678 | 0.649 | 0.685 | 0.714 | 0.947 | 94 |
| 35 | `fused_k3` | `bm25_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.585 | 0.662 | 0.649 | 0.684 | 0.718 | 0.947 | 94 |
| 36 | `1-3` | `bm25_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.596 | 0.661 | 0.649 | 0.680 | 0.708 | 0.947 | 94 |
| 37 | `2-5` | `logits_bm25_fused_top20` | `hidden_bm25_75_25` | 0.606 | 0.683 | 0.638 | 0.693 | 0.721 | 0.936 | 94 |
| 38 | `2-5` | `logits_bm25_fused_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.564 | 0.658 | 0.638 | 0.684 | 0.714 | 0.926 | 94 |
| 39 | `fused_k3` | `logits_bm25_fused_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.574 | 0.657 | 0.628 | 0.668 | 0.710 | 0.947 | 94 |
| 40 | `1-3` | `logits_bm25_fused_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.585 | 0.651 | 0.628 | 0.662 | 0.692 | 0.947 | 94 |
| 41 | `2-3-2_mem` | `hidden_top20` | `logits_only` | 0.255 | 0.264 | 0.319 | 0.302 | 0.334 | 0.872 | 94 |
| 42 | `2-3-2_mem` | `logits_top20` | `hidden_bm25_75_25` | 0.277 | 0.322 | 0.277 | 0.320 | 0.362 | 0.596 | 94 |
| 43 | `2-3-2_mem` | `logits_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.277 | 0.320 | 0.277 | 0.316 | 0.362 | 0.585 | 94 |
| 44 | `2-3-2_mem` | `bm25_top20` | `logits_only` | 0.213 | 0.206 | 0.277 | 0.234 | 0.275 | 0.638 | 94 |
| 45 | `fused_k3` | `hidden_top20` | `logits_only` | 0.181 | 0.193 | 0.266 | 0.233 | 0.285 | 0.766 | 94 |
| 46 | `1-3` | `hidden_top20` | `logits_only` | 0.170 | 0.151 | 0.245 | 0.201 | 0.226 | 0.840 | 94 |
| 47 | `2-3-2_mem` | `logits_bm25_fused_top20` | `logits_only` | 0.202 | 0.167 | 0.245 | 0.190 | 0.222 | 0.532 | 94 |
| 48 | `2-4-1_user_word` | `hidden_top20` | `logits_only` | 0.191 | 0.192 | 0.234 | 0.222 | 0.269 | 0.777 | 94 |
| 49 | `2-4-1_user_word` | `bm25_top20` | `logits_only` | 0.138 | 0.132 | 0.223 | 0.180 | 0.210 | 0.649 | 94 |
| 50 | `2-3-2_mem` | `logits_top20` | `logits_only` | 0.170 | 0.146 | 0.213 | 0.161 | 0.170 | 0.436 | 94 |
| 51 | `2-3-2_mem` | `logits_bm25_union20` | `logits_only` | 0.170 | 0.146 | 0.202 | 0.157 | 0.188 | 0.426 | 94 |
| 52 | `fused_k3` | `bm25_top20` | `logits_only` | 0.138 | 0.113 | 0.202 | 0.150 | 0.186 | 0.436 | 94 |
| 53 | `2-5` | `hidden_top20` | `logits_only` | 0.138 | 0.153 | 0.191 | 0.194 | 0.244 | 0.840 | 94 |
| 54 | `2-5` | `bm25_top20` | `logits_only` | 0.160 | 0.144 | 0.191 | 0.173 | 0.215 | 0.585 | 94 |
| 55 | `fused_k3` | `logits_top20` | `hidden_bm25_75_25` | 0.160 | 0.187 | 0.160 | 0.183 | 0.207 | 0.500 | 94 |
| 56 | `1-3` | `logits_top20` | `hidden_bm25_75_25` | 0.160 | 0.178 | 0.160 | 0.179 | 0.196 | 0.383 | 94 |
| 57 | `1-3` | `logits_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.160 | 0.175 | 0.160 | 0.174 | 0.195 | 0.372 | 94 |
| 58 | `fused_k3` | `logits_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.160 | 0.179 | 0.160 | 0.174 | 0.197 | 0.489 | 94 |
| 59 | `2-4-1_user_word` | `logits_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.138 | 0.166 | 0.138 | 0.163 | 0.189 | 0.553 | 94 |
| 60 | `2-4-1_user_word` | `logits_top20` | `hidden_bm25_75_25` | 0.138 | 0.167 | 0.138 | 0.162 | 0.186 | 0.553 | 94 |
| 61 | `1-3` | `bm25_top20` | `logits_only` | 0.085 | 0.081 | 0.138 | 0.106 | 0.149 | 0.372 | 94 |
| 62 | `2-5` | `logits_bm25_fused_top20` | `logits_only` | 0.096 | 0.079 | 0.138 | 0.106 | 0.145 | 0.436 | 94 |
| 63 | `1-3` | `logits_bm25_fused_top20` | `logits_only` | 0.064 | 0.053 | 0.138 | 0.090 | 0.125 | 0.298 | 94 |
| 64 | `2-5` | `logits_top20` | `hidden_bm25_75_25` | 0.117 | 0.131 | 0.117 | 0.134 | 0.149 | 0.383 | 94 |
| 65 | `2-5` | `logits_top20` | `mix_50_hidden_25_bm25_25_logits` | 0.117 | 0.133 | 0.117 | 0.133 | 0.153 | 0.394 | 94 |
| 66 | `2-4-1_user_word` | `logits_bm25_fused_top20` | `logits_only` | 0.074 | 0.071 | 0.106 | 0.086 | 0.134 | 0.415 | 94 |
| 67 | `fused_k3` | `logits_bm25_fused_top20` | `logits_only` | 0.085 | 0.073 | 0.096 | 0.084 | 0.128 | 0.287 | 94 |
| 68 | `fused_k3` | `logits_bm25_union20` | `logits_only` | 0.085 | 0.071 | 0.096 | 0.078 | 0.111 | 0.245 | 94 |
| 69 | `fused_k3` | `logits_top20` | `logits_only` | 0.085 | 0.071 | 0.096 | 0.076 | 0.083 | 0.234 | 94 |
| 70 | `1-3` | `logits_bm25_union20` | `logits_only` | 0.043 | 0.030 | 0.085 | 0.050 | 0.080 | 0.191 | 94 |
| 71 | `1-3` | `logits_top20` | `logits_only` | 0.053 | 0.035 | 0.085 | 0.047 | 0.049 | 0.138 | 94 |
| 72 | `2-4-1_user_word` | `logits_top20` | `logits_only` | 0.043 | 0.045 | 0.064 | 0.052 | 0.067 | 0.255 | 94 |
| 73 | `2-4-1_user_word` | `logits_bm25_union20` | `logits_only` | 0.043 | 0.045 | 0.053 | 0.048 | 0.091 | 0.234 | 94 |
| 74 | `2-5` | `logits_bm25_union20` | `logits_only` | 0.043 | 0.037 | 0.043 | 0.038 | 0.080 | 0.202 | 94 |
| 75 | `2-5` | `logits_top20` | `logits_only` | 0.032 | 0.029 | 0.032 | 0.028 | 0.045 | 0.160 | 94 |

## Inputs

- config: `concat_k3_norm_weighted_userword_tag_assoc`
- tokenizer: `/Users/gordonxiong/Desktop/Repos/memory_state/models/Qwen3.5-9B-MLX-4bit`
- logit variants: `['2-4-1_user_word', '1-3', '2-5', '2-3-2_mem']`
- fused logit variants: `['2-4-1_user_word', '1-3', '2-5']`
- screen top-k: 20
- score modes: `['mix_50_hidden_25_bm25_25_logits', 'logits_only', 'hidden_bm25_75_25']`
- elapsed_seconds: 173.6
