# Stage 3 Sparse Logits Fusion Probe

- Created UTC: `2026-05-12T03:15:43.263934+00:00`
- Dump: `/Users/gordonxiong/Desktop/Repos/memory_state/tensors/stage3/prompt_sweep/merged_subset0-100_cache2gb_logits256`
- Reference: [PromptReps](https://arxiv.org/abs/2404.18424)

| rank | cell | method | alpha | R@5 | NDCG@5 | MRR |
|---:|---|---|---:|---:|---:|---:|
| 1 | `1-3@L31` | `dense_plus_idf_overlap` | 0.50 | 0.766 | 0.778 | 0.799 |
| 2 | `1-3@L31` | `dense_plus_overlap` | 0.50 | 0.766 | 0.761 | 0.784 |
| 3 | `2-3-2_mem@L31` | `dense_only` | 1.00 | 0.766 | 0.757 | 0.780 |
| 4 | `1-3@L31` | `dense_plus_idf_weighted_dot` | 0.75 | 0.755 | 0.791 | 0.814 |
| 5 | `1-3@L31` | `dense_plus_overlap` | 0.75 | 0.755 | 0.788 | 0.821 |
| 6 | `1-3@L31` | `dense_plus_overlap` | 0.90 | 0.755 | 0.788 | 0.813 |
| 7 | `1-3@L31` | `dense_plus_idf_weighted_dot` | 0.90 | 0.755 | 0.788 | 0.812 |
| 8 | `1-3@L31` | `dense_plus_idf_overlap` | 0.75 | 0.755 | 0.787 | 0.812 |
| 9 | `1-3@L31` | `dense_plus_weighted_dot` | 0.90 | 0.755 | 0.787 | 0.811 |
| 10 | `1-3@L31` | `dense_plus_weighted_dot` | 0.75 | 0.755 | 0.787 | 0.813 |
| 11 | `1-3@L31` | `dense_only` | 1.00 | 0.755 | 0.784 | 0.805 |
| 12 | `1-3@L31` | `dense_plus_idf_overlap` | 0.90 | 0.755 | 0.783 | 0.802 |
| 13 | `2-3-2_mem@L31` | `dense_plus_idf_weighted_dot` | 0.90 | 0.755 | 0.766 | 0.807 |
| 14 | `2-3-2_mem@L31` | `dense_plus_weighted_dot` | 0.90 | 0.755 | 0.763 | 0.795 |
| 15 | `1-3@L31` | `dense_plus_idf_overlap` | 0.25 | 0.755 | 0.743 | 0.754 |
| 16 | `2-3-2_mem@L31` | `dense_plus_overlap` | 0.75 | 0.745 | 0.767 | 0.802 |
| 17 | `2-3-1@L30` | `dense_only` | 1.00 | 0.745 | 0.762 | 0.795 |
| 18 | `2-3-2_mem@L31` | `dense_plus_overlap` | 0.90 | 0.745 | 0.762 | 0.799 |
| 19 | `2-3-2_mem@L31` | `dense_plus_idf_overlap` | 0.75 | 0.745 | 0.761 | 0.797 |
| 20 | `2-3-1@L30` | `dense_plus_weighted_dot` | 0.90 | 0.745 | 0.761 | 0.794 |
| 21 | `2-3-1@L30` | `dense_plus_idf_overlap` | 0.90 | 0.745 | 0.761 | 0.788 |
| 22 | `2-3-1@L30` | `dense_plus_overlap` | 0.90 | 0.745 | 0.758 | 0.789 |
| 23 | `2-3-2_mem@L31` | `dense_plus_idf_overlap` | 0.50 | 0.745 | 0.758 | 0.788 |
| 24 | `2-3-2_mem@L31` | `dense_plus_weighted_dot` | 0.75 | 0.745 | 0.757 | 0.789 |
| 25 | `2-3-2_mem@L31` | `dense_plus_idf_overlap` | 0.90 | 0.745 | 0.754 | 0.788 |
| 26 | `2-3-1@L30` | `dense_plus_idf_weighted_dot` | 0.90 | 0.745 | 0.753 | 0.781 |
| 27 | `2-3-1@L30` | `dense_plus_weighted_dot` | 0.75 | 0.745 | 0.751 | 0.777 |
| 28 | `2-3-1@L30` | `dense_plus_overlap` | 0.75 | 0.745 | 0.748 | 0.778 |
| 29 | `2-3-2_mem@L31` | `dense_plus_idf_weighted_dot` | 0.75 | 0.745 | 0.748 | 0.770 |
| 30 | `2-3-1@L30` | `dense_plus_idf_weighted_dot` | 0.75 | 0.745 | 0.743 | 0.763 |
| 31 | `2-3-2_mem@L31` | `dense_plus_weighted_dot` | 0.50 | 0.745 | 0.740 | 0.757 |
| 32 | `1-3@L31` | `dense_plus_overlap` | 0.25 | 0.745 | 0.692 | 0.695 |
| 33 | `2-3-2_mem@L31` | `dense_plus_overlap` | 0.50 | 0.734 | 0.757 | 0.791 |
| 34 | `2-3-1@L30` | `dense_plus_idf_overlap` | 0.75 | 0.734 | 0.748 | 0.774 |
| 35 | `2-3-1@L30` | `dense_plus_weighted_dot` | 0.50 | 0.734 | 0.743 | 0.774 |
| 36 | `2-3-1@L30` | `dense_plus_idf_weighted_dot` | 0.50 | 0.734 | 0.740 | 0.771 |
| 37 | `2-3-1@L30` | `dense_plus_idf_overlap` | 0.50 | 0.734 | 0.735 | 0.755 |
| 38 | `1-3@L31` | `dense_plus_idf_weighted_dot` | 0.50 | 0.734 | 0.730 | 0.751 |
| 39 | `2-3-2_mem@L31` | `dense_plus_idf_weighted_dot` | 0.50 | 0.734 | 0.705 | 0.705 |
| 40 | `2-3-2_mem@L31` | `dense_plus_overlap` | 0.25 | 0.723 | 0.752 | 0.778 |
| 41 | `2-3-2_mem@L31` | `dense_plus_idf_overlap` | 0.25 | 0.723 | 0.750 | 0.775 |
| 42 | `2-3-1@L30` | `dense_plus_overlap` | 0.50 | 0.723 | 0.721 | 0.759 |
| 43 | `1-3@L31` | `dense_plus_weighted_dot` | 0.50 | 0.713 | 0.697 | 0.720 |
| 44 | `2-3-1@L30` | `dense_plus_overlap` | 0.25 | 0.713 | 0.690 | 0.714 |
| 45 | `2-3-2_mem@L31` | `logits_idf_overlap` | 0.00 | 0.702 | 0.726 | 0.759 |
| 46 | `2-3-2_mem@L31` | `dense_plus_idf_weighted_dot` | 0.25 | 0.702 | 0.645 | 0.636 |
| 47 | `2-3-1@L30` | `dense_plus_idf_overlap` | 0.25 | 0.691 | 0.697 | 0.729 |
| 48 | `2-3-2_mem@L31` | `logits_overlap` | 0.00 | 0.681 | 0.707 | 0.740 |
| 49 | `1-3@L31` | `logits_idf_overlap` | 0.00 | 0.681 | 0.658 | 0.672 |
| 50 | `2-3-1@L30` | `logits_idf_overlap` | 0.00 | 0.660 | 0.675 | 0.717 |
| 51 | `2-3-1@L30` | `logits_overlap` | 0.00 | 0.660 | 0.622 | 0.642 |
| 52 | `2-3-1@L30` | `dense_plus_idf_weighted_dot` | 0.25 | 0.649 | 0.653 | 0.670 |
| 53 | `2-3-2_mem@L31` | `dense_plus_weighted_dot` | 0.25 | 0.606 | 0.587 | 0.617 |
| 54 | `1-3@L31` | `dense_plus_idf_weighted_dot` | 0.25 | 0.596 | 0.568 | 0.593 |
| 55 | `2-3-1@L30` | `dense_plus_weighted_dot` | 0.25 | 0.564 | 0.564 | 0.602 |
| 56 | `1-3@L31` | `logits_overlap` | 0.00 | 0.553 | 0.500 | 0.523 |
| 57 | `2-3-2_mem@L31` | `logits_idf_weighted_dot` | 0.00 | 0.511 | 0.471 | 0.490 |
| 58 | `1-3@L31` | `dense_plus_weighted_dot` | 0.25 | 0.426 | 0.366 | 0.393 |
| 59 | `1-3@L31` | `logits_idf_weighted_dot` | 0.00 | 0.362 | 0.311 | 0.334 |
| 60 | `2-3-1@L30` | `logits_idf_weighted_dot` | 0.00 | 0.330 | 0.315 | 0.355 |
| 61 | `2-3-2_mem@L31` | `logits_weighted_dot` | 0.00 | 0.266 | 0.217 | 0.234 |
| 62 | `1-3@L31` | `logits_weighted_dot` | 0.00 | 0.117 | 0.084 | 0.104 |
| 63 | `2-3-1@L30` | `logits_weighted_dot` | 0.00 | 0.074 | 0.095 | 0.126 |
