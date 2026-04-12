# `/export gdoc` Master Plan (Revised)

**Date:** 2026-04-03 (revised after Sravya's commit af4caeb)
**Status:** Ready for build
**Synthesized from:** 4 expert plans + debate + Sravya overlap analysis

---

## 0. What Changed Since v1 of This Plan

Sravya pushed commit af4caeb with 12 new skills and 11 new agents, including a
`google-doc-creator` agent, `google-doc-reviewer` agent, and `google-doc-export`
skill. Her approach uses a **different MCP server** (`mcp__google-workspace__*`)
with richer document manipulation tools (batch_update_doc, inspect_doc_structure,
insert_doc_image, etc.) than Shane's existing `mcp__google-docs__*` MCP.

**Key finding:** The `google-workspace` MCP is NOT installed on Shane's machine.
Only `google-docs-mcp-server` exists at `~/.claude/mcp-servers/`. Sravya's
agents reference tools that don't exist in the current environment.

**Decision:** Keep python-docx as the generation engine (v1). Sravya's agents
become the v2 path when/if the google-workspace MCP is installed. The revised
plan below integrates the best of both approaches.

### What we adopted from Sravya

| Concept | Source | How We Use It |
|---------|--------|---------------|
| Self-healing reviewer pattern | `google-doc-reviewer` agent | Conceptual — post-upload checklist. V1: human-readable review file. V2: auto-fix via google-workspace MCP. |
| Auth preflight | `auth-preflight` skill | Adapted for our `mcp__google-docs__*` MCP (check `token.json`, not `~/.google_workspace_mcp/`) |
| Session handoff | `session-handoff` skill | State yaml pattern adopted for `outputs/gdoc_export.yaml` |
| Chart-to-Drive workflow | `chart-to-drive` skill | Concept useful for v2 (direct API image insertion). V1 embeds in .docx so not needed yet. |
| Image dedup on resume | `google-doc-creator` agent Step 5.0 | Adopted conceptually for re-export detection (source hash comparison) |
| Bottom-to-top insertion | Multiple agents | N/A for python-docx (no index shifting). Relevant only for v2 direct API path. |
| Table spacing rules | `google-doc-reviewer` Check 8 | Adopted for python-docx table generation (add_paragraph before/after tables) |
| Bold label list | `google-doc-export` skill Section D | Merged — our 4 labels + Sravya's 4 additional labels |
| 9-check reviewer checklist | `google-doc-reviewer` agent | Adapted as post-conversion verification checklist (manual in v1, automated in v2) |

### What we kept from our original plan (not in Sravya's work)

| Feature | Why |
|---------|-----|
| Analysis Readout template (Summary → Primary Learnings with >> links → Recommendations → Analysis → Resources) | Shane's actual template structure; Sravya's is generic |
| .docx local fallback | Zero-auth path; Sravya's approach requires Google auth to produce any output |
| Internal bookmark links (>> pattern) | Dual reading paths for 30-second vs 30-minute readers |
| Confidence badge + D/F gate | Validation integration |
| SQL in gray-shaded monospace table cells | Professional SQL presentation |
| Re-export version tracking with source hash | Avoids unnecessary re-creation |
| Narrative-to-structure parser | Maps pipeline artifacts to template sections |
| Content source mapping table | Explicit artifact → section mapping |
| 13-scenario error handling matrix | Systematic failure coverage |
| `/export all` exclusion | External resource creation must be explicit |
| Figure captions with numbering | `*Figure N: [title]. Source: [dataset], [date].*` |

### What exists in Sravya's code but isn't needed for this feature

| Sravya's Asset | Status |
|----------------|--------|
| `google-slides-creator` + `google-slides-reviewer` + `google-slides-export` | Separate feature (slides, not docs). Requires google-workspace MCP. |
| Experiment lifecycle (brief, srm-check, analyzer, readout) | Orthogonal pipeline — no overlap with export. |
| Presentation remediation (deck-critique, slide-transform, deck-rescue) | Separate feature. |
| Analysis design (hypothesis-sharpener, confound-scanner, feedback-synthesizer) | Pre-analysis pipeline — no overlap. |
| `deck_parser.py` | Marp/Slides parsing helper — not relevant to docs. |

---

## 1. Executive Summary

We are adding a `gdoc` format to the existing `/export` skill. When a user types
`/export gdoc` after a completed analysis, the system:

1. Generates a formatted `.docx` locally using python-docx (charts, headings,
   bookmarks, code blocks, tables)
2. Uploads it to Google Drive via `upload_file_to_drive(convert_to_google_doc=True)`
3. Returns a Google Doc URL

The `.docx` is always generated first as a local fallback. OAuth is lazy (triggers
on first use). Re-export always creates a new Google Doc. The document follows the
**Analysis Readout** template: a Summary section (with Primary Learnings + >> links
and Recommendations) for the 30-second reader, a full Analysis section with charts
for the 30-minute reader, and a Resources appendix with SQL queries.

---

## 2. Architecture

```
/export gdoc
     |
     v
Step 0: Auth Check
  - Probe: call read_document on a known doc ID (lightweight)
  - If no MCP / auth expired: run authorize_google_docs inline
  - If auth fails entirely: generate .docx only + manual upload instructions
     |
     v
Step 1: Find Source Material (existing export skill logic)
  - Priority: outputs/narrative_*.md > outputs/analysis_report_*.md
    > working/storyboard_*.md > working/pipeline_summary.md
  - Collect charts: outputs/charts/*.png
  - Collect SQL: working/sql_queries/*.sql or inline from agent logs
  - Read validation: outputs/validation_*.md
  - Read close-the-loop: outputs/close_the_loop_*.md
     |
     v
Step 2a: Parse → Build .docx (fully local, no Google needed)
  - gdoc_narrative_parser.py reads pipeline artifacts → structured data
  - gdoc_builder.py maps to Analysis Readout template → .docx
  - Charts embedded via add_picture(width=Inches(6.0))
  - SQL in gray-shaded monospace table cells
  - Internal bookmarks: >> links from Summary to Analysis sections
  - Save: outputs/report_{SLUG}_{DATE}.docx
     |
     v
Step 2b: Upload to Google Drive
  - upload_file_to_drive(file_path=docx_path, convert_to_google_doc=True)
  - Returns: { file_id, url }
     |
     v
Step 2c: Post-Upload Verification (v1: report only)
  - Read converted doc via read_document(file_id)
  - Quick checks: heading count matches, image placeholder text absent
  - If issues detected: note them in the output message
  - (v2: if google-workspace MCP available, run self-healing reviewer)
     |
     v
Step 2d: Write State
  - Write outputs/gdoc_export.yaml
     |
     v
Step 3: Report to User
  - "Your analysis is ready: {url}"
  - Mention .docx fallback location
  - If verification found issues, note them
```

### Key architectural decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Generation engine | python-docx (local) | google-docs MCP `write_formatted_content` only supports 5 block types. google-workspace MCP not installed. python-docx supports everything. |
| Image embedding | Embedded in .docx via `add_picture()` | Single atomic upload. No per-chart Drive uploads. No tmpfiles.org dependency. |
| Upload mechanism | `upload_file_to_drive(convert=true)` via `mcp__google-docs__*` | One MCP call. Available on Shane's machine today. |
| Post-upload QA | Read-back check (v1), self-healing reviewer (v2) | v1 can only read plain text back via `read_document`. v2 with google-workspace MCP enables `inspect_doc_structure` + targeted fixes. |
| Re-export strategy | Always new doc | No replace/delete API via MCP. Protects user's manual edits. |
| State tracking | `outputs/gdoc_export.yaml` | Tracks versions, source hash, enables re-export detection. |
| OAuth timing | Lazy on first `/export gdoc` | Student is motivated at export time. .docx fallback covers failures. |
| `/export all` | Excluded | External resource creation should be explicit. |
| Sravya's agents | Dormant until google-workspace MCP installed | Her google-doc-creator/reviewer reference tools that don't exist on Shane's machine. |

### MCP Server Status

| Server | Config Key | Available? | Tools Used By This Plan |
|--------|-----------|------------|------------------------|
| `google-docs` | `mcp__google-docs__*` | YES (installed at `~/.claude/mcp-servers/google-docs-mcp-server/`) but NOT in ai-analyst-plus `.mcp.json` | `authorize_google_docs`, `upload_file_to_drive`, `read_document` |
| `google-workspace` | `mcp__google-workspace__*` | NO (not installed) | None in v1. V2: `inspect_doc_structure`, `batch_update_doc`, etc. |

**Action required:** Add `google-docs` MCP to ai-analyst-plus `.mcp.json`.

---

## 3. Document Template Specification

### Heading Hierarchy

```
H1: [Action Headline Title]
    (subtitle: dataset + date range + analysis type — italic body text)
    (author + date — body text)
    (confidence badge — bold, if validation ran)

H2: Context
    (2-4 sentences: why this analysis exists, what decision it informs)

H2: Summary
    H3: Primary Learnings
        1. **[Action headline]** — [detail + key number]. >> See Finding 1
        2. **[Action headline]** — [detail + key number]. >> See Finding 2
        3. ...
    H3: Recommendations
        1. **[Action verb + scope]** — [rationale]. Confidence: [High/Medium/Low].
        2. ...

H2: Analysis
    H3: [Finding 1 Action Headline]
        (summary paragraph)
        H4: [Sub-finding 1a]
            (text + chart image + interpretation)
            *Figure N: [caption]. Source: [dataset], [date range].*
        H4: [Sub-finding 1b]
            (text + chart image + interpretation)
    H3: [Finding 2 Action Headline]
        H4: [Sub-finding 2a]
        H4: [Sub-finding 2b]
    H3: Synthesis
        (what findings mean together; root cause)
        (confidence note if validation ran)
    H3: Implications
        (cost of inaction, quantified)

H2: Next Steps
    H3: Recommended Actions
        (action items with owners and deadlines)
    H3: Success Tracking
        (metric to watch, baseline, target, check-in date)
    H3: Open Questions
        (questions the analysis raised but did not answer)

H2: Resources
    H3: Queries
        H4: Query 1: [Descriptive Title]
            **Used in:** Finding N — "[headline]"
            [SQL in gray-shaded monospace table cell]
        H4: Query 2: ...
    H3: Companion Analyses
        (links to related analyses, dashboards)
    H3: Data Sources
        (connection details, date ranges, row counts)
```

### Content Source Mapping

| Template Section | Pipeline Artifact | Assembly Logic |
|-----------------|-------------------|----------------|
| Title (H1) | `working/pipeline_summary.md` + `outputs/narrative_*.md` title | Use narrative title; transform to action headline if needed |
| Subtitle | Pipeline summary dataset name + date range | "{dataset} | {date_range} | {analysis_type}" |
| Author + Date | `.knowledge/user/profile.yaml` + pipeline run date | If no profile, use "AI Analyst" |
| Confidence badge | `outputs/validation_*.md` confidence score | "**Analysis Confidence:** {grade} ({score}/100)". Caveat if C or below. |
| Context | `outputs/narrative_*.md` Context section + `working/storyboard_*.md` | 2-4 sentences: who asked, what they assumed, what data was examined |
| Summary > Primary Learnings | `outputs/narrative_*.md` Key Findings | Action headline + first detail + >> bookmark link |
| Summary > Recommendations | `outputs/narrative_*.md` Recommendations | Ordered by confidence (High first) |
| Analysis sections | `outputs/narrative_*.md` Finding sections | Each finding → H3; sub-findings → H4 |
| Analysis > Charts | `outputs/charts/*.png` mapped via narrative references | One chart per H4, 6.0" wide, below the claim |
| Synthesis | Narrative root cause + storyboard resolution | What findings mean together |
| Implications | Narrative opportunity sizing | Quantified impact |
| Next Steps > Actions | Narrative recommendations (detailed) | Action items |
| Next Steps > Success Tracking | `outputs/close_the_loop_*.md` | Metric, baseline, target, check-in date |
| Resources > Queries | `working/sql_queries/*.sql` or inline SQL | Organized by finding, each with "Used in" backlink |
| Resources > Data Sources | Pipeline summary + connection config | Connection, date range, row counts |

### Chart Placement Rules

1. Charts follow the claim they support (never before the paragraph).
2. One chart per H4 sub-section.
3. Full-width only (6.0 inches). No side-by-side.
4. Caption below: `*Figure N: [action title]. Source: [dataset], [date range].*`
5. Missing chart → placeholder text: `[Chart: {filename} — file not found]`.
6. Empty paragraph before and after each chart for spacing (adopted from Sravya).

### SQL Presentation Rules

1. All SQL in Resources > Queries. No inline code in Analysis sections.
2. Each query: title + "Used in: Finding N" backlink + formatted SQL.
3. SQL in single-cell table: gray fill (#F2F2F2) + Courier New 9pt.
4. Analysis sections link to queries via parenthetical: `(Query 3)`.
5. Empty paragraph before and after each SQL table (adopted from Sravya).

### Bold Label List (Merged)

From our plan + Sravya's skill:
- "The Insight:"
- "Why this matters for product:"
- "Bottom line:"
- "Key context:"
- "Data quality flag:"
- "Sample size warning:"
- "The creative angle:"
- "The interpretation:"

---

## 4. Wave Structure

| Wave | Name | Tasks | Delivers |
|------|------|-------|----------|
| 1 | Foundation | 5 | python-docx dependency, gdoc_builder.py, .docx generation working locally |
| 2 | Google Integration | 5 | MCP config, auth flow, Drive upload, state yaml, export skill wiring |
| 3 | Polish | 5 | Bookmarks, confidence badge, captions, progress messages, post-upload verification |
| 4 | Hardening | 4 | Error handling, .gitignore, conversion test, edge cases |

---

## 5. Detailed Waves

### Wave 1: Foundation

**Goal:** Generate a well-formatted .docx from pipeline outputs, testable locally.

#### Task 1.1: Add python-docx to dependencies

- Add `python-docx>=1.1` to `requirements.txt`.
- **Files:** `requirements.txt`
- **Done:** `pip install -r requirements.txt` works.

#### Task 1.2: Create gdoc_builder.py skeleton

- Create `helpers/gdoc_builder.py` with `build_readout()`.
- Accepts: title, subtitle, author, date, context, findings, charts, recommendations, sql_queries, next_steps, confidence.
- Returns: path to generated .docx.
- Implement heading hierarchy (H1-H4), basic styling (11pt body, page breaks).
- **Files:** `helpers/gdoc_builder.py` (new)
- **Done:** .docx opens in Word/Pages with correct heading structure.

#### Task 1.3: Implement Summary section

- Primary Learnings: numbered list, bold action headlines, detail sentences.
- Recommendations: numbered, sorted by confidence (High first).
- **Files:** `helpers/gdoc_builder.py`
- **Done:** Summary renders correctly.

#### Task 1.4: Implement Analysis section with charts

- Each finding → H3 with action headline. Sub-findings → H4.
- Embed charts via `add_picture(width=Inches(6.0))`, centered.
- Figure captions in italic below each chart.
- Missing charts → placeholder text.
- Empty paragraph before/after each chart (Sravya's spacing rule).
- **Files:** `helpers/gdoc_builder.py`
- **Done:** Charts embedded, captioned, spaced.

#### Task 1.5: Implement Resources section with SQL

- SQL in single-cell tables: gray fill + Courier New 9pt.
- "Used in: Finding N" backlinks.
- Companion Analyses (bullets) and Data Sources (body text).
- Empty paragraph before/after each table (Sravya's table spacing rule).
- **Files:** `helpers/gdoc_builder.py`
- **Done:** SQL blocks visually distinct, backlinks present.

### Wave 2: Google Integration

**Goal:** Wire up MCP, auth, upload, state, and export skill.

#### Task 2.1: Add google-docs MCP to ai-analyst-plus

- Copy MCP config from monorepo's `.mcp.json` into ai-analyst-plus `.mcp.json`.
- Verify path: `~/.claude/mcp-servers/google-docs-mcp-server/`.
- **Files:** `.mcp.json`
- **Done:** `mcp__google-docs__*` tools available in ai-analyst-plus sessions.

#### Task 2.2: Implement auth check and lazy OAuth

- Add Step 0 to export skill: probe with `read_document` on a known doc.
- If fails: run `authorize_google_docs` inline.
- If still fails: .docx-only fallback with manual upload instructions.
- **Files:** `.claude/skills/export/skill.md`
- **Done:** Auth flow handles all three scenarios.

#### Task 2.3: Implement narrative parser

- Create `helpers/gdoc_narrative_parser.py`.
- Reads `outputs/narrative_*.md` → structured data for `build_readout()`.
- Also reads `working/pipeline_summary.md` (metadata), `outputs/validation_*.md` (confidence), `outputs/close_the_loop_*.md` (success tracking).
- Missing files → None values, not errors.
- **Files:** `helpers/gdoc_narrative_parser.py` (new)
- **Done:** Parser extracts all template sections from sample narrative.

#### Task 2.4: Implement upload and state tracking

- Call `upload_file_to_drive(convert_to_google_doc=True)`.
- Write `outputs/gdoc_export.yaml`: document_id, url, title, created_at, source_hash, local_docx path, charts_embedded count, version number, version history.
- On re-export: read existing yaml, increment version, append to history.
- **Files:** `helpers/gdoc_builder.py` (or new `helpers/gdoc_uploader.py`)
- **Done:** yaml written with correct schema. Re-export increments version.

#### Task 2.5: Wire into export skill

- Add `gdoc` format block to `.claude/skills/export/skill.md`.
- Steps: auth check → source scan → parse → build .docx → upload → state → report.
- Add `gdoc` to invocation list.
- Exclude from `/export all` (suggest it after completion instead).
- Re-export detection: if yaml exists + source hash unchanged → offer to open or re-create.
- **Files:** `.claude/skills/export/skill.md`
- **Done:** `/export gdoc` listed, complete with all steps and edge cases.

### Wave 3: Polish

**Goal:** Bookmarks, badges, captions, progress, and post-upload check.

#### Task 3.1: Internal bookmark links (>> pattern)

- Create bookmarks at each Analysis H3 heading: `finding-{N}`.
- In Summary Primary Learnings, `>>` hyperlinks jump to corresponding finding.
- Query references in Analysis link to Resources > Queries bookmarks.
- Uses python-docx oxml API for bookmark start/end + hyperlink elements.
- **Files:** `helpers/gdoc_builder.py`
- **Done:** >> links work in .docx. Note which survive Google Docs conversion.

#### Task 3.2: Confidence badge and D/F gate

- If validation data: `**Analysis Confidence:** {grade} ({score}/100)` below title.
- Grade C or below: add caveat sentence.
- Grade D/F: warn user before creating doc (only checkpoint in the flow).
- **Files:** `helpers/gdoc_builder.py`, `.claude/skills/export/skill.md`
- **Done:** Badge appears. D/F triggers warning.

#### Task 3.3: Chart captions with figure numbering

- Running counter across document.
- `*Figure {N}: {title}. Source: {dataset}, {date range}.*` — italic, 9pt, gray.
- **Files:** `helpers/gdoc_builder.py`
- **Done:** Sequential numbering, styled captions.

#### Task 3.4: Progress messages

- "Building document from analysis..."
- "Uploading to Google Drive..."
- "Checking document formatting..."
- "Done! Your analysis is ready."
- Auth: "Connecting your Google account..."
- **Files:** `.claude/skills/export/skill.md`
- **Done:** Messages appear at each stage.

#### Task 3.5: Post-upload verification (v1: read-back check)

- After upload, call `read_document(file_id)` to get plain text of converted doc.
- Quick checks:
  - Count headings (should match expected section count)
  - Check for placeholder text (`[Chart:` should not appear if all charts embedded)
  - Check document length is within expected range
- If issues found: append note to user report ("Note: N formatting elements may
  not have survived conversion. Review the doc.").
- This is the **v1 adaptation of Sravya's reviewer concept** — read-only, no fixes.
- **Files:** `.claude/skills/export/skill.md`
- **Done:** Verification runs, issues reported in output.

### Wave 4: Hardening

**Goal:** Error handling, gitignore, conversion test, edge cases.

#### Task 4.1: Full error handling

- try/except on all I/O in builder and uploader.
- Implement error matrix (Section 7).
- User-friendly messages; verbose errors to `working/export_gdoc_debug.log`.
- **Files:** `helpers/gdoc_builder.py`, `helpers/gdoc_uploader.py`
- **Done:** Every failure mode produces correct message + recovery.

#### Task 4.2: Verify .gitignore coverage

- Confirm `outputs/` covers .docx and yaml files.
- Confirm `working/` covers debug log.
- **Files:** `.gitignore` (only if needed)
- **Done:** No generated files appear in `git status`.

#### Task 4.3: Conversion fidelity test

- Create `tests/test_gdoc_conversion.py` — generates a representative .docx.
- Exercises all formatting: H1-H4, bold/italic, bullets, numbered lists,
  gray-shaded table cells, embedded PNGs, bookmarks, hyperlinks, page breaks.
- Manual test: upload to Drive, check what survives, document results.
- **Files:** `tests/test_gdoc_conversion.py` (new)
- **Done:** Test .docx generated. Conversion results documented.

#### Task 4.4: Edge cases in export skill

Six scenarios:
1. Multiple analyses → ask user which one (pick-one).
2. Partial analysis → export available, note gaps.
3. No charts → text-only doc with note.
4. Unchanged source → offer to open existing or force re-create.
5. Changed source → new doc, preserve version history.
6. Offline/no network → .docx only + message.
- **Files:** `.claude/skills/export/skill.md`
- **Done:** All six handled with user-facing messages.

---

## 6. Relationship to Sravya's Assets

### Assets that coexist (no conflict)

| Sravya's Asset | Relationship |
|----------------|-------------|
| `google-doc-export` skill | Style guide for direct Google Workspace MCP usage. Doesn't conflict with our python-docx approach — different engine, different MCP. |
| `google-doc-creator` agent | Dormant until google-workspace MCP is installed. When active, it's an alternative path for users who prefer live API construction. |
| `google-doc-reviewer` agent | Dormant until google-workspace MCP is installed. V2 of our post-upload verification. |
| `auth-preflight` skill | References google-workspace MCP credentials path. Needs adaptation for google-docs MCP. |
| `session-handoff` skill | Generic — works with any pipeline. Our yaml state pattern is compatible. |
| `chart-to-drive` skill | Useful for v2 (direct image insertion). Not needed for v1 (embedded in .docx). |
| All experiment/presentation/analysis-design skills | Orthogonal — no overlap with export. |

### Future v2 path (when google-workspace MCP is installed)

If/when the `google-workspace` MCP is installed on Shane's machine:

1. **Enable Sravya's reviewer:** After our .docx upload + conversion, run
   `google-doc-reviewer` to inspect the converted doc and auto-fix formatting
   issues (heading hierarchy, spacing, orphaned headings).

2. **Update auth-preflight:** Support both MCPs — check `token.json` (google-docs)
   and `~/.google_workspace_mcp/credentials/` (google-workspace).

3. **Optional direct creation path:** For users who want live-editable docs without
   the .docx intermediate, offer a direct API path using Sravya's google-doc-creator
   agent + our Analysis Readout template.

4. **Port template to Sravya's creator:** Update `google-doc-creator` agent to use
   our heading hierarchy (Summary with >> links, Recommendations, Resources with SQL)
   instead of the generic structure.

---

## 7. Error Handling Matrix

| Failure Mode | User Message | Recovery |
|-------------|-------------|----------|
| No analysis outputs found | "No analysis results to export. Run an analysis first." | Abort. |
| Google Docs MCP not configured | "Google Docs needs connecting. Setting up now (~60s)." | Run `authorize_google_docs`. If fails, next row. |
| OAuth token expired | "Google connection expired. Re-authenticating..." | Re-auth. If fails, next row. |
| OAuth fails (org restriction, browser, timeout) | "Google Docs connection failed. Your analysis is saved as Word: `outputs/report_{SLUG}_{DATE}.docx`. Upload manually to drive.google.com." | .docx deliverable + 3-step manual instructions. |
| Some charts missing | "Creating doc... ({N} of {M} charts missing — placeholders inserted)." | Proceed with available charts + placeholders. |
| All charts missing | "No charts found. Creating text-only doc." | Text-only doc. |
| Upload fails (non-auth) | "Drive upload failed. Your doc is saved locally at `outputs/report_{SLUG}_{DATE}.docx`." | .docx deliverable. Retry later. |
| API quota exceeded (429) | "Drive API rate-limited (resets in ~1 hour). .docx saved at `outputs/...`." | .docx deliverable. |
| python-docx not installed | "python-docx required. Run: `pip install python-docx`" | Abort. |
| Narrative parse error | "Could not parse analysis. Generating simplified doc from pipeline summary." | Fall back to pipeline_summary.md. |
| Confidence D/F | "Low confidence (grade {grade}). Doc will include caveat. Create anyway?" | User confirms or aborts. |
| Multiple analyses | "Found {N} analyses. Which one? (a) {title_1} (b) {title_2}" | User picks. |
| Source unchanged | "Doc already exists at {url}. No changes detected. Open it, or re-create?" | User chooses. |

---

## 8. File Manifest

### Files Created

| File | Purpose |
|------|---------|
| `helpers/gdoc_builder.py` | Core builder. python-docx → .docx from structured data. |
| `helpers/gdoc_narrative_parser.py` | Reads pipeline artifacts → structured data for builder. |

### Files Modified

| File | Change |
|------|--------|
| `requirements.txt` | Add `python-docx>=1.1` |
| `.mcp.json` | Add `google-docs` MCP server config |
| `.claude/skills/export/skill.md` | Add `gdoc` format block with full workflow |

### Files Generated at Runtime (Not Tracked)

| File | Purpose |
|------|---------|
| `outputs/report_{SLUG}_{DATE}.docx` | Local .docx deliverable and fallback |
| `outputs/gdoc_export.yaml` | Version history, doc IDs, source hash |
| `working/export_gdoc_debug.log` | Verbose error log |

---

## 9. Open Questions for Shane

### Q1: Document title format
- **A:** `ANALYSIS: Mobile Checkout Regression Costs $16K/Month` (scannable in Drive)
- **B:** `Mobile Checkout Regression Costs $16K/Month` (cleaner)
- **Default: B**

### Q2: Confidence badge
- Show always when validation data exists? Gate on D/F?
- **Default: Show always. Gate on D/F.**

### Q3: Cross-link to slide deck
- Include "See also: Slide Deck" in Resources?
- **Default: Include link only if deck exists. Reference local file path.**

### Q4: Format keyword
- `gdoc` (unambiguous) vs `doc` (natural)
- **Default: `gdoc`**

### Q5: Hard limits on sections
- Max 5 learnings, 8 charts, 3 recommendations? Or include everything?
- **Default: Soft limits (include all, note when count is high).**

### Q6: Branding
- Logo + brand colors in v1?
- **Default: Skip for v1. Professional defaults.**

### Q7: `/export docx` standalone
- Offer .docx without Drive upload as separate format?
- **Default: Yes, add as convenience alias.**

### Q8 (NEW): Install google-workspace MCP?
- Sravya's agents need it. Should we source/install it now, or defer to v2?
- **Default: Defer to v2. Ship v1 with google-docs MCP only.**

### Q9 (NEW): Update Sravya's agents to reference our template?
- Her google-doc-creator uses a generic template. Port our Analysis Readout
  structure into her agent for when v2 is active?
- **Default: Yes, when v2 is built.**

---

## 10. Testing Checklist

### Wave 1 (local .docx)
- [ ] .docx opens without errors in Word/Pages/LibreOffice
- [ ] H1-H4 heading hierarchy visible in document outline
- [ ] Summary: numbered learnings with bold headlines
- [ ] Recommendations sorted by confidence
- [ ] Charts embedded at 6.0" width, centered
- [ ] Missing charts → placeholder text
- [ ] SQL blocks: gray background + monospace
- [ ] Empty paragraph spacing before/after charts and tables
- [ ] Page breaks between major sections

### Wave 2 (Google integration)
- [ ] google-docs MCP accessible in ai-analyst-plus
- [ ] `authorize_google_docs` works inline
- [ ] `upload_file_to_drive(convert=true)` produces valid URL
- [ ] Google Doc preserves: headings, bold/italic, bullets, tables, images
- [ ] `outputs/gdoc_export.yaml` written with correct schema
- [ ] Re-export increments version
- [ ] `/export gdoc` listed in skill invocation
- [ ] `/export all` does NOT include gdoc

### Wave 3 (polish)
- [ ] >> links work in .docx
- [ ] >> links survive conversion (or degrade to text)
- [ ] Confidence badge appears when validation data exists
- [ ] D/F grade triggers warning
- [ ] Figure captions numbered sequentially
- [ ] Progress messages appear
- [ ] Post-upload verification runs

### Wave 4 (hardening)
- [ ] Auth failure → .docx fallback
- [ ] Upload failure → .docx fallback
- [ ] Multiple analyses → disambiguation
- [ ] Partial analysis → graceful export with gap notes
- [ ] No generated files in `git status`

### End-to-end
- [ ] Full pipeline on sample dataset → `/export gdoc` → doc in < 60 seconds
- [ ] PM reads Summary in 30 seconds, knows the key findings
- [ ] Charts inline, properly sized, captioned
- [ ] "Would I send this to my VP?" → yes
