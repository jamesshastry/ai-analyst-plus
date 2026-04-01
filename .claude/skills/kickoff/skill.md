# Skill: Kickoff

## Purpose
Introduce yourself to the AI Analyst Lab community on Slack. Posts a natural,
excited intro message to `#introductions` from the student's own Slack account.

## When to Use
- User says `/kickoff` or "introduce myself" or "kick it off"
- First time using Slack MCP — this is the icebreaker

## Invocation
`/kickoff` — introduce yourself to the community

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
   - Tell them: **"Got it! You'll need to restart Claude Code for Slack to connect. Run `claude` again and then `/kickoff`."**
   - Stop here — they need to restart for the MCP to pick up the new token

## Instructions

### Step 1: Gather Info

Ask the student three questions, one at a time:

1. **"What's your name?"**
2. **"What's your role and where do you work?"** (e.g., "Data Analyst at Spotify" or "PM at a fintech startup")
3. **"What are you most excited to learn this weekend?"**

### Step 2: Compose the Message

Write a short, natural intro post (2-4 sentences) using their answers. The message should:
- Sound like THEM, not like a template — conversational and genuine
- Start with a greeting ("Hey everyone!" / "What's up!" / etc.)
- Include their name, role, and what they're excited about
- End with energy — something like "Let's go!" or "Can't wait to get started!"
- End with a celebration emoji

**Example outputs** (for tone reference, don't copy these verbatim):
- "Hey everyone! I'm Marcus, a data analyst at Shopify. Pumped to learn how to build agents that automate the reporting I spend half my week on. Let's go! 🚀"
- "What's up! I'm Priya, a PM at a healthcare startup. Excited to finally stop waiting on the data team for every question I have. This is going to be fun! 🎉"
- "Hey! I'm Alex, career switcher trying to break into data. Honestly just blown away that you can build an AI analyst in a weekend. Let's do this! 💪"

### Step 3: Confirm Before Posting

Show the student the composed message and ask:
**"Here's your intro post for #introductions. Want me to send it, or would you like to change anything?"**

Do NOT post until they confirm.

### Step 4: Post to Slack

Post the message to the `#introductions` channel using the Slack MCP.

Use the channel name `introductions` when calling the Slack MCP send message tool.

### Step 5: Celebrate

After posting, say something like:
**"You're officially in! 🎉 Your intro is live in #introductions. Welcome to the AI Analyst Lab community. Now let's build something."**

## Rules
1. Always confirm before posting — never auto-send
2. Keep the message short — 2-4 sentences max
3. Make it sound natural, not templated — vary the greeting, structure, and emoji
4. If the student wants to write their own message instead, let them — just post what they give you
5. Only post once — if they run `/kickoff` again, remind them they already introduced themselves and offer `/show-off` instead
