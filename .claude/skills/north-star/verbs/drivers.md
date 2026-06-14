# Verb: /north-star drivers `["<nsm>"] [--window <start>:<end>]`

**Engine:** `helpers/north_star/drivers.py` (deterministic — same window in, same numbers out)
**Guardrail:** `input_tree.py` (the B×F×E inputs must be genuine drivers, none restating the NSM)
**Output:** a North Star report (markdown + Economist-styled HTML with a diverging chart)

## Purpose

Decompose what drove a throughput North Star over a window — `Completed = Breadth ×
Frequency × Efficiency`, with Depth (AOV) as a value guardrail — and **render the
report + chart automatically**, identical every run.

This exists because a freehand "decompose what drove the year" prompt is unreliable
for a demo: it picks its own window (so the numbers drift from your slides), it can
skip Depth, and it doesn't produce the report/chart without a follow-up. This verb
pins the window + definitions and emits the artifact. What's on the slide is what
shows up live.

## Workflow

### 1. Resolve the NSM and the window

- NSM: the argument, or `profile.nsm.current`, or default `weekly completed orders`.
- **Window:** if the user gave one (e.g. `--window 2024-02:2024-11`), use it. If NOT,
  **ask once:** "What window should I read — the full year (Jan–Dec, the standard
  report), or a clean stretch that excludes a spike like Black Friday (e.g. Feb–Nov)?"
  Default to the full range (first→last full month) if they don't care. The window is
  the one thing that changes the numbers, so it's worth one question.

### 2. Confirm the dataset

`/datasets` should show the source (NovaMart for the demo; `data/practice/orders.csv`).
The engine reads `orders.csv` from the data dir. If no dataset, tell the user to
`/connect-data` first.

### 3. Run the deterministic engine

```bash
python3 -m helpers.north_star drivers \
  --start <YYYY-MM> --end <YYYY-MM> \
  --nsm "<nsm>" \
  --out outputs/north-star/<org>/drivers-<timestamp>.md
```

Omit `--start/--end` for the full-year default. It writes `<out>.md` and `<out>.html`
and prints the stats JSON. **Re-running with the same window reproduces byte-identical
numbers** — that's the whole point.

### 4. Run the input-tree guardrail (proves the decomposition is honest)

The engine returns the per-month driver series under `_series`. Pipe it through the
guardrail to confirm `Completed = Breadth × Frequency × Efficiency` reconciles and no
input is the NSM restated:

```bash
python3 -c "import json,sys; from helpers.north_star import drivers as d; \
s=d.compute(start='<start>',end='<end>'); \
print(json.dumps({'nsm':s['_series']['completed'], \
'inputs':{'Breadth':s['_series']['buyers'],'Frequency':s['_series']['freq'],'Efficiency':s['_series']['eff']}}))" \
  | python3 -m helpers.north_star check-input-tree
```

Expect `ok: true`. (If a user ever points this at a headcount NSM, the guardrail
catches the restatement — same protection as `inputs`.)

### 5. Show the report

Open the HTML (`open <out>.html`) — the Economist report with the diverging chart —
and summarize the headline out loud: the growth multiple, the Breadth share, and the
Depth guardrail. The markdown version is the paste-to-Slack copy.

## Demo defaults (NovaMart, full year)

`/north-star drivers "weekly completed orders"` over Jan–Dec 2024 produces, every run:
- **6.0×** growth (1,037 → 6,215 orders/mo), Black Friday peak 2,387/wk
- **Breadth +99%**, Frequency +2%, Efficiency −1% (the three multiply into the NSM)
- **Depth guardrail: AOV −9%** ($80 → $73)
- repeat rate 34.9%, Plus 3.4% (1.50 vs 1.48 — no lift)

These match the lesson slides exactly. Pass `--window 2024-02:2024-11` to read the
structural year with Black Friday excluded.

## Failure modes

| Failure | Response |
|---|---|
| Window not in the data's full months | engine raises ValueError listing available months |
| Input restates the NSM (guardrail) | hard refuse — re-cast the NSM as a throughput count (see `verbs/inputs.md`) |
| No dataset connected | can't read orders.csv → tell user to `/connect-data` |
