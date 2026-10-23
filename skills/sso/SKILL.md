---
name: sso
description: How we add login and enterprise single sign-on to our apps, covering OIDC and OAuth with PKCE, SAML 2.0, SCIM provisioning, social login, multi-tenant org-level SSO with domain verification, role mapping, and when to buy (WorkOS, Auth0, Clerk) versus self-host (Keycloak) versus use the platform (Supabase Auth, Firebase/Identity Platform, Cognito). Use whenever implementing authentication, adding Google or Microsoft login, onboarding an enterprise customer who asks for SSO, SAML or SCIM, debugging OIDC or SAML errors, or designing org and role models for a B2B SaaS.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [security, auth, sso, saas]
---

# SSO and authentication

Authentication bugs are security bugs. Use maintained libraries and
providers for the protocol work, and spend our effort on the tenant model:
which org a user belongs to, what role they get, and what happens when they
leave.

## Before you start

1. Find what the project already uses: Supabase Auth, Firebase Auth,
   Clerk, Auth0, Auth.js/better-auth, django-allauth, Cognito, Keycloak. Add
   SSO *through* it if it supports it.
2. Clarify the requirement: social login (Google, Apple, Microsoft),
   **enterprise SSO** (customer's IdP: Okta, Entra ID, Google Workspace,
   JumpCloud), and/or **SCIM** (automatic user provisioning and
   deprovisioning).

## Choose the approach

| Situation | Default |
|---|---|
| B2B SaaS that will sell to enterprises | Managed SSO provider (WorkOS, Auth0, Clerk) or platform SSO (Supabase SAML, Identity Platform); per-org connections + SCIM without building SAML yourself |
| Self-hosting or data-residency needs | Keycloak / Zitadel as the IdP broker |
| Django app | `django-allauth` (supports OIDC and SAML) |
| Next.js app | the project's auth library; `openid-client` for raw OIDC |
| Go service | `coreos/go-oidc` for OIDC; SAML only via a maintained library |

Never hand-roll SAML XML signature validation.

## Rules that matter

- **OIDC:** authorization code flow with **PKCE**; validate `state` and
  `nonce`; verify the ID token's signature, `iss`, `aud`, `exp`. No implicit
  flow.
- **SAML:** validate the signature on the assertion (not just the response),
  audience, recipient/ACS URL, time window, and `InResponseTo`; cache
  assertion IDs to stop replay. Treat IdP-initiated login as higher risk.
- **Multi-tenant SSO:** SSO connections belong to an **organization**.
  Require **domain verification** (DNS TXT) before an org can claim
  `@company.com` users or enforce SSO for them.
- **Account linking** only on a *verified* email from a trusted source.
  Never auto-link because the emails match.
- **Roles:** map IdP groups to app roles explicitly; default to the least
  privileged role; keep at least one **break-glass admin** login that
  doesn't depend on the customer's IdP.
- **Deprovisioning:** SCIM `active=false` or a deleted user must revoke
  sessions and API tokens immediately, not at next login.
- **Sessions:** short-lived access tokens, rotating refresh tokens,
  server-side session revocation; secure, HttpOnly, SameSite cookies.
- Offer **passkeys/MFA** for password users; enforce MFA for admin roles.

## Verify loop

- Test against a real IdP dev tenant (Okta developer, Entra ID test tenant,
  Google Workspace) or a local Keycloak container, not only mocks.
- Negative tests: wrong audience, expired assertion, replayed assertion,
  unsigned assertion, email from an unverified domain, deprovisioned user
  with a live session.
- Walk the customer's admin setup steps yourself; SSO setup docs are part
  of the product.

## Changed recently (checked 2026-10-23)

- `passport-saml` and `python3-saml` haven't been published since
  2022–2023; prefer `@node-saml/node-saml` 5.x and `pysaml2` 7.x or a
  managed provider.
- Current majors: `openid-client` 6, `django-allauth` 65, `go-oidc` v3,
  `@workos-inc/node` 11, `@clerk/nextjs` 7, `better-auth` 1.

## Pitfalls

- "Sign in with Google" for a B2B app treated as SSO; it doesn't give the
  customer control over deprovisioning or org membership.
- Enforcing SSO before testing the org admin's own login, which locks the
  customer out.
- Storing IdP certificates without tracking expiry; rotations break logins
  silently.

## Sources

- `research/2026-10-23-product-platform-baseline.md` → SSO / identity.
