---
name: project-onboarding
description: Get oriented in an unfamiliar or rarely-touched codebase quickly and leave behind a CLAUDE.md so the next session starts informed. Use when starting work in a project for the first time, when asked to "understand this repo", "how does this project work", "set up this project", "where do I start", or before making a non-trivial change in code you haven't read yet.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [dev, onboarding]
---

# Project Onboarding

Builds a working mental model of a repository in a fixed order (how to run
it, how it's shaped, how changes are checked) and records it where future
sessions will find it.

## When to use

- First session in a repo, or the repo has no `CLAUDE.md`.
- Not for a quick one-line fix where the relevant file is already known.

## Steps

1. **Read what exists:** `README*`, `CLAUDE.md`, `CONTRIBUTING*`, `docs/`,
   and the PR template. Existing project docs override this skill.
2. **Identify the stack and entry points** from manifests (`package.json`,
   `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `Dockerfile`, …) and
   the top-level directory layout.
3. **Find the real commands** for install, build, test, lint, format and run.
   Prefer what CI actually runs (`.github/workflows/`, `Makefile`, scripts)
   over what the README claims; they drift.
4. **Prove the loop works:** run install and the fast test/lint commands once.
   Note anything that fails and what fixed it.
5. **Map the architecture** at the level of "where does a request / command
   enter, and where does it go": main modules, data stores, external
   services, and generated code that must not be hand-edited.
6. **Write or update `CLAUDE.md`** in the project with: stack, commands,
   layout, conventions observed (naming, error handling, test style), and
   gotchas found in step 4. Keep it short; it loads every session.
7. **Run `skill-retro`** for anything that should improve this skill itself.

## Pitfalls

- Don't trust a README's commands until one has actually run.
- Don't write a CLAUDE.md that restates the README; record what a newcomer
  (or a model) would otherwise get wrong.
