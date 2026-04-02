# Skill: Show Off LinkedIn

## Purpose
Generate a beautiful, screenshot-ready HTML architecture diagram of what the
student built — designed for posting on LinkedIn. Claude analyzes the student's
code, understands their architecture, and generates a custom 1080x1080 visual
in the AI Analyst Lab brand style.

The student does nothing except type `/show-off-linkedin` and screenshot the
result. Claude handles everything else.

## When to Use
- User says `/show-off-linkedin` or "LinkedIn showcase" or "share on LinkedIn"
- End of Day 1 or Day 2 when students want to share what they built

## Invocation
`/show-off-linkedin` — generate a LinkedIn-ready architecture diagram

## Instructions

### Step 1: Find the Student's Work

Same detection logic as `/show-off`. Do NOT ask the student to explain anything.

1. **Run `git status --short`** to see untracked (`??`) and modified (`M`) files
2. **Run `git diff`** to see what they changed in existing files
3. **Read the new/modified files** to understand what they actually contain

If the student HAS made commits:
4. **Run `git log --oneline --all --not --remotes`** to find local-only commits
5. Combine committed changes with uncommitted work

**Ignore** `.env`, `.gitignore`, `node_modules/`, lockfiles, `__pycache__/`, etc.

**Understand the architecture** — what components exist, how they connect,
what data flows where. Focus on agents, skills, helpers, analysis outputs,
charts, and pipelines. Count things: how many agents, how many charts, how
many tests, how many lines of code they wrote.

### Step 2: Choose a Layout Pattern

Based on what the student built, choose the best layout:

**Pattern A: Engine + Fan-out** (most common)
Use when: Student built a core analysis system that produces multiple outputs.
Structure: Input question → Engine block → Branch to output columns → File tree
Example: "Asked a question → analysis engine → experiment design + charts + deep dives → organized output"

**Pattern B: Linear Pipeline**
Use when: Student built a sequential multi-step pipeline.
Structure: Numbered steps flowing top to bottom, each with a badge (agent/python).
Example: "Data in → clean → analyze → visualize → report out"

**Pattern C: Component Showcase**
Use when: Student built several independent components (agents, skills, helpers)
that don't form a single pipeline.
Structure: Component count chips at top → individual component boxes with details → stats.
Example: "Built 3 agents + 2 helpers + 1 skill, each doing different things"

Most students will fit Pattern A. When in doubt, use Pattern A.

### Step 3: Generate the HTML

Read the design system reference at `references/design-system.html` in this
skill's directory. This file contains:
- All CSS classes and their visual styling
- A complete working example (Pattern A: engine + fan-out)
- Color variants for each component type

**Generate a complete, self-contained HTML file** using the CSS from the design
system. Copy the full `<style>` block from the reference, then write custom HTML
in the `<div class="content">` section for this specific student's build.

#### Available CSS components

**Layout:**
- `.slide` — 1080x1080 container (always use this)
- `.top-bar`, `.grid-bg`, `.glow`, `.brand` — background effects (always include)
- `.content` — padded flex column for all content
- `.section-divider` — subtle gradient line between sections
- `.flow-arrow` — centered `▼` between sections

**Header (always include):**
- `.eyebrow` — "BUILT WITH AI ANALYST LAB"
- `.title` + `.accent` — main headline with amber accent word
- `.subtitle` — one-line description

**Core blocks:**
- `.input-question` — the prompt/question that started the analysis
- `.engine-block` — the hero component (amber double-border, gradient fill)
  - `.engine-label` — uppercase label
  - `.engine-stack` — horizontal row of tool chains
  - `.engine-item` — individual tool chain (`.tool` for names, `.arrow` for →)

**Fan-out/Fan-in:**
- `.branch` container with `.branch-center-in` + `.branch-lines` + `.branch-drop`
- `.output-row` — flex row of output boxes
- Converge: `.converge-lines` + `.converge-drop` + `.converge-center-out`

**Output boxes** (5 color variants):
- `.output-box.agent` — indigo/purple (for AI agents)
- `.output-box.helper` — emerald/green (for Python helpers)
- `.output-box.output` — amber (for charts, reports, deliverables)
- `.output-box.data` — cyan (for data sources, databases)
- `.output-box.skill` — blue (for skills)
- Inside: `.box-label`, `.box-title`, `.box-items` (with `li` and `li.highlight`), `.box-count`

**File tree box:**
- `.file-tree-box` — shows organized output directory structure
- `.file-tree` with `.dir`, `.file`, `.count`, `.check` spans

**Component chips** (Pattern C):
- `.component-row` — horizontal row
- `.component-chip` with variants `.agent`, `.helper`, `.skill`, `.output`
- Inside: `.chip-count` (big number) + `.chip-label` (small label)

**Numbered steps** (Pattern B):
- `.steps-col` — vertical column
- `.step` with variants `.agent-step`, `.python-step`, `.output-step`
- Inside: `.step-node` (number), `.step-content` (`.step-title` + `.step-desc`), `.step-badge`

**Stats row (always include):**
- `.stats-row` with `.stat-item` containing `.stat-dot` + `.stat-text` (with `.num` spans)

#### Design rules

1. **Always 1080x1080.** This is LinkedIn's square format. The `.slide` class handles this.
2. **Tell a story top-to-bottom.** Input at top, output at bottom. The eye follows the flow.
3. **The engine block is the hero.** If they built a core system, give it the `.engine-block` treatment.
4. **Use color to distinguish component types.** Don't make everything amber — use purple for agents, green for helpers, cyan for data.
5. **Include real details.** Don't just say "charts" — list what charts. Don't just say "agent" — say what it does.
6. **Keep it tight but breathable.** Everything must fit in 1080x1080 without scrolling. But don't cram — whitespace makes it professional.
7. **Count things for the stats row.** Agents, charts, tests, lines of code — concrete numbers make it impressive.

### Step 4: Save and Open

Save the HTML file to the repo root:

```
showcase.html
```

Then open it in the browser:

```bash
open showcase.html
```

### Step 5: Tell the Student

Say something like:

**"Your LinkedIn showcase is open in your browser. Screenshot it and post it! Here's a caption suggestion:"**

Then draft a short LinkedIn caption (2-3 sentences, first person) that goes
with the image. Something like:

> Built this in a day at the AI Analyst Lab bootcamp. An AI-powered analysis
> engine that goes from business question to experiment design + 18 charts,
> fully organized. Wild what's possible with Claude Code + good architecture.

### Step 6: Clean up

The `showcase.html` file is for screenshot purposes only — remind the student
they can delete it after screenshotting. Don't commit it.

## Rules
1. The student should NOT have to explain what they built — Claude figures it out
2. Every showcase must be exactly 1080x1080 pixels
3. Copy the FULL CSS from the design system reference — don't write custom CSS
4. Only customize the HTML structure inside `.content`
5. Always include: header, main architecture section, stats row, brand watermark
6. Use real data from the student's code — never make up file names or counts
7. The visual should look like a product launch page, not a homework assignment
