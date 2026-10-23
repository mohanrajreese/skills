---
name: golang
description: How we write, lint, test and ship Go services and CLIs, covering module layout, error handling, context, concurrency, testing, golangci-lint v2 and recent Go releases. Use whenever working in a Go codebase, writing handlers, workers or CLIs, adding dependencies, fixing races or goroutine leaks, configuring golangci-lint, upgrading Go, or when you see go.mod, go.sum or *.go files.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, go, backend]
---

# Go

Boring, explicit Go: errors wrapped with context, `context.Context`
threaded through, no leaked goroutines, and a lint/test loop that runs with
the race detector.

## Before you start

1. Read `go.mod`: the `go` line (language version), any `toolchain` line,
   and `tool` directives (Go 1.24+ tracks dev tools like `sqlc` or `mockgen`
   there; run them with `go tool <name>`).
2. Check `.golangci.yml`: `version: "2"` means golangci-lint v2 config;
   v1 configs need `golangci-lint migrate`.
3. Learn the layout before adding packages (`cmd/<binary>/main.go`,
   `internal/...`). Follow it rather than importing a new structure.

## Defaults for new projects

- Latest Go (1.27 today); keep `go` in `go.mod` at the oldest version you
  must support.
- Layout: `cmd/<name>` for binaries, `internal/` for everything not meant to
  be imported elsewhere. No `pkg/` or `utils` grab-bags.
- `log/slog` for structured logs; `net/http` routing (method + path
  patterns, Go 1.22+) unless the project already uses a router.
- Postgres via `pgx/v5` (+ `sqlc` for typed queries); config from env.
- golangci-lint v2 in CI; `govulncheck` for dependencies.

## Verify loop

```bash
go build ./...
go vet ./...
go test -race -count=1 ./...
golangci-lint run
go mod tidy && git diff --exit-code go.mod go.sum   # deps are tidy
govulncheck ./...                                   # before releases
```

## Rules that matter

- **Errors:** return them, wrap with context using
  `fmt.Errorf("load user %d: %w", id, err)`, inspect with `errors.Is` /
  `errors.As`. Don't log *and* return the same error; handle it once.
- **Context:** first parameter, named `ctx`, passed down to every I/O call.
  Never store it in structs. Respect cancellation in loops.
- **Goroutines:** every goroutine has an owner and an exit path. Use
  `errgroup`, or `sync.WaitGroup.Go` (Go 1.25+), and cancel via context.
  Close channels from the sending side only.
- **Interfaces:** define them where they're consumed, keep them small;
  return concrete types.
- **Tests:** table-driven with `t.Run`; `t.Context()` (1.24+) for
  per-test contexts; `testing/synctest` (1.25+) for time-dependent
  concurrent code instead of `time.Sleep`.
- **HTTP servers:** set `ReadHeaderTimeout` and friends; never use the
  default client without a timeout for outbound calls.

## Changed recently (checked 2026-10-23)

- **Go 1.27** (Aug 2026) is current, with 1.26 the other supported line.
  Release notes not yet reviewed in this library (open question in the
  research note); read go.dev/doc/go1.27 before relying on new features.
- **Go 1.26:** `new(expr)` initialises a pointer from a value (handy for
  optional fields); `go fix` now runs modernizer analyzers and can apply
  fixes; `go tool doc` removed, use `go doc`; new GC.
- **Go 1.25:** `testing/synctest` stable, container-aware `GOMAXPROCS`,
  `sync.WaitGroup.Go`.
- **Go 1.24:** `tool` directive in `go.mod` (`go get -tool ...`),
  `testing.B.Loop`, `os.Root` for path-traversal-safe file access.
- **golangci-lint v2** has a new config format (`version: "2"`, `linters`
  plus `formatters` sections).

## Pitfalls

- Loop variable capture bugs are gone since Go 1.22, but only for modules
  whose `go` line is ≥ 1.22.
- `defer` inside loops (resources pile up until the function returns).
- Nil-map writes and nil-interface-holding-nil-pointer comparisons.
- `time.After` in long-lived `select` loops; use a `time.Timer` or context.

## Sources

- `research/2026-10-23-stack-baseline.md` → Go section.
