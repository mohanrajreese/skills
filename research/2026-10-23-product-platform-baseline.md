# Product and platform baseline: integrations, security, AI, delivery

Questions:
1. What are the current rules, versions and recent changes for WhatsApp
   Business Platform, Razorpay, SSO libraries, security standards, AI/agent
   tooling and spec-driven development tools?
2. Which of these change often enough that a skill must say "check the live
   source" instead of stating a number?

Checked 2026-10-23. Source tags as in `2026-10-23-stack-baseline.md`:
**[registry]**, **[primary]**, **[secondary]**.

## WhatsApp Business Platform

- **Business-scoped user IDs (BSUIDs):** Meta began sharing BSUIDs in April
  2026 to support WhatsApp usernames; support is required for all partners
  and directly integrated businesses. The BSUID appears as `user_id` in
  message webhooks. Sending to a BSUID was announced for July 2026. Business
  username reservation opened 2026-06-29. Source: Meta developer docs
  "Business-scoped user IDs" and the WhatsApp changelog (via search).
  [primary]
- A user who has set a username may not expose their phone number to a
  business they message for the first time. Username rollout reportedly
  paused in India. [secondary]
- **AI policy:** from 2026-01-15, providers whose general-purpose AI
  assistant *is* the product may not use the Business API (applied to new
  users from 2025-10-15). Business bots for support, booking and order
  tracking remain allowed; Meta decides edge cases. From 2026-02-16 Meta
  charges "AI Providers" for non-template messages in countries where it must
  support them. [secondary: multiple news outlets, respond.io; consistent]
- **Pricing:** per-message pricing by template category (marketing,
  utility, authentication, service) has applied since 2025-07-01 [prior
  knowledge]. Reports of further changes on 2026-10-01 (service and
  in-window utility messages becoming billable) **conflict** between sources.
  Check Meta's pricing page before quoting costs. [secondary, conflicting]
- On-Premises API was sunset in 2025; Cloud API is the supported path.
  [prior knowledge]

## Razorpay

- SDKs: `razorpay` npm 2.9.8, PyPI 2.0.1, Go `razorpay-go` v1.4.1, Flutter
  `razorpay_flutter` 1.4.7. [registry]
- Node SDK helpers: `Razorpay.validateWebhookSignature(body, signature,
  secret)` and `validatePaymentVerification({order_id | subscription_id,
  payment_id}, signature, secret)`. The payload is `order_id|payment_id` for
  orders and `payment_id|subscription_id` for subscriptions (HMAC-SHA256).
  Source: razorpay/razorpay-node `lib/utils/razorpay-utils.js`. [primary]
- **RBI e-mandate rules (2026 framework):** recurring debits up to ₹15,000
  per transaction without additional factor of authentication (AFA);
  ₹1,00,000 for insurance premiums, mutual fund subscriptions and credit
  card bills; pre-debit notification at least 24 hours before each debit.
  Source: Razorpay blog, Outlook Business (via search). [secondary] Confirm
  against the RBI circular for compliance decisions.
- Recurring payment confirmation can lag (reported up to T+3 days), so
  webhook handling must not assume same-day confirmation. [secondary: Chargebee
  docs]

## SSO / identity

- Libraries: `openid-client` 6.8.8, `@node-saml/node-saml` 5.1.0
  (`passport-saml` last published 2022, unmaintained), `better-auth` 1.7.12,
  `@auth/core` 0.41.3 / `next-auth` 4.24.15, `@clerk/nextjs` 7.9.19,
  `@auth0/nextjs-auth0` 4.33.0, `@workos-inc/node` 11.0.0; Python
  `django-allauth` 65.20.1, `authlib` 1.9.1, `pysaml2` 7.5.5
  (`python3-saml` last published 2023); Go `coreos/go-oidc/v3` v3.21.0,
  `crewjam/saml` v0.5.1. [registry]

## Security standards

- **OWASP Top 10:2025 is final.** A01 Broken Access Control (now includes
  SSRF), A02 Security Misconfiguration, A03 Software Supply Chain Failures
  (new), A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07
  Authentication Failures, A08 Software or Data Integrity Failures, A09
  Security Logging and Alerting Failures, A10 Mishandling of Exceptional
  Conditions (new). Source: github.com/OWASP/Top10 `2025/docs/en`. [primary]
- **OWASP GenAI LLM Top 10 2026** (published 2026-08-04): LLM01 Prompt
  Injection, LLM02 Sensitive Information Disclosure, LLM03 Excessive Agency,
  LLM04 Supply Chain, LLM05 Data and Model Poisoning, LLM06 Unbounded
  Consumption, LLM07 Misinformation, LLM08 Hidden Context Exposure, LLM09
  Vector and Embedding Weaknesses, LLM10 Improper Output Handling. Source:
  github.com/GenAI-Security-Project/GenAI-LLM-Top10 `2026/final`. [primary]
- OWASP ASVS 5.0 (May 2025) is the detailed verification standard. [prior
  knowledge]
- **India DPDP Act / Rules:** Rules notified 2025-11-13/14 with an 18-month
  phased rollout; core obligations (consent, notices, security safeguards,
  breach notification, children's data, rights) apply from about 2027-05-13.
  Consent-manager milestone dates conflict (mid-2026 vs November 2026).
  Source: AZB Partners, Mondaq, India Briefing (via search). [secondary,
  consistent on the overall structure]

## AI agents and agentic coding

- Claude models (cached 2026-10-06 in the `claude-api` skill): default
  `claude-opus-5-5` ($4/$20 per MTok); `claude-sonnet-5-5` ($2/$10);
  `claude-haiku-5-5` ($0.10/$0.50); `claude-fable-5-1` most capable
  ($10/$50). [primary: claude-api skill]
- API drift that breaks older code: assistant prefill rejected on current
  models; forced `tool_choice` (`any`/`tool`) returns 400 on Opus 5.5 /
  Sonnet 5.5 / Fable 5.1; `thinking: {type: "adaptive"}` replaces
  `budget_tokens`; `temperature`/`top_p`/`top_k` rejected from API version
  2026-10-21. [primary: claude-api skill]
- Four ways to build an agent: manual loop, SDK Tool Runner, Managed Agents
  (Anthropic hosts loop + sandbox), Claude Agent SDK (Claude Code harness as a
  library, self-hosted). [primary: claude-api skill]
- SDKs: `@anthropic-ai/sdk` 1.1.0, `anthropic` (PyPI) 2.1.0,
  `@anthropic-ai/claude-agent-sdk` 0.3.309, `claude-agent-sdk` (PyPI)
  0.2.173, `@modelcontextprotocol/sdk` 1.32.1, `mcp` (PyPI) 2.3.0, Vercel
  `ai` 7.0.150, Claude Code 2.1.309. [registry]
- **MCP spec:** revisions 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25,
  **2026-07-28** (latest). Source: modelcontextprotocol/modelcontextprotocol
  `docs/specification`. [primary] 2026-07-28 removes protocol-level sessions
  (no initialize handshake or `Mcp-Session-Id`), adds `server/discover` and an
  extensions framework; older versions enter a 12-month deprecation window.
  [secondary]
- Claude Code subagent frontmatter supports at least `name`, `description`,
  `tools`, `model`, plus `permissionMode`, `skills`, `mcpServers`, `hooks`,
  `memory`, `effort`, `background` (string evidence from the installed
  2.1.309 binary). [primary, indirect]

## Spec-driven development

- GitHub Spec Kit: `uv tool install specify-cli`, `specify init <project>
  --integration <agent>`; flow `/speckit-constitution` (once) →
  `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` →
  `/speckit-implement` → `/speckit-converge` (repeat until "Converged");
  extensions for bug fixing (`specify extension add bug`) and idea
  assessment (`specify extension add assess`). Source: github/spec-kit
  README. [primary]
- Kiro organizes specs per feature as requirements, design and tasks files,
  with steering docs. [secondary: martinfowler.com]

## Figma

- Official Figma MCP server + Figma plugin skills (`figma-design-to-code`
  mandatory before `get_design_context`; `figma-code-connect`;
  `figma-generate-design`; `figma-generate-library`). Design-to-code rules:
  request a screenshot as the visual target, reuse project components and
  Code Connect mappings, download every asset, no temporary Figma asset URLs
  in code. Source: installed Figma plugin skills. [primary]
- `@figma/code-connect` 2.0.2, `style-dictionary` 5.7.0. [registry]

## Payments and billing (other)

- `stripe` npm 23.0.1, PyPI 16.0.0. [registry]

## Open questions

- Exact WhatsApp pricing changes from 2026-10-01 and current per-country
  rates.
- Current Graph API version for WhatsApp Cloud API calls.
- RBI e-mandate category list: confirm against the RBI circular.
- DPDP consent-manager effective date.

## Verified against SDK source (2026-10-23)

- razorpay-python `razorpay/utility/utility.py`: `verify_payment_signature`,
  `verify_payment_link_signature`, `verify_subscription_payment_signature`,
  `verify_webhook_signature(body, signature, secret)`. [primary]
- razorpay-node `lib/utils/razorpay-utils.js`: `validateWebhookSignature`,
  `validatePaymentVerification` (order or subscription branch). [primary]

## From prior knowledge (before 2026-06), not re-verified here

- Razorpay webhook event-ID header name (`x-razorpay-event-id`) and the
  auto-refund of uncaptured authorized payments.
- WhatsApp webhook verification (`hub.mode` / `hub.verify_token` /
  `hub.challenge`, `X-Hub-Signature-256` with the app secret), 24-hour
  customer service window, template categories, per-message pricing since
  2025-07-01, Embedded Signup / Tech Provider for multi-tenant onboarding.
- OIDC/SAML validation rules (PKCE, state/nonce, assertion signature,
  audience, `InResponseTo`, replay cache); SCIM deprovisioning semantics.
- OWASP ASVS 5.0 (May 2025); the 2025 npm supply-chain worm campaign that
  targeted freshly published package versions.
- SaaS tenancy patterns, pricing practice (value metric, good/better/best,
  reverse trials, annual discount), subscription state machines, dunning.
