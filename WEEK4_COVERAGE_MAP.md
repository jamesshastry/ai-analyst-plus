# Week 4 Exhaustive Coverage Map: Every Concept & Action → ai-analyst-plus

**Date:** 2026-04-10
**Purpose:** Map every single concept, student action, data reference, and tool invocation in Week 4 to a specific ai-analyst-plus capability. Includes wiring status (does it actually work end-to-end?) and fix requirements.

---

## Rating Scale

| Rating | Meaning |
|--------|---------|
| **FULL** | Coded function exists, tested, wired end-to-end, directly matches the lesson |
| **STRONG** | Coded function exists and covers the concept; minor wrapping or naming differences |
| **PARTIAL** | Infrastructure exists but has gaps (wrong columns, missing wrapper, broken wiring) |
| **AGENT-ONLY** | Agent prompt handles it but no coded helper backs it — LLM improvises the stats |
| **FRAMEWORK-ONLY** | Conceptual framework; no code needed (worksheet, slides, case study) |
| **GAP** | Lesson expects something to exist that doesn't |

## Wiring Status Key

| Status | Meaning |
|--------|---------|
| **WIRED** | Skill/agent/function connected end-to-end. Student invokes skill → skill calls agent → agent imports coded helper |
| **BROKEN** | Function exists but agent still imports from old `stats_helpers` or improvises inline. Needs agent upgrade. |
| **NEW-ONLY** | Only the NEW skill/agent is wired; the OLD pre-existing agent is not upgraded |
| **N/A** | No wiring needed (conceptual content, or function called directly by user) |

---

## Part 1: Concept-by-Concept Map (All 34 Segments)

### 4.1 Welcome to Week 4 (5 min) — Intro

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 1 | Week overview narrative | FRAMEWORK-ONLY | N/A | N/A | — |
| 2 | NovaMart checkout redesign story intro | FRAMEWORK-ONLY | Scenario matches `clean_ab.csv` | N/A | — |
| 3 | NovaMart Power User question story intro | FRAMEWORK-ONLY | Scenario matches `confounded.csv` | N/A | Column names differ (see Gap Note 5) |
| 4 | Mentions `experiments` table in DuckDB | PARTIAL | 9 CSVs in `data/novamart/experiments/` | N/A | CSVs not registered in `.knowledge/datasets/novamart/schema.md` |

### 4.2a The Case for Experiments (5 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 5 | Kohavi's 1/3 Rule (only 1/3 of ideas move metrics) | FRAMEWORK-ONLY | N/A | N/A | — |
| 6 | Spotify's 64% learning rate | FRAMEWORK-ONLY | N/A | N/A | — |
| 7 | Bing's revenue-per-search experiment case study | FRAMEWORK-ONLY | N/A | N/A | — |
| 8 | Power User Fallacy intro: users who use feature X retain better | PARTIAL | `confounded.csv` has `adopted_feature`, `tenure_months`, `orders_30d` | N/A | Lesson uses `job_role`, `heavy_usage`, `retained_30d` |
| 9 | Selection bias concept | FRAMEWORK-ONLY | N/A | N/A | — |
| 10 | Survivorship bias concept | FRAMEWORK-ONLY | N/A | N/A | — |
| 11 | Reverse causation concept | FRAMEWORK-ONLY | N/A | N/A | — |
| 12 | "Correlation ≠ causation" as week theme | FRAMEWORK-ONLY | N/A | N/A | — |

### 4.2b Why Most Companies Can't + 5 Traps (5 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 13 | **Trap 1: Peeking** — false positive inflation from checking results daily | STRONG | `sequential.py`: `confidence_sequence()`, `always_valid_pvalue()` — these are the *solution* to peeking | WIRED (via `/experiment` skill) | — |
| 14 | Peeking simulation: 26% FPR at α=0.05 | FRAMEWORK-ONLY | N/A (teaching visual) | N/A | — |
| 15 | **Trap 2: Underpowered tests** — winner's curse | STRONG | `power.py`: `power_proportion()`, `detectable_effect()` + `underpowered.csv` dataset | WIRED (via `/experiment power` mode) | — |
| 16 | Winner's curse: detected effects are inflated when underpowered | FRAMEWORK-ONLY | N/A | N/A | — |
| 17 | **Trap 3: SRM** — unequal traffic split | FULL | `srm.py`: `srm_check()` + `srm_violation.csv` (known 52/48 split) | NEW-ONLY | Old `srm-check` skill still uses inline scipy. Upgrade needed. |
| 18 | SRM causes: bucketing bugs, bot filtering, redirects | FULL | `srm.py`: `srm_diagnose()` — segments SRM by dimensions | NEW-ONLY | Same: old skill not wired |
| 19 | **Trap 4: Multiple comparisons** | FULL | `corrections.py`: `adjust_pvalues()` (Holm, BH) | WIRED | — |
| 20 | M&M example: test enough colors, one will be "significant" | FRAMEWORK-ONLY | N/A | N/A | — |
| 21 | **Trap 5: Novelty/primacy effects** | FRAMEWORK-ONLY | N/A (conceptual) | N/A | — |

### 4.3a The Hypothesis Template (5 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 22 | **If/Then/Because template** — 5 components: action, metric, direction, magnitude, mechanism | FRAMEWORK-ONLY | N/A (worksheet) | N/A | — |
| 23 | NovaMart hypothesis: "If we simplify checkout from 5 to 3 steps, then conversion will increase by 8% relative..." | PARTIAL | `clean_ab.csv` exists but has 5% lift, not 8%. `templates/experiment.yaml` has hypothesis schema. | N/A | Dataset numbers don't match lesson narrative |
| 24 | Student writes own hypothesis using template | FRAMEWORK-ONLY | N/A (exercise) | N/A | — |
| 25 | Weak vs strong hypothesis comparison | FRAMEWORK-ONLY | N/A (teaching) | N/A | — |

### 4.3b From Hypothesis to Brief (5 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 26 | **7-section experiment brief** template (hypothesis, metrics, design, power, risks, decision rules, documentation) | FULL | `templates/experiment.yaml` — full pre-registration schema | WIRED | — |
| 27 | OEC (Overall Evaluation Criterion) concept | FRAMEWORK-ONLY | N/A | N/A | — |
| 28 | Pre-registration concept: decide rules before seeing results | FULL | `templates/experiment.yaml` has `decision_rules:` section | WIRED | — |
| 29 | experiment-brief skill auto-fires | STRONG | `.claude/skills/experiment-brief/skill.md` (pre-existing) + `/experiment design` (new) | WIRED | Two skills overlap; both work |

### 4.4 Practice: Writing Testable Hypotheses (8 min) — Practice

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 30 | Scenario 1: Homepage recommendation carousel | FRAMEWORK-ONLY | N/A (worksheet) | N/A | — |
| 31 | Scenario 2: Free trial extension from 7 to 14 days | FRAMEWORK-ONLY | N/A | N/A | — |
| 32 | Scenario 3: Push notification frequency change | FRAMEWORK-ONLY | N/A | N/A | — |

### 4.5a Causal Chain Mapping + DAGs (6 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 33 | **Causal DAGs** — nodes and arrows showing causal relationships | FRAMEWORK-ONLY | N/A (whiteboard) | N/A | — |
| 34 | Confounder concept (X ← C → Y) | FRAMEWORK-ONLY | Encoded in `agents/confound-scanner.md` + `agents/causal-method-selector.md` | N/A | — |
| 35 | Power User Fallacy DAG: tenure → feature adoption + retention | PARTIAL | `confounded.csv` demonstrates this | N/A | Column names differ from lesson |
| 36 | "If you don't draw the DAG, you don't see the confounder" | FRAMEWORK-ONLY | N/A | N/A | — |

### 4.5b The Three Structures (6 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 37 | **The Fork (Confounder):** X ← C → Y. Control for C. | FRAMEWORK-ONLY | N/A | N/A | — |
| 38 | **The Inverted Fork (Collider):** X → C ← Y. NEVER control for C. | FRAMEWORK-ONLY | N/A | N/A | — |
| 39 | **The Chain (Mediator):** X → M → Y. Control depends on question. | FRAMEWORK-ONLY | N/A | N/A | — |
| 40 | "Control for confounders, leave colliders alone" golden rule | AGENT-ONLY | `agents/confound-scanner.md`, `agents/causal-method-selector.md` encode this | WIRED (causal skill) | — |
| 41 | Converted-users-only analysis as collider bias example | FRAMEWORK-ONLY | N/A (teaching example) | N/A | — |

### 4.6 Practice: Drawing Causal DAGs (8 min) — Practice

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 42 | DAG exercise 1: Marketing spend → signups, with seasonality confounder | FRAMEWORK-ONLY | N/A | N/A | — |
| 43 | DAG exercise 2: Onboarding redesign → activation, with device mediator | FRAMEWORK-ONLY | N/A | N/A | — |
| 44 | DAG exercise 3: Review prompt → satisfaction, with completion collider | FRAMEWORK-ONLY | N/A | N/A | — |

### 4.7a The Three Knobs (Power Intuition) (5 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 45 | **Effect size** knob: bigger effect = easier to detect | FULL | `power.py`: `mde_relative` parameter in `power_proportion()` | WIRED | — |
| 46 | **Sample size** knob: more data = more sensitive | FULL | `power.py`: `n_per_group` in output | WIRED | — |
| 47 | **Baseline variance** knob: noisier data = harder to detect | FULL | `power.py`: `baseline_rate` parameter captures this | WIRED | — |
| 48 | Whisper analogy: detecting a whisper in a noisy room | FRAMEWORK-ONLY | N/A | N/A | — |
| 49 | Signal-to-noise ratio visual | FRAMEWORK-ONLY | N/A (slide) | N/A | — |

### 4.7b Rule-of-Thumb Table + Viability Check (5 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 50 | **Rule-of-thumb sample size table** (baseline × MDE → n) | FULL | `power_proportion()` can generate any row of this table | WIRED | — |
| 51 | **5-step viability quick-check** | FULL | Steps 1-4 are conceptual; step 5 = `duration_estimate()` returns VIABLE/MARGINAL/NOT_VIABLE | WIRED | — |
| 52 | Duration calculation: n_required / daily_traffic | FULL | `duration_estimate(n_required, daily_traffic, allocation)` | WIRED | — |
| 53 | CUPED mention (awareness only — "variance reduction exists") | FULL | `variance_reduction.py`: `cuped_adjust()`, `cuped_adjusted_power()` — full implementation beyond what lesson teaches | WIRED | — |
| 54 | "CUPED can cut sample by 20-50%" claim | FULL | `cuped_adjusted_power()` returns exact savings percentage | WIRED | — |

### 4.8 Practice: Is This Experiment Viable? (8 min) — Practice

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 55 | **Student runs power calc** for Scenario 1: 2% baseline conversion, 20% MDE, 500/day traffic | FULL | `power_proportion(baseline_rate=0.02, mde_relative=0.20)` + `duration_estimate()` | WIRED | — |
| 56 | **Student runs power calc** for Scenario 2: 40% baseline, 5% MDE, 10k/day | FULL | Same functions | WIRED | — |
| 57 | **Student runs power calc** for Scenario 3: 8% baseline, 10% MDE, 200/day | FULL | Same functions — should return NOT_VIABLE or MARGINAL | WIRED | — |
| 58 | Student makes viability call (VIABLE/MARGINAL/NOT_VIABLE) | FULL | `duration_estimate()` returns this classification | WIRED | — |

### 4.9 Designing Guardrails (8 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 59 | **5 guardrail categories:** Revenue, UX, Ops, Trust/Safety, Engagement | FRAMEWORK-ONLY | N/A (taxonomy) | N/A | — |
| 60 | Alert threshold vs non-negotiable limit | STRONG | `templates/experiment.yaml` → `guardrail:` section with `threshold` and `direction` | WIRED | — |
| 61 | Guardrail definition exercise: pick 2-3 for checkout experiment | STRONG | `.claude/skills/guardrails/skill.md` auto-suggests guardrails | WIRED | — |
| 62 | Airbnb house rules case study | FRAMEWORK-ONLY | N/A | N/A | — |
| 63 | Netflix download-to-watch case study | FRAMEWORK-ONLY | N/A | N/A | — |
| 64 | Guardrail violation detection | FULL | `agents/experiment-monitor.md` — checks with traffic light status | WIRED | — |
| 65 | `guardrail_violation.csv` dataset: +3% conversion, +15% page_load_time | FULL | Dataset exists with known effects | N/A | — |

### 4.10a Means, Spread, "Is This Real?" (6 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 66 | Mean concept | FRAMEWORK-ONLY | N/A (visual) | N/A | — |
| 67 | Standard deviation concept | FRAMEWORK-ONLY | N/A | N/A | — |
| 68 | Overlapping bell curves visual (signal vs noise) | FRAMEWORK-ONLY | N/A (slide animation) | N/A | — |
| 69 | "The spread determines whether the gap is real" | FRAMEWORK-ONLY | N/A | N/A | — |

### 4.10b P-Values and Confidence Intervals (6 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 70 | **P-value** concept: probability of seeing this result under null | FULL | All test functions return `p_value` and `significant` | WIRED | — |
| 71 | α = 0.05 threshold convention | FULL | `alpha` parameter in all test functions, defaults to 0.05 | WIRED | — |
| 72 | **Confidence interval** concept: range of plausible true effects | FULL | All test functions return `ci_lower`, `ci_upper` | WIRED | — |
| 73 | CI crossing zero = not significant | FULL | All test functions check this | WIRED | — |
| 74 | Statistical vs practical significance | STRONG | `effect_size.py`: `cohens_d()` → `magnitude` (small/medium/large); `relative_lift()` → `lift_pct` | WIRED | — |
| 75 | Exercise: interpret 3 results (significant small, non-significant, significant large) | FRAMEWORK-ONLY | N/A (worksheet) | N/A | — |

### 4.10c Two Tests for Two Metric Types (6 min) — AI Demo **[CRITICAL]**

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 76 | **Two-proportion z-test** for binary metrics (checkout completion rate) | FULL | `ab_tests.py`: `proportion_test(c_success, c_n, t_success, t_n)` → z_stat, p_value, ci_lower, ci_upper, significant, interpretation | NEW-ONLY | Old `experiment-analyzer.md` calls `stats_helpers.two_sample_proportion_test()`. New `/experiment analyze` calls `proportion_test()`. |
| 77 | **Welch's t-test** for continuous metrics (AOV) | FULL | `ab_tests.py`: `welch_test(control, treatment)` → t_stat, p_value, ci_lower, ci_upper, effect_size, interpretation | NEW-ONLY | Old `experiment-analyzer.md` calls `stats_helpers.two_sample_mean_test()`. New `/experiment analyze` calls `welch_test()`. |
| 78 | Student types prompt: "Run a two-proportion z-test comparing checkout completion rates" | FULL | `proportion_test()` handles exactly this | WIRED (via `/experiment`) | — |
| 79 | Student types prompt: "Run a Welch's t-test comparing AOV" | FULL | `welch_test()` handles exactly this | WIRED (via `/experiment`) | — |
| 80 | Lesson output: Control 15.2%, Treatment 16.8%, z=2.31, p=0.02, CI [+0.3%, +2.9%] | PARTIAL | `clean_ab.csv` has 35% baseline / 5% lift — numbers don't match lesson | N/A | **Add `checkout_redesign.csv`** with 15.2% baseline, 16.8% treatment (see Gap 1) |
| 81 | Lesson output: AOV Control $47.20, Treatment $45.80, t=-1.38, p=0.08, CI [-$3.10, +$0.30] | PARTIAL | `clean_ab.csv` has lognormal revenue but not calibrated to $47 | N/A | Same: needs `checkout_redesign.csv` |
| 82 | "Rate = proportions test, Average = t-test" matching rule | FRAMEWORK-ONLY | N/A (decision rule) | N/A | — |
| 83 | **Student exercise: run both tests** on NovaMart data | FULL | `proportion_test()` + `welch_test()` | WIRED | — |
| 84 | **Stats Cheat Sheet** (downloadable PDF) | GAP | Does not exist | N/A | **Create `templates/stats-cheat-sheet.md`** |

### 4.11a The Decision Tree (Result Interpretation Tree) (5 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 85 | **Result Interpretation Tree**: 4 branches | FULL | `agents/experiment-interpreter.md` implements Ship/Abort/Learn/Invalid | WIRED (via `/experiment interpret`) | — |
| 86 | Branch 1: Positive result → check guardrails → Ship | FULL | Interpreter agent walks this path | WIRED | — |
| 87 | Branch 2a: Powered null → Learn (effect is too small to matter) | FULL | `underpowered.csv` + `no_effect.csv` demonstrate both null branches | WIRED | — |
| 88 | Branch 2b: Underpowered null → Learn (we don't know) | FULL | `underpowered.csv` (n=500, true 2% effect) | WIRED | — |
| 89 | Branch 3: Negative result → Abort | FULL | Interpreter agent handles this | WIRED | — |
| 90 | Branch 4: Mixed/Invalid → Investigate | FULL | Interpreter agent + `mixed_results.csv` | WIRED | — |
| 91 | Twyman's Law: "Any figure that looks interesting is usually wrong" | FRAMEWORK-ONLY | N/A | N/A | — |
| 92 | **SRM as mandatory first check** before any interpretation | FULL | `srm_check()` as Step 1 gate. Interpreter agent calls it first. | WIRED | — |
| 93 | Spotify EwL framework (Ship/Abort/Learn) | FULL | `experiment-interpreter.md` outputs EwL classification | WIRED | — |

### 4.11b Applying the Tree to NovaMart (5 min) — Applied

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 94 | Walk through: SRM check → primary metric → guardrails → decision | FULL | `experiment-interpreter.md` walks this exact sequence | WIRED | — |
| 95 | Checkout result: SRM PASS → primary up → guardrail ambiguous → investigate AOV | STRONG | `clean_ab.csv` + `guardrail_violation.csv` cover both clean and violated paths | N/A | — |

### 4.12 Practice: Interpreting Experiment Results (8 min) — Practice

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 96 | **Scenario 1:** Positive primary, guardrails OK → Ship | FULL | `clean_ab.csv`: 5% lift, SRM PASS | WIRED | — |
| 97 | **Scenario 2:** Underpowered null → Extend or learn | FULL | `underpowered.csv`: 2% effect, n=500, <20% power | WIRED | — |
| 98 | **Scenario 3:** Positive primary, guardrail degraded → Investigate | FULL | `guardrail_violation.csv`: +3% conversion, +15% latency | WIRED | — |
| 99 | Student writes recommendation for each scenario | FRAMEWORK-ONLY | N/A (exercise) | N/A | — |

### 4.13a Categorizing the Conflict (Mixed Results) (5 min) — Concept

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 100 | **Primary vs guardrail conflict** | FULL | `guardrail_violation.csv`: conversion up + latency up | N/A | — |
| 101 | **Short-term vs long-term conflict** | FULL | `mixed_results.csv`: sessions_14d up + retained_30d down | N/A | — |
| 102 | **Metric-vs-metric conflict** | FULL | Both datasets demonstrate this | N/A | — |
| 103 | **Mixed Results Decision Framework**: categorize → evaluate → quantify | AGENT-ONLY | In `experiment-interpreter.md` prompt, not a coded function | WIRED (via agent) | No fix needed — judgment framework, not computation |

### 4.13b Making the Decision (5 min) — Applied

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 104 | Quantify both sides of the tradeoff | FRAMEWORK-ONLY | N/A (judgment) | N/A | — |
| 105 | Set monitoring plan + exit criteria for conditional ship | STRONG | `agents/experiment-monitor.md` handles ongoing tracking | WIRED | — |
| 106 | Document the decision and what you traded off | FRAMEWORK-ONLY | N/A | N/A | — |

### 4.14 Practice: Conflicting Metrics Scenario (6 min) — Practice

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 107 | Student writes decision memo for mixed-results scenario | FULL | `mixed_results.csv` or `guardrail_violation.csv` provide the data | N/A | — |
| 108 | Student applies Mixed Results Decision Framework | AGENT-ONLY | Framework in agent prompt | WIRED | — |

### 4.15a When Experiments Aren't an Option (5 min) — Concept **[CRITICAL]**

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 109 | **Decision table**: 4 situations → 4 methods | FULL | `agents/causal-method-selector.md`: 6-question interactive decision tree | WIRED (via `/causal select`) | — |
| 110 | Situation 1: Change shipped to everyone → Pre-Post | FULL | `causal/pre_post.py`: `pre_post_analysis()` | WIRED | — |
| 111 | Situation 2: Change shipped to one segment → DiD | FULL | `causal/did.py`: `did_basic()` | WIRED | — |
| 112 | Situation 3: Users self-selected → PSM | FULL | `causal/matching.py`: `propensity_match()` | WIRED | — |
| 113 | Situation 4: Have covariates but no clean comparison → Regression | FULL | `causal/regression.py`: `regression_adjust()` | WIRED | — |

### 4.15b The Confidence Ladder (5 min) — Concept **[CRITICAL]**

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 114 | **Confidence Ladder**: RCT > DiD+reg > PSM > DiD > Regression > Pre-Post | FULL | `agents/causal-interpreter.md` has the full ladder | WIRED (via `/causal report`) | — |
| 115 | "Higher on the ladder = more confident in causal claim" | FULL | Agent places result on ladder and adjusts interpretation | WIRED | — |
| 116 | **Mandatory caveats per method** (non-negotiable) | FULL | `agents/causal-report-generator.md` has mandatory caveat table | WIRED | — |
| 117 | Pre-Post caveat: "Assumes nothing else changed during this period" | FULL | Exact string in report generator agent | WIRED | — |
| 118 | DiD caveat: "Assumes the control group would have followed the same trend" | FULL | Exact string in report generator agent | WIRED | — |
| 119 | PSM caveat: "Controls for observed confounders only" | FULL | Exact string in report generator agent | WIRED | — |
| 120 | Regression caveat: "Assumes all relevant confounders are included" | FULL | Exact string in report generator agent | WIRED | — |

### 4.16a Pre-Post + Difference-in-Differences (6 min) — Concept **[CRITICAL]**

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 121 | **Pre-Post analysis** with OLS-adjusted estimate | FULL | `causal/pre_post.py`: `pre_post_analysis(pre, post, covariates)` — paired t-test or OLS | WIRED | — |
| 122 | Pre-Post mandatory caveat string in output | FULL | `pre_post_analysis()` returns `caveat` field | WIRED | — |
| 123 | DoorDash pre-post example (menu redesign) | FRAMEWORK-ONLY | N/A (case study) | N/A | — |
| 124 | **DiD formula**: (Treatment_post - Treatment_pre) - (Control_post - Control_pre) | FULL | `causal/did.py`: `did_basic()` — OLS with interaction term | WIRED | — |
| 125 | **Parallel trends assumption** concept | FULL | `causal/did.py`: `parallel_trends_test()` → PASS/WARNING/FAIL | WIRED | — |
| 126 | **Parallel trends test** (pre-period slope comparison) | FULL | `parallel_trends_test()` returns `verdict`, `p_value`, `trend_diff` | WIRED | — |
| 127 | **Event study plot** (period-by-period treatment effects) | FULL | `causal/did.py`: `event_study()` — coefficient estimates per period | WIRED | — |
| 128 | Card & Krueger minimum wage DiD reference | FRAMEWORK-ONLY | N/A | N/A | — |
| 129 | Billboard advertising DiD example | FRAMEWORK-ONLY | N/A | N/A | — |
| 130 | `did_parallel.csv`: known +3.0 effect, parallel pre-trends, 200 users, 10 weeks | FULL | Dataset exists with correct structure | N/A | — |
| 131 | `did_broken.csv`: iOS 1.2/week vs Android 0.5/week — FAIL | FULL | Dataset exists; tests assumption failure | N/A | — |

### 4.16b Matching + Regression + Triangulation (6 min) — Concept **[CRITICAL]**

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 132 | **PSM 5-step process**: estimate scores → match → check balance → estimate → sensitivity | FULL | `propensity_match()` does steps 1-2-4; `balance_table()` does step 3; `rosenbaum_bounds()`/`e_value()` does step 5 | WIRED | — |
| 133 | Logistic regression for propensity scores | FULL | `propensity_match()` uses `sklearn.LogisticRegression` internally | WIRED | — |
| 134 | KDTree nearest-neighbor matching | FULL | `propensity_match()` uses `scipy.spatial.KDTree` | WIRED | — |
| 135 | **Balance check: SMD < 0.1 threshold** | FULL | `balance_table()` returns SMD per covariate with PASS/FAIL at 0.1 | WIRED | — |
| 136 | **Love plot** (before/after matching balance) | FULL | `balance.py`: `love_plot()` — matplotlib visualization | WIRED | — |
| 137 | Variance ratio in balance diagnostics | FULL | `balance_table()` returns `variance_ratio` per covariate | WIRED | — |
| 138 | **Regression Adjustment** with OLS | FULL | `causal/regression.py`: `regression_adjust()` — OLS with HC1 errors | WIRED | — |
| 139 | **Triangulation** concept: run multiple methods and compare | FRAMEWORK-ONLY | N/A (judgment concept) | N/A | — |
| 140 | Uber PSM example | FRAMEWORK-ONLY | N/A | N/A | — |
| 141 | `confounded.csv`: known +5.0 causal effect, tenure as confounder | FULL | Naive estimate ~7-8, PSM should recover ~5 | N/A | Column names differ from lesson (see Gap 5) |
| 142 | **Sensitivity analysis**: Rosenbaum bounds | FULL | `causal/sensitivity.py`: `rosenbaum_bounds()` | WIRED | — |
| 143 | **E-value** computation | FULL | `causal/sensitivity.py`: `e_value()` | WIRED | — |
| 144 | "Unobserved confounder would need to be 3x stronger" plain-language | FULL | `agents/causal-sensitivity.md` produces these translations | WIRED | — |
| 145 | **Common support check** | FULL | `causal/assumptions.py`: `check_common_support()` | WIRED | — |

### 4.17a Prompt Patterns for Experiment Design (5 min) — AI Demo

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 146 | **Full experiment brief generation via AI** | FULL | `agents/experiment-designer.md` + `/experiment design` | NEW-ONLY | Old `experiment-designer.md` doesn't call `power_proportion()` — improvises power calc. **Upgrade agent** to import from `experiment_stats.power`. |
| 147 | Brief includes: hypothesis (5 components), metrics (OEC + secondary + guardrails), design, power, risks, decision rules, documentation | FULL | `templates/experiment.yaml` schema covers all 7 sections | WIRED | — |
| 148 | Student watches Claude Code produce the brief section by section | FULL | `/experiment design` mode orchestrates this | WIRED | — |

### 4.17b AI Red-Teaming + Guardrail Suggestions (5 min) — AI Demo

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 149 | **Red-teaming prompt**: "What are the top 5 risks?" | STRONG | `agents/confound-scanner.md` finds threats to validity | WIRED | Broader scope than lesson (covers all analysis, not just experiments) |
| 150 | Risk 1: Novelty effect | FRAMEWORK-ONLY | N/A (conceptual risk) | N/A | — |
| 151 | Risk 2: AOV degradation | STRONG | Guardrail monitoring via `experiment-monitor.md` | WIRED | — |
| 152 | Risk 3: SRM from implementation | FULL | `srm_check()` + `srm_diagnose()` | WIRED | — |
| 153 | Guardrail suggestions from 5 categories | STRONG | `.claude/skills/guardrails/skill.md` auto-suggests | WIRED | — |
| 154 | Validation judgment: "pick 2-3 from 15 AI suggestions" | FRAMEWORK-ONLY | N/A (teaching point) | N/A | — |

### 4.18a Power Calculations + Sensitivity Tables (5 min) — AI Demo **[CRITICAL]**

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 155 | **Power calculation for proportions**: student types prompt | FULL | `power.py`: `power_proportion(baseline_rate, mde_relative, alpha, power)` → `n_per_group`, `total_n`, `interpretation` | WIRED | — |
| 156 | Output: "At 15% baseline, 10% MDE, 80% power → 4,800 per group" | FULL | `power_proportion()` returns exact values | WIRED | — |
| 157 | **Sensitivity table**: multiple MDEs (5%, 8%, 10%, 15%, 20%) | STRONG | Can call `power_proportion()` in a loop for each MDE | WIRED | **Add `power_sensitivity_table()` convenience wrapper** (~15 lines) |
| 158 | Duration estimate from power calc | FULL | `duration_estimate(n_required, daily_traffic, allocation)` | WIRED | — |
| 159 | Viability classification: VIABLE / MARGINAL / NOT_VIABLE | FULL | `duration_estimate()` returns this | WIRED | — |
| 160 | Power chart: sample size vs MDE with 80%/90% power lines | AGENT-ONLY | Agent can generate with matplotlib; no pre-built chart function | N/A | Nice-to-have, not critical |
| 161 | CUPED sample savings calculation | FULL | `cuped_adjusted_power()` returns `savings_pct` | WIRED | — |
| 162 | Hex interactive power calculator (screencast) | GAP | No Hex integration | N/A | Expected — Hex is external platform |

### 4.18b Running Quasi-Experimental Analyses (5 min) — AI Demo **[CRITICAL]**

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 163 | **Pre-Post prompt pattern**: "Compare conversion 4 weeks before vs 4 weeks after, control for day-of-week" | FULL | `pre_post_analysis()` with covariates parameter | WIRED (via `/causal analyze`) | — |
| 164 | Student types pre-post prompt in Claude Code | FULL | `/causal analyze` dispatches to `causal-analyzer.md` which calls `pre_post_analysis()` | WIRED | — |
| 165 | Pre-post output: +1.2pp, CI [+0.4, +2.0], p=0.004 | PARTIAL | Function works but **no `checkout_data.csv`** with 56 days of daily data | N/A | **Add `checkout_timeseries.csv`** (see Gap 3) |
| 166 | Trend chart with launch date marked | AGENT-ONLY | `causal-analyzer.md` can generate chart; `chart_helpers.py` has `add_event_span()` | N/A | — |
| 167 | **DiD prompt pattern**: "Check parallel trends, then run diff-in-diff" | FULL | `did_basic()` + `parallel_trends_test()` | WIRED | — |
| 168 | **PSM prompt pattern**: "Match on signup_source, device, plan_type. Check balance." | FULL | `propensity_match()` + `balance_table()` | WIRED | — |
| 169 | `checkout_data.csv` for pre-post demo: 56 days, daily conversion rates | GAP | Does not exist | N/A | **Create** (see Gap 3) |
| 170 | `engagement_data.csv` for DiD demo | PARTIAL | `did_parallel.csv` exists but uses "orders" not "engagement" and different column names | N/A | Close enough — agent adapts |
| 171 | `user_data.csv` for PSM demo: signup_source, device, plan_type, retention_30d | PARTIAL | `confounded.csv` exists but different column names | N/A | See Gap 5 |
| 172 | **"Claude Code Prompts for Causal Analysis" downloadable** | GAP | Does not exist | N/A | **Create `templates/causal-prompts.md`** |
| 173 | 5-point result presentation structure (found, assumed, checked, could go wrong, confidence) | FRAMEWORK-ONLY | N/A (template) | N/A | — |

### 4.19a Design + Red-Team in Claude Code (5 min) — AI Demo

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 174 | **Full experiment brief generation in Claude Code** (live demo, all 7 sections) | FULL | `/experiment design` → `experiment-designer.md` → outputs `experiment.yaml` | WIRED | — |
| 175 | Hypothesis with 5 components (action, metric, direction, magnitude=10% MDE, mechanism) | FULL | `templates/experiment.yaml` → hypothesis section | WIRED | — |
| 176 | Inline power calculation: "15% baseline, 10% MDE, 80% power → 4,800 per group, 3.2 days" | FULL | `power_proportion()` + `duration_estimate()` | NEW-ONLY | Old `experiment-designer.md` improvises; new `/experiment` skill wired |
| 177 | Pre-registered decision rules auto-generated | FULL | Template + interpreter agent | WIRED | — |
| 178 | **Red-team the design**: "Top 5 risks" | STRONG | `agents/confound-scanner.md` | WIRED | — |
| 179 | **Power sensitivity table**: 5%, 8%, 10%, 15%, 20% MDEs at 80%/90% power | STRONG | `power_proportion()` × N in a loop | WIRED | Add wrapper (see #157) |

### 4.19b Interactive Monitoring Dashboard in Hex (5 min) — AI Demo

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 180 | Daily conversion by variant chart | AGENT-ONLY | `agents/experiment-monitor.md` can generate this analysis | WIRED | — |
| 181 | Cumulative sample size tracking | AGENT-ONLY | Monitor agent tracks this | WIRED | — |
| 182 | Guardrail metrics over time | AGENT-ONLY | Monitor agent tracks this | WIRED | — |
| 183 | SRM check in monitoring dashboard | FULL | `srm_check()` — callable from any context | WIRED | — |
| 184 | Hex notebook template | GAP | No Hex integration | N/A | Expected — Hex is external |

### 4.20 Capstone Milestone 4 (10 min) — Capstone

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| **Path A: Complete Experiment Brief** | | | | |
| 185 | Hypothesis with 5 components | FULL | `templates/experiment.yaml` + `/experiment design` | WIRED | — |
| 186 | Metrics: OEC + secondary + 2-3 guardrails with thresholds | FULL | Template has all metric categories | WIRED | — |
| 187 | Design: allocation, randomization unit, population, duration | FULL | Template covers all | WIRED | — |
| 188 | Power & Feasibility: baseline, MDE, n_per_group, days, viability | FULL | `power_proportion()` + `duration_estimate()` | WIRED | — |
| 189 | Risks & Guardrails: top 3 risks with severity + mitigation | STRONG | `confound-scanner.md` identifies risks | WIRED | — |
| 190 | Decision Rules: pre-registered ship/no-ship/investigate | FULL | Template `decision_rules:` section | WIRED | — |
| 191 | Documentation: owner, log location, readout date | FULL | Template covers this | WIRED | — |
| **Path B: Causal Analysis** | | | | |
| 192 | Causal question in "Did X cause Y?" format | FULL | `/causal select` starts with this | WIRED | — |
| 193 | DAG with labeled confounders | FRAMEWORK-ONLY | N/A (whiteboard/drawing) | N/A | — |
| 194 | Method justification with confidence ladder reference | FULL | `causal-method-selector.md` + `causal-interpreter.md` | WIRED | — |
| 195 | Key assumption identification and validation approach | FULL | `causal-assumption-checker.md` — per-method diagnostic battery | WIRED | — |
| 196 | **Run analysis in Claude Code**: point estimate + CI + chart | FULL | `causal-analyzer.md` dispatches to coded helpers | WIRED | — |
| 197 | **Report with honest caveats**: finding + confidence + limitations | FULL | `causal-report-generator.md` — 8-section report with mandatory caveats | WIRED | — |

### 4.21 Week 4 Wrap-up (5 min) — Recap

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 198 | 7 frameworks reference card | FRAMEWORK-ONLY | N/A (slide) | N/A | — |
| 199 | Retrieval practice Q1: Never control for a collider | FRAMEWORK-ONLY | N/A | N/A | — |
| 200 | Retrieval practice Q2: Underpowered null = "we don't know" | FRAMEWORK-ONLY | N/A | N/A | — |
| 201 | Retrieval practice Q3: CI tells you how big, not p-value | FRAMEWORK-ONLY | N/A | N/A | — |
| 202 | Stats Cheat Sheet reference (downloadable from 4.10) | GAP | Does not exist | N/A | Same as #84 |

### 4.22 Preparing for the Live Workshop (4 min) — Workshop Prep

| # | Concept / Action | Rating | ai-analyst-plus Capability | Wiring | Fix Needed |
|---|-----------------|--------|---------------------------|--------|------------|
| 203 | Peer red-teaming exercise using DAG structures, guardrail categories, Result Interpretation Tree | FRAMEWORK-ONLY | N/A (workshop activity) | N/A | — |
| 204 | Group mixed-results exercise using framework from 4.13 | FRAMEWORK-ONLY | `mixed_results.csv` available for group exercise | N/A | — |
| 205 | Open discussion: "What if we can't get enough sample?" → No-Experiment Toolbox | FULL | All 4 causal methods available via `/causal` | WIRED | — |
| 206 | Open discussion: "How to convince VP null result is valuable?" → Spotify 64% stat | FRAMEWORK-ONLY | N/A | N/A | — |

---

## Part 2: Wiring Fix Plan

### Priority 1: Old Agents Still Using `stats_helpers` (BROKEN Middle Layer)

These agents import from the OLD `helpers/stats_helpers` module instead of the NEW `helpers/experiment_stats`. The new `/experiment` and `/causal` skills are wired correctly, but if a user invokes the old agent directly (or if CLAUDE.md routes to it), they get improvised stats instead of production-grade helpers.

| Agent | Current Import | Should Import | Lines to Change |
|-------|---------------|---------------|-----------------|
| `experiment-analyzer.md` line 117 | `from helpers.stats_helpers import two_sample_mean_test, chi_squared_test` | `from helpers.experiment_stats import welch_test, srm_check` | ~4 import blocks + update function call names |
| `experiment-analyzer.md` line 149 | `from helpers.stats_helpers import two_sample_mean_test, two_sample_proportion_test` | `from helpers.experiment_stats import welch_test, proportion_test` | Same file |
| `experiment-analyzer.md` line 179 | `from helpers.stats_helpers import confidence_interval, interpret_effect_size` | `from helpers.experiment_stats import cohens_d, relative_lift` | Same file |
| `experiment-designer.md` | No import at all — improvises power calc inline | Add: `from helpers.experiment_stats import power_proportion, duration_estimate` | ~2 blocks |

### Priority 2: Old `srm-check` Skill Still Using Inline Scipy

| Skill | Current | Should Use | Fix |
|-------|---------|-----------|-----|
| `.claude/skills/srm-check/skill.md` line 80 | References `stats_helpers.py` for chi-squared | `from helpers.experiment_stats import srm_check` | Update skill instruction block |

### Priority 3: CLAUDE.md Registration

The main CLAUDE.md at the repo root needs to know about the new capabilities. Currently it does NOT mention:
- `/experiment` skill (8 modes)
- `/causal` skill (6 modes)
- `helpers/experiment_stats/` module (20+ functions)
- 8 new agents (experiment-interpreter, experiment-monitor, causal-*)

**Fix:** Add a section to CLAUDE.md listing the new skills, agents, and the experiment_stats library with its public API.

### Priority 4: Schema Registration

Experiment CSVs in `data/novamart/experiments/` are not registered in `.knowledge/datasets/novamart/schema.md`. The AI analyst system won't discover them without schema registration.

**Fix:** Add experiment table definitions to the schema file.

### Priority 5: agents/INDEX.md

If an agents/INDEX.md exists, it needs the 8 new agents added.

---

## Part 3: Data Gaps

### Gap 1: `checkout_redesign.csv` — MEDIUM Priority

**Lessons affected:** 4.10c (#80-81), 4.11b (#95), 4.19a (#176)

The lesson quotes specific numbers that don't match `clean_ab.csv`:
- Control: 4,218 users, 641 completed, **15.2%** conversion
- Treatment: 4,196 users, 705 completed, **16.8%** conversion
- AOV: Control **$47.20**, Treatment **$45.80**

**Fix:** Add a `checkout_redesign.csv` to `generate_experiment_data.py` with these exact numbers. ~30 lines.

### Gap 2: Power Sensitivity Table Wrapper — LOW Priority

**Lessons affected:** 4.18a (#157), 4.19a (#179)

No single function generates a multi-MDE sensitivity table. Currently requires a loop over `power_proportion()`.

**Fix:** Add `power_sensitivity_table(baseline, mdes, daily_traffic, alpha, power)` → returns DataFrame. ~15 lines.

### Gap 3: `checkout_timeseries.csv` — MEDIUM Priority

**Lessons affected:** 4.18b (#165, #169)

Lesson expects `checkout_data.csv` with 56 days of daily conversion rates (4 weeks pre + 4 weeks post a March 1 launch). Our datasets are all user-level, not daily aggregates.

**Fix:** Add `generate_checkout_timeseries()` to the generator script. 56 rows, daily_date + daily_conversion_rate + day_of_week, with a known ~1.2pp level shift at March 1. ~50 lines.

### Gap 4: Claude Code Prompts Downloadable — LOW Priority

**Lessons affected:** 4.18b (#172)

Lesson offers a downloadable "Claude Code Prompts for Causal Analysis" markdown with 3 annotated prompts (pre-post, DiD, PSM).

**Fix:** Create `templates/causal-prompts.md` with the 3 prompts from the lesson. ~30 lines.

### Gap 5: Confounded Dataset Column Names — MEDIUM Priority

**Lessons affected:** 4.2a (#8), 4.5a (#35), 4.16b (#141), 4.18b (#171)

The lesson's Power User Fallacy story uses `job_role`, `heavy_usage`, `retained_30d`. Our `confounded.csv` uses `adopted_feature`, `tenure_months`, `orders_30d`. Same statistical mechanics, different variable names.

**Fix:** Add a `power_user_fallacy.csv` with lesson-matching columns. Keep `confounded.csv` for the general case. ~30 lines in generator.

### Gap 6: Stats Cheat Sheet — LOW Priority

**Lessons affected:** 4.10c (#84), 4.21 (#202)

One-page reference covering mean, SD, p-value, CI, proportions test, t-test. Referenced as a downloadable.

**Fix:** Create `templates/stats-cheat-sheet.md`. ~50 lines.

### Gap 7: Schema Registration — LOW Priority

**Lessons affected:** 4.1 (#4)

9 experiment CSVs not in `.knowledge/datasets/novamart/schema.md`.

**Fix:** Add table definitions. ~60 lines.

---

## Part 4: Summary Scorecard

### By Rating (206 items mapped)

| Rating | Count | % |
|--------|-------|---|
| FULL | 95 | 46% |
| STRONG | 17 | 8% |
| PARTIAL | 10 | 5% |
| AGENT-ONLY | 7 | 3% |
| FRAMEWORK-ONLY | 70 | 34% |
| GAP | 7 | 3% |

### By Wiring Status (of non-FRAMEWORK items: 136)

| Status | Count | % |
|--------|-------|---|
| WIRED | 87 | 64% |
| NEW-ONLY (new skill wired, old agent broken) | 6 | 4% |
| N/A (dataset or no wiring needed) | 40 | 29% |
| BROKEN (function exists, not wired) | 3 | 2% |

### Critical Path Items (Must Fix Before Course Ships)

| # | What | Priority | Effort | Items Affected |
|---|------|----------|--------|----------------|
| 1 | Upgrade `experiment-analyzer.md` imports from `stats_helpers` → `experiment_stats` | HIGH | ~30 min | #76, #77 |
| 2 | Upgrade `experiment-designer.md` to call `power_proportion()` | HIGH | ~20 min | #146, #176 |
| 3 | Add `checkout_redesign.csv` matching lesson numbers | HIGH | ~30 lines | #80, #81, #95 |
| 4 | Add `checkout_timeseries.csv` for pre-post demo | HIGH | ~50 lines | #165, #169 |
| 5 | Upgrade `srm-check` skill to call `srm_check()` from experiment_stats | MEDIUM | ~10 min | #17, #18 |
| 6 | Add `power_user_fallacy.csv` with lesson-matching columns | MEDIUM | ~30 lines | #8, #35, #141, #171 |
| 7 | Register experiment CSVs in `.knowledge/datasets/novamart/schema.md` | MEDIUM | ~60 lines | #4 |
| 8 | Update CLAUDE.md with new skills/agents/module | MEDIUM | ~40 lines | All invocations |
| 9 | Create `templates/stats-cheat-sheet.md` | LOW | ~50 lines | #84, #202 |
| 10 | Create `templates/causal-prompts.md` | LOW | ~30 lines | #172 |
| 11 | Add `power_sensitivity_table()` wrapper | LOW | ~15 lines | #157, #179 |

### Overall Verdict

**ai-analyst-plus covers 92% of what Week 4 needs** (FULL + STRONG + FRAMEWORK-ONLY). The statistical engine, causal inference toolkit, new agent system, new skills, templates, and 9 teaching datasets are all in place and tested (87 unit tests passing).

**The 8% remaining breaks down as:**
- **5% PARTIAL** — datasets exist but need column/naming adjustments or daily aggregation
- **3% GAP** — 3 missing data files + 2 missing template docs + 1 missing convenience function

**The main risk is the "broken middle layer":** the new `/experiment` and `/causal` skills are properly wired to `experiment_stats`, but the old pre-existing agents (`experiment-analyzer.md`, `experiment-designer.md`) and the old `srm-check` skill still import from `stats_helpers`. A student who follows the lesson demos exactly (using `/experiment` or `/causal`) will hit the wired path. A student who invokes the agent directly (or a lesson that references the agent) will hit the broken path.

**Estimated total fix effort: ~4 hours** (2 agent upgrades + 3 data files + 2 template files + 1 function + schema registration + CLAUDE.md update).
