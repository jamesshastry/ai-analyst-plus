---
name: data-quality-check
description: Validate data completeness, consistency, coverage, freshness, and statistical sanity before analysis from Codex. Use at the start of data analysis, before querying or drawing conclusions, after connecting or switching datasets, when results look suspicious, when users ask if data is clean, or when they ask about a specific table and need more than schema.
---

# Data Quality Check

## Purpose

Validate data completeness, consistency, coverage, freshness, and statistical sanity before
analysis. Report issues with severity so the user knows what blocks analysis versus what
should be carried as a caveat.

This is the Codex-native counterpart to the legacy Claude data-quality-check skill.

## When to use

Use this skill proactively:

- at the start of any new analysis that will query or interpret data;
- when connecting, switching, or profiling datasets;
- when results look surprising or suspicious;
- when the user asks whether data is clean, complete, fresh, validated, or reliable;
- when the user asks about a specific named table and needs more than cached schema.

For purely structural schema lookup, `$data-inspect` is enough. For table-scoped questions
such as “tell me about orders,” pair schema inspection with at least a minimum DQ probe.

## Required context

1. Read `.knowledge/active.yaml` to identify the active dataset.
2. Read `.knowledge/datasets/{active}/manifest.yaml` when present.
3. Read `.knowledge/datasets/{active}/schema.md`.
4. Read `.knowledge/datasets/{active}/quirks.md` when present.
5. Use `helpers.connection_manager.ConnectionManager` for data access when probing real
   tables.
6. Log executed SQL with `scripts/log_query.py` when the broader analysis workflow requires
   query logging.

Never guess the dataset. Never expose credentials from manifests or errors.

## Minimum table-scoped probe

When a user asks about a specific table, run or request permission to run:

- row count;
- null rate per column, flagging anything above 5%;
- date range on the primary timestamp/date column when one exists;
- duplicate check on documented primary key or likely ID column;
- table-specific notes from `quirks.md`.

If the table is extremely large or warehouse cost is a concern, say so and ask before the
full probe. Still try to run the cheapest row-count and primary-key duplicate checks when
safe.

## Check sequence

Run checks in this order. Stop and report immediately when a blocker invalidates the planned
analysis.

### 1. Completeness

Check:

- null rates per column;
- nulls in primary keys and critical analysis columns;
- missing date ranges for time-series data;
- unexpected zeros in revenue, count, quantity, or denominator columns.

Severity guide:

- **BLOCKER**: primary key nulls, more than 50% nulls in a critical analysis column, entire
  required date ranges missing.
- **WARNING**: 5–50% nulls in an analysis column, scattered missing dates, unexpected zeros
  in key numeric columns.
- **INFO**: less than 5% nulls in non-critical columns or expected weekend/business-day gaps.

### 2. Consistency

Check:

- duplicate primary keys;
- referential integrity for documented foreign keys;
- mixed date formats;
- inconsistent casing/whitespace in categorical values;
- orphan records.

Severity guide:

- **BLOCKER**: duplicate primary keys or broken referential integrity affecting more than
  10% of relevant rows.
- **WARNING**: mixed date formats, orphan records under 10%, inconsistent category casing in
  analysis dimensions.
- **INFO**: minor casing or whitespace issues that can be normalized with caveats.

### 3. Coverage

Use helper functions when operating on DataFrames:

```python
from helpers.sql_helpers import check_temporal_coverage, check_value_domain
```

Check:

- expected date coverage;
- required cohorts/segments;
- expected category domains;
- whether key segments are entirely missing.

Severity guide:

- **BLOCKER**: key segments entirely missing or temporal coverage below 80% for the analysis
  window.
- **WARNING**: segments with materially fewer rows than expected, coverage 80–95%, unexpected
  category values.
- **INFO**: minor imbalances or coverage above 95%.

### 4. Statistical sanity

Use helper functions when reading DataFrames:

```python
from helpers.data_quality_extras import check_null_concentration, check_outliers
```

Check:

- impossible values, such as negative revenue unless refunds are expected, conversion rates
  outside `[0, 1]`, future event dates, or negative durations;
- outliers via IQR as primary and z-score as a cross-check;
- highly skewed distributions;
- columns that are effectively empty.

Severity guide:

- **BLOCKER**: impossible values in critical metrics, more than 95% nulls, or values that
  make the planned metric invalid.
- **WARNING**: extreme outliers, more than 50% nulls, or high skew that affects mean-based
  metrics.
- **INFO**: moderate outliers or mild skew.

### 5. Time-series anomaly scan

For date-indexed metric columns, aggregate to daily or weekly grain first; do not run anomaly
checks directly on raw event rows. Use rolling mean/standard deviation bands or an existing
repo helper if available.

Report anomalies as observations, not conclusions:

```text
Notable patterns detected:
- orders dropped 32% below normal on 2026-03-14.
- signups spiked 48% above normal during launch week.
```

Severity guide:

- **WARNING**: material spike/drop that may affect the analysis window.
- **INFO**: no notable anomalies or minor expected seasonality.

### 6. Freshness

For each table with a date/timestamp column, check the most recent date and infer cadence
when possible.

Report:

```text
Data freshness:
- events: most recent = 2026-06-27 (1 day ago) OK
- orders: most recent = 2026-06-20 (8 days ago) WARNING
```

Severity guide:

- **WARNING**: data is stale relative to inferred cadence or business expectation.
- **INFO**: data is fresh or explicitly static/historical.

## Output format

Write a concise report in this shape. Save it to `working/data_quality/` when the check is
substantial or part of a longer analysis.

```markdown
# Data Quality Report: [Dataset Name]
## Date: [YYYY-MM-DD]
## Scope: [dataset/table/question]

### Summary
| Severity | Count | Details |
|----------|------:|---------|
| BLOCKER | X | Must fix before analysis |
| WARNING | X | Carry as caveat / investigate |
| INFO | X | Awareness only |

### BLOCKERS
[List each blocker with table/column, rows affected, impact, suggested fix]

### WARNINGS
[List each warning with likely impact and recommended handling]

### INFO
[List awareness items]

### Data Profile
| Table | Rows | Columns | Date Range | Key Columns |
|-------|-----:|--------:|------------|-------------|

### Recommendation
[PROCEED | PROCEED WITH CAUTION | BLOCKED] — [why]
```

Recommendation definitions:

- **PROCEED**: no blockers and only minor warnings.
- **PROCEED WITH CAUTION**: no blockers but warnings materially affect interpretation; include
  caveats in findings.
- **BLOCKED**: blockers found; fix or explicitly scope around them before analysis.

## Anti-patterns

- Do not skip quality checks because the data “looks fine.”
- Do not treat all nulls as equal; distinguish critical from non-critical fields.
- Do not silently fix data. Document every cleaning or exclusion choice.
- Do not analyze through known blockers unless the user explicitly narrows scope around them.
- Do not assume dates, time zones, primary keys, or categorical domains are clean.
- Do not present anomalies as causal explanations without follow-up analysis.
