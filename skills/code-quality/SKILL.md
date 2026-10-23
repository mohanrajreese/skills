---
name: code-quality
description: How we keep and review code quality, covering automated quality gates per stack (format, lint, types, tests, complexity limits, diff coverage, dependency and secret scans), a prioritised code review checklist, code smells, extra checks for AI-written code, safe refactoring, tech debt tracking, and a review report with severities. Use whenever reviewing a pull request or diff, setting up CI quality checks or pre-commit hooks for a repo, deciding if code is good enough to merge, refactoring messy code, measuring complexity or coverage, or auditing the health of an existing codebase.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [engineering, quality, review, ci]
---

# Code quality

Quality means the code is **correct, secure, readable, easy to change and
tested**. Machines check what they can on every commit; humans (and
agents) review the rest, approving once a change **improves overall code
health, even if it isn't perfect**.

## 1. Automated gates (set up once per repo)

| Gate | Python | TypeScript | Go | Flutter |
|---|---|---|---|---|
| Format | `ruff format --check` | Prettier / Biome | `gofmt` (via golangci-lint) | `dart format --set-exit-if-changed` |
| Lint | `ruff check` | ESLint / Biome | golangci-lint v2 | `flutter analyze` |
| Types | mypy / pyright | `tsc --noEmit` | compiler | analyzer |
| Tests | pytest | Vitest / Playwright | `go test -race` | `flutter test` |
| Complexity | Ruff `C901` | ESLint `complexity` / Biome cognitive complexity | `gocognit`, `funlen` | review |
| Deps & secrets | pip-audit, gitleaks | npm audit, gitleaks | govulncheck, gitleaks | gitleaks |

- Run the fast gates in **pre-commit** and everything in **CI**; CI must
  block merge on failure.
- Coverage: require tests for *changed* code (diff coverage ≈ 80% is a good
  bar) rather than chasing a global percentage.
- Complexity: start around 10–15 per function and treat a breach as a
  prompt to simplify, not a number to game.
- Introducing gates to an old repo: apply to changed files first, fix the
  backlog gradually; never one giant reformat mixed with real changes.

## 2. Review checklist (in priority order)

1. **Correctness:** does it do what the spec/ticket says, including edge
   and error cases? Any race conditions, off-by-one errors, time zone or
   money mistakes?
2. **Security:** authz on every data access, input validation, secrets,
   webhook verification (`security`).
3. **Design and simplicity:** right place, right size; no speculative
   abstractions (`design-principles`); fits existing patterns.
4. **Tests:** cover the behaviour and the failure paths; would they fail if
   the code were wrong? No tests weakened to pass.
5. **Readability:** names, structure, comments explaining why
   (`coding-standards`).
6. **Operability:** logging, metrics, migrations safe, rollout/rollback.
7. **Performance:** only where it matters (N+1 queries, unbounded loops,
   large payloads), and backed by measurement.

Label comments by **severity**: `blocker` (must fix), `major` (should fix
before merge), `minor` (fix or follow-up), `nit` (optional, style). Praise
good decisions too.

## 3. Code smells to name in reviews

Long function, long parameter list, deep nesting, boolean flag parameters,
god object or file, feature envy (logic living far from its data),
shotgun surgery (one change touches many files), primitive obsession (raw
strings or ints for money, IDs, statuses), dead or commented-out code,
speculative generality, comments that excuse confusing code, flaky or
order-dependent tests.

## 4. Extra checks for AI-written code

- APIs, functions or config keys that don't exist (check against the docs or
  the installed version).
- Unrequested scope: extra files, options, abstractions, rewrites of
  untouched code.
- Swallowed errors, broad `try/except`, silent fallbacks that hide failures.
- Tests that assert mocks rather than behaviour, or were edited to pass.
- Duplicated helpers that already exist elsewhere in the repo.
- Version drift: patterns from older framework versions (see each stack
  skill's "Changed recently").

## 5. Refactoring and tech debt

- Refactor in small, behaviour-preserving steps with tests green after each
  step; keep refactor commits separate from feature commits.
- Boy-scout rule within the files you're already touching, not the whole
  repo.
- Record debt you can't fix now (`docs/tech-debt.md` or tickets) with its
  cost ("every new payment method needs edits in 4 places") so it can be
  prioritised, and reserve regular capacity for it.

## Review report format

```markdown
## Review: <PR/diff> — verdict: approve | approve with nits | changes requested
Blockers: …
Major: …
Minor / nits: …
Good: …
Simplification opportunities: …
```

## Sources

- `research/2026-10-23-engineering-principles.md` (Google code review
  standard, tool settings).
