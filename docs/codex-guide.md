# Codex Guide

AI Analyst Plus is still primarily Claude Code-first, but Codex-native support is being added
under `.agents/skills/`.

## How to invoke Codex skills

Codex skills are **not slash commands**. Invoke them in natural language or with the `$` skill
name form:

```text
Use $skill-parity-review to review metric-spec.
Use $skill-parity-review to port metric-spec to Codex and bring it to parity with the Claude skill.
Use $metric-spec to define checkout conversion rate.
Use $independent-review to validate this finding with a blind second pass.
Use $claude-review to have Claude independently check this Codex result.
```

Do not use underscore slash commands like `/skill_parity_review`; Codex will treat that as an
unknown built-in command. Use `$skill-parity-review` or a natural-language request instead.

## Available Codex skills

See `.agents/skills/INDEX.md` for the current list. As of now:

- `$independent-review` — provider-neutral blind second-pass validation.
- `$claude-review` — ask Claude to validate a Codex-produced result from a blind brief.
- `$skill-parity-review` — compare/port Claude and Codex skill pairs.
- `$metric-spec` — define, document, and register metrics.

## Current limitations

Codex support is partial. Many workflows remain legacy Claude Code slash-command workflows
under `.claude/skills/`, including `/run-pipeline`, `/connect-data`, `/reliability`, and
export workflows. Use `$skill-parity-review` to port high-value Claude skills into
`.agents/skills/` one at a time.

## Testing

Use the local virtual environment when available:

```bash
.venv/bin/python -m pytest tests/test_codex_skills.py tests/test_codex_validation.py
```
