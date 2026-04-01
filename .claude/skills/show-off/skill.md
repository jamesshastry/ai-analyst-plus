# Skill: Show Off

## Purpose
Share what you've built with the AI Analyst Lab community on Slack. Posts a
short, proud showcase message to `#show-and-tell` from the student's own account.

## When to Use
- User says `/show-off` or "share what I built" or "show the community"
- After completing an analysis, pipeline run, or building something cool

## Invocation
`/show-off` — share what you've built with the community

## Prerequisites
- Slack MCP server must be configured with the student's user token
- If Slack MCP tools are not available, tell the student:
  "Slack isn't connected yet. Run `/kickoff` first to connect your Slack account."
- Student should have already run `/kickoff` — if not, suggest they do that first

## Instructions

### Step 1: Figure Out What They Built

Ask: **"What did you just build or figure out? Give me the quick version."**

Let them describe it in their own words. If they're vague, ask one follow-up like:
- "What was the question you were trying to answer?"
- "What data did you use?"
- "What surprised you about the result?"

### Step 2: Check for Artifacts

Look in the current working directory for recent outputs that would make the post
more concrete. Check for:
- Charts or visualizations (PNG, SVG)
- Analysis summaries
- Pipeline outputs
- Interesting data findings

If you find something good, mention it: **"I see you generated [artifact]. Want me to mention that in the post?"**

### Step 3: Compose the Message

Write a short showcase post (2-4 sentences) that:
- Leads with what they built or discovered (not "I just used AI to...")
- Includes a specific detail that makes it real (a number, a finding, a dataset)
- Shows genuine excitement without being over-the-top
- Ends with an invitation or energy

**Example outputs** (for tone, don't copy verbatim):
- "Just built a full funnel analysis for NovaMart's checkout flow — turns out 34% of users drop off at the shipping step. The AI Analyst found the pattern in about 10 seconds. Wild. Anyone else finding checkout insights? 📊"
- "Ran my first end-to-end pipeline! Asked 'which product categories are growing fastest?' and got back a full breakdown with charts. Took maybe 2 minutes total. This is going to change how I do weekly reporting. 🔥"
- "My AI Analyst just caught something I've been missing for months — our mobile conversion rate is half of desktop, but only on weekends. Already thinking about what to test. 💡"

### Step 4: Confirm Before Posting

Show the student the message and ask:
**"Here's your post for #show-and-tell. Want me to send it, or change anything?"**

Do NOT post until they confirm.

### Step 5: Post to Slack

Post the message to the `#show-and-tell` channel using the Slack MCP.

Use the channel name `show-and-tell` when calling the Slack MCP send message tool.

### Step 6: Celebrate

After posting, say something like:
**"Posted! 🎉 Check #show-and-tell to see it live. Keep building — you can `/show-off` again anytime."**

## Rules
1. Always confirm before posting — never auto-send
2. Keep the message short — 2-4 sentences max
3. Lead with the WHAT, not the tool — "I found X" not "I used AI to find X"
4. If the student wants to write their own message, let them
5. No limit on how many times they can show off — encourage it
6. If they haven't run `/kickoff` yet, nudge them to do that first
