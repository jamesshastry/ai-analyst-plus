---
name: first-run-welcome
description: Provide an adaptive welcome experience at session start based on the user's setup state. This skill should trigger at the very beginning of every new session, before any analytical work begins. Use this skill whenever a session starts, when Knowledge Bootstrap runs, when the user opens Claude Code for the first time, when returning to the tool after a break, at the start of any conversation, when initializing the environment, during session initialization, at the beginning of any interaction, or when the user first connects. The skill detects whether the user is brand new (cold start), has incomplete setup (partial setup), or is a returning user (warm start), and provides the appropriate onboarding or welcome message accordingly. Always apply this skill at session start to ensure users get the right experience based on their setup progress.
---

# Skill: First-Run Welcome

## Purpose
Provide an adaptive welcome experience based on setup state. Routes new users
through `/setup` for guided onboarding. Welcomes returning users with context
about their active dataset and quick actions.

## When to Use
- Session start (triggered by Knowledge Bootstrap)
- Before any analysis work begins

## Instructions

### Step 1: Detect setup state

Read `.knowledge/setup-state.yaml`. Classify into one of three states:

1. **Cold start** — file does not exist OR `setup_complete: false` with no
   `phases_completed` (empty or missing).
2. **Partial setup** — file exists, `setup_complete: false`, and at least one
   entry in `phases_completed`.
3. **Warm start** — file exists and `setup_complete: true`.

### Step 2: Route based on state

---

#### Cold Start (no setup-state.yaml or setup_complete: false, no phases done)

Present this welcome:

```
Welcome to AI Analyst — your analytical partner for product teams.

I help you turn business questions into validated insights, charts, and
presentations. Think funnel analysis, segmentation, root cause investigation,
trend detection — from question to slide deck.

Let's get you set up. I'll walk you through a quick interview to learn about
your data, your role, and what you want to analyze.

Starting setup now...
```

After presenting this message, hand control to the `/setup` skill. This means:
- STATE that setup is starting (included in the message above)
- Then use the Skill tool to invoke the setup skill: `Skill(skill="setup")`
- Do NOT manually execute setup interview questions yourself
- Let the setup skill handle all onboarding

Do NOT show dataset info, tutorial content, or example queries. The setup flow handles all onboarding.

---

#### Partial Setup (some phases complete, setup not finished)

Read `phases_completed` and `phases_remaining` from `.knowledge/setup-state.yaml`.

Present this message using the actual phase names:

```
Welcome back! Your setup is partially complete.

Done: [comma-separated list of phases_completed]
Remaining: [comma-separated list of phases_remaining]

Want to pick up where you left off? Type `/setup` to resume, or ask me
a question if you'd rather dive in.
```

Keep the tone friendly and concise. The user can choose to complete setup or dive into analysis.

---

#### Warm Start (setup_complete: true)

Read context from:
- `.knowledge/active.yaml` → `active_dataset` name
- `.knowledge/datasets/{active}/manifest.yaml` → table count (count of tables in the manifest)
- `.knowledge/analyses/index.yaml` → `last_updated` for last analysis date (or "none yet" if empty)

Present this message with the actual values:

```
Welcome back! Here's where things stand:

Dataset: [DATASET_NAME] ([N] tables)
Last analysis: [DATE or "none yet"]

Quick actions:
- Ask a question — "What's our conversion rate by channel?"
- /explore — interactive data exploration
- /run-pipeline — full analysis from question to deck

What would you like to work on?
```

Keep the tone warm but professional. The quick actions are examples — don't list every possible command.

**If `active_dataset` is null** (setup complete but no data connected), show:

```
Welcome back! Setup is complete but no dataset is active yet.

- /connect-data — add a dataset
- /datasets — see available datasets

What would you like to do?
```

### Step 3: Proceed

After presenting the welcome:
- **Cold start:** Use the Skill tool to invoke the setup skill: `Skill(skill="setup")`. Do not proceed with analysis until setup is complete.
- **Partial setup:** Wait for the user's response. If they type `/setup`, invoke it with the Skill tool. If they ask a question, route through Question Router (setup can be finished later).
- **Warm start:** Wait for the user's response. If they ask a question, route through Question Router. If they use a command like `/explore`, invoke that skill.

## Anti-Patterns

1. **Don't show the formal welcome if the user's FIRST message is a question.** This skill is for session start when the user hasn't typed anything yet OR when Knowledge Bootstrap runs. If the user opens the session and immediately asks "What's our conversion rate?", answer the question directly — you can weave in a brief "Welcome back" naturally but don't show the full welcome template. The welcome is for empty session starts, not for interrupting user questions.

2. **Don't show dataset details or tutorial content on cold start.** The `/setup` skill handles all onboarding. Just present the welcome message and hand off to setup.

3. **Don't overwhelm with feature lists.** Keep each welcome variant concise. The templates above are complete — don't add more commands, examples, or explanations.

4. **Don't reference specific datasets like NovaMart, or mention bootcamp/workshop content.** This is a general-purpose tool. When showing warm start welcome, use the ACTUAL dataset name from active.yaml, not a hardcoded example.

5. **Don't execute setup yourself.** For cold start, use the Skill tool to invoke setup — don't manually ask setup interview questions. Let the setup skill own the onboarding flow.
