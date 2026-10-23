---
name: security
description: How we keep apps secure across our stack, covering lightweight threat modeling, the OWASP Top 10 2025 and the OWASP GenAI LLM Top 10 2026 as review checklists, secrets handling, dependency and supply-chain hygiene, authorization, security headers, logging, incident basics, and India DPDP Act and GDPR data duties. Use whenever reviewing code or a design for security, handling personal or payment data, adding auth or file uploads or webhooks or AI features, preparing a release or security questionnaire, responding to a vulnerability or leaked secret, or setting up scanning in CI.
metadata:
  status: seed
  version: 0.2.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [security, compliance, review]
---

# Security

Security is a review habit with checklists, not a phase. This skill gives
the checklists and says where each risk usually hides in *our* stack.

## Before you start

1. Identify the assets: personal data, payment data, credentials, tenant
   data, money movement, admin actions.
2. **Threat-model in 10 minutes** for any new feature: list the entry points
   (HTTP, webhooks, queues, uploads, LLM inputs), who can reach them, and
   what an attacker gains. Write the top 3 risks into the spec.
3. Check which stack skills apply (`django`, `nextjs`, `supabase`,
   `firebase`, …); each lists its stack-specific security rules.

## Review checklist: OWASP Top 10:2025

| # | Risk | Where it bites us |
|---|---|---|
| A01 | Broken Access Control (incl. SSRF) | Missing object-level checks; Supabase RLS/grants; Firebase rules; server actions; URL fetchers |
| A02 | Security Misconfiguration | `DEBUG=True`, open buckets, permissive CORS, default service accounts |
| A03 | Software Supply Chain Failures | Unpinned deps, install scripts, compromised packages, unreviewed CI actions |
| A04 | Cryptographic Failures | Homegrown crypto, weak password hashing, secrets in code |
| A05 | Injection | String-built SQL, shell commands, template injection, LLM output used as code/SQL |
| A06 | Insecure Design | No rate limits, trust in client-side checks, no abuse cases in the spec |
| A07 | Authentication Failures | Session handling, MFA gaps, account linking (see `sso`) |
| A08 | Software or Data Integrity Failures | Unverified webhooks (WhatsApp, Razorpay, Shopify), unsigned updates, unsafe deserialization |
| A09 | Security Logging and Alerting Failures | No audit trail for admin/money actions; no alerts |
| A10 | Mishandling of Exceptional Conditions | Fail-open error paths, stack traces to users, partial writes on errors |

## AI features: OWASP GenAI LLM Top 10 2026

Prompt injection (LLM01), sensitive information disclosure (LLM02),
**excessive agency** (LLM03), supply chain (LLM04), data/model poisoning
(LLM05), **unbounded consumption** (LLM06), misinformation (LLM07), hidden
context exposure (LLM08), vector/embedding weaknesses (LLM09), **improper
output handling** (LLM10). In practice: treat all model input from users,
documents, web pages and tool results as untrusted; give agents the minimum
tools and require human approval for irreversible actions; cap tokens,
cost and loop length per user; never execute or render model output
without validation (see `ai-agents`).

## Baseline controls for every project

- **Secrets:** env/secret manager only; secret scanning in CI (gitleaks or
  GitHub secret scanning) and pre-commit. A leaked secret is **rotated**,
  not just deleted from git.
- **Dependencies:** lockfiles committed; `npm audit` / `pip-audit` /
  `govulncheck` / `osv-scanner` in CI; Dependabot or Renovate. Review new
  dependencies; prefer a short delay before adopting brand-new releases
  (supply-chain worms target fresh versions). Pin GitHub Actions to SHAs.
- **SAST:** Semgrep or CodeQL on PRs. Claude Code's `/security-review` for a
  focused pass on a diff.
- **Authorization** checked server-side on every read and write of tenant
  data; tests for "user B can't read user A's object".
- **Input/output:** validate at boundaries; parameterised queries; encode
  output; size limits on uploads, with type checks and storage outside the
  web root.
- **HTTP:** HTTPS only, HSTS, CSP, secure cookies, CORS allow-lists, rate
  limiting on auth, OTP, webhook and AI endpoints.
- **Audit log** for logins, role changes, exports, payments, admin actions.
- **Backups** tested by restoring.

## Data protection (India DPDP, GDPR)

Go deeper with `data-security` (data lifecycle controls) and
`india-it-compliance` (IT Act, CERT-In, intermediary rules).


- Collect the minimum; record purpose and consent; support access,
  correction and deletion requests; keep a breach-notification runbook.
- **DPDP Rules** were notified in Nov 2025 with an 18-month phase-in; core
  obligations apply from around **May 2027**. Build consent, notices, data
  deletion and breach handling now. GDPR applies if you serve EU users.
- Keep personal data out of logs, analytics events, LLM prompts sent to
  third parties (unless covered by terms) and error trackers.

## Incident basics

Leaked secret → rotate → check usage logs → scope impact → notify if
required → retro (`skill-retro`). Vulnerability report → acknowledge →
reproduce → fix → disclose.

## Sources

- `research/2026-10-23-product-platform-baseline.md` → Security standards
  (OWASP Top10 repo, OWASP GenAI LLM Top 10 2026, DPDP reporting).
