---
name: saas
description: Our blueprint for building multi-tenant B2B and B2C SaaS products, covering the tenancy model, organizations and roles, auth and SSO, billing and entitlements, onboarding, admin and support tooling, audit logs, notifications, observability, rate limits, data export and deletion, backups, and a launch checklist of what must exist on day one versus later. Use whenever starting a new SaaS product, adding multi-tenancy or teams and workspaces to an app, planning a SaaS MVP, reviewing a SaaS architecture, or preparing a SaaS launch.
metadata:
  status: seed
  version: 0.2.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [saas, architecture, product]
---

# SaaS blueprint

Some SaaS foundations are painful to retrofit (tenant isolation, org
model, audit trail, billing events). Build those on day one even in an MVP;
defer the rest.

## Tenancy model

| Model | Use when | Notes |
|---|---|---|
| **Pooled: shared tables + `org_id`** (default) | Most SaaS | Every tenant table has `org_id NOT NULL`, indexed; enforce with Postgres RLS (Supabase) or a mandatory query scope (Django manager, repository layer in Go) |
| Schema per tenant | Strong isolation for a few hundred tenants | Migrations run N times |
| Database per tenant | Enterprise/regulatory isolation, data residency | Highest ops cost; automate provisioning |

Write a test that proves tenant A can't read tenant B's data through every
API surface.

## Core domain model

`users` ↔ `memberships(role)` ↔ `organizations`, plus `invitations`,
`api_keys` (scoped, hashed), `audit_events`, `subscriptions` and
`entitlements` (see `subscription-billing`). A user can belong to several
organizations; the active org is explicit in every request.

## Day one vs later

| Day one (MVP) | Later (when customers ask) |
|---|---|
| Org + membership + roles (owner, admin, member) | Custom roles / fine-grained permissions |
| Email + Google login, MFA for admins | Enterprise SSO (SAML/OIDC), SCIM (`sso`) |
| Tenant isolation + tests | Schema/db-per-tenant, data residency |
| Billing with webhooks + entitlements | Usage-based billing, invoicing/PO flows |
| Audit log of security and billing events | Customer-visible audit log export |
| Transactional email (and WhatsApp if India-first) | In-app notification centre, digests |
| Error tracking, structured logs, uptime check | Tracing, per-tenant dashboards, status page |
| Per-tenant rate limits on expensive endpoints | Plan-based quotas UI |
| Data export + account deletion path (DPDP/GDPR) | DPA templates, sub-processor list page |
| Automated backups with a tested restore | Point-in-time recovery drills, multi-region |
| Admin panel with **audited** impersonation | Support tooling, health scores |

## Rules that matter

- **The org is the customer.** Billing, settings, data ownership and SSO
  attach to the org, not the user.
- Feature flags and entitlements are separate: flags roll out code;
  entitlements reflect what the customer paid for.
- Every background job and webhook carries `org_id` and runs with the same
  tenant scoping as requests.
- Noisy-neighbour protection: per-org rate limits and job concurrency caps,
  especially for AI and messaging features.
- Environments: dev / staging / prod with separate databases, keys and
  payment/WhatsApp test modes.

## Launch checklist

- [ ] Signup → onboarding → first value in minutes (measure it)
- [ ] Pricing page and billing live in production mode
- [ ] Terms, privacy policy, cookie/consent where required
- [ ] Security baseline from `security` done; secrets rotated from dev
- [ ] Backups restored once; on-call/alerting owner named
- [ ] Support channel and status communication path
- [ ] Analytics on activation, conversion, retention

## Next steps

Shape the product with `brainstorm` → `feature-feasibility` → pick the stack
with `tech-stack-chooser` → design with `system-design` → estimate with
`cloud-cost-planning` → build with `spec-driven-development` → launch with
`marketing`.
