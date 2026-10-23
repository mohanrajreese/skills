---
name: nextjs
description: How we build and upgrade Next.js App Router apps, covering Server and Client Components, Server Actions, caching and revalidation, proxy (formerly middleware), env vars and deployment, with the Next.js 16 breaking changes models often get wrong. Use whenever working in a Next.js project, writing pages, layouts, route handlers or server actions, debugging caching or hydration, configuring next.config, upgrading Next.js or React, or when you see next.config, app/ or proxy.ts. Pair with the typescript and tailwind skills.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, nextjs, react, frontend]
---

# Next.js

Next.js 16 changed several defaults and renamed APIs. The most common
mistake is writing Next 14-style code into a Next 16 project, so step 1
always comes first.

## Before you start

1. **Check the installed version** (`npm ls next`) and router (`app/` vs
   `pages/`). Write for *that* version.
2. **Use version-matched docs.** Next 16.2+ bundles docs in
   `node_modules/next/dist/docs/`, and `AGENTS.md` can point at them
   (`npx @next/codemod@canary agents-md`). When unsure about an API, read
   the bundled docs rather than relying on memory.
3. Check `next.config.*` for `cacheComponents`, `reactCompiler`, image
   config and custom webpack settings (Turbopack is now the default bundler).

## Defaults for new projects

- App Router, TypeScript, Tailwind v4, ESLint or Biome run directly (not via
  `next lint`, which no longer exists).
- Server Components by default; `"use client"` only on the interactive leaves.
- Data reads in Server Components; writes through Server Actions or route
  handlers.
- Deploy target decided up front (Vercel, Firebase App Hosting, a container
  on Cloud Run/ECS); it affects image optimisation, ISR and caching.

## Verify loop

```bash
npm run build            # catches server/client boundary and type errors dev mode misses
npx tsc --noEmit
npm run lint             # separate step: next build no longer lints
npm run dev              # click through the changed routes; watch the terminal for warnings
```

## Rules that matter

- **Server Actions are public HTTP endpoints.** Authenticate, authorise and
  validate input (zod) inside every action, even if the button is hidden.
- **Secrets stay server-side.** Only `NEXT_PUBLIC_*` vars reach the browser.
  Import `server-only` in modules that touch secrets or the DB so a client
  import fails the build.
- **Request APIs are async:** `await cookies()`, `await headers()`,
  `await params`, `await searchParams`.
- **Caching is explicit.** With `cacheComponents: true`, use `"use cache"`
  plus `cacheLife`/`cacheTag`. After mutations use
  `revalidateTag(tag, 'max')` for stale-while-revalidate, or `updateTag(tag)`
  inside a Server Action when the user must see their own write immediately.
- **Keep the client bundle small:** pass serialisable props from server to
  client components; don't import server-only libraries into `"use client"`
  files.

## Changed recently: Next.js 16 (checked 2026-10-23, latest 16.4)

- Node 20.9+ and TypeScript 5.1+ required; React 19.2+.
- Turbopack is the default for `dev` **and** `build`; `--webpack` opts out.
  Custom webpack config needs porting or the flag.
- Synchronous `cookies`/`headers`/`params`/`searchParams` access removed.
- `middleware.ts` → **`proxy.ts`** (export `proxy`). `proxy` runs on Node
  only, so code that needs the Edge runtime stays as `middleware`.
- `revalidateTag` needs a second argument (cacheLife profile); new
  `updateTag` and `refresh`.
- `experimental.ppr` / `dynamicIO` / `useCache` → `cacheComponents: true`.
- Removed: `next lint`, the `eslint` config key, `serverRuntimeConfig` /
  `publicRuntimeConfig` (use env vars), AMP. `images.domains` is deprecated
  (use `remotePatterns`); several `next/image` defaults changed. Parallel
  route slots need `default.js`.
- Upgrade path: `npx next@canary upgrade --agent=latest` or
  `npx @next/codemod@canary upgrade latest`, then work the official
  migration checklist. Don't enable Cache Components or React Compiler just
  to finish an upgrade.

## Pitfalls

- Hydration mismatches from `Date.now()`, `Math.random()`, locale formatting
  or `window` checks during render. Move them into effects or the server.
- Calling your own route handlers from Server Components (an extra network
  hop); call the underlying function directly.
- Putting auth checks only in `proxy`/layouts; check again where data is read.

## Sources

- `research/2026-10-23-stack-baseline.md` → Next.js section (official v16
  upgrade guide).
