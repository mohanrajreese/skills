---
name: shopify
description: How we build Shopify apps (React Router template, Admin GraphQL API, webhooks, Polaris web components), Shopify Functions and Liquid themes with the Shopify CLI, including API versioning and the deprecations that bite such as Scripts shutdown, the Remix template and REST Admin. Use whenever working on a Shopify app, theme, checkout or extension, writing Liquid, GraphQL Admin queries, webhooks or Functions, handling app install or auth, upgrading the Shopify API version, or when you see shopify.app.toml, shopify.extension.toml, .liquid files or the Shopify CLI.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, shopify, ecommerce]
---

# Shopify

Three surfaces with different rules: **apps** (a web app embedded in the
admin), **extensions/Functions** (code Shopify runs inside checkout and
admin), and **themes** (Liquid storefronts). Work out which one you're in
first.

## Before you start

1. Identify the surface: `shopify.app.toml` → app; `extensions/*/shopify.extension.toml`
   → app extension or Function; `layout/theme.liquid` + `sections/` → theme.
2. **Pin the API version.** Find it in `shopify.app.toml`
   (`[webhooks] api_version`), `shopify.server.ts` (`apiVersion`) and
   extension tomls. Shopify ships quarterly versions (`YYYY-01/04/07/10`),
   each supported for about a year. Use the docs for that version.
3. For apps, check the framework: the **React Router** template
   (`@shopify/shopify-app-react-router`) is current; Remix-based apps
   (`@shopify/shopify-app-remix`) are legacy and have an upgrade path.

## Defaults for new work

- New apps: `shopify app init` with the React Router template, Admin
  **GraphQL** API (REST Admin is legacy, and new public apps must use
  GraphQL), Polaris **web components** for UI, app-specific webhooks declared
  in `shopify.app.toml`.
- Custom checkout, discount, shipping or payment logic: **Shopify Functions**
  and Checkout UI extensions, never Scripts or `checkout.liquid`.
- Themes: Online Store 2.0 (JSON templates, sections and blocks), editable
  in the theme editor; no hardcoded content merchants should control.

## Verify loop

```bash
shopify app dev                     # tunnel + dev store; reinstall if scopes changed
npm run typecheck && npm run lint
npm run graphql-codegen             # if the app uses typed GraphQL
shopify app function run            # inside a Function's folder, with a sample input
shopify app deploy                  # pushes config, webhooks and extensions
shopify theme dev --store <store>   # themes: live preview
shopify theme check                 # themes: Liquid lint
```

## Rules that matter

- **Auth:** go through `authenticate.admin(request)` /
  `authenticate.webhook(request)` / `authenticate.public.*` from the app
  package; never hand-roll OAuth or HMAC checks.
- **Webhooks:** declare them in the toml (Shopify syncs them on deploy);
  respond with 200 fast and process asynchronously; make handlers
  idempotent (deliveries repeat, and the webhook ID header identifies them).
  Public apps must handle the three compliance topics
  (`customers/data_request`, `customers/redact`, `shop/redact`).
- **GraphQL limits:** cost-based rate limiting. Request only the fields you
  need, paginate with cursors, and use bulk operations for large
  exports/imports.
- **Scopes:** request the minimum; changing scopes forces merchants to
  re-approve.
- **Embedded app navigation:** use the router's `Link`/App Bridge, not raw
  `<a>`, or the session breaks inside the admin iframe.
- **Themes:** keep logic in snippets, pass data with `render` parameters
  (not `include`), lazy-load images with `image_url` + `image_tag`, and test
  in the theme editor, not only on the storefront.

## Changed recently (checked 2026-10-23)

- Current template targets Admin API **2026-10** and sets
  `future.expiringOfflineAccessTokens: true` (offline tokens expire and are
  refreshed by the library, so don't cache them forever elsewhere).
- **Shopify Scripts stopped executing on 2026-06-30** (editing froze
  2026-04-15). Any remaining Script logic must be rebuilt as Functions:
  line items → Discount / Cart Transform / Validation APIs, shipping →
  Delivery Customization, payments → Payment Customization.
- **Remix app template deprecated** in favour of React Router (the
  `Upgrading from Remix` guide in the template repo's wiki).
- **Polaris React is in maintenance**; new UI uses Polaris web components
  (`s-page`, `s-button`, …) loaded by App Home.
- Shopify CLI is at 4.x; old `@shopify/app`/`@shopify/theme` 3.x installs
  should be updated.

## Pitfalls

- Testing webhooks only via `shopify app webhook trigger`: the `admin`
  context is `undefined` for CLI-triggered events, so trigger real events in
  a dev store too.
- Webhooks created in the Shopify admin UI fail HMAC validation for your app;
  use toml-declared subscriptions.
- Forgetting to bump the API version each quarter until a version is retired
  and calls start failing.

## Sources

- `research/2026-10-23-stack-baseline.md` → Shopify section (template repo,
  shopify.dev changelog).
