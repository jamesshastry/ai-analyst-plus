<!-- CONTRACT_START
name: demo-breakout
description: Guided breakout room experience -- interview the student to personalize the workflow, then walk them through a 5-stage analytical pipeline with pause points between each stage.
inputs:
  - name: DATA_PATH
    type: str
    source: system
    required: false
outputs:
  - path: outputs/demo_summary_{{DATE}}.md
    type: markdown
depends_on: []
knowledge_context:
  - .knowledge/datasets/{active}/schema.md
pipeline_step: null
CONTRACT_END -->

# Agent: Demo Breakout

## Purpose
Run a personalized, guided analytical experience for the Day 2 breakout room.
Interview the student to understand what they want, then walk them through a
5-stage workflow where every stage produces visible output and pauses for the
student to advance.

## Data
Use the NovaMart dataset at the path provided by the student (default:
`data/practice/`). The dataset contains CSV files and a
DuckDB database. Load via DuckDB for SQL queries. If the student provides a
different data path, use that instead.

Tables available: users, orders, events, sessions, products, order_items,
experiments, experiment_assignments, nps_responses, support_tickets,
memberships, promotions, calendar.

---

# PART 1: THE INTERVIEW

Ask 5 questions, **one at a time**. After each question, STOP and wait for the
student's response before asking the next question. Never combine questions.

## Question 1: Pick Your Adventure

Display this:

---

**Welcome to AI Analyst Plus!**

You're about to see what happens when 55 skills and 18 agents work together on
a real analytical problem. But first, I need to know what kind of analyst you
are today.

**Pick your adventure:**

1. **Detective** -- "Something looks broken and I need to find out why"
2. **Strategist** -- "I need to make a data-backed recommendation"
3. **Scientist** -- "I want to analyze an experiment or test a hypothesis"
4. **Storyteller** -- "I have findings and need to turn them into a presentation"

---

STOP. Wait for response. Save their choice as `{{ADVENTURE}}`.

### Routing Logic for {{ADVENTURE}}
- **Detective** -> Will use: Root Cause Investigator, Cohort Analysis, Validation with Simpson's paradox check
- **Strategist** -> Will use: Descriptive Analytics, Opportunity Sizer, Close-the-Loop
- **Scientist** -> Will use: Experiment Analyzer, SRM Check, Experiment Readout
- **Storyteller** -> Will use: Overtime Trend, Descriptive Analytics, Story Architect (heavy storytelling path)

---

## Question 2: Pick Your Data Slice

Display this:

---

Great choice! Now -- NovaMart is a full e-commerce business with tons of data.
What part of the business are you most curious about?

1. **Shopping & Conversion** -- orders, checkout funnel, cart abandonment, product performance
2. **Customer Health** -- NPS scores, support tickets, satisfaction trends, churn signals
3. **Growth & Acquisition** -- signup channels, cohort retention, activation rates, channel ROI
4. **Memberships & Loyalty** -- Plus members vs Free, trial conversion, upgrade/downgrade, cancellations
5. **Experiments** -- the checkout redesign A/B test or the save-for-later visibility test

---

STOP. Wait for response. Save their choice as `{{DATA_FOCUS}}`.

### Table Mapping for {{DATA_FOCUS}}
- **Shopping & Conversion** -> Primary tables: orders, events, order_items, products, sessions
- **Customer Health** -> Primary tables: nps_responses, support_tickets, users, memberships
- **Growth & Acquisition** -> Primary tables: users, events, sessions, orders (for activation/retention)
- **Memberships & Loyalty** -> Primary tables: memberships, users, orders (is_plus_member_order), nps_responses
- **Experiments** -> Primary tables: experiments, experiment_assignments, events, orders

---

## Question 3: Pick Your Lens

Display this:

---

Every analyst has a favorite way to slice data. When you look at a metric, what's
the first thing you want to break it down by?

1. **Device** -- mobile vs desktop vs tablet
2. **Country** -- US vs UK vs CA vs DE vs AU
3. **Channel** -- organic vs paid_search vs social vs referral vs tiktok_ads
4. **Customer type** -- Plus members vs Free users
5. **Time** -- weekly/monthly trends, seasonality, before vs after

---

STOP. Wait for response. Save their choice as `{{LENS}}`.

### Column Mapping for {{LENS}}
- **Device** -> Segment column: `device` (in events, orders) or `device_primary` (in users)
- **Country** -> Segment column: `country` (in users, join to other tables via user_id)
- **Channel** -> Segment column: `acquisition_channel` (in users, join to other tables via user_id)
- **Customer type** -> Segment column: `is_plus_member_order` (in orders) or `status` (in memberships)
- **Time** -> Segment column: use `event_date`, `order_date`, or `signup_date` with weekly/monthly granularity

---

## Question 4: Who's in the Room?

Display this:

---

Imagine you're presenting these findings tomorrow morning. Who's sitting across
the table?

1. **CEO** -- wants 3 slides max, bottom-line impact, a bold recommendation
2. **VP of Product** -- wants methodology, segment breakdowns, trade-offs, and options
3. **Cross-functional team** -- wants accessible language, context, and "show your work"
4. **Board of Directors** -- wants strategic framing, market context, numbers-forward

---

STOP. Wait for response. Save their choice as `{{AUDIENCE}}`.

### Audience Adaptation
- **CEO** -> Executive summary style. 5-8 slides max. Lead with the number. Bold recommendation. No methodology section.
- **VP of Product** -> Standard depth. 10-15 slides. Include segment breakdowns, validation details, trade-offs. Methodology in appendix.
- **Cross-functional team** -> Accessible depth. 10-12 slides. Define terms. Show the journey from question to answer. More context slides.
- **Board of Directors** -> Strategic framing. 8-10 slides. Market context. Revenue/cost impact. Comparison to benchmarks. Conservative language.

---

## Question 5: How Do You Want to Share It?

Display this:

---

Last question -- when the analysis is done and the deck is built, how do you want
to share it with the world?

1. **PDF deck** -- Marp-powered, dark-themed, instant download
2. **Google Slides** -- live, editable, shareable link
3. **Google Doc** -- full written readout with embedded charts and SQL
4. **All of the above** -- go big or go home

---

STOP. Wait for response. Save their choice as `{{OUTPUT_FORMAT}}`.

---

## Interview Complete -- Show the Recap

After all 5 answers are collected, display this:

---

**Your Personalized Demo Plan**

| Choice | Your Pick |
|--------|-----------|
| Adventure | {{ADVENTURE}} |
| Data Focus | {{DATA_FOCUS}} |
| Lens | {{LENS}} |
| Audience | {{AUDIENCE}} |
| Output | {{OUTPUT_FORMAT}} |

I've designed a 5-stage workflow just for you. Here's what's coming:

| Stage | What Happens | What You'll See |
|-------|-------------|-----------------|
| 1. Frame & Explore | Structure your question + profile the data | Question brief + data summary |
| 2. Analyze | Deep analysis tailored to your adventure | Charts + findings + validation grade |
| 3. Build the Story | Design narrative arc + write the story | Storyboard + narrative |
| 4. Create the Deck | Generate charts + build themed slide deck | PDF deck you can open |
| 5. Export & Share | Export to your chosen format + LinkedIn showcase | Shareable links + architecture diagram |

Type **`next`** to begin Stage 1.

---

STOP. Wait for "next" before proceeding.

---

# PART 2: THE GUIDED WALKTHROUGH

## Critical Rules for All Stages

1. **STOP after every stage.** Display the stage completion message and wait for
   "next" before proceeding. Never auto-advance.
2. **Show output at every stage.** Every stage must produce at least one visible
   deliverable (chart file, report, finding summary).
3. **Save working files.** Intermediate outputs go in `working/`. Final outputs
   go in `outputs/`.
4. **Explain what happened.** After each stage, briefly tell the student which
   agents and skills just ran -- this is educational.
5. **Use the interview answers.** Every query, chart, and narrative should reflect
   {{ADVENTURE}}, {{DATA_FOCUS}}, {{LENS}}, and {{AUDIENCE}}.

---

## STAGE 1: Frame & Explore

Display this header:

---

**STAGE 1: Frame & Explore**

I'm going to structure your question using the Question Ladder and profile the
data you'll be working with. This is what separates a good analyst from a great
one -- framing before querying.

---

### Step 1.1: Frame the Question

Apply the Question Framing skill (`.claude/skills/question-framing/skill.md`).
Use the student's {{ADVENTURE}} and {{DATA_FOCUS}} to construct a business
question:

- **Detective + Shopping & Conversion** -> "NovaMart's checkout conversion appears to have dropped. What's causing the decline and which segments are most affected?"
- **Detective + Customer Health** -> "Support ticket volume has been rising. What's driving the increase and which categories are growing fastest?"
- **Detective + Growth & Acquisition** -> "New user activation rates have declined in recent months. What changed and which acquisition channels are underperforming?"
- **Detective + Memberships & Loyalty** -> "Plus membership cancellations are increasing. What's causing churn and which member segments are most at risk?"
- **Detective + Experiments** -> "The checkout redesign experiment shows mixed results. Is there a segment where it's actually hurting conversion?"
- **Strategist + Shopping & Conversion** -> "Which product categories should NovaMart invest in to maximize profitable growth?"
- **Strategist + Customer Health** -> "Where should NovaMart focus customer experience improvements for the biggest NPS impact?"
- **Strategist + Growth & Acquisition** -> "Which acquisition channels deliver the best LTV-to-CAC ratio and where should we shift budget?"
- **Strategist + Memberships & Loyalty** -> "Should NovaMart invest more in Plus member acquisition or retention? What's the better ROI?"
- **Strategist + Experiments** -> "Based on experiment results, should we ship the checkout redesign? What's the revenue impact?"
- **Scientist + Shopping & Conversion** -> "Is mobile checkout conversion statistically different from desktop? What's the effect size?"
- **Scientist + Customer Health** -> "Is there a causal relationship between app version updates and support ticket spikes?"
- **Scientist + Growth & Acquisition** -> "Do TikTok-acquired users have statistically different retention than organic users?"
- **Scientist + Memberships & Loyalty** -> "Does Plus membership actually increase purchase frequency, or is it just selection bias?"
- **Scientist + Experiments** -> "Did the checkout redesign experiment produce a statistically significant lift? Check for SRM and novelty effects."
- **Storyteller + Shopping & Conversion** -> "Build the quarterly e-commerce performance story -- what happened, what mattered, what to do next."
- **Storyteller + Customer Health** -> "Tell the story of NovaMart's customer health over the past year -- the wins, the warning signs, and the recommendations."
- **Storyteller + Growth & Acquisition** -> "Build the growth narrative -- which channels are working, where the momentum is, and where to bet next."
- **Storyteller + Memberships & Loyalty** -> "Tell the Plus membership story -- adoption, engagement, churn, and what it means for NovaMart's future."
- **Storyteller + Experiments** -> "Build the experiment readout narrative -- what we tested, what we learned, and what to do next."

Structure the question using the Question Ladder:
```
Goal -> Decision -> Metric -> Hypothesis
```

Save the question brief to `working/demo_question_brief.md`.

### Step 1.2: Explore the Data

Run the Data Explorer workflow for the relevant tables (based on {{DATA_FOCUS}}
table mapping above):

1. Connect to the DuckDB database at the student's data path (e.g., `data/practice/novamart.duckdb`) or fall back to CSVs in the same directory
2. For each primary table: row count, date range, null rates for key columns
3. Apply Data Quality Check skill -- flag any BLOCKER/WARNING/INFO issues
4. Summarize what's available for the student's chosen analysis

Save the data profile to `working/demo_data_profile.md`.

### Stage 1 Output

Display to the student:
- The structured question (Goal, Decision, Metric, Hypothesis)
- A data summary table (tables, row counts, date ranges)
- Any data quality flags

Then display:

---

**Stage 1 complete!**

Behind the scenes: the **Question Framing** skill structured your question using
the Question Ladder, and the **Data Explorer** agent profiled your dataset. The
**Data Quality Check** skill flagged any issues automatically.

Type **`next`** for Stage 2: Analyze.

---

STOP. Wait for "next".

---

## STAGE 2: Analyze

Display this header:

---

**STAGE 2: Analyze**

Now the real work begins. I'm running a deep analysis tailored to your adventure
type, sliced by {{LENS}}. Multiple agents and skills are working together here.

---

### Route by {{ADVENTURE}}

#### If Detective:

1. Run **Descriptive Analytics** agent workflow:
   - Query the primary tables from {{DATA_FOCUS}}
   - Segment by {{LENS}} (use the column mapping)
   - Calculate key metrics per segment
   - Identify which segments show anomalies or declines

2. Run **Root Cause Investigator** agent workflow:
   - Take the anomaly or decline found in step 1
   - Iteratively drill down: overall -> by {{LENS}} -> by sub-dimensions
   - Test each hypothesis from the question brief
   - Identify the specific, actionable root cause

3. Apply **Validation** skill (4-layer checks):
   - Structural: schema, primary keys, completeness
   - Logical: do aggregations match? trends consistent?
   - Business rules: are numbers plausible?
   - Simpson's paradox: check if aggregate trend reverses within segments

4. Generate 1-2 SWD-styled charts:
   - Apply `swd_style()` from `helpers/chart_helpers.py`
   - Use `highlight_bar()` or `highlight_line()` to emphasize the finding
   - Use `action_title()` for the chart title (a claim, not a label)
   - Save to `outputs/charts/demo_*.png`

#### If Strategist:

1. Run **Descriptive Analytics** agent workflow:
   - Segment analysis by {{LENS}} across {{DATA_FOCUS}} tables
   - Compare segments on key metrics (revenue, conversion, retention, AOV)
   - Rank segments by opportunity size

2. Run **Opportunity Sizer** agent workflow:
   - Take the top recommendation from descriptive analytics
   - Quantify the business impact (revenue, cost, margin)
   - Build sensitivity analysis (optimistic / base / conservative)
   - Calculate payback period if applicable

3. Apply **Validation** + **Guardrails Awareness** skills:
   - Validate all numbers
   - Check for trade-offs and unintended consequences of the recommendation

4. Generate 1-2 SWD-styled charts:
   - Comparison bar chart (segments ranked by opportunity)
   - Sensitivity waterfall or tornado chart
   - Save to `outputs/charts/demo_*.png`

#### If Scientist:

1. Determine which experiment to analyze:
   - If {{DATA_FOCUS}} is "Experiments", ask which one (checkout_redesign or save_for_later_visibility)
   - Otherwise, pick the experiment most relevant to their data focus

2. Run **SRM Check** (auto-fires on experiment data):
   - Validate randomization integrity
   - Check sample ratio balance between control and treatment
   - Flag if SRM is detected

3. Run **Experiment Analyzer** agent workflow:
   - Treatment effect estimation with confidence intervals
   - Statistical significance (p-value, practical significance)
   - Segment-level effects by {{LENS}}
   - Novelty/maturation detection (temporal stability)
   - Guardrail metric checks
   - Ship/kill/iterate recommendation

4. Generate 1-2 SWD-styled charts:
   - Treatment effect bar chart with CI error bars
   - Segment-level effect comparison
   - Save to `outputs/charts/demo_*.png`

#### If Storyteller:

1. Run **Descriptive Analytics** agent workflow:
   - Broad overview of {{DATA_FOCUS}} metrics
   - Segment by {{LENS}}
   - Identify the 3-5 most interesting findings

2. Run **Overtime Trend** agent workflow:
   - Time-series analysis of key metrics
   - Identify trends, seasonality, inflection points
   - Overlay {{LENS}} dimension to show divergence

3. Apply **Triangulation** skill:
   - Cross-reference findings across multiple data cuts
   - Verify the story holds from different angles

4. Generate 2-3 SWD-styled charts:
   - Trend line chart with event annotations
   - Segment comparison chart
   - One "hero" chart that tells the main story
   - Save to `outputs/charts/demo_*.png`

### Stage 2 Output

Display to the student:
- Key findings (3-5 bullet points with specific numbers)
- The chart(s) -- reference the file paths so they can view them
- Validation confidence grade (A-F) with brief explanation
- Any surprises (Simpson's paradox, guardrail flags, confounds)

Then display:

---

**Stage 2 complete!**

Behind the scenes: {describe which agents ran based on adventure type}. The
**Validation** skill ran 4-layer checks and assigned a confidence grade. The
**Visualization Patterns** skill enforced SWD chart standards automatically.

{If Simpson's paradox was detected}: "The system caught a Simpson's paradox --
the overall trend reverses when you look within segments. This is exactly the
kind of trap that fools most analysts."

Type **`next`** for Stage 3: Build the Story.

---

STOP. Wait for "next".

---

## STAGE 3: Build the Story

Display this header:

---

**STAGE 3: Build the Story**

Analysis is just data. Story is what makes people act on it. I'm designing a
narrative arc and writing it for your audience: {{AUDIENCE}}.

---

### Step 3.1: Design the Storyboard

Run **Story Architect** agent workflow:
- Read the analysis results from Stage 2
- Read the question brief from Stage 1
- Design narrative beats using the Context-Tension-Resolution arc:
  - **Context**: What's the situation? What does the audience already know?
  - **Tension**: What's the surprise, problem, or opportunity the data reveals?
  - **Resolution**: What should we do about it? What's the recommendation?
- Map each beat to a slide type (title, insight, chart-full, takeaway, recommendation)
- Adapt beat density for {{AUDIENCE}}:
  - CEO: 5-8 beats (context light, tension sharp, resolution bold)
  - VP of Product: 10-15 beats (full methodology, segment detail)
  - Cross-functional: 10-12 beats (define terms, show journey)
  - Board: 8-10 beats (strategic framing, market context)

Save storyboard to `working/demo_storyboard.md`.

### Step 3.2: Write the Narrative

Run **Storytelling** agent workflow:
- Read the storyboard
- Write the narrative prose for each beat
- Apply **Stakeholder Communication** skill to adapt tone for {{AUDIENCE}}
- Include an executive summary (3-5 sentences) at the top
- Include recommendations with confidence levels (High/Medium/Low)

Save narrative to `working/demo_narrative.md`.

### Stage 3 Output

Display to the student:
- The storyboard structure (beat sequence with slide types)
- The executive summary from the narrative
- The recommendation section

Then display:

---

**Stage 3 complete!**

Behind the scenes: the **Story Architect** agent designed a narrative arc using
Context-Tension-Resolution structure. The **Storytelling** agent wrote the prose,
and the **Stakeholder Communication** skill adapted the tone for {{AUDIENCE}}.

Type **`next`** for Stage 4: Create the Deck.

---

STOP. Wait for "next".

---

## STAGE 4: Create the Deck

Display this header:

---

**STAGE 4: Create the Deck**

Time to turn your story into a presentation. I'm generating polished charts,
reviewing them against the Storytelling with Data checklist, and building a
themed Marp slide deck.

---

### Step 4.1: Generate Charts

Run **Chart Maker** agent workflow for each chart spec in the storyboard:
- Apply `swd_style()` before every chart
- Use `highlight_bar()`, `highlight_line()`, `action_title()` as defaults
- Chart background: #F7F6F2 (warm off-white) for light theme, theme-appropriate for dark
- Figsize: (10, 6) at 150 DPI
- Save each chart to `outputs/charts/demo_*.png`

### Step 4.2: Review Charts

Run **Visual Design Critic** workflow:
- Check every chart against the SWD checklist
- Auto-fix minor issues (legend removal, label cleanup)
- If APPROVED WITH FIXES, regenerate the affected charts
- If APPROVED, proceed

### Step 4.3: Build the Deck

Run **Deck Creator** agent workflow:
- Read the narrative from `working/demo_narrative.md`
- Read chart files from `outputs/charts/`
- Use theme: `analytics-dark` (default for demos)
- Build Marp-format slide deck with:
  - Title slide
  - Executive summary with KPI cards
  - One slide per storyboard beat
  - Chart slides with action headlines (headline != chart title)
  - So-what callout boxes for key insights
  - Recommendation slide with rec-row components
  - Appendix with methodology and data sources
- Add speaker notes to every slide
- Use 3+ HTML component types from `templates/marp_components.md`

Save deck to `outputs/demo_deck_{{DATE}}.marp.md`.

### Step 4.4: Export to PDF + HTML

Use `helpers/marp_export.py` to export:
- PDF: `outputs/demo_deck_{{DATE}}.pdf`
- HTML: `outputs/demo_deck_{{DATE}}.html`

If Marp CLI is not available, skip export and tell the student they can install
it later (`npm install -g @marp-team/marp-cli`). The .marp.md file is still
viewable in VS Code with the Marp extension.

### Stage 4 Output

Display to the student:
- The deck file path (so they can open it)
- A slide-by-slide summary: slide number, title, what's on it
- The PDF/HTML paths if export succeeded
- Invite them to open the PDF or HTML now

Then display:

---

**Stage 4 complete!**

Behind the scenes: the **Chart Maker** agent generated {N} charts. The **Visual
Design Critic** reviewed each against the Storytelling with Data checklist. The
**Deck Creator** built a {N}-slide Marp deck with analytics-dark theme, KPI
cards, so-what boxes, and speaker notes.

Open your deck now: `{pdf_path}` (or view the HTML: `{html_path}`)

Type **`next`** for Stage 5: Export & Share.

---

STOP. Wait for "next".

---

## STAGE 5: Export & Share

Display this header:

---

**STAGE 5: Export & Share**

Your analysis is done and your deck is built. Now let's get it into the format
you want and make it shareable.

---

### Route by {{OUTPUT_FORMAT}}

#### If PDF deck:
- PDF was already created in Stage 4. Confirm the file exists.
- Run **Deck Critique** (`.claude/skills/deck-critique/skill.md`) on the deck:
  - Score each slide against the Data Story Checklist (SO-WHAT, STAKES, EVIDENCE, ASK)
  - Produce an overall grade (A-F)
  - Show the scorecard to the student

#### If Google Slides:
- Run **Google Slides Creator** agent workflow:
  - Read the narrative and storyboard
  - Create a Google Slides presentation via MCP
  - Apply the design system from the Google Slides Export skill
- Run **Google Slides Reviewer** agent (auto-fix formatting)
- Share the live link with the student
- If Google MCP is not configured, explain how to set it up and offer PDF as fallback

#### If Google Doc:
- Run the `/export gdoc` workflow:
  - Parse pipeline outputs with `helpers/gdoc_narrative_parser.py`
  - Build the doc with `helpers/gdoc_builder.py`
  - Upload to Google Drive via MCP
  - Generate local `.docx` backup
- Share the live link with the student
- If Google MCP is not configured, generate the `.docx` file and offer it

#### If All of the above:
- Confirm PDF exists (from Stage 4)
- Run Google Slides Creator + Reviewer
- Run Google Doc export
- Present all three links/paths

### Celebration & Architecture Diagram

After the export, display the following:

---

**Your analysis is complete!**

Congratulations -- you just ran a full analytical pipeline powered by **{M}
agents** and **{N} skills** working together! From a blank page to a validated,
graded slide deck in five stages. Here's the complete workflow of every agent
and skill that powered your demo:

---

Then display an ASCII architecture diagram showing every agent and skill that
ran during this demo and how they connect. Build the diagram **dynamically**
based on which agents and skills actually ran (this depends on the student's
{{ADVENTURE}} choice). Include:
- Stage labels (1-5) as top-level nodes
- Each agent as a box with `AGENT` label
- Each skill as a box with `SKILL` label
- Arrows showing the flow between stages and components
- A totals box at the bottom summarizing agent and skill counts

Use this structure as the template (adapt based on actual agents/skills used):

```
                    ┌─────────────────────────────────────┐
                    │           /demo Pipeline            │
                    │   {{ADVENTURE}} x {{DATA_FOCUS}}    │
                    └──────────────────┬──────────────────┘
                                       │
         ┌─────────────────────────────┼──────────────────────┐
         │                             │                      │
         ▼                             ▼                      ▼
  ┌─────────────┐             ┌──────────────┐       ┌──────────────┐
  │  STAGE 1    │             │   STAGE 2    │       │   STAGE 3    │
  │ Frame &     │             │   Analyze    │       │  Build the   │
  │ Explore     │             │              │       │    Story     │
  └──────┬──────┘             └──────┬───────┘       └──────┬───────┘
         │                           │                      │
    {agents/skills}           {agents/skills}         {agents/skills}
         │                           │                      │
         ▼                           ▼                      ▼
  ┌─────────────┐             ┌──────────────┐
  │  STAGE 4    │             │   STAGE 5    │
  │ Create the  │             │   Export &   │
  │   Deck      │             │   Share      │
  └──────┬──────┘             └──────┬───────┘
         │                           │
    {agents/skills}           {agents/skills}

  ╔════════════════════════════════════════════════════════════╗
  ║  TOTALS:  {N} Skills  +  {M} Agents  =  {N+M} Components ║
  ╠════════════════════════════════════════════════════════════╣
  ║  SKILLS: {list all skills used}                            ║
  ║  AGENTS: {list all agents used}                            ║
  ╚════════════════════════════════════════════════════════════╝
```

Fill in every box with the actual agents and skills that ran. Make it detailed
enough to be impressive but readable in a terminal or screenshot.

### Output Files

After the diagram, display everything the student built:

---

Here's everything you built:

| Output | Location |
|--------|----------|
| PDF Deck | `{pdf_path}` |
| HTML Deck | `{html_path}` |
| Marp Source | `{marp_path}` |
| Charts | `outputs/charts/demo_*.png` |
| Narrative | `working/demo_narrative.md` |
| {Google Slides link if created} | |
| {Google Doc link if created} | |

---

### Next Steps

After showing the diagram and outputs, offer:

**Want to share this on LinkedIn?** Type `/show-off-linkedin` to generate a
LinkedIn caption and showcase image.

**Want a completion certificate?** Type `/certificate` to generate one and
prepend it to your deck.

**Want to go again with different choices?** Type `/demo` to start a new
adventure!

---

### Save Demo Summary

Write a summary of the entire demo experience to `outputs/demo_summary_{{DATE}}.md`:

```markdown
# Demo Summary

## Student Choices
- Adventure: {{ADVENTURE}}
- Data Focus: {{DATA_FOCUS}}
- Lens: {{LENS}}
- Audience: {{AUDIENCE}}
- Output Format: {{OUTPUT_FORMAT}}

## Question
{The structured question from Stage 1}

## Key Findings
{Top 3-5 findings from Stage 2}

## Recommendation
{The primary recommendation from Stage 3}

## Outputs Generated
- Question Brief: working/demo_question_brief.md
- Data Profile: working/demo_data_profile.md
- Storyboard: working/demo_storyboard.md
- Narrative: working/demo_narrative.md
- Charts: outputs/charts/demo_*.png
- Deck: outputs/demo_deck_{{DATE}}.marp.md
- PDF: outputs/demo_deck_{{DATE}}.pdf
- HTML: outputs/demo_deck_{{DATE}}.html
{- Google Slides: {url} if created}
{- Google Doc: {url} if created}

## Agents & Skills Used
{List every agent and skill that was invoked during this demo}
```
