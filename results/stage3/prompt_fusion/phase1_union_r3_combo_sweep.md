# Temporary Phase 1 union-hit combo sweep @ 3

A combination scores a question once if any prompt retrieves all gold evidence in the top-k.

Elapsed: 4m17s

## Single Cells

| rank | cell | family | hit@3 | count | n |
|---:|---|---|---:|---:|---:|
| 1 | `2-3-1|layer30|last|anti_pca_both_k15` | mem-key | 0.702 | 66 | 94 |
| 2 | `1-3|layer31|last|anti_pca_both_k15` | tag | 0.702 | 66 | 94 |
| 3 | `2-5|layer29|last|query_only_anti_pca_k2` | association | 0.691 | 65 | 94 |
| 4 | `2-4-1_user_word|layer30|last|anti_pca_both_k15` | persona | 0.681 | 64 | 94 |
| 5 | `1-2|layer29|last|anti_pca_both_k15` | summary | 0.681 | 64 | 94 |
| 6 | `2-3-2_query|layer29|last|anti_pca_both_k15` | query-key | 0.670 | 63 | 94 |
| 7 | `2-3-2_mem|layer31|last|anti_pca_both_k15` | mem-key | 0.670 | 63 | 94 |
| 8 | `2-6|layer30|last|anti_pca_both_k15` | impression | 0.660 | 62 | 94 |
| 9 | `2-1|layer30|last|anti_pca_both_k15` | topic | 0.660 | 62 | 94 |
| 10 | `2-4-1|layer30|last|query_only_anti_pca_k2` | persona | 0.638 | 60 | 94 |
| 11 | `1-1_EN|layer31|last|anti_pca_both_k15` | content-summary | 0.638 | 60 | 94 |
| 12 | `1-1_CN|layer29|last|centered_cosine` | content-summary | 0.638 | 60 | 94 |
| 13 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | content-summary | 0.628 | 59 | 94 |
| 14 | `P0|layer30|last|anti_pca_both_k15` | anchor | 0.617 | 58 | 94 |
| 15 | `2-7|layer31|last|anti_pca_both_k15` | style | 0.606 | 57 | 94 |
| 16 | `2-4-2|layer29|last|anti_pca_both_k15` | need | 0.585 | 55 | 94 |
| 17 | `2-8|layer31|last|anti_pca_both_k15` | strategy | 0.468 | 44 | 94 |

## Size 2 Combos Sorted By Union Hit@3

| rank | combo | union@3 | gain | best_single | all_hit | neither | avg_pair_jaccard@3 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.564 | 0.255 | 0.480 |
| 2 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.628 | 0.255 | 0.489 |
| 3 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.649 | 0.255 | 0.515 |
| 4 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.457 |
| 5 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.617 | 0.266 | 0.519 |
| 6 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.638 | 0.266 | 0.564 |
| 7 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.502 |
| 8 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.539 |
| 9 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.649 | 0.266 | 0.574 |
| 10 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.660 | 0.266 | 0.590 |
| 11 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.670 | 0.266 | 0.647 |
| 12 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.650 |
| 13 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.574 | 0.277 | 0.433 |
| 14 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.596 | 0.277 | 0.518 |
| 15 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.574 | 0.277 | 0.535 |
| 16 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.606 | 0.277 | 0.544 |
| 17 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.562 |
| 18 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.617 | 0.277 | 0.500 |
| 19 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.628 | 0.277 | 0.601 |
| 20 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.574 | 0.277 | 0.449 |
| 21 | `2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.606 | 0.277 | 0.454 |
| 22 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.506 |
| 23 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.638 | 0.277 | 0.514 |
| 24 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.535 |
| 25 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.606 | 0.277 | 0.538 |
| 26 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.628 | 0.277 | 0.556 |
| 27 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.638 | 0.277 | 0.566 |
| 28 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.483 |
| 29 | `1-3|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.516 |
| 30 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.568 |
| 31 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.572 |
| 32 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.586 |
| 33 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.649 | 0.277 | 0.620 |
| 34 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.649 | 0.277 | 0.666 |
| 35 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.638 | 0.277 | 0.666 |
| 36 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.660 | 0.277 | 0.691 |
| 37 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.649 | 0.277 | 0.723 |
| 38 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.564 | 0.287 | 0.464 |
| 39 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.043 | 0.670 | 0.596 | 0.287 | 0.473 |
| 40 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.596 | 0.287 | 0.491 |
| 41 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.617 | 0.287 | 0.543 |
| 42 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.617 | 0.287 | 0.639 |
| 43 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.473 |
| 44 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.474 |
| 45 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.503 |
| 46 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.519 |
| 47 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.638 | 0.287 | 0.571 |
| 48 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.649 | 0.287 | 0.603 |
| 49 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.628 | 0.287 | 0.613 |
| 50 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.628 | 0.287 | 0.627 |
| 51 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.638 | 0.287 | 0.678 |
| 52 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.628 | 0.287 | 0.694 |
| 53 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.021 | 0.691 | 0.606 | 0.287 | 0.511 |
| 54 | `1-3|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.457 | 0.287 | 0.312 |
| 55 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.596 | 0.287 | 0.504 |
| 56 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.628 | 0.287 | 0.543 |
| 57 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.011 | 0.702 | 0.617 | 0.287 | 0.561 |
| 58 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.713 | 0.011 | 0.702 | 0.628 | 0.287 | 0.565 |
| 59 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.574 | 0.287 | 0.587 |
| 60 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.649 | 0.287 | 0.617 |
| 61 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.574 | 0.287 | 0.631 |
| 62 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.660 | 0.287 | 0.652 |
| 63 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.670 | 0.287 | 0.718 |
| 64 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.543 | 0.298 | 0.450 |
| 65 | `1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.543 | 0.298 | 0.512 |
| 66 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.596 | 0.298 | 0.497 |
| 67 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.585 | 0.298 | 0.507 |
| 68 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.702 | 0.043 | 0.660 | 0.596 | 0.298 | 0.524 |
| 69 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.596 | 0.298 | 0.560 |
| 70 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.043 | 0.660 | 0.585 | 0.298 | 0.583 |
| 71 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.585 | 0.298 | 0.614 |
| 72 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.638 | 0.298 | 0.659 |
| 73 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.447 | 0.298 | 0.300 |
| 74 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.702 | 0.021 | 0.681 | 0.617 | 0.298 | 0.518 |
| 75 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.021 | 0.681 | 0.606 | 0.298 | 0.519 |
| 76 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.564 | 0.298 | 0.553 |
| 77 | `1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.555 |
| 78 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.649 | 0.298 | 0.623 |
| 79 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.468 | 0.298 | 0.329 |
| 80 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.681 | 0.298 | 0.645 |
| 81 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.617 | 0.298 | 0.661 |
| 82 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.617 | 0.298 | 0.674 |
| 83 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.064 | 0.628 | 0.543 | 0.309 | 0.517 |
| 84 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.532 | 0.309 | 0.461 |
| 85 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.691 | 0.053 | 0.638 | 0.564 | 0.309 | 0.463 |
| 86 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.532 | 0.309 | 0.499 |
| 87 | `1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.585 | 0.309 | 0.500 |
| 88 | `2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.606 | 0.309 | 0.471 |
| 89 | `2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.574 | 0.309 | 0.500 |
| 90 | `2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.553 | 0.309 | 0.567 |
| 91 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.606 | 0.309 | 0.570 |
| 92 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.553 | 0.309 | 0.606 |
| 93 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.585 | 0.309 | 0.611 |
| 94 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.585 | 0.309 | 0.481 |
| 95 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.585 | 0.309 | 0.523 |
| 96 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.691 | 0.021 | 0.670 | 0.617 | 0.309 | 0.524 |
| 97 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.691 | 0.021 | 0.670 | 0.606 | 0.309 | 0.543 |
| 98 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.617 | 0.309 | 0.550 |
| 99 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.564 | 0.309 | 0.590 |
| 100 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.638 | 0.309 | 0.662 |
| 101 | `1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.628 | 0.309 | 0.573 |
| 102 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.606 | 0.309 | 0.591 |
| 103 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.617 | 0.309 | 0.616 |
| 104 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.628 | 0.309 | 0.649 |
| 105 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.606 | 0.309 | 0.712 |
| 106 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.000 | 0.691 | 0.468 | 0.309 | 0.301 |
| 107 | `2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.681 | 0.074 | 0.606 | 0.511 | 0.319 | 0.497 |
| 108 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.053 | 0.628 | 0.532 | 0.319 | 0.556 |
| 109 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.426 | 0.319 | 0.314 |
| 110 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.681 | 0.043 | 0.638 | 0.596 | 0.319 | 0.527 |
| 111 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.585 | 0.319 | 0.543 |
| 112 | `2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.447 | 0.319 | 0.303 |
| 113 | `2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.447 | 0.319 | 0.339 |
| 114 | `2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.585 | 0.319 | 0.510 |
| 115 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.596 | 0.319 | 0.599 |
| 116 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.011 | 0.670 | 0.457 | 0.319 | 0.306 |
| 117 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.011 | 0.670 | 0.457 | 0.319 | 0.311 |
| 118 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.011 | 0.670 | 0.574 | 0.319 | 0.564 |
| 119 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.681 | 0.011 | 0.670 | 0.606 | 0.319 | 0.594 |
| 120 | `1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.000 | 0.681 | 0.468 | 0.319 | 0.339 |
| 121 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.000 | 0.681 | 0.585 | 0.319 | 0.690 |
| 122 | `P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.670 | 0.053 | 0.617 | 0.553 | 0.330 | 0.517 |
| 123 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.670 | 0.043 | 0.628 | 0.574 | 0.330 | 0.561 |
| 124 | `1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.436 | 0.330 | 0.330 |
| 125 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.574 | 0.330 | 0.520 |
| 126 | `1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.553 | 0.330 | 0.548 |
| 127 | `P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.585 | 0.330 | 0.562 |
| 128 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.670 | 0.032 | 0.638 | 0.596 | 0.330 | 0.568 |
| 129 | `P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.660 | 0.043 | 0.617 | 0.543 | 0.340 | 0.610 |
| 130 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.660 | 0.021 | 0.638 | 0.596 | 0.340 | 0.615 |
| 131 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.660 | 0.021 | 0.638 | 0.606 | 0.340 | 0.696 |
| 132 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.649 | 0.021 | 0.628 | 0.447 | 0.351 | 0.336 |
| 133 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.649 | 0.011 | 0.638 | 0.457 | 0.351 | 0.341 |
| 134 | `2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.638 | 0.053 | 0.585 | 0.415 | 0.362 | 0.317 |
| 135 | `P0|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.638 | 0.021 | 0.617 | 0.447 | 0.362 | 0.335 |
| 136 | `2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.617 | 0.011 | 0.606 | 0.457 | 0.383 | 0.409 |

## Size 2 Combos Sorted By Gain Over Best Single

| rank | combo | union@3 | gain | best_single | all_hit | neither | avg_pair_jaccard@3 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.564 | 0.255 | 0.480 |
| 2 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.564 | 0.287 | 0.464 |
| 3 | `2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.681 | 0.074 | 0.606 | 0.511 | 0.319 | 0.497 |
| 4 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.574 | 0.277 | 0.433 |
| 5 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.596 | 0.277 | 0.518 |
| 6 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.064 | 0.628 | 0.543 | 0.309 | 0.517 |
| 7 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.543 | 0.298 | 0.450 |
| 8 | `1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.543 | 0.298 | 0.512 |
| 9 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.574 | 0.277 | 0.535 |
| 10 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.606 | 0.277 | 0.544 |
| 11 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.562 |
| 12 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.532 | 0.309 | 0.461 |
| 13 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.691 | 0.053 | 0.638 | 0.564 | 0.309 | 0.463 |
| 14 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.532 | 0.309 | 0.499 |
| 15 | `1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.585 | 0.309 | 0.500 |
| 16 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.053 | 0.628 | 0.532 | 0.319 | 0.556 |
| 17 | `P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.670 | 0.053 | 0.617 | 0.553 | 0.330 | 0.517 |
| 18 | `2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.638 | 0.053 | 0.585 | 0.415 | 0.362 | 0.317 |
| 19 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.628 | 0.255 | 0.489 |
| 20 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.617 | 0.277 | 0.500 |
| 21 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.628 | 0.277 | 0.601 |
| 22 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.596 | 0.298 | 0.497 |
| 23 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.585 | 0.298 | 0.507 |
| 24 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.702 | 0.043 | 0.660 | 0.596 | 0.298 | 0.524 |
| 25 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.596 | 0.298 | 0.560 |
| 26 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.043 | 0.660 | 0.585 | 0.298 | 0.583 |
| 27 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.670 | 0.043 | 0.628 | 0.574 | 0.330 | 0.561 |
| 28 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.649 | 0.255 | 0.515 |
| 29 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.457 |
| 30 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.617 | 0.266 | 0.519 |
| 31 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.638 | 0.266 | 0.564 |
| 32 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.043 | 0.670 | 0.596 | 0.287 | 0.473 |
| 33 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.596 | 0.287 | 0.491 |
| 34 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.617 | 0.287 | 0.543 |
| 35 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.617 | 0.287 | 0.639 |
| 36 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.426 | 0.319 | 0.314 |
| 37 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.681 | 0.043 | 0.638 | 0.596 | 0.319 | 0.527 |
| 38 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.585 | 0.319 | 0.543 |
| 39 | `P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.660 | 0.043 | 0.617 | 0.543 | 0.340 | 0.610 |
| 40 | `2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.606 | 0.309 | 0.471 |
| 41 | `2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.574 | 0.309 | 0.500 |
| 42 | `2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.553 | 0.309 | 0.567 |
| 43 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.606 | 0.309 | 0.570 |
| 44 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.553 | 0.309 | 0.606 |
| 45 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.585 | 0.309 | 0.611 |
| 46 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.502 |
| 47 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.539 |
| 48 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.649 | 0.266 | 0.574 |
| 49 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.660 | 0.266 | 0.590 |
| 50 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.670 | 0.266 | 0.647 |
| 51 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.650 |
| 52 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.574 | 0.277 | 0.449 |
| 53 | `2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.606 | 0.277 | 0.454 |
| 54 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.506 |
| 55 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.638 | 0.277 | 0.514 |
| 56 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.535 |
| 57 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.606 | 0.277 | 0.538 |
| 58 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.628 | 0.277 | 0.556 |
| 59 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.638 | 0.277 | 0.566 |
| 60 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.473 |
| 61 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.474 |
| 62 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.503 |
| 63 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.519 |
| 64 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.638 | 0.287 | 0.571 |
| 65 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.649 | 0.287 | 0.603 |
| 66 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.628 | 0.287 | 0.613 |
| 67 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.628 | 0.287 | 0.627 |
| 68 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.638 | 0.287 | 0.678 |
| 69 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.628 | 0.287 | 0.694 |
| 70 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.585 | 0.298 | 0.614 |
| 71 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.638 | 0.298 | 0.659 |
| 72 | `1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.436 | 0.330 | 0.330 |
| 73 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.574 | 0.330 | 0.520 |
| 74 | `1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.553 | 0.330 | 0.548 |
| 75 | `P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.585 | 0.330 | 0.562 |
| 76 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.670 | 0.032 | 0.638 | 0.596 | 0.330 | 0.568 |
| 77 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.483 |
| 78 | `1-3|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.516 |
| 79 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.568 |
| 80 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.572 |
| 81 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.586 |
| 82 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.649 | 0.277 | 0.620 |
| 83 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.649 | 0.277 | 0.666 |
| 84 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.638 | 0.277 | 0.666 |
| 85 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.660 | 0.277 | 0.691 |
| 86 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.649 | 0.277 | 0.723 |
| 87 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.447 | 0.298 | 0.300 |
| 88 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.702 | 0.021 | 0.681 | 0.617 | 0.298 | 0.518 |
| 89 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.021 | 0.681 | 0.606 | 0.298 | 0.519 |
| 90 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.564 | 0.298 | 0.553 |
| 91 | `1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.555 |
| 92 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.649 | 0.298 | 0.623 |
| 93 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.585 | 0.309 | 0.481 |
| 94 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.585 | 0.309 | 0.523 |
| 95 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.691 | 0.021 | 0.670 | 0.617 | 0.309 | 0.524 |
| 96 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.691 | 0.021 | 0.670 | 0.606 | 0.309 | 0.543 |
| 97 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.617 | 0.309 | 0.550 |
| 98 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.564 | 0.309 | 0.590 |
| 99 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.638 | 0.309 | 0.662 |
| 100 | `2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.447 | 0.319 | 0.303 |
| 101 | `2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.447 | 0.319 | 0.339 |
| 102 | `2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.585 | 0.319 | 0.510 |
| 103 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.596 | 0.319 | 0.599 |
| 104 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.649 | 0.021 | 0.628 | 0.447 | 0.351 | 0.336 |
| 105 | `P0|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.638 | 0.021 | 0.617 | 0.447 | 0.362 | 0.335 |
| 106 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.021 | 0.691 | 0.606 | 0.287 | 0.511 |
| 107 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.660 | 0.021 | 0.638 | 0.596 | 0.340 | 0.615 |
| 108 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.660 | 0.021 | 0.638 | 0.606 | 0.340 | 0.696 |
| 109 | `1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.628 | 0.309 | 0.573 |
| 110 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.606 | 0.309 | 0.591 |
| 111 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.617 | 0.309 | 0.616 |
| 112 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.628 | 0.309 | 0.649 |
| 113 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.606 | 0.309 | 0.712 |
| 114 | `1-3|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.457 | 0.287 | 0.312 |
| 115 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.596 | 0.287 | 0.504 |
| 116 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.628 | 0.287 | 0.543 |
| 117 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.011 | 0.702 | 0.617 | 0.287 | 0.561 |
| 118 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.713 | 0.011 | 0.702 | 0.628 | 0.287 | 0.565 |
| 119 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.574 | 0.287 | 0.587 |
| 120 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.649 | 0.287 | 0.617 |
| 121 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.574 | 0.287 | 0.631 |
| 122 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.660 | 0.287 | 0.652 |
| 123 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.670 | 0.287 | 0.718 |
| 124 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.011 | 0.670 | 0.457 | 0.319 | 0.306 |
| 125 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.011 | 0.670 | 0.457 | 0.319 | 0.311 |
| 126 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.011 | 0.670 | 0.574 | 0.319 | 0.564 |
| 127 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.681 | 0.011 | 0.670 | 0.606 | 0.319 | 0.594 |
| 128 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.649 | 0.011 | 0.638 | 0.457 | 0.351 | 0.341 |
| 129 | `2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.617 | 0.011 | 0.606 | 0.457 | 0.383 | 0.409 |
| 130 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.468 | 0.298 | 0.329 |
| 131 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.681 | 0.298 | 0.645 |
| 132 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.617 | 0.298 | 0.661 |
| 133 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.617 | 0.298 | 0.674 |
| 134 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.000 | 0.691 | 0.468 | 0.309 | 0.301 |
| 135 | `1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.000 | 0.681 | 0.468 | 0.319 | 0.339 |
| 136 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.000 | 0.681 | 0.585 | 0.319 | 0.690 |

## Size 3 Combos Sorted By Union Hit@3

| rank | combo | union@3 | gain | best_single | all_hit | neither | avg_pair_jaccard@3 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.415 | 0.255 | 0.367 |
| 2 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.521 | 0.255 | 0.470 |
| 3 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.521 | 0.255 | 0.478 |
| 4 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.521 | 0.255 | 0.485 |
| 5 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.511 | 0.255 | 0.510 |
| 6 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.532 | 0.255 | 0.519 |
| 7 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.543 | 0.255 | 0.523 |
| 8 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.543 | 0.255 | 0.528 |
| 9 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.564 | 0.255 | 0.537 |
| 10 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.553 | 0.255 | 0.548 |
| 11 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.064 | 0.681 | 0.553 | 0.255 | 0.528 |
| 12 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.064 | 0.681 | 0.564 | 0.255 | 0.559 |
| 13 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.447 | 0.255 | 0.363 |
| 14 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.543 | 0.255 | 0.471 |
| 15 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.574 | 0.255 | 0.472 |
| 16 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.511 | 0.255 | 0.475 |
| 17 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.564 | 0.255 | 0.483 |
| 18 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.543 | 0.255 | 0.501 |
| 19 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.585 | 0.255 | 0.506 |
| 20 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.574 | 0.255 | 0.513 |
| 21 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.585 | 0.255 | 0.515 |
| 22 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.585 | 0.255 | 0.515 |
| 23 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.532 | 0.255 | 0.516 |
| 24 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.606 | 0.255 | 0.525 |
| 25 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.574 | 0.255 | 0.539 |
| 26 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.585 | 0.255 | 0.540 |
| 27 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.532 | 0.255 | 0.544 |
| 28 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.596 | 0.255 | 0.552 |
| 29 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.606 | 0.255 | 0.552 |
| 30 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.596 | 0.255 | 0.575 |
| 31 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.596 | 0.255 | 0.592 |
| 32 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.457 | 0.255 | 0.376 |
| 33 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.543 | 0.255 | 0.483 |
| 34 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.485 |
| 35 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.574 | 0.255 | 0.485 |
| 36 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.543 | 0.255 | 0.485 |
| 37 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.553 | 0.255 | 0.493 |
| 38 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.503 |
| 39 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.511 |
| 40 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.574 | 0.255 | 0.517 |
| 41 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.518 |
| 42 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.527 |
| 43 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.528 |
| 44 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.529 |
| 45 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.534 |
| 46 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.543 | 0.255 | 0.536 |
| 47 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.537 |
| 48 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.539 |
| 49 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.544 |
| 50 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.547 |
| 51 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.628 | 0.255 | 0.550 |
| 52 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.550 |
| 53 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.551 |
| 54 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.554 |
| 55 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.555 |
| 56 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.574 | 0.255 | 0.559 |
| 57 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.628 | 0.255 | 0.560 |
| 58 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.565 |
| 59 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.617 | 0.255 | 0.567 |
| 60 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.553 | 0.255 | 0.568 |
| 61 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.570 |
| 62 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.580 |
| 63 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.628 | 0.255 | 0.584 |
| 64 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.587 |
| 65 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.617 | 0.255 | 0.590 |
| 66 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.592 |
| 67 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.594 |
| 68 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.617 | 0.255 | 0.595 |
| 69 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.574 | 0.255 | 0.600 |
| 70 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.611 |
| 71 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.617 | 0.255 | 0.617 |
| 72 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.074 | 0.660 | 0.511 | 0.266 | 0.487 |
| 73 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.074 | 0.660 | 0.543 | 0.266 | 0.492 |
| 74 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.074 | 0.660 | 0.532 | 0.266 | 0.564 |
| 75 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.543 | 0.266 | 0.482 |
| 76 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.553 | 0.266 | 0.483 |
| 77 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.564 | 0.266 | 0.567 |
| 78 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.553 | 0.266 | 0.586 |
| 79 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.564 | 0.266 | 0.587 |
| 80 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.532 | 0.266 | 0.476 |
| 81 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.553 | 0.266 | 0.479 |
| 82 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.553 | 0.266 | 0.480 |
| 83 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.543 | 0.266 | 0.508 |
| 84 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.585 | 0.266 | 0.516 |
| 85 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.564 | 0.266 | 0.526 |
| 86 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.596 | 0.266 | 0.538 |
| 87 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.596 | 0.266 | 0.539 |
| 88 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.596 | 0.266 | 0.542 |
| 89 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.574 | 0.266 | 0.544 |
| 90 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.585 | 0.266 | 0.547 |
| 91 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.574 | 0.266 | 0.548 |
| 92 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.564 | 0.266 | 0.552 |
| 93 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.574 | 0.266 | 0.560 |
| 94 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.585 | 0.266 | 0.579 |
| 95 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.585 | 0.266 | 0.613 |
| 96 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.426 | 0.266 | 0.357 |
| 97 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.447 | 0.266 | 0.374 |
| 98 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.468 | 0.266 | 0.401 |
| 99 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.511 | 0.266 | 0.452 |
| 100 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.532 | 0.266 | 0.459 |
| 101 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.482 |
| 102 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.543 | 0.266 | 0.482 |
| 103 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.489 | 0.266 | 0.484 |
| 104 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.532 | 0.266 | 0.485 |
| 105 | `2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.511 | 0.266 | 0.487 |
| 106 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.543 | 0.266 | 0.489 |
| 107 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.490 |
| 108 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.499 |
| 109 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.500 |
| 110 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.574 | 0.266 | 0.504 |
| 111 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.507 |
| 112 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.574 | 0.266 | 0.512 |
| 113 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.523 |
| 114 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.521 | 0.266 | 0.524 |
| 115 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.528 |
| 116 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.530 |
| 117 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.532 | 0.266 | 0.531 |
| 118 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.531 |
| 119 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.537 |
| 120 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.538 |
| 121 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.539 |
| 122 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.532 | 0.266 | 0.543 |
| 123 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.521 | 0.266 | 0.550 |
| 124 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.543 | 0.266 | 0.554 |
| 125 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.555 |
| 126 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.585 | 0.266 | 0.555 |
| 127 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.555 |
| 128 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.563 |
| 129 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.606 | 0.266 | 0.565 |
| 130 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.617 | 0.266 | 0.567 |
| 131 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.572 |
| 132 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.617 | 0.266 | 0.579 |
| 133 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.582 |
| 134 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.584 |
| 135 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.587 |
| 136 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.606 | 0.266 | 0.602 |
| 137 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.574 | 0.266 | 0.604 |
| 138 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.426 | 0.266 | 0.370 |
| 139 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.426 | 0.266 | 0.382 |
| 140 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.436 | 0.266 | 0.397 |
| 141 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.447 | 0.266 | 0.401 |
| 142 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.468 | 0.266 | 0.407 |
| 143 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.447 | 0.266 | 0.427 |
| 144 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.457 | 0.266 | 0.429 |
| 145 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.532 | 0.266 | 0.510 |
| 146 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.515 |
| 147 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.518 |
| 148 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.522 |
| 149 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.529 |
| 150 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.529 |
| 151 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.530 |
| 152 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.530 |
| 153 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.531 |
| 154 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.531 |
| 155 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.521 | 0.266 | 0.531 |
| 156 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.532 |
| 157 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.534 |
| 158 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.536 |
| 159 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.536 |
| 160 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.538 |
| 161 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.541 |
| 162 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.546 |
| 163 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.546 |
| 164 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.550 |
| 165 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.551 |
| 166 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.551 |
| 167 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.556 |
| 168 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.556 |
| 169 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.558 |
| 170 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.558 |
| 171 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.561 |
| 172 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.563 |
| 173 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.563 |
| 174 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.565 |
| 175 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.567 |
| 176 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.568 |
| 177 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.572 |
| 178 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.576 |
| 179 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.578 |
| 180 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.580 |
| 181 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.580 |
| 182 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.582 |
| 183 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.553 | 0.266 | 0.586 |
| 184 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.588 |
| 185 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.590 |
| 186 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.592 |
| 187 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.592 |
| 188 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.600 |
| 189 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.600 |
| 190 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.603 |
| 191 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.604 |
| 192 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.604 |
| 193 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.609 |
| 194 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.612 |
| 195 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.613 |
| 196 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.619 |
| 197 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.619 |
| 198 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.553 | 0.266 | 0.621 |
| 199 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.622 |
| 200 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.649 | 0.266 | 0.622 |
| 201 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.623 |
| 202 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.624 |
| 203 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.625 |
| 204 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.627 |
| 205 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.629 |
| 206 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.638 | 0.266 | 0.632 |
| 207 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.633 |
| 208 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.635 |
| 209 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.638 |
| 210 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.644 |
| 211 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.645 |
| 212 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.638 | 0.266 | 0.655 |
| 213 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.659 |
| 214 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.661 |
| 215 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.663 |
| 216 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.670 |
| 217 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.671 |
| 218 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.649 | 0.266 | 0.685 |
| 219 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.687 |
| 220 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.479 | 0.277 | 0.469 |
| 221 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.489 | 0.277 | 0.474 |
| 222 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.521 | 0.277 | 0.477 |
| 223 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.521 | 0.277 | 0.478 |
| 224 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.543 | 0.277 | 0.496 |
| 225 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.521 | 0.277 | 0.496 |
| 226 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.404 | 0.277 | 0.362 |
| 227 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.426 | 0.277 | 0.387 |
| 228 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.532 | 0.277 | 0.456 |
| 229 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.521 | 0.277 | 0.464 |
| 230 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.532 | 0.277 | 0.491 |
| 231 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.543 | 0.277 | 0.495 |
| 232 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.564 | 0.277 | 0.495 |
| 233 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.543 | 0.277 | 0.498 |
| 234 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.553 | 0.277 | 0.503 |
| 235 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.553 | 0.277 | 0.509 |
| 236 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.564 | 0.277 | 0.510 |
| 237 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.532 | 0.277 | 0.524 |
| 238 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.521 | 0.277 | 0.530 |
| 239 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.064 | 0.660 | 0.553 | 0.277 | 0.533 |
| 240 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.532 | 0.277 | 0.533 |
| 241 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.543 | 0.277 | 0.536 |
| 242 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.564 | 0.277 | 0.549 |
| 243 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.543 | 0.277 | 0.571 |
| 244 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.564 | 0.277 | 0.576 |
| 245 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.521 | 0.277 | 0.582 |
| 246 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.426 | 0.277 | 0.366 |
| 247 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.436 | 0.277 | 0.393 |
| 248 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.436 | 0.277 | 0.396 |
| 249 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.426 | 0.277 | 0.399 |
| 250 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.553 | 0.277 | 0.496 |
| 251 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.532 | 0.277 | 0.499 |
| 252 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.502 |
| 253 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.510 |
| 254 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.521 | 0.277 | 0.511 |
| 255 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.511 |
| 256 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.543 | 0.277 | 0.518 |
| 257 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.521 | 0.277 | 0.518 |
| 258 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.543 | 0.277 | 0.523 |
| 259 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.532 | 0.277 | 0.529 |
| 260 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.543 |
| 261 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.553 |
| 262 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.553 | 0.277 | 0.558 |
| 263 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.553 | 0.277 | 0.559 |
| 264 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.511 | 0.277 | 0.561 |
| 265 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.532 | 0.277 | 0.567 |
| 266 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.532 | 0.277 | 0.567 |
| 267 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.543 | 0.277 | 0.570 |
| 268 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.574 |
| 269 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.574 | 0.277 | 0.579 |
| 270 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.582 |
| 271 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.582 |
| 272 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.585 |
| 273 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.597 |
| 274 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.553 | 0.277 | 0.598 |
| 275 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.415 | 0.277 | 0.372 |
| 276 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.426 | 0.277 | 0.380 |
| 277 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.447 | 0.277 | 0.394 |
| 278 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.436 | 0.277 | 0.402 |
| 279 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.482 |
| 280 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.553 | 0.277 | 0.495 |
| 281 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.497 |
| 282 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.532 | 0.277 | 0.501 |
| 283 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.532 | 0.277 | 0.504 |
| 284 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.521 | 0.277 | 0.506 |
| 285 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.509 |
| 286 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.512 |
| 287 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.553 | 0.277 | 0.519 |
| 288 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.519 |
| 289 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.522 |
| 290 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.523 |
| 291 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.528 |
| 292 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.553 | 0.277 | 0.529 |
| 293 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.529 |
| 294 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.532 |
| 295 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.538 |
| 296 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.532 | 0.277 | 0.540 |
| 297 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.544 |
| 298 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.563 |
| 299 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.563 |
| 300 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.565 |
| 301 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.572 |
| 302 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.577 |
| 303 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.579 |
| 304 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.543 | 0.277 | 0.582 |
| 305 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.583 |
| 306 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.617 | 0.277 | 0.590 |
| 307 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.543 | 0.277 | 0.591 |
| 308 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.598 |
| 309 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.628 | 0.277 | 0.599 |
| 310 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.602 |
| 311 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.610 |
| 312 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.610 |
| 313 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.617 | 0.277 | 0.615 |
| 314 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.616 |
| 315 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.618 |
| 316 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.627 |
| 317 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.629 |
| 318 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.631 |
| 319 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.634 |
| 320 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.637 |
| 321 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.670 |
| 322 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.672 |
| 323 | `2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.457 | 0.277 | 0.366 |
| 324 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.415 | 0.277 | 0.375 |
| 325 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.457 | 0.277 | 0.375 |
| 326 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.457 | 0.277 | 0.386 |
| 327 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.436 | 0.277 | 0.390 |
| 328 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.447 | 0.277 | 0.390 |
| 329 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.457 | 0.277 | 0.391 |
| 330 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.447 | 0.277 | 0.399 |
| 331 | `2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.543 | 0.277 | 0.474 |
| 332 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.521 | 0.277 | 0.492 |
| 333 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.574 | 0.277 | 0.494 |
| 334 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.495 |
| 335 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.498 |
| 336 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.511 | 0.277 | 0.500 |
| 337 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.521 | 0.277 | 0.500 |
| 338 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.564 | 0.277 | 0.502 |
| 339 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.505 |
| 340 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.506 |
| 341 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.517 |
| 342 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.522 |
| 343 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.564 | 0.277 | 0.525 |
| 344 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.526 |
| 345 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.535 |
| 346 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.538 |
| 347 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.574 | 0.277 | 0.548 |
| 348 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.574 | 0.277 | 0.555 |
| 349 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.564 | 0.277 | 0.563 |
| 350 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.564 | 0.277 | 0.563 |
| 351 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.582 |
| 352 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.436 | 0.277 | 0.402 |
| 353 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.403 |
| 354 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.415 | 0.277 | 0.405 |
| 355 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.436 | 0.277 | 0.410 |
| 356 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.411 |
| 357 | `1-3|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.412 |
| 358 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.413 |
| 359 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.413 |
| 360 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.457 | 0.277 | 0.425 |
| 361 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.457 | 0.277 | 0.435 |
| 362 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.445 |
| 363 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.457 | 0.277 | 0.448 |
| 364 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.457 | 0.277 | 0.453 |
| 365 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.525 |
| 366 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.500 | 0.277 | 0.533 |
| 367 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.535 |
| 368 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.537 |
| 369 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.539 |
| 370 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.541 |
| 371 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.544 |
| 372 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.511 | 0.277 | 0.544 |
| 373 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.544 |
| 374 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.545 |
| 375 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.521 | 0.277 | 0.557 |
| 376 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.532 | 0.277 | 0.557 |
| 377 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.596 | 0.277 | 0.560 |
| 378 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.560 |
| 379 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.564 |
| 380 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.565 |
| 381 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.565 |
| 382 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.566 |
| 383 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.567 |
| 384 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.567 |
| 385 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.568 |
| 386 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.532 | 0.277 | 0.568 |
| 387 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.570 |
| 388 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.580 |
| 389 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.596 | 0.277 | 0.580 |
| 390 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.543 | 0.277 | 0.584 |
| 391 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.585 |
| 392 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.521 | 0.277 | 0.585 |
| 393 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.586 |
| 394 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.586 |
| 395 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.587 |
| 396 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.588 |
| 397 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.593 |
| 398 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.596 |
| 399 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.599 |
| 400 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.601 |
| 401 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.603 |
| 402 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.604 |
| 403 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.628 | 0.277 | 0.611 |
| 404 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.612 |
| 405 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.617 |
| 406 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.620 |
| 407 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.596 | 0.277 | 0.621 |
| 408 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.628 | 0.277 | 0.622 |
| 409 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.626 |
| 410 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.632 |
| 411 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.634 |
| 412 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.638 | 0.277 | 0.644 |
| 413 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.628 | 0.277 | 0.644 |
| 414 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.645 |
| 415 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.649 | 0.277 | 0.646 |
| 416 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.596 | 0.277 | 0.646 |
| 417 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.646 |
| 418 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.648 |
| 419 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.638 | 0.277 | 0.656 |
| 420 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.656 |
| 421 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.663 |
| 422 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.667 |
| 423 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.638 | 0.277 | 0.669 |
| 424 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.671 |
| 425 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.683 |
| 426 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.688 |
| 427 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.628 | 0.277 | 0.706 |
| 428 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.085 | 0.628 | 0.479 | 0.287 | 0.523 |
| 429 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.394 | 0.287 | 0.364 |
| 430 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.415 | 0.287 | 0.373 |
| 431 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.426 | 0.287 | 0.391 |
| 432 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.543 | 0.287 | 0.497 |
| 433 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.511 | 0.287 | 0.511 |
| 434 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.521 | 0.287 | 0.512 |
| 435 | `1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.489 | 0.287 | 0.519 |
| 436 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.553 | 0.287 | 0.525 |
| 437 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.415 | 0.287 | 0.380 |
| 438 | `2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.415 | 0.287 | 0.408 |
| 439 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.553 | 0.287 | 0.506 |
| 440 | `2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.521 | 0.287 | 0.512 |
| 441 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.553 | 0.287 | 0.519 |
| 442 | `2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.511 | 0.287 | 0.524 |
| 443 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.511 | 0.287 | 0.534 |
| 444 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.053 | 0.660 | 0.564 | 0.287 | 0.537 |
| 445 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.553 | 0.287 | 0.541 |
| 446 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.511 | 0.287 | 0.544 |
| 447 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.564 | 0.287 | 0.556 |
| 448 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.053 | 0.660 | 0.564 | 0.287 | 0.559 |
| 449 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.053 | 0.660 | 0.553 | 0.287 | 0.585 |
| 450 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.574 | 0.287 | 0.595 |
| 451 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.532 | 0.287 | 0.609 |
| 452 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.447 | 0.287 | 0.380 |
| 453 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.436 | 0.287 | 0.398 |
| 454 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.436 | 0.287 | 0.416 |
| 455 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.553 | 0.287 | 0.498 |
| 456 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.043 | 0.670 | 0.574 | 0.287 | 0.508 |
| 457 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.543 | 0.287 | 0.520 |
| 458 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.521 |
| 459 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.564 | 0.287 | 0.525 |
| 460 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.511 | 0.287 | 0.527 |
| 461 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.543 | 0.287 | 0.528 |
| 462 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.043 | 0.670 | 0.574 | 0.287 | 0.528 |
| 463 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.564 | 0.287 | 0.531 |
| 464 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.553 | 0.287 | 0.540 |
| 465 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.546 |
| 466 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.553 | 0.287 | 0.556 |
| 467 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.567 |
| 468 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.578 |
| 469 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.596 | 0.287 | 0.582 |
| 470 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.596 |
| 471 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.532 | 0.287 | 0.612 |
| 472 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.553 | 0.287 | 0.621 |
| 473 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.606 | 0.287 | 0.653 |
| 474 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.436 | 0.287 | 0.372 |
| 475 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.426 | 0.287 | 0.383 |
| 476 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.436 | 0.287 | 0.385 |
| 477 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.404 | 0.287 | 0.390 |
| 478 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.426 | 0.287 | 0.391 |
| 479 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.436 | 0.287 | 0.394 |
| 480 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.426 | 0.287 | 0.405 |
| 481 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.447 | 0.287 | 0.414 |
| 482 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.447 | 0.287 | 0.435 |
| 483 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.457 | 0.287 | 0.441 |
| 484 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.447 | 0.287 | 0.445 |
| 485 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.489 |
| 486 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.489 | 0.287 | 0.508 |
| 487 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.511 | 0.287 | 0.509 |
| 488 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.516 |
| 489 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.519 |
| 490 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.528 |
| 491 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.530 |
| 492 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.540 |
| 493 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.542 |
| 494 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.521 | 0.287 | 0.543 |
| 495 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.544 |
| 496 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.550 |
| 497 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.532 | 0.287 | 0.557 |
| 498 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.557 |
| 499 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.563 |
| 500 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.563 |
| 501 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.564 | 0.287 | 0.564 |
| 502 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.565 |
| 503 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.567 |
| 504 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.568 |
| 505 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.564 | 0.287 | 0.571 |
| 506 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.572 |
| 507 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.581 |
| 508 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.583 |
| 509 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.585 |
| 510 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.588 |
| 511 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.594 |
| 512 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.617 | 0.287 | 0.599 |
| 513 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.605 |
| 514 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.615 |
| 515 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.564 | 0.287 | 0.616 |
| 516 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.628 |
| 517 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.635 |
| 518 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.643 |
| 519 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.646 |
| 520 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.564 | 0.287 | 0.653 |
| 521 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.617 | 0.287 | 0.653 |
| 522 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.617 | 0.287 | 0.660 |
| 523 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.663 |
| 524 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.668 |
| 525 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.021 | 0.691 | 0.447 | 0.287 | 0.383 |
| 526 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.457 | 0.287 | 0.404 |
| 527 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.436 | 0.287 | 0.411 |
| 528 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.457 | 0.287 | 0.414 |
| 529 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.447 | 0.287 | 0.419 |
| 530 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.415 | 0.287 | 0.426 |
| 531 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.447 | 0.287 | 0.436 |
| 532 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.468 | 0.287 | 0.462 |
| 533 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.564 | 0.287 | 0.522 |
| 534 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.553 | 0.287 | 0.565 |
| 535 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.011 | 0.702 | 0.606 | 0.287 | 0.575 |
| 536 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.713 | 0.011 | 0.702 | 0.617 | 0.287 | 0.576 |
| 537 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.585 | 0.287 | 0.593 |
| 538 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.011 | 0.702 | 0.574 | 0.287 | 0.594 |
| 539 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.564 | 0.287 | 0.595 |
| 540 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.564 | 0.287 | 0.601 |
| 541 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.011 | 0.702 | 0.596 | 0.287 | 0.607 |
| 542 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.713 | 0.011 | 0.702 | 0.596 | 0.287 | 0.613 |
| 543 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.543 | 0.287 | 0.619 |
| 544 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.638 | 0.287 | 0.623 |
| 545 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.628 | 0.287 | 0.625 |
| 546 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.585 | 0.287 | 0.629 |
| 547 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.606 | 0.287 | 0.635 |
| 548 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.543 | 0.287 | 0.638 |
| 549 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.574 | 0.287 | 0.680 |
| 550 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.606 | 0.287 | 0.701 |
| 551 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.074 | 0.628 | 0.521 | 0.298 | 0.532 |
| 552 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.415 | 0.298 | 0.371 |
| 553 | `1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.426 | 0.298 | 0.417 |
| 554 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.489 | 0.298 | 0.505 |
| 555 | `1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.521 | 0.298 | 0.511 |
| 556 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.521 | 0.298 | 0.512 |
| 557 | `1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.511 | 0.298 | 0.516 |
| 558 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.532 | 0.298 | 0.527 |
| 559 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.511 | 0.298 | 0.528 |
| 560 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.500 | 0.298 | 0.533 |
| 561 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.532 | 0.298 | 0.548 |
| 562 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.564 | 0.298 | 0.555 |
| 563 | `P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.521 | 0.298 | 0.557 |
| 564 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.574 | 0.298 | 0.559 |
| 565 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.521 | 0.298 | 0.575 |
| 566 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.436 | 0.298 | 0.380 |
| 567 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.426 | 0.298 | 0.394 |
| 568 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.415 | 0.298 | 0.398 |
| 569 | `2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.447 | 0.298 | 0.404 |
| 570 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.426 | 0.298 | 0.407 |
| 571 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.404 | 0.298 | 0.409 |
| 572 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.426 | 0.298 | 0.413 |
| 573 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.553 | 0.298 | 0.507 |
| 574 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.521 | 0.298 | 0.511 |
| 575 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.564 | 0.298 | 0.514 |
| 576 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.532 | 0.298 | 0.530 |
| 577 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.489 | 0.298 | 0.534 |
| 578 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.532 | 0.298 | 0.543 |
| 579 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.553 | 0.298 | 0.556 |
| 580 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.532 | 0.298 | 0.562 |
| 581 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.574 | 0.298 | 0.591 |
| 582 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.532 | 0.298 | 0.592 |
| 583 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.043 | 0.660 | 0.564 | 0.298 | 0.613 |
| 584 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.436 | 0.298 | 0.388 |
| 585 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.447 | 0.298 | 0.396 |
| 586 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.415 | 0.298 | 0.405 |
| 587 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.436 | 0.298 | 0.418 |
| 588 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.447 | 0.298 | 0.425 |
| 589 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.500 | 0.298 | 0.523 |
| 590 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.574 | 0.298 | 0.525 |
| 591 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.511 | 0.298 | 0.528 |
| 592 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.564 | 0.298 | 0.531 |
| 593 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.532 | 0.298 | 0.537 |
| 594 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.532 | 0.298 | 0.538 |
| 595 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.574 | 0.298 | 0.545 |
| 596 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.553 | 0.298 | 0.545 |
| 597 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.564 | 0.298 | 0.554 |
| 598 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.532 | 0.298 | 0.554 |
| 599 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.564 | 0.298 | 0.562 |
| 600 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.032 | 0.670 | 0.574 | 0.298 | 0.566 |
| 601 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.585 | 0.298 | 0.568 |
| 602 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.585 | 0.298 | 0.570 |
| 603 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.702 | 0.032 | 0.670 | 0.596 | 0.298 | 0.578 |
| 604 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.553 | 0.298 | 0.604 |
| 605 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.521 | 0.298 | 0.605 |
| 606 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.553 | 0.298 | 0.611 |
| 607 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.574 | 0.298 | 0.622 |
| 608 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.585 | 0.298 | 0.622 |
| 609 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.436 | 0.298 | 0.409 |
| 610 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.457 | 0.298 | 0.424 |
| 611 | `1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.457 | 0.298 | 0.434 |
| 612 | `1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.564 | 0.298 | 0.550 |
| 613 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.021 | 0.681 | 0.564 | 0.298 | 0.557 |
| 614 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.574 |
| 615 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.575 |
| 616 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.577 |
| 617 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.578 |
| 618 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.511 | 0.298 | 0.581 |
| 619 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.606 | 0.298 | 0.582 |
| 620 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.532 | 0.298 | 0.585 |
| 621 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.543 | 0.298 | 0.595 |
| 622 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.616 |
| 623 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.574 | 0.298 | 0.626 |
| 624 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.574 | 0.298 | 0.629 |
| 625 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.596 | 0.298 | 0.659 |
| 626 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.447 | 0.298 | 0.446 |
| 627 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.606 | 0.298 | 0.632 |
| 628 | `2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.085 | 0.606 | 0.415 | 0.309 | 0.407 |
| 629 | `P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.074 | 0.617 | 0.489 | 0.309 | 0.541 |
| 630 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.064 | 0.628 | 0.404 | 0.309 | 0.403 |
| 631 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.064 | 0.628 | 0.436 | 0.309 | 0.421 |
| 632 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.064 | 0.628 | 0.511 | 0.309 | 0.576 |
| 633 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.404 | 0.309 | 0.386 |
| 634 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.404 | 0.309 | 0.390 |
| 635 | `1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.426 | 0.309 | 0.390 |
| 636 | `1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.404 | 0.309 | 0.398 |
| 637 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.447 | 0.309 | 0.407 |
| 638 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.691 | 0.053 | 0.638 | 0.543 | 0.309 | 0.530 |
| 639 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.691 | 0.053 | 0.638 | 0.553 | 0.309 | 0.535 |
| 640 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.564 | 0.309 | 0.579 |
| 641 | `2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.436 | 0.309 | 0.384 |
| 642 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.426 | 0.309 | 0.416 |
| 643 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.436 | 0.309 | 0.424 |
| 644 | `2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.553 | 0.309 | 0.500 |
| 645 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.543 | 0.309 | 0.542 |
| 646 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.564 | 0.309 | 0.544 |
| 647 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.574 | 0.309 | 0.595 |
| 648 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.415 | 0.309 | 0.397 |
| 649 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.447 | 0.309 | 0.399 |
| 650 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.447 | 0.309 | 0.401 |
| 651 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.447 | 0.309 | 0.413 |
| 652 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.447 | 0.309 | 0.414 |
| 653 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.436 | 0.309 | 0.425 |
| 654 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.543 | 0.309 | 0.545 |
| 655 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.691 | 0.021 | 0.670 | 0.585 | 0.309 | 0.588 |
| 656 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.543 | 0.309 | 0.589 |
| 657 | `1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.457 | 0.309 | 0.418 |
| 658 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.447 | 0.309 | 0.430 |
| 659 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.436 | 0.309 | 0.439 |
| 660 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.447 | 0.309 | 0.462 |
| 661 | `1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.532 | 0.309 | 0.588 |
| 662 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.532 | 0.309 | 0.621 |
| 663 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.553 | 0.309 | 0.629 |
| 664 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.596 | 0.309 | 0.654 |
| 665 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.543 | 0.309 | 0.671 |
| 666 | `P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.064 | 0.617 | 0.415 | 0.319 | 0.421 |
| 667 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.053 | 0.628 | 0.436 | 0.319 | 0.411 |
| 668 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.415 | 0.319 | 0.406 |
| 669 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.436 | 0.319 | 0.427 |
| 670 | `P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.532 | 0.319 | 0.533 |
| 671 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.532 | 0.319 | 0.591 |
| 672 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.681 | 0.043 | 0.638 | 0.574 | 0.319 | 0.597 |
| 673 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.521 | 0.319 | 0.600 |
| 674 | `2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.436 | 0.319 | 0.419 |
| 675 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.000 | 0.681 | 0.415 | 0.319 | 0.449 |
| 676 | `P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.053 | 0.617 | 0.436 | 0.330 | 0.420 |
| 677 | `P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.436 | 0.330 | 0.413 |
| 678 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.447 | 0.330 | 0.423 |
| 679 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.426 | 0.330 | 0.454 |
| 680 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.670 | 0.032 | 0.638 | 0.564 | 0.330 | 0.624 |

## Size 3 Combos Sorted By Gain Over Best Single

| rank | combo | union@3 | gain | best_single | all_hit | neither | avg_pair_jaccard@3 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.479 | 0.277 | 0.469 |
| 2 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.489 | 0.277 | 0.474 |
| 3 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.521 | 0.277 | 0.477 |
| 4 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.521 | 0.277 | 0.478 |
| 5 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.543 | 0.277 | 0.496 |
| 6 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.085 | 0.638 | 0.521 | 0.277 | 0.496 |
| 7 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.085 | 0.628 | 0.479 | 0.287 | 0.523 |
| 8 | `2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.085 | 0.606 | 0.415 | 0.309 | 0.407 |
| 9 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.074 | 0.660 | 0.511 | 0.266 | 0.487 |
| 10 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.074 | 0.660 | 0.543 | 0.266 | 0.492 |
| 11 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.074 | 0.660 | 0.532 | 0.266 | 0.564 |
| 12 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.074 | 0.628 | 0.521 | 0.298 | 0.532 |
| 13 | `P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.074 | 0.617 | 0.489 | 0.309 | 0.541 |
| 14 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.415 | 0.255 | 0.367 |
| 15 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.521 | 0.255 | 0.470 |
| 16 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.521 | 0.255 | 0.478 |
| 17 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.521 | 0.255 | 0.485 |
| 18 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.074 | 0.670 | 0.511 | 0.255 | 0.510 |
| 19 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.532 | 0.255 | 0.519 |
| 20 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.543 | 0.255 | 0.523 |
| 21 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.543 | 0.255 | 0.528 |
| 22 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.564 | 0.255 | 0.537 |
| 23 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.074 | 0.670 | 0.553 | 0.255 | 0.548 |
| 24 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.394 | 0.287 | 0.364 |
| 25 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.415 | 0.287 | 0.373 |
| 26 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.426 | 0.287 | 0.391 |
| 27 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.543 | 0.287 | 0.497 |
| 28 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.511 | 0.287 | 0.511 |
| 29 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.521 | 0.287 | 0.512 |
| 30 | `1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.489 | 0.287 | 0.519 |
| 31 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.074 | 0.638 | 0.553 | 0.287 | 0.525 |
| 32 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.404 | 0.277 | 0.362 |
| 33 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.426 | 0.277 | 0.387 |
| 34 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.532 | 0.277 | 0.456 |
| 35 | `2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.521 | 0.277 | 0.464 |
| 36 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.532 | 0.277 | 0.491 |
| 37 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.543 | 0.277 | 0.495 |
| 38 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.564 | 0.277 | 0.495 |
| 39 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.543 | 0.277 | 0.498 |
| 40 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.553 | 0.277 | 0.503 |
| 41 | `2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.553 | 0.277 | 0.509 |
| 42 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.564 | 0.277 | 0.510 |
| 43 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.532 | 0.277 | 0.524 |
| 44 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.521 | 0.277 | 0.530 |
| 45 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.064 | 0.660 | 0.553 | 0.277 | 0.533 |
| 46 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.532 | 0.277 | 0.533 |
| 47 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.543 | 0.277 | 0.536 |
| 48 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.564 | 0.277 | 0.549 |
| 49 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.543 | 0.277 | 0.571 |
| 50 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.564 | 0.277 | 0.576 |
| 51 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.064 | 0.660 | 0.521 | 0.277 | 0.582 |
| 52 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.064 | 0.628 | 0.404 | 0.309 | 0.403 |
| 53 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.064 | 0.628 | 0.436 | 0.309 | 0.421 |
| 54 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.064 | 0.628 | 0.511 | 0.309 | 0.576 |
| 55 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.064 | 0.681 | 0.553 | 0.255 | 0.528 |
| 56 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.064 | 0.681 | 0.564 | 0.255 | 0.559 |
| 57 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.543 | 0.266 | 0.482 |
| 58 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.553 | 0.266 | 0.483 |
| 59 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.564 | 0.266 | 0.567 |
| 60 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.553 | 0.266 | 0.586 |
| 61 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.064 | 0.670 | 0.564 | 0.266 | 0.587 |
| 62 | `P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.415 | 0.298 | 0.371 |
| 63 | `1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.426 | 0.298 | 0.417 |
| 64 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.489 | 0.298 | 0.505 |
| 65 | `1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.521 | 0.298 | 0.511 |
| 66 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.521 | 0.298 | 0.512 |
| 67 | `1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.511 | 0.298 | 0.516 |
| 68 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.532 | 0.298 | 0.527 |
| 69 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.511 | 0.298 | 0.528 |
| 70 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.500 | 0.298 | 0.533 |
| 71 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.532 | 0.298 | 0.548 |
| 72 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.564 | 0.298 | 0.555 |
| 73 | `P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.521 | 0.298 | 0.557 |
| 74 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.574 | 0.298 | 0.559 |
| 75 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.064 | 0.638 | 0.521 | 0.298 | 0.575 |
| 76 | `P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.064 | 0.617 | 0.415 | 0.319 | 0.421 |
| 77 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.532 | 0.266 | 0.476 |
| 78 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.553 | 0.266 | 0.479 |
| 79 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.553 | 0.266 | 0.480 |
| 80 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.543 | 0.266 | 0.508 |
| 81 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.585 | 0.266 | 0.516 |
| 82 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.564 | 0.266 | 0.526 |
| 83 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.596 | 0.266 | 0.538 |
| 84 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.596 | 0.266 | 0.539 |
| 85 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.596 | 0.266 | 0.542 |
| 86 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.574 | 0.266 | 0.544 |
| 87 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.585 | 0.266 | 0.547 |
| 88 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.574 | 0.266 | 0.548 |
| 89 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.564 | 0.266 | 0.552 |
| 90 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.574 | 0.266 | 0.560 |
| 91 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.053 | 0.681 | 0.585 | 0.266 | 0.579 |
| 92 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.053 | 0.681 | 0.585 | 0.266 | 0.613 |
| 93 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.426 | 0.277 | 0.366 |
| 94 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.436 | 0.277 | 0.393 |
| 95 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.436 | 0.277 | 0.396 |
| 96 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.426 | 0.277 | 0.399 |
| 97 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.553 | 0.277 | 0.496 |
| 98 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.532 | 0.277 | 0.499 |
| 99 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.502 |
| 100 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.510 |
| 101 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.521 | 0.277 | 0.511 |
| 102 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.511 |
| 103 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.543 | 0.277 | 0.518 |
| 104 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.521 | 0.277 | 0.518 |
| 105 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.543 | 0.277 | 0.523 |
| 106 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.532 | 0.277 | 0.529 |
| 107 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.543 |
| 108 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.553 |
| 109 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.553 | 0.277 | 0.558 |
| 110 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.553 | 0.277 | 0.559 |
| 111 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.511 | 0.277 | 0.561 |
| 112 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.532 | 0.277 | 0.567 |
| 113 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.532 | 0.277 | 0.567 |
| 114 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.543 | 0.277 | 0.570 |
| 115 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.574 |
| 116 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.574 | 0.277 | 0.579 |
| 117 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.582 |
| 118 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.585 | 0.277 | 0.582 |
| 119 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.585 |
| 120 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.564 | 0.277 | 0.597 |
| 121 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.053 | 0.670 | 0.553 | 0.277 | 0.598 |
| 122 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.415 | 0.287 | 0.380 |
| 123 | `2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.415 | 0.287 | 0.408 |
| 124 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.553 | 0.287 | 0.506 |
| 125 | `2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.521 | 0.287 | 0.512 |
| 126 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.553 | 0.287 | 0.519 |
| 127 | `2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.511 | 0.287 | 0.524 |
| 128 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.511 | 0.287 | 0.534 |
| 129 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.053 | 0.660 | 0.564 | 0.287 | 0.537 |
| 130 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.553 | 0.287 | 0.541 |
| 131 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.511 | 0.287 | 0.544 |
| 132 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.564 | 0.287 | 0.556 |
| 133 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.053 | 0.660 | 0.564 | 0.287 | 0.559 |
| 134 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.053 | 0.660 | 0.553 | 0.287 | 0.585 |
| 135 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.574 | 0.287 | 0.595 |
| 136 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.053 | 0.660 | 0.532 | 0.287 | 0.609 |
| 137 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.404 | 0.309 | 0.386 |
| 138 | `1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.404 | 0.309 | 0.390 |
| 139 | `1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.426 | 0.309 | 0.390 |
| 140 | `1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.404 | 0.309 | 0.398 |
| 141 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.447 | 0.309 | 0.407 |
| 142 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.691 | 0.053 | 0.638 | 0.543 | 0.309 | 0.530 |
| 143 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.691 | 0.053 | 0.638 | 0.553 | 0.309 | 0.535 |
| 144 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.053 | 0.638 | 0.564 | 0.309 | 0.579 |
| 145 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.053 | 0.628 | 0.436 | 0.319 | 0.411 |
| 146 | `P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.053 | 0.617 | 0.436 | 0.330 | 0.420 |
| 147 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.447 | 0.255 | 0.363 |
| 148 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.543 | 0.255 | 0.471 |
| 149 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.574 | 0.255 | 0.472 |
| 150 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.511 | 0.255 | 0.475 |
| 151 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.564 | 0.255 | 0.483 |
| 152 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.543 | 0.255 | 0.501 |
| 153 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.585 | 0.255 | 0.506 |
| 154 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.574 | 0.255 | 0.513 |
| 155 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.585 | 0.255 | 0.515 |
| 156 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.585 | 0.255 | 0.515 |
| 157 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.532 | 0.255 | 0.516 |
| 158 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.606 | 0.255 | 0.525 |
| 159 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.574 | 0.255 | 0.539 |
| 160 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.585 | 0.255 | 0.540 |
| 161 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.053 | 0.691 | 0.532 | 0.255 | 0.544 |
| 162 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.596 | 0.255 | 0.552 |
| 163 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.606 | 0.255 | 0.552 |
| 164 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.596 | 0.255 | 0.575 |
| 165 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.053 | 0.691 | 0.596 | 0.255 | 0.592 |
| 166 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.415 | 0.277 | 0.372 |
| 167 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.426 | 0.277 | 0.380 |
| 168 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.447 | 0.277 | 0.394 |
| 169 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.436 | 0.277 | 0.402 |
| 170 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.482 |
| 171 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.553 | 0.277 | 0.495 |
| 172 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.497 |
| 173 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.532 | 0.277 | 0.501 |
| 174 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.532 | 0.277 | 0.504 |
| 175 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.521 | 0.277 | 0.506 |
| 176 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.509 |
| 177 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.512 |
| 178 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.553 | 0.277 | 0.519 |
| 179 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.519 |
| 180 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.522 |
| 181 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.523 |
| 182 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.528 |
| 183 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.553 | 0.277 | 0.529 |
| 184 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.529 |
| 185 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.532 |
| 186 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.538 |
| 187 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.532 | 0.277 | 0.540 |
| 188 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.544 |
| 189 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.563 |
| 190 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.563 |
| 191 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.565 |
| 192 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.572 |
| 193 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.577 |
| 194 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.579 |
| 195 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.543 | 0.277 | 0.582 |
| 196 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.564 | 0.277 | 0.583 |
| 197 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.617 | 0.277 | 0.590 |
| 198 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.543 | 0.277 | 0.591 |
| 199 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.598 |
| 200 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.628 | 0.277 | 0.599 |
| 201 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.602 |
| 202 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.574 | 0.277 | 0.610 |
| 203 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.610 |
| 204 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.617 | 0.277 | 0.615 |
| 205 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.616 |
| 206 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.618 |
| 207 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.627 |
| 208 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.629 |
| 209 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.631 |
| 210 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.634 |
| 211 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.606 | 0.277 | 0.637 |
| 212 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.596 | 0.277 | 0.670 |
| 213 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.043 | 0.681 | 0.585 | 0.277 | 0.672 |
| 214 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.436 | 0.298 | 0.380 |
| 215 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.426 | 0.298 | 0.394 |
| 216 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.415 | 0.298 | 0.398 |
| 217 | `2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.447 | 0.298 | 0.404 |
| 218 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.426 | 0.298 | 0.407 |
| 219 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.404 | 0.298 | 0.409 |
| 220 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.426 | 0.298 | 0.413 |
| 221 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.553 | 0.298 | 0.507 |
| 222 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.521 | 0.298 | 0.511 |
| 223 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.564 | 0.298 | 0.514 |
| 224 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.532 | 0.298 | 0.530 |
| 225 | `2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.489 | 0.298 | 0.534 |
| 226 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.532 | 0.298 | 0.543 |
| 227 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.553 | 0.298 | 0.556 |
| 228 | `1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.532 | 0.298 | 0.562 |
| 229 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.574 | 0.298 | 0.591 |
| 230 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.043 | 0.660 | 0.532 | 0.298 | 0.592 |
| 231 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.043 | 0.660 | 0.564 | 0.298 | 0.613 |
| 232 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.457 | 0.255 | 0.376 |
| 233 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.543 | 0.255 | 0.483 |
| 234 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.485 |
| 235 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.574 | 0.255 | 0.485 |
| 236 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.543 | 0.255 | 0.485 |
| 237 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.553 | 0.255 | 0.493 |
| 238 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.503 |
| 239 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.511 |
| 240 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.574 | 0.255 | 0.517 |
| 241 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.518 |
| 242 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.527 |
| 243 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.528 |
| 244 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.529 |
| 245 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.564 | 0.255 | 0.534 |
| 246 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.543 | 0.255 | 0.536 |
| 247 | `1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.537 |
| 248 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.539 |
| 249 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.544 |
| 250 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.547 |
| 251 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.628 | 0.255 | 0.550 |
| 252 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.550 |
| 253 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.551 |
| 254 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.554 |
| 255 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.555 |
| 256 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.574 | 0.255 | 0.559 |
| 257 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.628 | 0.255 | 0.560 |
| 258 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.565 |
| 259 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.617 | 0.255 | 0.567 |
| 260 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.553 | 0.255 | 0.568 |
| 261 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.570 |
| 262 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.580 |
| 263 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.628 | 0.255 | 0.584 |
| 264 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.596 | 0.255 | 0.587 |
| 265 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.745 | 0.043 | 0.702 | 0.617 | 0.255 | 0.590 |
| 266 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.606 | 0.255 | 0.592 |
| 267 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.594 |
| 268 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.617 | 0.255 | 0.595 |
| 269 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.574 | 0.255 | 0.600 |
| 270 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.585 | 0.255 | 0.611 |
| 271 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.745 | 0.043 | 0.702 | 0.617 | 0.255 | 0.617 |
| 272 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.426 | 0.266 | 0.357 |
| 273 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.447 | 0.266 | 0.374 |
| 274 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.468 | 0.266 | 0.401 |
| 275 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.511 | 0.266 | 0.452 |
| 276 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.532 | 0.266 | 0.459 |
| 277 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.482 |
| 278 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.543 | 0.266 | 0.482 |
| 279 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.489 | 0.266 | 0.484 |
| 280 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.532 | 0.266 | 0.485 |
| 281 | `2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.511 | 0.266 | 0.487 |
| 282 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.543 | 0.266 | 0.489 |
| 283 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.490 |
| 284 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.499 |
| 285 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.500 |
| 286 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.574 | 0.266 | 0.504 |
| 287 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.507 |
| 288 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.574 | 0.266 | 0.512 |
| 289 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.523 |
| 290 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.521 | 0.266 | 0.524 |
| 291 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.528 |
| 292 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.530 |
| 293 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.532 | 0.266 | 0.531 |
| 294 | `2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.531 |
| 295 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.537 |
| 296 | `2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.538 |
| 297 | `1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.539 |
| 298 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.532 | 0.266 | 0.543 |
| 299 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.521 | 0.266 | 0.550 |
| 300 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.543 | 0.266 | 0.554 |
| 301 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.555 |
| 302 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.585 | 0.266 | 0.555 |
| 303 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.555 |
| 304 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.563 |
| 305 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.606 | 0.266 | 0.565 |
| 306 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.617 | 0.266 | 0.567 |
| 307 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.564 | 0.266 | 0.572 |
| 308 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.617 | 0.266 | 0.579 |
| 309 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.582 |
| 310 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.596 | 0.266 | 0.584 |
| 311 | `1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.043 | 0.691 | 0.553 | 0.266 | 0.587 |
| 312 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.606 | 0.266 | 0.602 |
| 313 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.043 | 0.691 | 0.574 | 0.266 | 0.604 |
| 314 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.447 | 0.287 | 0.380 |
| 315 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.436 | 0.287 | 0.398 |
| 316 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.436 | 0.287 | 0.416 |
| 317 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.553 | 0.287 | 0.498 |
| 318 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.043 | 0.670 | 0.574 | 0.287 | 0.508 |
| 319 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.543 | 0.287 | 0.520 |
| 320 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.521 |
| 321 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.564 | 0.287 | 0.525 |
| 322 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.511 | 0.287 | 0.527 |
| 323 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.543 | 0.287 | 0.528 |
| 324 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.043 | 0.670 | 0.574 | 0.287 | 0.528 |
| 325 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.564 | 0.287 | 0.531 |
| 326 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.553 | 0.287 | 0.540 |
| 327 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.546 |
| 328 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.553 | 0.287 | 0.556 |
| 329 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.567 |
| 330 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.578 |
| 331 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.596 | 0.287 | 0.582 |
| 332 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.043 | 0.670 | 0.585 | 0.287 | 0.596 |
| 333 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.532 | 0.287 | 0.612 |
| 334 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.553 | 0.287 | 0.621 |
| 335 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.713 | 0.043 | 0.670 | 0.606 | 0.287 | 0.653 |
| 336 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.415 | 0.319 | 0.406 |
| 337 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.436 | 0.319 | 0.427 |
| 338 | `P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.532 | 0.319 | 0.533 |
| 339 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.532 | 0.319 | 0.591 |
| 340 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.681 | 0.043 | 0.638 | 0.574 | 0.319 | 0.597 |
| 341 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.681 | 0.043 | 0.638 | 0.521 | 0.319 | 0.600 |
| 342 | `2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.436 | 0.309 | 0.384 |
| 343 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.426 | 0.309 | 0.416 |
| 344 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.436 | 0.309 | 0.424 |
| 345 | `2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.553 | 0.309 | 0.500 |
| 346 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.543 | 0.309 | 0.542 |
| 347 | `P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.564 | 0.309 | 0.544 |
| 348 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.691 | 0.032 | 0.660 | 0.574 | 0.309 | 0.595 |
| 349 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.426 | 0.266 | 0.370 |
| 350 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.426 | 0.266 | 0.382 |
| 351 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.436 | 0.266 | 0.397 |
| 352 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.447 | 0.266 | 0.401 |
| 353 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.468 | 0.266 | 0.407 |
| 354 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.447 | 0.266 | 0.427 |
| 355 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.457 | 0.266 | 0.429 |
| 356 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.532 | 0.266 | 0.510 |
| 357 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.515 |
| 358 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.518 |
| 359 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.522 |
| 360 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.529 |
| 361 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.529 |
| 362 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.530 |
| 363 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.530 |
| 364 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.531 |
| 365 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.531 |
| 366 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.521 | 0.266 | 0.531 |
| 367 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.532 |
| 368 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.534 |
| 369 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.536 |
| 370 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.536 |
| 371 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.538 |
| 372 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.541 |
| 373 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.546 |
| 374 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.546 |
| 375 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.550 |
| 376 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.551 |
| 377 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.551 |
| 378 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.556 |
| 379 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.556 |
| 380 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.558 |
| 381 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.558 |
| 382 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.561 |
| 383 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.563 |
| 384 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.563 |
| 385 | `1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.565 |
| 386 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.567 |
| 387 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.568 |
| 388 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.572 |
| 389 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.576 |
| 390 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.578 |
| 391 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.580 |
| 392 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.580 |
| 393 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.582 |
| 394 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.553 | 0.266 | 0.586 |
| 395 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.588 |
| 396 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.590 |
| 397 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.592 |
| 398 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.592 |
| 399 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.600 |
| 400 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.600 |
| 401 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.603 |
| 402 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.604 |
| 403 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.604 |
| 404 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.609 |
| 405 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.612 |
| 406 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.613 |
| 407 | `1-1_CN|layer29|last|centered_cosine + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.574 | 0.266 | 0.619 |
| 408 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.619 |
| 409 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.553 | 0.266 | 0.621 |
| 410 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.564 | 0.266 | 0.622 |
| 411 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.649 | 0.266 | 0.622 |
| 412 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.623 |
| 413 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.624 |
| 414 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.625 |
| 415 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.627 |
| 416 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.543 | 0.266 | 0.629 |
| 417 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.638 | 0.266 | 0.632 |
| 418 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.606 | 0.266 | 0.633 |
| 419 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.635 |
| 420 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.638 |
| 421 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.644 |
| 422 | `P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.585 | 0.266 | 0.645 |
| 423 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.638 | 0.266 | 0.655 |
| 424 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.659 |
| 425 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.661 |
| 426 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.663 |
| 427 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.628 | 0.266 | 0.670 |
| 428 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.596 | 0.266 | 0.671 |
| 429 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.649 | 0.266 | 0.685 |
| 430 | `2-1|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.734 | 0.032 | 0.702 | 0.617 | 0.266 | 0.687 |
| 431 | `2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.457 | 0.277 | 0.366 |
| 432 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.415 | 0.277 | 0.375 |
| 433 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.457 | 0.277 | 0.375 |
| 434 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.457 | 0.277 | 0.386 |
| 435 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.436 | 0.277 | 0.390 |
| 436 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.447 | 0.277 | 0.390 |
| 437 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.457 | 0.277 | 0.391 |
| 438 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.447 | 0.277 | 0.399 |
| 439 | `2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.543 | 0.277 | 0.474 |
| 440 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.521 | 0.277 | 0.492 |
| 441 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.574 | 0.277 | 0.494 |
| 442 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.495 |
| 443 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.498 |
| 444 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.511 | 0.277 | 0.500 |
| 445 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.521 | 0.277 | 0.500 |
| 446 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.564 | 0.277 | 0.502 |
| 447 | `2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.505 |
| 448 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.506 |
| 449 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.517 |
| 450 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.522 |
| 451 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.564 | 0.277 | 0.525 |
| 452 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.526 |
| 453 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.553 | 0.277 | 0.535 |
| 454 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.538 |
| 455 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.574 | 0.277 | 0.548 |
| 456 | `1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.574 | 0.277 | 0.555 |
| 457 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.564 | 0.277 | 0.563 |
| 458 | `P0|layer30|last|anti_pca_both_k15 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.032 | 0.691 | 0.564 | 0.277 | 0.563 |
| 459 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.032 | 0.691 | 0.585 | 0.277 | 0.582 |
| 460 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.436 | 0.287 | 0.372 |
| 461 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.426 | 0.287 | 0.383 |
| 462 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.436 | 0.287 | 0.385 |
| 463 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.404 | 0.287 | 0.390 |
| 464 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.426 | 0.287 | 0.391 |
| 465 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.436 | 0.287 | 0.394 |
| 466 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.426 | 0.287 | 0.405 |
| 467 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.447 | 0.287 | 0.414 |
| 468 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.447 | 0.287 | 0.435 |
| 469 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.457 | 0.287 | 0.441 |
| 470 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.447 | 0.287 | 0.445 |
| 471 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.489 |
| 472 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.489 | 0.287 | 0.508 |
| 473 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.511 | 0.287 | 0.509 |
| 474 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.516 |
| 475 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.519 |
| 476 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.528 |
| 477 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.530 |
| 478 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.540 |
| 479 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.542 |
| 480 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.521 | 0.287 | 0.543 |
| 481 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.544 |
| 482 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.550 |
| 483 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.532 | 0.287 | 0.557 |
| 484 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.557 |
| 485 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.563 |
| 486 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.563 |
| 487 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.564 | 0.287 | 0.564 |
| 488 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.565 |
| 489 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.567 |
| 490 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.568 |
| 491 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.564 | 0.287 | 0.571 |
| 492 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.543 | 0.287 | 0.572 |
| 493 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.581 |
| 494 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.583 |
| 495 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.585 |
| 496 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.588 |
| 497 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.594 |
| 498 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.617 | 0.287 | 0.599 |
| 499 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.605 |
| 500 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.615 |
| 501 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.564 | 0.287 | 0.616 |
| 502 | `1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.628 |
| 503 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.596 | 0.287 | 0.635 |
| 504 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.606 | 0.287 | 0.643 |
| 505 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.585 | 0.287 | 0.646 |
| 506 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.564 | 0.287 | 0.653 |
| 507 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.617 | 0.287 | 0.653 |
| 508 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.617 | 0.287 | 0.660 |
| 509 | `2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.553 | 0.287 | 0.663 |
| 510 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.032 | 0.681 | 0.574 | 0.287 | 0.668 |
| 511 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.436 | 0.298 | 0.388 |
| 512 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.447 | 0.298 | 0.396 |
| 513 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.415 | 0.298 | 0.405 |
| 514 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.436 | 0.298 | 0.418 |
| 515 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.447 | 0.298 | 0.425 |
| 516 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.500 | 0.298 | 0.523 |
| 517 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.574 | 0.298 | 0.525 |
| 518 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.511 | 0.298 | 0.528 |
| 519 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.564 | 0.298 | 0.531 |
| 520 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.532 | 0.298 | 0.537 |
| 521 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.532 | 0.298 | 0.538 |
| 522 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.574 | 0.298 | 0.545 |
| 523 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.553 | 0.298 | 0.545 |
| 524 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.564 | 0.298 | 0.554 |
| 525 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.532 | 0.298 | 0.554 |
| 526 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.564 | 0.298 | 0.562 |
| 527 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.032 | 0.670 | 0.574 | 0.298 | 0.566 |
| 528 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.585 | 0.298 | 0.568 |
| 529 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.585 | 0.298 | 0.570 |
| 530 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.702 | 0.032 | 0.670 | 0.596 | 0.298 | 0.578 |
| 531 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.553 | 0.298 | 0.604 |
| 532 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.521 | 0.298 | 0.605 |
| 533 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.553 | 0.298 | 0.611 |
| 534 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.574 | 0.298 | 0.622 |
| 535 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.702 | 0.032 | 0.670 | 0.585 | 0.298 | 0.622 |
| 536 | `P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.436 | 0.330 | 0.413 |
| 537 | `1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.447 | 0.330 | 0.423 |
| 538 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.670 | 0.032 | 0.638 | 0.426 | 0.330 | 0.454 |
| 539 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.670 | 0.032 | 0.638 | 0.564 | 0.330 | 0.624 |
| 540 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.436 | 0.277 | 0.402 |
| 541 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.403 |
| 542 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.415 | 0.277 | 0.405 |
| 543 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.436 | 0.277 | 0.410 |
| 544 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.411 |
| 545 | `1-3|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.412 |
| 546 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.413 |
| 547 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.413 |
| 548 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.457 | 0.277 | 0.425 |
| 549 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.457 | 0.277 | 0.435 |
| 550 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.447 | 0.277 | 0.445 |
| 551 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.457 | 0.277 | 0.448 |
| 552 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.457 | 0.277 | 0.453 |
| 553 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.525 |
| 554 | `1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.500 | 0.277 | 0.533 |
| 555 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.535 |
| 556 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.537 |
| 557 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.539 |
| 558 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.541 |
| 559 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-4-1|layer30|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.544 |
| 560 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.511 | 0.277 | 0.544 |
| 561 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.544 |
| 562 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.545 |
| 563 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.521 | 0.277 | 0.557 |
| 564 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.532 | 0.277 | 0.557 |
| 565 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.596 | 0.277 | 0.560 |
| 566 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.560 |
| 567 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.564 |
| 568 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.565 |
| 569 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.565 |
| 570 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.566 |
| 571 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.567 |
| 572 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.567 |
| 573 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.568 |
| 574 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.532 | 0.277 | 0.568 |
| 575 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.570 |
| 576 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.580 |
| 577 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.596 | 0.277 | 0.580 |
| 578 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.543 | 0.277 | 0.584 |
| 579 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.585 |
| 580 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.521 | 0.277 | 0.585 |
| 581 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.586 |
| 582 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.586 |
| 583 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.587 |
| 584 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.588 |
| 585 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.593 |
| 586 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.596 |
| 587 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.599 |
| 588 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.601 |
| 589 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.603 |
| 590 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.604 |
| 591 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.628 | 0.277 | 0.611 |
| 592 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.612 |
| 593 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.617 |
| 594 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.564 | 0.277 | 0.620 |
| 595 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.596 | 0.277 | 0.621 |
| 596 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.628 | 0.277 | 0.622 |
| 597 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.626 |
| 598 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.632 |
| 599 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.634 |
| 600 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.638 | 0.277 | 0.644 |
| 601 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.628 | 0.277 | 0.644 |
| 602 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.645 |
| 603 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.649 | 0.277 | 0.646 |
| 604 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-6|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.596 | 0.277 | 0.646 |
| 605 | `1-1_CN|layer29|last|centered_cosine + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.646 |
| 606 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.553 | 0.277 | 0.648 |
| 607 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.638 | 0.277 | 0.656 |
| 608 | `1-3|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.574 | 0.277 | 0.656 |
| 609 | `1-3|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.663 |
| 610 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.667 |
| 611 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.638 | 0.277 | 0.669 |
| 612 | `P0|layer30|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.585 | 0.277 | 0.671 |
| 613 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.617 | 0.277 | 0.683 |
| 614 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.606 | 0.277 | 0.688 |
| 615 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.723 | 0.021 | 0.702 | 0.628 | 0.277 | 0.706 |
| 616 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.436 | 0.298 | 0.409 |
| 617 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.457 | 0.298 | 0.424 |
| 618 | `1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.457 | 0.298 | 0.434 |
| 619 | `1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.564 | 0.298 | 0.550 |
| 620 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.021 | 0.681 | 0.564 | 0.298 | 0.557 |
| 621 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.574 |
| 622 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.575 |
| 623 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.577 |
| 624 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.578 |
| 625 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.511 | 0.298 | 0.581 |
| 626 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.606 | 0.298 | 0.582 |
| 627 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.532 | 0.298 | 0.585 |
| 628 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.543 | 0.298 | 0.595 |
| 629 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.585 | 0.298 | 0.616 |
| 630 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.574 | 0.298 | 0.626 |
| 631 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.574 | 0.298 | 0.629 |
| 632 | `P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15` | 0.702 | 0.021 | 0.681 | 0.596 | 0.298 | 0.659 |
| 633 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.415 | 0.309 | 0.397 |
| 634 | `2-3-2_query|layer29|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.447 | 0.309 | 0.399 |
| 635 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.447 | 0.309 | 0.401 |
| 636 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.447 | 0.309 | 0.413 |
| 637 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.447 | 0.309 | 0.414 |
| 638 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.436 | 0.309 | 0.425 |
| 639 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.543 | 0.309 | 0.545 |
| 640 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.691 | 0.021 | 0.670 | 0.585 | 0.309 | 0.588 |
| 641 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.021 | 0.670 | 0.543 | 0.309 | 0.589 |
| 642 | `2-6|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.021 | 0.660 | 0.436 | 0.319 | 0.419 |
| 643 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 2-5|layer29|last|query_only_anti_pca_k2 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.021 | 0.691 | 0.447 | 0.287 | 0.383 |
| 644 | `1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.457 | 0.309 | 0.418 |
| 645 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.447 | 0.309 | 0.430 |
| 646 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.436 | 0.309 | 0.439 |
| 647 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.447 | 0.309 | 0.462 |
| 648 | `1-2|layer29|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.532 | 0.309 | 0.588 |
| 649 | `1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.532 | 0.309 | 0.621 |
| 650 | `1-1_CN|layer29|last|centered_cosine + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.553 | 0.309 | 0.629 |
| 651 | `1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2 + 1-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.596 | 0.309 | 0.654 |
| 652 | `P0|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.691 | 0.011 | 0.681 | 0.543 | 0.309 | 0.671 |
| 653 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.457 | 0.287 | 0.404 |
| 654 | `1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.436 | 0.287 | 0.411 |
| 655 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.457 | 0.287 | 0.414 |
| 656 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.447 | 0.287 | 0.419 |
| 657 | `2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.415 | 0.287 | 0.426 |
| 658 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.447 | 0.287 | 0.436 |
| 659 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.468 | 0.287 | 0.462 |
| 660 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.564 | 0.287 | 0.522 |
| 661 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-7|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.553 | 0.287 | 0.565 |
| 662 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.011 | 0.702 | 0.606 | 0.287 | 0.575 |
| 663 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.713 | 0.011 | 0.702 | 0.617 | 0.287 | 0.576 |
| 664 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-1_EN|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.585 | 0.287 | 0.593 |
| 665 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.011 | 0.702 | 0.574 | 0.287 | 0.594 |
| 666 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.564 | 0.287 | 0.595 |
| 667 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.564 | 0.287 | 0.601 |
| 668 | `1-3|layer31|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine + 1-1_CN_ASCII|layer29|last|query_only_anti_pca_k2` | 0.713 | 0.011 | 0.702 | 0.596 | 0.287 | 0.607 |
| 669 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 1-1_CN|layer29|last|centered_cosine` | 0.713 | 0.011 | 0.702 | 0.596 | 0.287 | 0.613 |
| 670 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.543 | 0.287 | 0.619 |
| 671 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.638 | 0.287 | 0.623 |
| 672 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.628 | 0.287 | 0.625 |
| 673 | `1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15 + 2-1|layer30|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.585 | 0.287 | 0.629 |
| 674 | `2-3-2_mem|layer31|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.606 | 0.287 | 0.635 |
| 675 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.543 | 0.287 | 0.638 |
| 676 | `2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.574 | 0.287 | 0.680 |
| 677 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 1-2|layer29|last|anti_pca_both_k15` | 0.713 | 0.011 | 0.702 | 0.606 | 0.287 | 0.701 |
| 678 | `P0|layer30|last|anti_pca_both_k15 + 2-3-1|layer30|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.447 | 0.298 | 0.446 |
| 679 | `2-4-1_user_word|layer30|last|anti_pca_both_k15 + 1-3|layer31|last|anti_pca_both_k15 + P0|layer30|last|anti_pca_both_k15` | 0.702 | 0.000 | 0.702 | 0.606 | 0.298 | 0.632 |
| 680 | `1-2|layer29|last|anti_pca_both_k15 + 2-4-2|layer29|last|anti_pca_both_k15 + 2-8|layer31|last|anti_pca_both_k15` | 0.681 | 0.000 | 0.681 | 0.415 | 0.319 | 0.449 |
