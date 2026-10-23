---
name: coding-standards
description: Our cross-language coding standards for Python, TypeScript, Go, Dart and SQL, covering what takes precedence, formatting by tools, naming, functions, modules, error handling, comments, types and validation, constants and config, logging, money and time, tests, dependencies, and commit and pull request conventions (Conventional Commits, small PRs). Use whenever writing or reviewing code in any of our projects, setting up linters and formatters for a new repo, writing a commit message or PR description, resolving style disagreements, or onboarding someone to how we write code. Language-specific rules live in the stack skills.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [engineering, standards, conventions]
---

# Coding standards

Consistency beats personal preference. Tools enforce what they can; this
skill covers what tools can't.

## Precedence

1. **The project's existing conventions** (its `CLAUDE.md`, linters, and
   the code around the change). Match the surrounding code.
2. The language community standard, enforced by the formatter (PEP 8 via
   `ruff format`, `gofmt`, Prettier/Biome, `dart format`).
3. This skill.

Never hand-format, and never mix style changes into a behaviour change.

## Naming

- Names reveal intent and use the **domain's words** (order, mandate,
  template, tenant); one word per concept across the codebase.
- Booleans read as questions: `is_active`, `hasAccess`, `canRefund`.
- Put **units in names** where there's ambiguity: `timeout_ms`,
  `amount_paise`, `size_bytes`, `expires_at` (a timestamp).
- No abbreviations beyond well-known ones (`id`, `url`, `db`).
- Casing per language: Python `snake_case` / `PascalCase` classes; TS
  `camelCase` / `PascalCase` types and components; Go `MixedCaps` (exported
  = capitalised); Dart `lowerCamelCase` / `UpperCamelCase`; SQL
  `snake_case`, plural table names.

## Functions and modules

- A function does one thing at one level of abstraction; if you need "and"
  to describe it, split it.
- **Guard clauses and early returns** instead of deep nesting.
- More than ~3 parameters → pass an object/struct. No boolean flag
  parameters that switch behaviour; write two functions.
- Keep side effects visible: functions that write to the DB or call APIs
  are named like it (`save_order`, `sendTemplateMessage`).
- Organise by **feature**, not by technical type (`orders/` rather than
  `models/`, `services/`, `utils/` at the top level). No `utils` grab-bags.
- Keep the public surface of a module small; everything else is private or
  internal.

## Errors

- Never swallow errors. Handle them, or add context and propagate.
- Fail fast on invalid input or state, at the boundary.
- Separate user-facing messages (safe, actionable) from internal detail
  (logged with context, never shown).
- Don't use exceptions for normal control flow.

## Types, validation, data

- Type the boundaries (function signatures, API payloads, DB rows).
  Validate external data once at the edge, then trust the types inside.
- No magic numbers or strings: named constants or config.
- **Money:** integer minor units + currency. **Time:** store UTC
  (`timestamptz`), convert at the edges, and inject a clock for tests.
- IDs are opaque strings or UUIDs to clients; never expose sequential IDs
  where they leak business data.

## Comments and docs

- Comments explain **why** (a constraint, a gotcha, a link to the spec),
  not what the code already says.
- Docstrings on public functions and modules; README per service/app.
- `TODO(owner): … (ticket)`, never bare TODOs. Delete commented-out code.

## Logging

Structured logs (key-value/JSON) with request/tenant IDs; levels used
meaningfully; **no secrets or personal data** (see `security`).

## Tests

- Test names state behaviour: `test_refund_fails_when_payment_not_captured`.
- Arrange / act / assert; one behaviour per test; deterministic (fixed
  clock, no real network, no `sleep`).
- Test the public behaviour, not private internals; fake external services
  at the boundary.

## Dependencies

Every new dependency needs a reason: maintained, licence OK, not trivially
replaceable by the standard library. Pin it with the lockfile.

## Commits and pull requests

- **Conventional Commits:** `feat(orders): add COD fallback`,
  `fix(webhooks): dedupe Razorpay events`, `refactor:`, `test:`, `docs:`,
  `chore:`; `!` or a `BREAKING CHANGE:` footer for breaking changes.
- **Small PRs:** ~100–400 changed lines is healthy; split anything near
  1,000. Separate refactors from behaviour changes.
- PR description: what and why, how it was tested, screenshots for UI,
  risks and rollout notes, linked spec/ticket.

## Sources

- `research/2026-10-23-engineering-principles.md` (Conventional Commits
  1.0.0, Google eng-practices); language rules in the stack skills.
