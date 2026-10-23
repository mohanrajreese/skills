---
name: whatsapp-integration
description: How we integrate the WhatsApp Business Platform (Cloud API) for notifications, two-way support chat, OTP, interactive messages, Flows and AI-assisted bots, covering templates, the 24-hour window, webhooks, BSUIDs and usernames, Meta's AI chatbot policy, pricing and multi-tenant onboarding. Use whenever building or debugging anything that sends or receives WhatsApp messages, choosing between Meta's Cloud API and a BSP such as Gupshup, Interakt, AiSensy or Twilio, designing message templates, handling WhatsApp webhooks, adding a bot or AI agent on WhatsApp, or estimating WhatsApp messaging costs.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [integration, messaging, whatsapp, india]
---

# WhatsApp integration

WhatsApp is a regulated channel. Meta controls who you may message, when,
with what content and at what price. Most failed integrations ignored one of
those rules rather than hitting a technical bug.

## Before you start

1. **Decide the access path:**
   - **Direct Cloud API** (Meta-hosted, Graph API): lowest per-message cost
     and full control, but you own templates, webhooks, compliance and support.
   - **BSP** (Gupshup, Interakt, AiSensy, Twilio, 360dialog, …): faster
     onboarding, inbox UI, and support in India; adds markup and lock-in.
   - **Multi-tenant SaaS** onboarding *your customers'* numbers: become a
     Meta Tech Provider and use **Embedded Signup**.
2. Confirm prerequisites: Meta Business portfolio (verified), WhatsApp
   Business Account, a phone number not registered on the consumer or
   Business app, approved display name.
3. **Check the AI policy if a bot is involved** (see "Changed recently").

## Core rules

- **Opt-in first.** Message only users who opted in to WhatsApp messages
  from you. Store when and where they opted in.
- **24-hour customer service window:** after a user messages you, you can
  reply with free-form messages for 24 hours. Outside the window you can
  only send **approved templates**.
- **Templates** have a category (marketing, utility, authentication) that
  drives price and approval. Meta can re-categorise them. Keep utility
  templates strictly transactional; anything promotional is marketing.
- **Quality rating and messaging limits** gate how many unique users you can
  reach per day. Blocks and reports lower quality, so don't spam marketing
  templates.

## Webhooks

```text
GET  /webhooks/whatsapp   verify: if hub.mode == "subscribe" and hub.verify_token matches → return hub.challenge
POST /webhooks/whatsapp   verify X-Hub-Signature-256 = HMAC-SHA256(raw body, APP SECRET) → enqueue → 200 fast
```

- Verify the signature on the **raw** body before parsing.
- Acknowledge fast (return 200) and process asynchronously. Meta retries on
  failure, so **dedupe by message ID** (`messages[].id`) and status IDs.
- Handle `statuses` (sent, delivered, read, failed with error codes) as
  well as `messages`. Failed statuses are where template, policy and payment
  problems show up.
- Download media by media ID promptly (media URLs are short-lived and need
  the access token); store it in your own bucket.

## Defaults for new work

- Model contacts with **BSUID as the primary identity** and phone number
  as an optional attribute (see below).
- Keep template definitions in the repo (name, language, category, body,
  variables, example values) and sync them by script, so they're reviewable
  and not edited ad hoc in the dashboard.
- Use **system-user access tokens** (long-lived, scoped) for server calls,
  stored in a secret manager; never use a personal user token.
- Pin the Graph API version in config and upgrade it deliberately.
- Interactive messages (reply buttons, lists) and **WhatsApp Flows** (forms)
  beat free-text parsing for structured input.
- OTPs: use authentication templates with copy-code or one-tap buttons. Not
  marketing or utility templates.

## Changed recently (checked 2026-10-23)

- **BSUIDs and usernames:** since April 2026 webhooks carry a
  business-scoped user ID (`user_id`). Users with a username may not share
  their phone number with you. Support for BSUIDs is mandatory. Don't key
  contacts only by phone. Sending to a BSUID was announced for July 2026;
  confirm in the changelog.
- **AI policy (from 2026-01-15):** general-purpose AI assistants whose main
  product *is* the chatbot are banned from the Business API. Bots that serve
  the business's own customers (support, booking, order status) are allowed.
  Keep any AI agent scoped to your business use case, with a human handoff.
- **Pricing:** per-message pricing by category since July 2025; further
  changes around 2026-10-01 are reported inconsistently. **Always check
  Meta's current pricing page** before estimating (see `cloud-cost-planning`).
- On-Premises API is sunset. Use the Cloud API.

## Verify loop

- Send each template to the test number(s) from the app dashboard; check
  every variable renders.
- Replay recorded webhook payloads (message, status, failed status, media)
  through the handler in tests, including duplicate deliveries.
- Check a message outside the 24-hour window fails cleanly and falls back
  to a template.

## Pitfalls

- Treating `200 OK` from the send API as delivered; delivery arrives later
  as a status webhook, and may be `failed`.
- One shared access token for all tenants in a multi-tenant app; each WABA
  needs its own credentials and rate-limit handling.
- Logging full message bodies and phone numbers; they are personal data
  under DPDP/GDPR (see `security`).

## Sources

- `research/2026-10-23-product-platform-baseline.md` → WhatsApp section.
