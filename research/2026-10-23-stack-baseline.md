# Stack baseline: current versions and recent changes

Questions:
1. What is the current stable version of each technology in our stack?
2. What changed in the last ~12 months that older habits (and model memory)
   get wrong?
3. What is deprecated or shutting down soon?

Checked 2026-10-23. Source tags: **[registry]** = package registry API
(pypi.org, registry.npmjs.org, proxy.golang.org, pub.dev, Flutter release
JSON), the most reliable source for "latest version". **[primary]** =
official docs or repo. **[secondary]** = third-party write-up, still to be
confirmed against a primary source.

## Python

- CPython 3.15.0 final released 2026-10-09; 3.15.1 due 2026-12-01.
  Source: PEP 790 (github.com/python/peps), checked 2026-10-23. [primary]
- 3.14 branch is at 3.14.9+. Free-threaded build officially supported since
  3.14 (PEP 779). [primary] / [secondary]
- uv 0.13.5, ruff 0.17.2, ty 0.0.91 (still 0.0.x, i.e. pre-1.0), mypy 2.4.0,
  pytest 9.1.1, pydantic 2.14.1, psycopg 3.3.6. [registry]
- Ruff 0.16.0 (2026-07-23): default rule set grew from 59 to 413 rules; Ruff
  formats Python code blocks in Markdown by default; `# ruff: ignore[...]`
  comments added. Ruff 0.17.0 (2026-10-09): default target Python 3.11 when
  none configured; several DTZ rules dropped from defaults.
  Source: github.com/astral-sh/ruff CHANGELOG.md and changelogs/0.16.x.md. [primary]

## Django

- Django 6.1.2 (2026-10-06), requires Python 3.12+. [registry]
- 6.1 released 2026-08-05. Mainstream support ends April 2027, extended
  December 2027. Supports Python 3.12–3.15 (3.15 as of 6.1.3).
  New: model field fetch modes (`FETCH_ONE`/`FETCH_PEERS`/`FETCH_RAISE`,
  `QuerySet.fetch_mode()`); database-level `on_delete` (`DB_CASCADE`,
  `DB_SET_NULL`, `DB_SET_DEFAULT`, no delete signals); `MAILERS` setting
  replacing `EMAIL_BACKEND`/`EMAIL_*` in 7.0.
  Source: django/django docs/releases/6.1.txt. [primary]
- 6.0 (2025-12-03): Content Security Policy support, template partials,
  built-in Tasks framework (`django.tasks`, `@task`, `.enqueue()`, `TASKS`
  setting; built-in backends are for dev/test, no worker included), modern
  email API, `DEFAULT_AUTO_FIELD` defaults to `BigAutoField`, Python < 3.12
  dropped. Source: django/django docs/releases/6.0.txt. [primary]
- DRF 3.18.3, django-stubs 6.1.2, pytest-django 4.14.0. [registry]

## TypeScript / Node tooling

- typescript 7.0.2 is `latest` on npm (7.0 released 2026-07-08); 7.1 in
  beta. 7.0 is the native Go port; the command is `tsc` again (preview builds
  used `tsgo`). [registry] / [primary: microsoft/typescript-go README]
- 7.0 has no stable programmatic API yet (README: "API: not ready"). Tools
  that use the API (typescript-eslint, some framework checkers) may need TS 6;
  Microsoft publishes `@typescript/typescript6` with a `tsc6` binary.
  [primary] / [secondary]
- TS 6.0 changed defaults (`strict: true`, `module: esnext`, `types: []`,
  `rootDir` = tsconfig dir) and deprecated `moduleResolution: node`/`node10`,
  `baseUrl`, AMD/UMD/System modules and import `asserts`; 7.0 removes them.
  `"ignoreDeprecations": "6.0"` silences them temporarily. [secondary:
  Visual Studio Magazine 2026-03-23, LogRocket] — confirm against the
  official release notes before relying on the exact list.
- eslint 10.13.0, @biomejs/biome 2.6.2, prettier 3.9.10, vitest 5.0.5,
  @playwright/test 1.64.1, zod 4.6.7, drizzle-orm 0.45.4, @prisma/client
  7.10.1. [registry]

## Next.js / React

- next 16.4.2 (2026-10-15), react 19.3.1. [registry]
- Next 16 (2025-10-21) breaking changes, from the official upgrade guide
  (vercel/next.js docs/01-app/02-guides/upgrading/version-16.mdx): [primary]
  - Node 20.9+ and TypeScript 5.1+ required.
  - Turbopack is the default for `next dev` and `next build`; `--webpack`
    opts out.
  - Sync access to `cookies`, `headers`, `draftMode`, `params`,
    `searchParams` removed; async only.
  - `middleware` renamed to `proxy` (`proxy.ts`, export `proxy`); proxy runs
    on the Node.js runtime only. Edge middleware should stay `middleware`.
  - `revalidateTag(tag, profile)` needs a cacheLife profile; new
    `updateTag` (Server Actions, read-your-writes) and `refresh`.
  - PPR / `dynamicIO` / `useCache` flags replaced by `cacheComponents: true`.
  - `next lint` removed and `next build` no longer lints; the `eslint`
    config key is gone.
  - `serverRuntimeConfig` / `publicRuntimeConfig` removed; `images.domains`
    deprecated; several `next/image` defaults changed; parallel routes need
    `default.js`; AMP removed.
  - `npx @next/codemod@canary agents-md` points `AGENTS.md` at docs bundled
    in `node_modules/next/dist/docs/`; from 16.2 `next dev` keeps it current.

## Tailwind CSS

- tailwindcss 4.3.3 (2026-07-16). 4.3.0 (2026-05-08) added `@container-size`,
  scrollbar, scrollbar-gutter, zoom and tab utilities; 4.2 added new palettes
  (mauve, olive, mist, taupe) and a webpack plugin.
  Source: github.com/tailwindlabs/tailwindcss/releases. [primary] / [registry]

## Go

- Latest toolchain go1.27.3; go1.26.10 is the other supported line.
  Source: proxy.golang.org/golang.org/toolchain/@v/list. [registry]
- Go 1.26 (Feb 2026): `new(expr)`, `go fix` rebuilt on the analysis framework
  (modernizers), `cmd/doc`/`go tool doc` removed in favour of `go doc`, new
  `crypto/hpke`, experimental `simd/archsimd`, new garbage collector.
  Source: go.dev/doc/go1.26 (via search). [primary]
- Go 1.27 release notes not yet reviewed here. **Open question.**
- golangci-lint v2.15.0, pgx v5.11.0, sqlc v1.31.1, aws-sdk-go-v2 v1.47.4. [registry]

## Postgres

- Latest minors: 18.6, 17.11, 16.15, 15.19, 14.24; 13.23 is the final 13.x
  (13 is EOL). PostgreSQL 19 is at RC1, not GA as of 2026-10-23.
  Source: git tags of github.com/postgres/postgres. [primary]
- PG 14 reaches end of life in November 2026 (five-year policy). [policy,
  from memory — confirm on postgresql.org/support/versioning]
- PG 19 headline features per beta notes (may change before GA): `REPACK`
  (with `CONCURRENTLY`), `WAIT` for read-your-writes on standbys, logical
  replication of sequences, `pg_plan_advice`. [secondary + beta announcement]

## Shopify

- Official app template is React Router (`Shopify/shopify-app-template-react-router`);
  the Remix template is deprecated. Template pins Admin API `2026-10`
  (`ApiVersion.October26`), `future.expiringOfflineAccessTokens: true`,
  app-specific webhooks declared in `shopify.app.toml`, Prisma session
  storage, Node `>=22.12`. Source: template repo main branch. [primary]
- @shopify/cli 4.9.4, @shopify/shopify-app-react-router 4.0.0,
  @shopify/shopify-app-remix 6.0.2 (existing apps), @shopify/polaris (React)
  last published 2025-03-26. [registry]
- Polaris web components are the default UI for new apps; Polaris React is in
  maintenance. [secondary: Shopify community forum, Gadget blog]
- Shopify Scripts: editing frozen 2026-04-15, execution stopped 2026-06-30;
  replacement is Shopify Functions. Source: shopify.dev changelog (via
  search). [primary]

## AWS

- aws-cdk-lib 2.274.0; CDK CLI `aws-cdk` 2.1146.1 (CLI versioned separately
  from the library). [registry]
- Lambda: `nodejs24.x` deprecation 2028-04-30; `python3.14` 2029-06-30;
  `nodejs26.x` and `python3.15` in preview. Cached doc copies disagree on
  older runtimes (Node 20 2026-04-30, Python 3.10 2026-10-31).
  Source: docs.aws.amazon.com lambda-runtimes (via search). [primary, cached]

## Google Cloud

- Container Registry is shut down; Artifact Registry (including `gcr.io`
  repositories hosted in AR) replaces it. Source: cloud.google.com
  Artifact Registry transition docs (via search). [primary]

## Firebase

- firebase (JS) 13.1.0, firebase-admin 14.5.0, firebase-functions 7.4.0,
  firebase-tools 15.34.1; FlutterFire firebase_core 5.1.0, cloud_firestore
  7.1.0. [registry]
- Dynamic Links shut down 2025-08-25. Firebase Extensions service shuts down
  2027-03-31; deployed extensions keep running but can't be updated through
  Firebase; CLI 15.32.0+ has migration tooling to Cloud Functions (2nd gen).
  Source: firebase.google.com Extensions FAQ and Dynamic Links FAQ (via
  search). [primary]

## Supabase

- supabase-js 2.118.0, CLI 2.122.0, @supabase/ssr 0.12.7, supabase_flutter
  2.18.3. [registry]
- API keys: publishable `sb_publishable_...` replaces `anon`, secret
  `sb_secret_...` replaces `service_role`; legacy keys deprecated by end of
  2026. New keys are not JWTs: send them in the `apikey` header, not as a
  Bearer token. Source: supabase docs guides/functions/auth-headers.mdx,
  guides/api/api-keys (via search). [primary]
- Tables need explicit `grant`s to be reachable via the Data API; bundle
  grants with RLS in the same migration. Views bypass RLS unless made
  `security_invoker`. Wrap `auth.uid()` as `(select auth.uid())` and index
  policy columns. Source: supabase/supabase apps/docs guides/api/securing-your-api.mdx,
  guides/database/postgres/row-level-security.mdx. [primary]
- Declarative schemas live in `supabase/schemas/`; migrations generated with
  `supabase db schema declarative sync` on the `pg-delta` diff engine
  (default for new `supabase init`; legacy projects use `migra`).
  Source: guides/local-development/declarative-database-schemas.mdx,
  diff-engines.mdx. [primary]

## Flutter

- Flutter 3.47.7 stable (2026-10-08), Dart 3.13.5.
  Source: storage.googleapis.com/flutter_infra_release/releases/releases_linux.json. [registry]
- flutter_riverpod 3.4.3, flutter_bloc 9.1.1, go_router 18.1.1, freezed 4.0.3,
  dio 5.11.1, flutter_lints 6.0.0, very_good_analysis 11.0.0. [registry]

## Open questions

- Go 1.27 release notes: what changed, and does it affect our lint config?
- TS 6.0 deprecation list: confirm against the official release notes.
- Exact Supabase date when legacy `anon`/`service_role` keys stop working.
- Current Google Play target-API and App Store Xcode/SDK minimums for
  Flutter releases.

## Recommendation for the library

Create one skill per technology with a "Changed recently" section that cites
this note. Re-run this research every 90 days (or when a major version
ships) and bump each affected skill's `last-reviewed`.

## CLI commands verified (2026-10-23)

Ran `--help` against the installed tools: firebase-tools 15 (`deploy --only`,
`deploy --dry-run`, `emulators:exec`), Shopify CLI 4 (`app function run`,
`app webhook trigger`), Supabase CLI 2.122.0 (`db schema declarative`,
`test db`, `gen types --local`; the older `gen types typescript` form is no
longer documented), gcloud (`run services logs read`). supabase-js exposes
`auth.getClaims()`.

## From prior knowledge (before 2026-06), not re-verified here

Used in the skills because they are long-standing and well documented, but
not checked against a source in this pass:

- Tailwind v3 → v4 utility renames, v4 browser floor (Safari 16.4 / Chrome
  111 / Firefox 128), `@custom-variant` dark-mode syntax.
- ESLint flat config only (legacy `.eslintrc` removed in ESLint 10).
- Go 1.24/1.25 features (`tool` directive, `t.Context()`, `testing.B.Loop`,
  `os.Root`, `testing/synctest`, `sync.WaitGroup.Go`, container-aware
  `GOMAXPROCS`).
- PostgreSQL 18 features (`uuidv7()`, virtual generated columns, AIO, skip
  scan, `OLD`/`NEW` in `RETURNING`) and the zero-downtime migration patterns.
- Shopify: REST Admin API legacy and GraphQL required for new public apps;
  compliance webhooks; quarterly API versions supported ~12 months.
- AWS JS SDK v2 and Go SDK v1 end of support (2025); Cloud Functions renamed
  Cloud Run functions (2024).
