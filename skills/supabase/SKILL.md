---
name: supabase
description: How we build on Supabase, covering Row Level Security and grants, the new publishable and secret API keys, local development with the Supabase CLI, migrations and declarative schemas, type generation, Auth with SSR, Edge Functions and Storage. Use whenever working in a project that uses Supabase from Next.js, Flutter or a server, writing RLS policies or SQL migrations for Supabase, configuring supabase-js or @supabase/ssr, deploying Edge Functions, rotating or migrating API keys, or when you see a supabase/ folder or config.toml. Pair with the postgres skill for general SQL and migration safety.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, supabase, postgres, backend]
---

# Supabase

Supabase exposes Postgres directly to clients through the Data API, so
**grants and Row Level Security are the authorization layer.** A table
without both set correctly is either unreachable or wide open.

## Before you start

1. Check for a local setup: `supabase/config.toml`, `supabase/migrations/`,
   `supabase/schemas/` (declarative schema), `supabase/functions/`. Note
   which diff engine `config.toml` enables (`[experimental.pgdelta]` → pg-delta;
   otherwise legacy migra).
2. Check which keys the app uses: new `sb_publishable_...` / `sb_secret_...`
   or legacy `anon` / `service_role` JWTs.
3. Find where the client is created (`createBrowserClient` /
   `createServerClient` from `@supabase/ssr`, or `supabase_flutter`).

## Defaults for new work

- **All schema changes as migrations** in the repo, applied locally first
  (`supabase start`, `supabase db reset`), never only through the dashboard.
  Projects on pg-delta can keep the source of truth in `supabase/schemas/*.sql`
  and generate migrations with `supabase db schema declarative sync`.
- **Every table in an exposed schema:** `enable row level security`,
  explicit `grant`s for `anon` / `authenticated` / `service_role`, and
  policies, all **in the same migration**.
- **Generated types:** `supabase gen types --local > src/types/database.ts`
  after each migration (TypeScript is the default; `--lang=dart|go|python|swift`
  for others); commit them.
- **Keys:** publishable key in clients; secret key only on servers or in
  Edge Functions, never in a browser or mobile bundle (it bypasses RLS).
- **Next.js:** `@supabase/ssr` with cookie-based sessions; check the user on
  the server with `getUser()`/`getClaims()`, not by trusting `getSession()`.

## Verify loop

```bash
supabase start                      # local stack
supabase db reset                   # replay all migrations + seed.sql from scratch
supabase test db                    # pgTAP tests, if present (RLS tests belong here)
supabase gen types --local > src/types/database.ts && git diff --stat
supabase functions serve            # Edge Functions locally
```

Before release, review the **Security Advisor** and **Performance Advisor**
in the dashboard for the target project; they flag tables without RLS,
exposed `security definer` functions and missing indexes.

## Rules that matter

- **RLS policies:** target roles explicitly (`to authenticated`), wrap
  helpers as `(select auth.uid())` so they're evaluated once per statement,
  and **index every column a policy filters on**. Write separate policies
  per operation; `update` needs both `using` and `with check`.
- **Views bypass RLS by default** (they run as their owner). Create them
  `with (security_invoker = true)` or keep them out of exposed schemas.
- **`security definer` functions** run with owner privileges: put them in a
  non-exposed schema, set `search_path = ''`, and check authorization inside.
- **Don't trust `user_metadata`** in policies (users can edit it); use
  `app_metadata` or your own tables for roles.
- **Edge Functions:** verify the caller (JWT or `apikey`), read secrets
  from `Deno.env` (`supabase secrets set`), and return proper CORS headers.
- **Storage:** buckets private by default, with storage RLS policies on
  `storage.objects`.

## Changed recently (checked 2026-10-23)

- **API keys:** publishable (`sb_publishable_`) replaces `anon`, secret
  (`sb_secret_`) replaces `service_role`. **Legacy keys are deprecated by
  the end of 2026**, so migrate now. The new keys are **not JWTs**: send them
  in the `apikey` header, not `Authorization: Bearer`.
- **Explicit grants:** a table isn't reachable through the Data API until a
  role is granted privileges; missing grants return `42501` with a hint
  naming the `grant` to add.
- **Declarative schemas + pg-delta** diff engine are the default for new
  `supabase init` projects; older projects stay on migra until switched.

## Pitfalls

- Turning RLS on with no policies (everything denied), then "fixing" it with
  the secret key in the client.
- Editing the remote database in Studio, so it drifts from migrations.
  `supabase db pull` to capture, then commit.
- Transaction-mode pooler connections with prepared statements or session
  state (see the `postgres` skill).

## Sources

- `research/2026-10-23-stack-baseline.md` → Supabase section (supabase docs
  in the supabase/supabase repo).
