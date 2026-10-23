---
name: subagent-suggester
description: Analyze a repository and its recurring tasks, then suggest and write Claude Code subagents (.claude/agents/*.md) that are actually worth having, such as a read-only code reviewer, test runner, migration reviewer, security auditor or docs researcher, each with a sharp description, minimal tools and the right model. Use whenever someone asks which subagents or agents to create, wants to set up a team of agents for a project, asks how to parallelise work with agents, or wants to review, trim or fix existing subagent definitions.
metadata:
  status: seed
  version: 0.2.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [ai, claude-code, subagents, agentic-coding]
---

# Subagent suggester

A subagent is worth creating when isolating work in its own context, with
its own tools and model, makes results better, cheaper or safer. Every
extra agent also adds a description the main agent must route between, so
**suggest few, sharp agents**.

## When a subagent earns its place

- **Context isolation:** big reads or searches whose details the main
  thread doesn't need (log triage, codebase sweeps, doc research).
- **A repeated specialised job** with its own checklist (PR review,
  migration safety review, security audit, test-failure triage).
- **Least privilege:** a reviewer that should only read; a researcher that
  should only browse.
- **Cheaper model fits:** mechanical work a smaller or lower-effort model
  handles well.
- **Parallelism:** independent tasks that can run side by side.

Not worth it: one-off tasks, anything the built-in agents already cover
(general-purpose, Explore for read-only search, Plan for planning), or
duplicates of a skill. Use a skill when it's knowledge, a subagent when
it's a separate worker.

## Steps

1. **Survey the repo:** stack (load the matching stack skills), CI checks,
   `CLAUDE.md`, existing `.claude/agents/`, and what the team repeatedly
   asks agents to do (ask, or look at recent PRs and issues).
2. **Shortlist 2–5 candidates** using the criteria above. For each, write
   the job, trigger, inputs, output format, tools needed and model.
3. **Present the shortlist** with a one-line reason each, and anything you
   chose *not* to create and why. Let the user pick.
4. **Write the chosen agents** to `.claude/agents/<name>.md` (project,
   committed) or `~/.claude/agents/` (personal).
5. **Test each one** on a real task; tighten the description if it
   triggers too often or never; log the result with `skill-retro`.

## Agent file format

```markdown
---
name: migration-reviewer
description: Reviews database migrations for lock risk, data loss and zero-downtime safety. Use proactively whenever a diff adds or changes migrations (Django, Prisma, Drizzle, Supabase, golang-migrate).
tools: Read, Grep, Glob, Bash
model: sonnet
---
You review database migrations. Follow the postgres skill's "Safe migration
patterns". For each migration report: operations, lock level, table size
risk, safer alternative, verdict (safe / needs change). Do not edit files.
```

- `description` decides when it's used: say what it does **and** when
  ("use proactively when …").
- `tools`: the minimum. Reviewers get read-only tools. Omitting `tools`
  inherits everything, which is rarely what you want.
- `model`: `haiku`/`sonnet` for mechanical or high-volume jobs,
  `opus`/`inherit` for judgement-heavy reviews.
- Newer Claude Code versions support more fields (e.g. `permissionMode`,
  `skills`, `mcpServers`, `hooks`, `memory`, `effort`). Check `/agents` or
  the docs for your installed version before using them.

## Starter catalogue for our stack

| Agent | Job | Tools | Model |
|---|---|---|---|
| `code-reviewer` | Review a diff with the `code-quality` checklist and `design-principles` red flags | read-only | opus/inherit |
| `test-runner` | Run the suite, triage failures, propose minimal fixes | Read, Grep, Glob, Bash | sonnet |
| `migration-reviewer` | Postgres/Django/Supabase migration safety | read-only + Bash | sonnet |
| `security-auditor` | `security` checklist on auth, webhooks, uploads, AI features | read-only | opus/inherit |
| `docs-researcher` | Check current versions/APIs from primary sources with dates | WebSearch, WebFetch, Read | sonnet |
| `figma-implementer` | Implement a Figma frame via the `figma` workflow | full + Figma MCP | inherit |

Pick from this list only where the repo actually has the matching work.

## Sources

- Claude Code subagent fields: `research/2026-10-23-product-platform-baseline.md`
  → AI agents and agentic coding.
