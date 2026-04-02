# Skill: Show Off

## Purpose
Automatically analyze what the student has built and share a visual showcase
to the AI Analyst Lab community on Slack. Claude does all the work — figures
out what the student changed, builds a beautiful ASCII diagram of their work,
writes a short narrative, and posts it.

The key challenge: this repo is a shared template that students clone and build
on top of. The skill must distinguish the student's work from what was already
in the repo. Never showcase the whole repo — only the student's additions and
modifications.

## When to Use
- User says `/show-off` or "share what I built" or "show the community"
- After completing an analysis, pipeline, or building something cool

## Invocation
`/show-off` — share what you've built with the community

## Prerequisites
- Slack MCP server must be configured with the student's user token
- If Slack MCP tools are not available, run the **Slack Connect Flow** below first

## Slack Connect Flow

If the student hasn't connected Slack yet (no `SLACK_TOKEN` in `.env`, or Slack MCP tools aren't available):

1. Tell them: **"First, let's connect your Slack account. I'm opening a link in your browser — sign in to Slack and click Allow."**
2. Run: `open "https://slack-auth.shane-aea.workers.dev"` to open the OAuth page in their browser
3. Tell them: **"After you click Allow, you'll see a token on the page. Copy it and paste it here."**
4. When they paste the token (starts with `xoxp-`):
   - Write it to `.env` file: `SLACK_TOKEN=xoxp-...`
   - Tell them: **"Got it! You'll need to restart Claude Code for Slack to connect. Run `claude` again and then `/show-off`."**
   - Stop here — they need to restart for the MCP to pick up the new token

## Instructions

### Step 1: Find the Student's Work

Do NOT ask the student to explain anything. Figure it out yourself.

The goal is to identify what THIS student built — not what was already in the
repo when they cloned it. Students typically clone the repo and start building
without committing, so their work shows up as untracked and modified files.

**Always start with `git status`** — this is the most reliable signal:

1. **Run `git status --short`** to see untracked (`??`) and modified (`M`) files
2. **Run `git diff`** to see what they changed in existing files
3. **Read the new/modified files** to understand what they actually contain

Untracked files (`??`) are things the student created from scratch. Modified
files (`M`) are things they customized. Together, these tell you what they built.

**If the student HAS made commits**, also check for their commits specifically:

4. **Run `git log --oneline --all --not --remotes`** to find local-only commits
   (commits the student made that aren't in the original repo)
5. If that returns results, **run `git diff <first-student-commit>~..HEAD --stat`**
   to see the cumulative changes from their commits
6. Combine committed changes with any uncommitted work from step 1

**Ignore files that aren't interesting for a showcase:** `.env`, `.gitignore`
changes, `node_modules/`, lockfiles, `__pycache__/`, etc.

**Understand what they built** — read the key files and figure out the
architecture: what components exist, how they connect, what data flows where.
Focus on agents, skills, helpers, analysis outputs, charts, and pipelines.

### Step 2: Write the Narrative

Write 2-3 sentences that explain what they built and what it does. This goes
BEFORE the diagram. It should answer: "What did I make and why is it cool?"

The narrative should be:
- Written in first person ("I built...")
- Specific about what the code actually does — not vague
- Mention the tools/techniques used (DuckDB, scipy, SWD style, etc.)
- Convey why it's impressive in plain language

**Examples** (for tone, don't copy):
- "I built an experiment design pipeline that takes a business question, runs
  power analysis on real data, and outputs publication-ready charts + a full
  design doc. Also built 18 SWD-style visualizations and a helper that
  auto-organizes every output."
- "I built a root cause investigator that drills through dimensions
  automatically until it finds the specific segment driving a metric change.
  Tested it on checkout drop-off — it found the iOS payment bug in 3 queries."

### Step 3: Build the ASCII Diagram

The diagram is the visual centerpiece. It should look beautiful and
professional — something people stop scrolling to look at. Think of it as
a mini architecture poster, not a quick sketch.

**Design principles:**

1. **Tell a story top-to-bottom.** Start with the input (a question, data
   source, or trigger) at the top. End with the output (charts, reports,
   organized files) at the bottom. The reader should follow the flow.

2. **Use visual hierarchy.** The most important component (the engine, the
   core pipeline) gets a double-line border (`╔═╗`). Everything else gets
   single-line (`┌─┐`). This draws the eye to what matters.

3. **Put detail inside boxes.** Use bullet points (`○`) to list what each
   component does. Show file trees with `├──` and `└──`. Don't leave boxes
   empty — they should tell you what's inside at a glance.

4. **Fan out and converge.** If the system produces multiple outputs, fan
   the flow out into parallel columns, then converge back. This creates a
   satisfying diamond shape.

5. **Use generous whitespace.** Don't cram boxes together. Let the diagram
   breathe. Padding inside boxes (empty lines above/below content) makes
   them readable.

6. **Keep lines aligned.** Vertical pipes (`│`) should be perfectly aligned.
   Horizontal connectors (`─`) should be consistent width. Sloppy alignment
   ruins the whole thing.

**Reference example** (adapt to what they actually built):

```
               "Should we redesign mobile checkout?"
                                │
                                ▼
               ╔═══════════════════════════════╗
               ║         ANALYSIS ENGINE       ║
               ║                               ║
               ║   DuckDB ──→ SQL ──→ pandas   ║
               ║   scipy  ──→ power analysis   ║
               ║   matplotlib ──→ SWD style    ║
               ╚═══════════════╤═══════════════╝
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
 ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
 │                 │ │                 │ │                 │
 │   EXPERIMENT    │ │    SHOWCASE     │ │   DEEP DIVES    │
 │    DESIGNER     │ │   10 charts     │ │    4 charts     │
 │                 │ │                 │ │                 │
 │  ○ power curve  │ │  ○ funnels     │ │  ○ rev bridge   │
 │  ○ device gap   │ │  ○ retention   │ │  ○ retention    │
 │  ○ decisions    │ │  ○ NPS         │ │  ○ funnel×dev   │
 │  ○ timeline     │ │  ○ channels    │ │  ○ promo ROI    │
 │                 │ │  ○ experiments │ │                 │
 │  + design doc   │ │  ○ forecast    │ │                 │
 │                 │ │  ○ promos      │ │                 │
 └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │                                 │
             │   run_dir.py                    │
             │                                 │
             │   outputs/                      │
             │    └── 2026-04-01_topic/        │
             │         ├── charts/             │
             │         │    └── 18 PNGs        │
             │         └── experiment_design.md│
             │                                 │
             │   symlink: latest → current run │
             │   tests: 12 passing ✅          │
             │                                 │
             └─────────────────────────────────┘
```

### Step 4: Compose the Post

The Slack message has three parts in this order:

1. **Narrative** (2-3 sentences from Step 2) — what you built and what it does
2. **Diagram** (from Step 3) — wrapped in triple backticks for monospace
3. No extra fluff — the narrative and diagram speak for themselves

### Step 5: Confirm Before Posting

Show the student the full message and ask:
**"Here's your showcase for #show-and-tell. Want me to send it, or change anything?"**

Do NOT post until they confirm.

### Step 6: Post to Slack

Post the message to the `#show-and-tell` channel using the Slack MCP.

Use the channel name `show-and-tell` when calling the Slack MCP send message tool.

Wrap the ASCII diagram in triple backticks so Slack renders it in monospace.

### Step 7: Celebrate

After posting, say something like:
**"Posted! 🎉 Check #show-and-tell to see it live. Keep building — you can `/show-off` again anytime."**

## Rules
1. Always confirm before posting — never auto-send
2. The student should NOT have to explain what they built — Claude figures it out
3. The ASCII diagram must be beautiful — use visual hierarchy, generous whitespace, and clean alignment
4. The narrative explains what it does — the diagram shows how it works
5. Works with or without git commits — `git status` is the primary detection method
6. Only showcase the student's work — never the whole repo
7. No limit on show-offs — encourage it every time they build something new
8. If they haven't run `/kickoff` yet, nudge them to do that first
