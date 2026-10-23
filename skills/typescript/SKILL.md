---
name: typescript
description: How we configure, type-check, lint and test TypeScript and Node.js code, including the TypeScript 7 native compiler and the TypeScript 6 default and deprecation changes that break older tsconfig files. Use whenever writing or reviewing TypeScript or JavaScript, editing tsconfig.json or package.json, fixing type errors, setting up ESLint, Biome, Vitest or Playwright, choosing a Node version, or upgrading TypeScript. For framework specifics also use the nextjs or shopify skills.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, typescript, node, frontend, backend]
---

# TypeScript

Strict types at the edges, fast feedback in the middle, and awareness of the
TypeScript 6 → 7 transition that is changing tsconfig behaviour.

## Before you start

1. Check the package manager from the lockfile (`package-lock.json` → npm,
   `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lock` → bun). Use only
   that one.
2. Check the installed TypeScript major (`npx tsc -v`) and read
   `tsconfig.json` before suggesting options. Defaults changed in 6.0, so the
   same config means different things on 5.x and 6+.
3. Check the Node version (`.nvmrc`, `engines`, CI, Dockerfile).

## Defaults for new projects

- Node: current Active LTS (24 today; 26 when it enters LTS). Node 20 is
  end-of-life.
- `tsconfig`: `"strict": true`, `"noUncheckedIndexedAccess": true`,
  `"verbatimModuleSyntax": true`, explicit `"types"` (e.g. `["node"]`),
  `"moduleResolution": "bundler"` for bundled apps or `"nodenext"` for Node
  packages. No `baseUrl`; put full prefixes in `paths`.
- Lint/format: ESLint (flat config) + typescript-eslint + Prettier, **or**
  Biome alone. Pick one per repo.
- Tests: Vitest for unit tests, Playwright for end-to-end.
- Runtime validation at boundaries: zod (v4).

## Verify loop

```bash
npx tsc --noEmit          # or the project's "typecheck" script
npm run lint              # whatever the repo defines
npx vitest run            # unit tests
npx playwright test       # e2e, when the change touches user flows
```

## Rules that matter

- Never silence the compiler with `any`, `as unknown as T`, or `// @ts-ignore`
  without a comment saying why; prefer `unknown` + narrowing.
- Parse, don't cast: data from `fetch`, `JSON.parse`, env vars, forms and
  webhooks goes through a schema (zod) before it is typed.
- Model states with discriminated unions; use `satisfies` to check object
  literals without widening.
- `import type` for type-only imports (required with `verbatimModuleSyntax`).
- Handle every promise: `await` it, return it, or explicitly `void` it with a
  reason. Floating promises hide errors.

## Changed recently (checked 2026-10-23)

- **TypeScript 7.0** (Jul 2026) is the native (Go) compiler and `latest` on
  npm; builds are roughly 10× faster. The command is still `tsc`. It has
  **no stable programmatic API yet**, so typescript-eslint and other
  API-based tools may need TS 6 alongside it (`@typescript/typescript6`,
  binary `tsc6`). If lint breaks after upgrading, check that first. Projects
  can stay on 5.9/6.x until their tooling supports 7.
- **TypeScript 6.0** changed defaults: `strict` on, `module: esnext`,
  **`types: []`** (global types like `process` or `describe` vanish unless
  listed in `"types"`), `rootDir` = the tsconfig's folder. It deprecated
  `moduleResolution: node`/`node10`, `baseUrl`, AMD/UMD/System output and
  import `asserts`, and 7.0 removes them. `"ignoreDeprecations": "6.0"` is
  a temporary escape hatch, not a fix. (Exact list from secondary sources;
  confirm against the official notes when upgrading.)
- **ESLint 10** and **Vitest 5** are current. Use flat config
  (`eslint.config.js`); legacy `.eslintrc` is gone.

## Pitfalls

- Fixing type errors by loosening `tsconfig` (turning off `strict` or
  `noUncheckedIndexedAccess`) instead of fixing the code.
- Path aliases that work in the editor but not at runtime: the bundler,
  test runner and Node all need the same alias config.
- `Date`, `bigint` and `Map` don't survive `JSON.stringify`; serialize
  explicitly across network boundaries.

## Sources

- `research/2026-10-23-stack-baseline.md` → TypeScript / Node tooling.
