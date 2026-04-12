# data-generation/

Everything that **creates** synthetic data for this repo. All generated artifacts land in `../data/` — this directory contains only the code that produces them.

## One command

```bash
python data-generation/generate_all.py
```

Generates everything. Use `--world` or `--experiments` to run just one half.

## What gets produced

| Output path | Source | Contents |
|---|---|---|
| `data/practice/` | `generate.py` | Full NovaMart e-commerce world: 13 tables (users, products, events, orders, memberships, NPS, support, experiments, …), CSV + `novamart_practice.duckdb`. ~50K users, 500 products, 2024 calendar year. 5 analytical stories injected (ticket spike, activation drop, NPS paradox, power-user fallacy, checkout confound). |
| `data/capstone/` | `generate.py` → `capstone/apply_landmines.py` | Same shape as practice, but with data-quality landmines (duplicate events, missing windows, null devices, delayed timestamps, dropped sessions table, etc.) for the capstone exercise. Practice + capstone are generated in one run. |
| `data/experiments/` | `experiments/generate_experiment_data.py` | 12 standalone A/B-test and causal-inference datasets, each with a JSON answer key in `_answers/`. Used by `/experiment`, `/causal`, SRM checks, and the experiment-stats helpers. |

## Layout

```
data-generation/
├── README.md              ← this file
├── generate_all.py        ← single entry point (runs both halves)
├── generate.py            ← NovaMart world orchestrator (8 phases)
├── config.yaml            ← all knobs for the world (users, products, stories, capstone landmines)
├── requirements.txt
├── BUILD_SPEC.md          ← detailed spec for the world generator
│
├── generators/            ← 11 modular table builders (calendar → users → events → …)
├── stories/               ← analytical stories injected after base generation
├── capstone/              ← landmine application for the capstone dataset
│
├── experiments/           ← self-contained experiment-lab generator
│   └── generate_experiment_data.py
│
├── export.py              ← CSV writer
├── load_duckdb.py         ← DuckDB database builder
└── quality_gates.py       ← post-generation validation
```

## How the two systems relate

Both ship under the "NovaMart" brand but operate at different layers:

- **NovaMart world** is the **simulated business**. It's messy, rich, and has embedded patterns that analysts are supposed to discover. Use it for descriptive analysis, funnels, segmentation, root-cause investigation.
- **Experiment lab** is a set of **teaching toys** — each CSV is a single, isolated experiment scenario (clean A/B, SRM violation, guardrail conflict, underpowered, confounded, DiD parallel, DiD broken, …) with a known ground-truth answer key. Use it when exercising `/experiment`, `/causal`, or SRM check skills.

They do not share rows or IDs. Don't join across them.

## Using the output as the active dataset

Running the generator produces files on disk. It does **not** auto-register
anything with the knowledge base — that's a separate, user-initiated step so
the repo stays dataset-agnostic.

To use the generated NovaMart data for analysis:

1. Run the generator: `python data-generation/generate_all.py`
2. Register it: `/connect-data` (guided) **or** manually create
   `.knowledge/datasets/novamart/manifest.yaml` pointing at
   `data/practice/novamart_practice.duckdb`
3. Set it active: `/switch-dataset novamart` or edit `.knowledge/active.yaml`

If you already have your own data, skip all of this — connect your own source
instead. The repo does not assume NovaMart exists.

## Determinism

Every generator uses a seeded RNG. Re-running produces identical output. Seeds:

- World: `config.yaml → general.random_seed` (42)
- Capstone landmines: `config.yaml → capstone.random_seed` (123)
- Experiment lab: per-dataset seeds 101–112 hardcoded in `generate_experiment_data.py`

## Regenerating

Generated artifacts under `data/practice/`, `data/capstone/`, and `data/experiments/` are **gitignored**. If you pull this repo fresh, run `generate_all.py` once to populate them.
