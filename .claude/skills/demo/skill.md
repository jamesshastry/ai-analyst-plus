---
name: demo
description: |
  Launch the Day 2 breakout room guided experience. Runs a conversational
  interview to personalize the analytical workflow, then walks the student
  through a multi-stage pipeline with pause points between each stage.

  Use this skill whenever the user says "/demo", "start the demo", "breakout
  room", "let's do the demo", "run the demo", "demo time", or any mention of
  starting the guided breakout room experience.
---

# Skill: /demo

## Purpose
Launch a personalized, guided analytical experience for the Day 2 breakout
room. This skill reads and executes the `demo-breakout` agent, which interviews
the student to customize their workflow, then walks them through 5 stages of
analysis with pause points between each.

## When to Use
- User says `/demo` or "start the demo" or "breakout room"
- Day 2 of the bootcamp -- students are exploring AI Analyst Plus capabilities

## Invocation
`/demo` -- start the guided breakout room experience

## Instructions

1. Read the agent file at `agents/demo-breakout.md`
2. Execute the agent workflow exactly as written -- it handles everything:
   - Part 1: A 5-question conversational interview (one question at a time)
   - Part 2: A 5-stage guided walkthrough with "next" as the advance command
3. Do NOT skip the interview or combine questions -- each question must be
   asked separately and the student must respond before the next question
4. Do NOT skip pause points between stages -- always wait for "next"
5. The interview answers become the variables that shape every stage

## Rules
1. **One question at a time.** Never dump multiple interview questions at once.
2. **Always pause between stages.** Wait for the student to type "next" before
   proceeding to the next stage.
3. **Show output at every stage.** Every stage must produce something visible
   (a chart, a report, a finding, a deck) before pausing.
4. **Use dark theme by default.** Analytics-dark looks best for demos and
   screenshots.
5. **Be encouraging.** This is a learning experience -- celebrate what the
   system produces and explain what just happened behind the scenes.
6. **Always show the architecture diagram at the end.** After Stage 5, display
   an ASCII diagram showing every agent and skill used and how they flow
   together. This makes the system's power visible and is great for screenshots.
7. **Always show file links at the end.** After the ASCII diagram, display the
   PDF and HTML deck paths clearly so the student can open their deliverables.
