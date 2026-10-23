# Engineering principles: coding standards, code quality, design

Questions:
1. Which established sources should our coding-standards, code-quality and
   design-principles skills rest on?
2. Which tool settings enforce them in each of our languages?

Checked 2026-10-23. Unlike the stack baselines, most of this material is
stable; the risk is misquoting it, not it going stale.

## Code review standard

- Google Engineering Practices, "The Standard of Code Review": reviewers
  should favour approving a change once it **definitely improves the overall
  code health** of the system, even if it isn't perfect; there is no perfect
  code, only better code. Source: github.com/google/eng-practices
  `review/reviewer/standard.md`. [primary]
- "Small CLs": about 100 lines is usually a reasonable change size and 1,000
  lines is usually too large; there are no hard rules. Source:
  `review/developer/small-cls.md`. [primary]

## Commit messages

- Conventional Commits 1.0.0: `fix:` → SemVer PATCH, `feat:` → MINOR,
  `BREAKING CHANGE:` footer or `!` after type/scope → MAJOR; other types
  (`build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf`, `test`) are
  allowed; optional scope in parentheses. Source:
  conventional-commits/conventionalcommits.org `content/v1.0.0/index.md`.
  [primary]

## Design principles (well-established, from prior knowledge)

- **KISS**: prefer the simplest design that works.
- **YAGNI** (Extreme Programming; Martin Fowler's "Yagni" essay): don't
  build capability for presumed future needs; the cost of building,
  carrying and repairing it usually exceeds the cost of adding it later.
- **Rule of three** (Don Roberts, via Fowler's *Refactoring*): tolerate
  duplication until the third occurrence, then abstract.
- "Duplication is far cheaper than the wrong abstraction" (Sandi Metz,
  2016).
- **DRY** (Hunt & Thomas, *The Pragmatic Programmer*): every piece of
  *knowledge* has a single authoritative representation. It's about
  knowledge, not identical-looking text.
- **SOLID** (Robert C. Martin): Single Responsibility, Open/Closed, Liskov
  Substitution, Interface Segregation, Dependency Inversion.
- **Four rules of simple design** (Kent Beck): passes the tests, reveals
  intention, no duplication, fewest elements, in priority order.

## Enforcement tools per stack (from the stack baselines and prior knowledge)

| Language | Format | Lint | Complexity rule |
|---|---|---|---|
| Python | `ruff format` | `ruff check` | `C901` (mccabe `max-complexity`) |
| TypeScript | Prettier or Biome | ESLint (flat config) or Biome | ESLint `complexity`; Biome `noExcessiveCognitiveComplexity` |
| Go | `gofmt`/`goimports` | golangci-lint v2 | `gocognit`, `gocyclo`, `funlen` |
| Dart/Flutter | `dart format` | `flutter analyze` + lint package | no built-in metric; review (DCM is a commercial option) |
| SQL | sqlfluff (optional) | sqlfluff | — |

Verified 2026-10-23: `ruff rule C901` ("complex-structure", derived from
mccabe) and `biome explain noExcessiveCognitiveComplexity` both resolve in
current releases. ESLint `complexity` and golangci-lint `gocognit` /
`gocyclo` / `funlen` are from prior knowledge; confirm when adding them to a
project config.
