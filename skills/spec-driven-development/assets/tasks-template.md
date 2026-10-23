# Tasks NNN: <feature name>

Plan: ./plan.md · `[P]` = can run in parallel with other `[P]` tasks in the same group.

| ID | Task | Depends on | Check (how we know it's done) | AC |
|---|---|---|---|---|
| T001 | <schema migration> | — | migration applies on a fresh DB; `makemigrations --check` clean | AC1 |
| T002 [P] | <API endpoint> | T001 | integration test passes | AC1, AC2 |
| T003 [P] | <UI screen> | T001 | e2e test + matches design screenshot | AC1 |
| T004 | <webhook / integration> | T002 | replayed + duplicate payload tests pass | AC2 |

## Coverage
Every acceptance criterion appears in at least one task's AC column.
