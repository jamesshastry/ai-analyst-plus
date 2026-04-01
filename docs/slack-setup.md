# Slack Setup Guide

Connect your Slack account so the AI Analyst can post to the AI Analyst Lab community as you.

## What You Need

- A Slack account in the **AI Analyst Lab** workspace
- 2 minutes

## Setup Steps

### 1. Get Your Slack Token

Click this link to authorize the AI Analyst app with your Slack account:

**[Authorize Slack →](https://slack.com/oauth/v2/authorize?client_id=YOUR_CLIENT_ID&user_scope=chat:write,channels:read,users:read)**

> **Note:** This grants the AI Analyst permission to post messages as you and read channel lists. It does NOT give access to your DMs, private channels, or any other workspace data.

After clicking "Allow", you'll see a page with your token. Copy it.

### 2. Add Token to Your Config

Create a `.env` file in the root of this repo (if it doesn't exist already) and add:

```
SLACK_TOKEN=xoxp-your-token-here
```

### 3. Verify It Works

Restart Claude Code, then run:

```
/kickoff
```

This will introduce you to the community in `#introductions`. If it works, you're all set!

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Slack isn't connected" | Make sure `.env` has your `SLACK_TOKEN` and you restarted Claude Code |
| "Channel not found" | Make sure you've joined `#introductions` in the AI Analyst Lab Slack workspace |
| Token expired | Re-authorize using the link above |

## What Can It Do?

Once connected, you can use:
- `/kickoff` — Introduce yourself to the community
- `/show-off` — Share what you've built with the community

Messages post as **you** (your name, your profile picture) — not as a bot.
