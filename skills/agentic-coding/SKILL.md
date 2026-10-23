---
name: agentic-coding
description: How we work with AI coding agents such as Claude Code (also Copilot, Cursor and Codex) across our repos, covering CLAUDE.md and AGENTS.md, this skills library as a plugin, plan mode, task framing, verification before claiming done, permissions and hooks, subagents and parallel worktrees, MCP servers, headless runs in CI, context hygiene, and reviewing AI-written code. Use whenever setting up a repo for coding agents, writing or trimming CLAUDE.md, configuring Claude Code settings, hooks or permissions, planning how to split work across agent sessions, automating agent runs in CI, or when agent output quality is poor and the setup needs fixing.
metadata:
  status: seed
  version: 0.2.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [ai, agentic-coding, claude-code, workflow]
---

# Agentic coding

A coding agent is as good as the context and feedback loop it gets: what
the project is, how to check its work, and what "done" means. Set those up
once per repo, then give each task a crisp goal.

## Repo setup (once per project)

1. **`CLAUDE.md`** (and/or `AGENTS.md` for other agents): stack, exact
   commands (install, test, lint, typecheck, run), layout, conventions, and
   gotchas. Keep it short (it loads every session) and correct (stale
   instructions are worse than none). `project-onboarding` writes the first
   version; trim it when it grows.
2. **Install this library** as a plugin so stack skills load in every repo
   (`/plugin marketplace add mohanrajreese/skills`, then
   `/plugin install dev-skills@mohanrajreese-skills`), or enable it for the
   team in `.claude/settings.json`.
3. **Fast, scriptable checks** the agent can run: one command each for
   tests, lint and typecheck. If a human needs tribal knowledge to verify a
   change, the agent can't verify it either.
4. **Permissions:** allow-list safe, frequent commands (test runners,
   linters, `git status/diff`) in `.claude/settings.json`; keep deploys,
   migrations against shared DBs and pushes to main behind approval.
5. **Hooks** for things that must always happen, not "should": format on
   edit, block writes to generated/secret files, run fast checks before
   stop.
6. **MCP servers** (`.mcp.json`) only for systems the agent genuinely needs
   (issue tracker, DB read replica, Figma); scope credentials read-only where
   possible.
7. **Subagents** for recurring specialised work; use `subagent-suggester`.

## Per-task workflow

1. **Frame the task:** goal, constraints, acceptance criteria, and where to
   look. Point at a spec (`spec-driven-development`) for anything bigger
   than a small fix.
2. **Plan first** for non-trivial changes (plan mode / ask for a plan), then
   review the plan before any edits. Correcting a plan is cheaper than
   correcting a diff.
3. **Work in small, verifiable steps**; each step ends with the relevant
   checks passing.
4. **Verify before "done":** tests, lint, typecheck, and for UI, actually
   load the page. "It should work" isn't verification.
5. **Review the diff** like a teammate's PR with the `code-quality`
   checklist (`/code-review`, and `/security-review` for sensitive areas).
   Watch for invented APIs, skipped error handling, weakened tests, scope
   creep and the overengineering red flags in `design-principles`.
6. **Retro:** if the agent hit a gotcha, record it (`skill-retro`) so the
   next session doesn't.

## Scaling up

- **Parallel sessions:** separate git worktrees or cloud sessions per
  independent task; never two agents editing the same files.
- **Subagents** keep the main context clean for broad searches and reviews.
- **Headless/CI:** `claude -p "<task>"` with an explicit allow-list for
  repeatable jobs (triage, changelog, dependency bumps); the Claude GitHub
  app/Action for PR-driven work.
- **Context hygiene:** start a fresh session per unrelated task; compact or
  clear long sessions; put durable knowledge in CLAUDE.md or skills, not in
  chat.

## Pitfalls

- A giant CLAUDE.md full of generic advice; it costs context every turn
  and buries the rules that matter.
- Letting the agent "fix" failing tests by changing assertions, skipping
  tests or loosening types.
- Granting broad permissions (any shell command, prod credentials) to save
  a few approval clicks.
- Accepting large unreviewed diffs because CI is green.
- Agents overengineer by default (extra layers, options, defensive code).
  Ask for the minimal change and check against `design-principles`.
