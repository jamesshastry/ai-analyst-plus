# Skill: Show Off LinkedIn

## Purpose
Generate a beautiful, screenshot-ready HTML architecture diagram of what the
user built — designed for posting on LinkedIn. Claude analyzes the user's
code, understands their architecture, and generates a custom 1080x1080 visual
in the AI Analyst Lab brand style.

The user does nothing except type `/show-off-linkedin`, confirm the post,
and hit Post on LinkedIn. Claude handles everything else — renders the image,
drafts the caption, opens LinkedIn, and copies the caption to clipboard.

## When to Use
- User says `/show-off-linkedin` or "LinkedIn showcase" or "share on LinkedIn"
- After completing a significant milestone and wanting to share on LinkedIn

## Invocation
`/show-off-linkedin` — generate a LinkedIn-ready architecture diagram

## Instructions

### Step 1: Find the User's Work

Same detection logic as `/show-off`. Do NOT ask the user to explain anything.

1. **Run `git status --short`** to see untracked (`??`) and modified (`M`) files
2. **Run `git diff`** to see what they changed in existing files
3. **Read the new/modified files** to understand what they actually contain

If the user HAS made commits:
4. **Run `git log --oneline --all --not --remotes`** to find local-only commits
5. Combine committed changes with uncommitted work

**Ignore** `.env`, `.gitignore`, `node_modules/`, lockfiles, `__pycache__/`, etc.

**Understand the architecture** — what components exist, how they connect,
what data flows where. Focus on agents, skills, helpers, analysis outputs,
charts, and pipelines. Count things: how many agents, how many charts, how
many tests, how many lines of code they wrote.

### Step 2: Choose a Layout Pattern

Based on what the user built, choose the best layout:

**Pattern A: Engine + Fan-out** (most common)
Use when: User built a core analysis system that produces multiple outputs.
Structure: Input question → Engine block → Branch to output columns → File tree
Example: "Asked a question → analysis engine → experiment design + charts + deep dives → organized output"

**Pattern B: Linear Pipeline**
Use when: User built a sequential multi-step pipeline.
Structure: Numbered steps flowing top to bottom, each with a badge (agent/python).
Example: "Data in → clean → analyze → visualize → report out"

**Pattern C: Component Showcase**
Use when: User built several independent components (agents, skills, helpers)
that don't form a single pipeline.
Structure: Component count chips at top → individual component boxes with details → stats.
Example: "Built 3 agents + 2 helpers + 1 skill, each doing different things"

Most users will fit Pattern A. When in doubt, use Pattern A.

### Step 3: Generate the HTML

Read the design system reference at `references/design-system.html` in this
skill's directory. This file contains:
- All CSS classes and their visual styling
- A complete working example (Pattern A: engine + fan-out)
- Color variants for each component type

**Generate a complete, self-contained HTML file** using the CSS from the design
system. Copy the full `<style>` block from the reference, then write custom HTML
in the `<div class="content">` section for this specific user's build.

#### Available CSS components

**Layout:**
- `.slide` — 1080x1080 container (always use this)
- `.top-bar`, `.grid-bg`, `.glow`, `.brand` — background effects (always include)
- `.content` — padded flex column for all content
- `.flow-section` — **IMPORTANT**: wrap the core flow (engine → branch → outputs → converge → arrow) in this. It uses `flex: 1` + `justify-content: center` to fill the middle of the slide evenly and prevent dead space at the bottom.
- `.bottom-section` — wrap file-tree + stats in this. Uses `margin-top: auto` to anchor at the bottom.
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
6. **Fill the full 1080x1080 — no dead space.** Use `.flow-section` around the core flow and `.bottom-section` around file-tree + stats. This distributes content evenly so there's no blank gap at the bottom. People view these on phones — make text readable.
7. **Count things for the stats row.** Agents, charts, tests, lines of code — concrete numbers make it impressive.

### Step 4: Render to PNG

Save the HTML file to the repo root as `showcase.html`, then render it to
a crisp PNG using the render script:

```bash
node scripts/render-showcase.mjs showcase.html showcase.png
```

This produces a 2160x2160 retina PNG (2x scale of 1080x1080) — perfect for
LinkedIn's image quality. The first run installs puppeteer and downloads
Chromium (~280MB), subsequent runs are instant.

Also copy the PNG to the user's Desktop so they can find it easily:

```bash
cp showcase.png ~/Desktop/showcase.png
```

If the render script fails (missing Node.js, Chromium issues), fall back to
opening the HTML in the browser and telling the user to screenshot manually.

### Step 5: Draft the LinkedIn Caption

Write a short caption — **4-6 lines max, under 200 characters total.** This
must fit in a LinkedIn URL parameter, so brevity is non-negotiable.

The image IS the post. The caption just sets up what they're looking at and
invites engagement. Think of it like a text message about something cool you
built, not a LinkedIn thought piece.

#### Rules

- **Lead with what they built, not where they were.** "Built an analysis
  pipeline that does X" not "Just tried out AI Analyst Lab"
- **One specific number.** 18 charts, 3 agents, 50K rows — pick the most
  impressive one
- **No hashtags. No emojis. No "I'm thrilled to announce."**
- **End with a short engagement hook.** "Want to see how?" or "Comment if
  you want the details" — one line, casual
- **Write like a text message.** If it sounds like a LinkedIn influencer
  wrote it, rewrite it. If it sounds like AI wrote it, rewrite it harder.
- **Mention AI Analyst Lab naturally** — as context, not a pitch

#### Example captions (for tone, adapt to what they actually built):

- "Built an analysis pipeline today that takes a business question and comes
  back with charts + experiment designs. Want to see how it works?"

- "3 AI agents, 18 charts, zero Python written by me. Built this in a day.
  Comment if you want the details."

- "Asked my AI analyst one question. Got back a full experiment design with
  power analysis. This is what I built today."

### Step 6: Confirm Before Posting

Show the user:
1. The rendered PNG (open it: `open showcase.png`)
2. The LinkedIn caption

Ask: **"Here's your LinkedIn showcase and caption. Want me to open LinkedIn
so you can post it, or change anything first?"**

Do NOT proceed until they confirm.

### Step 7: Post to LinkedIn

The caption goes in the URL (auto-fills the compose box). The image goes on
the clipboard (user pastes once). One paste, one click.

```bash
# Put the image on the clipboard
osascript -e 'set the clipboard to (read (POSIX file "PNG_ABSOLUTE_PATH") as «class PNGf»)'

# Open LinkedIn with caption pre-filled via URL parameter
# IMPORTANT: URL-encode the caption text. It MUST be under 200 chars or it gets truncated.
open "https://www.linkedin.com/feed/?shareActive=true&text=URL_ENCODED_CAPTION"
```

Tell the user:

**"LinkedIn is open with your caption. Cmd+V to paste your image, then hit Post!"**

**Fallback:** If pasting the image doesn't work in LinkedIn's composer, tell
the user: "Click the image icon in the composer and select `showcase.png`
from your Desktop."

### Step 8: Clean up

After they've posted (or decided not to), the `showcase.html` and
`showcase.png` files can be deleted — they're not part of the project:

```bash
rm -f showcase.html showcase.png
```

Don't auto-delete — ask first or just mention they can clean up.

## Rules
1. The user should NOT have to explain what they built — Claude figures it out
2. Every showcase must be exactly 1080x1080 pixels
3. Copy the FULL CSS from the design system reference — don't write custom CSS
4. Only customize the HTML structure inside `.content`
5. Always include: header, main architecture section, stats row, brand watermark
6. Use real data from the user's code — never make up file names or counts
7. The visual should look like a product launch page, not a homework assignment
