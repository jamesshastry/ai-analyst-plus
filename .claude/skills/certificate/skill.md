# Skill: Certificate

## Purpose
Generate a certificate of completion, prepend it to the student's Marp slide
deck as the first slide, render the full deck to PDF, and open LinkedIn for
sharing.

End of Day 2 moment. The student types `/certificate`, Claude does the rest.

## When to Use
- User says `/certificate` or "generate certificate" or "completion certificate"
- End of Day 2 when students have a finished deck

## Invocation
`/certificate` — generate a certificate of completion and add it to the deck

## Instructions

### Step 1: Find the Deck

Ask the student: **"Where's your output deck? (path to your `.marp.md` file)"**

If the student gives a path, use it. If they say something vague ("the deck",
"my slides"), look for `.marp.md` files:

```bash
find outputs/ -name "*.marp.md" -type f 2>/dev/null | head -5
```

If multiple decks exist, show the list and ask which one.

### Step 2: Get the Student's Name

Try these sources in order — use the first one that returns a real name:

1. **Check `.knowledge/user/profile.md`** — look for `Name:` field
2. **Check git config:** `git config user.name`
3. **Ask the student:** "What name should go on the certificate?"

### Step 3: Generate Certificate HTML

Read the certificate template from this skill's references:
`references/certificate-template.html` (in this skill's directory)

Copy the **entire** HTML file and replace the two placeholders:
- `{{STUDENT_NAME}}` — the student's full name
- `{{DATE}}` — today's date formatted as `Month Day, Year` (e.g., "April 1, 2026")

Save the filled template as `certificate.html` in the repo root.

### Step 4: Render Certificate to PNG

```bash
node scripts/render-certificate.mjs certificate.html certificate.png
```

This produces a 3840x2160 retina PNG (2x scale of 1920x1080) — matches the
16:9 Marp slide dimensions exactly.

If the render script fails (missing Node.js, Chromium issues), fall back to
opening the HTML in the browser and telling the student to screenshot manually.

### Step 5: Prepend Certificate to Deck

Read the student's `.marp.md` file. Find the end of the YAML frontmatter
(the closing `---`). Insert the certificate slide immediately after it,
**before** the first content slide:

```markdown
<!-- _paginate: false -->
<!-- _footer: "" -->

![bg](certificate.png)

---
```

This uses Marp's background image syntax to fill the entire slide with the
certificate PNG. The `_paginate: false` and `_footer: ""` directives hide
the page number and footer on the certificate slide only.

**Important:** The `certificate.png` path must be relative to the `.marp.md`
file location. If the deck is in `outputs/`, copy the PNG there too:

```bash
cp certificate.png outputs/certificate.png
```

### Step 6: Render Full Deck to PDF

Detect the theme from the deck's YAML frontmatter (`theme:` field), then
render with Marp CLI. **The output PDF must be named
`Certificate of Completion.pdf`** — this is what the student sees and shares.

```bash
npx @marp-team/marp-cli --no-stdin --pdf --html --allow-local-files \
  --theme themes/DETECTED_THEME.css \
  DECK_PATH \
  -o "Certificate of Completion.pdf"
```

For example, if the deck is `outputs/deck_novamart_2026-04-01.marp.md` with
`theme: analytics-light`:

```bash
npx @marp-team/marp-cli --no-stdin --pdf --html --allow-local-files \
  --theme themes/analytics-light.css \
  outputs/deck_novamart_2026-04-01.marp.md \
  -o "Certificate of Completion.pdf"
```

### Step 7: Copy PDF to Desktop and Open It

```bash
cp "Certificate of Completion.pdf" ~/Desktop/
open ~/Desktop/"Certificate of Completion.pdf"
```

Tell the student: **"Your Certificate of Completion is on your Desktop — take
a look!"**

This is the moment. Let them see the full deck with their certificate as the
first slide. Give them a beat before moving to LinkedIn.

### Step 8: Confirm Before LinkedIn

Draft a short LinkedIn caption (under 200 characters).

**Caption rules** (same as show-off-linkedin):
- Lead with what they built, not where they were
- One specific number (charts, agents, datasets, etc.)
- No hashtags, no emojis, no "I'm thrilled to announce"
- End with a short engagement hook
- Mention AI Analyst Lab naturally — as context, not a pitch

**Example captions** (adapt to what they actually built):
- "Built an AI analyst that turns business questions into charts and experiment designs. Here's my certificate + the deck. Want to see the pipeline?"
- "Went from zero to a working AI analysis pipeline in a weekend. 18 charts, 3 agents, all from plain English questions."

Ask: **"Here's the caption for LinkedIn. Want me to open LinkedIn so you can
post it, or change anything first?"**

Do NOT proceed until they confirm.

### Step 9: Post to LinkedIn

```bash
# Copy certificate PNG to Desktop for upload
cp certificate.png ~/Desktop/certificate.png

# Copy the caption text to clipboard
echo -n "CAPTION_TEXT" | pbcopy

# Open LinkedIn with caption pre-filled
open "https://www.linkedin.com/feed/?shareActive=true&text=URL_ENCODED_CAPTION"
```

Tell the student:
**"LinkedIn is open with your caption pre-filled. Click the image icon in the
composer and upload `certificate.png` from your Desktop, then hit Post!"**

### Step 10: Clean Up

After they've posted (or decided not to), the temporary files can be deleted:

```bash
rm -f certificate.html certificate.png
```

Don't auto-delete — ask first or just mention they can clean up.
The `Certificate of Completion.pdf` on the Desktop is theirs to keep.

## Rules
1. The certificate must be exactly 1920x1080 (16:9) to match Marp deck slides
2. Always use the full HTML template from `references/certificate-template.html`
3. The certificate slide must be the FIRST slide in the deck (after frontmatter)
4. The rendered PDF must be named `Certificate of Completion.pdf`
5. Always open the PDF for preview, not the PNG
6. Always confirm with the student before opening LinkedIn
7. The LinkedIn caption must be under 200 characters
8. Never fabricate the student's name — always source it from profile, git, or ask
9. The certificate has three instructor signatures — do not modify the instructor names
