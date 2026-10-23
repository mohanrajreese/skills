---
name: postgres
description: How we design Postgres schemas, write safe zero-downtime migrations, diagnose slow queries with EXPLAIN, index, pool connections and lock down access, plus which Postgres versions are current or end-of-life. Use whenever writing SQL, creating or altering tables, writing migrations in any framework (Django, Prisma, Drizzle, sqlc, Supabase), investigating slow queries or locks, choosing column types or keys, or upgrading Postgres. Pair with the supabase skill for Supabase-specific features.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, database, postgres, sql]
---

# Postgres

Most production database incidents are migrations that lock a busy table or
queries that stopped using an index. This skill exists to prevent both.

## Before you start

1. Find the server version (`select version();`, or the managed service
   console). Features below depend on it.
2. Find who owns schema changes: the framework's migration tool (Django,
   Prisma, Drizzle, golang-migrate, Supabase CLI). Make changes through it,
   never by hand in production.
3. Estimate table sizes (`select relname, n_live_tup from
   pg_stat_user_tables order by 2 desc;`) before writing a migration;
   "safe" depends on size and traffic.

## Defaults for new schemas

- Primary keys: `bigint generated always as identity`, or `uuid` using
  **`uuidv7()`** (PG 18+) when IDs are created client-side or exposed. v7
  keeps index locality that random v4 UUIDs lose.
- `timestamptz` (never `timestamp`), `text` (not `varchar(n)` unless the
  limit is a real rule), `numeric` for money, `jsonb` only for
  genuinely schemaless data.
- `NOT NULL` by default; `CHECK`, `UNIQUE` and foreign keys in the database,
  not only in app code. **Index every foreign key column** (Postgres does
  not do it automatically).
- App connects as a least-privilege role, never the superuser/owner.

## Safe migration patterns

| Change | Safe way |
|---|---|
| Any DDL on a busy table | `set lock_timeout = '5s';` first so it fails fast instead of queueing every query behind it |
| Add column | Nullable, or with a constant default (instant since PG 11) |
| Add NOT NULL | Add `CHECK (col is not null) NOT VALID` → `VALIDATE CONSTRAINT` → `SET NOT NULL` → drop the check |
| Add foreign key | `ADD CONSTRAINT ... NOT VALID`, then `VALIDATE CONSTRAINT` separately |
| Add index | `CREATE INDEX CONCURRENTLY` (outside a transaction; Django: `AddIndexConcurrently` with `atomic = False`) |
| Backfill | In batches (e.g. 1–10k rows per statement), not one giant `UPDATE` |
| Rename/drop column | Expand → migrate code → contract over separate deploys |
| Change column type | New column + backfill + switch, unless the cast is known to be metadata-only |

## Diagnosing slow queries

```sql
explain (analyze, buffers) <query>;   -- real timings and I/O; run on prod-like data
select query, calls, mean_exec_time from pg_stat_statements
  order by total_exec_time desc limit 20;   -- needs the extension enabled
select pid, wait_event_type, state, query from pg_stat_activity
  where state <> 'idle';                    -- what's running or blocked now
```

Look for sequential scans on large tables, row-estimate mismatches (run
`analyze`), and sorts or hashes spilling to disk.

## Changed recently (checked 2026-10-23)

- **Current: PostgreSQL 18** (18.6). **19 is at RC1** and expected to ship
  shortly; don't target it in production until it is GA and your managed
  provider supports it.
- **PG 13 is end-of-life; PG 14 reaches end-of-life in November 2026.**
  Plan upgrades for anything on 14 or older.
- PG 18 highlights: `uuidv7()`, virtual generated columns, asynchronous I/O,
  btree skip scan, `OLD`/`NEW` in `RETURNING`.
- PG 19 (per beta notes, may change): `REPACK [CONCURRENTLY]` replacing
  `VACUUM FULL`/`CLUSTER`, `WAIT` for read-your-writes on standbys,
  logical replication of sequences.

## Pitfalls

- Long transactions (including idle-in-transaction sessions) block vacuum
  and hold locks; set `idle_in_transaction_session_timeout`.
- Transaction-mode poolers (PgBouncer, Supavisor) break session state:
  `SET`, advisory locks, and named prepared statements unless the driver and
  pooler are configured for it.
- `OFFSET` pagination on large tables; use keyset pagination
  (`where (created_at, id) < (...) order by ... limit n`).
- `count(*)` on huge tables for UI badges; use estimates or cached counts.

## Sources

- `research/2026-10-23-stack-baseline.md` → Postgres section.
