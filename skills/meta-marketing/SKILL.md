---
name: meta-marketing
description: How we build on Meta's marketing platform (Facebook, Instagram, WhatsApp ads), covering Business portfolio and ad account setup, Meta Pixel plus Conversions API with event deduplication and match quality, product catalogs (including Shopify's Facebook and Instagram app), Advantage+ campaigns after the legacy API retirement, Marketing API versioning, Click-to-WhatsApp and Lead Ads integrations, Instagram APIs, app events, measurement and ad policies. Use whenever setting up or debugging Meta Pixel, Conversions API, catalogs, ad campaign automation, lead ads webhooks, Instagram publishing, Click-to-WhatsApp ads, or when ROAS or event tracking from Meta looks wrong.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [marketing, meta, ads, integration]
---

# Meta marketing (Facebook, Instagram, WhatsApp ads)

Meta's ad delivery is only as good as the conversion data it receives.
Most of our engineering work here is **getting accurate, deduplicated,
consented events and catalog data to Meta**, and keeping API integrations
on supported versions.

## Before you start

1. Who owns the assets: a **Business portfolio** owned by the client, with
   our access granted as a partner. Never run client ads from personal
   accounts.
2. Platform: **Shopify store** → use Meta's official *Facebook & Instagram*
   sales channel app (Pixel, Conversions API and catalog sync built in), not
   custom code. **Custom web/app** → Pixel + Conversions API from our
   backend.
3. Verify the domain in Business settings; decide which events matter
   (usually `Purchase`, `Lead`, `CompleteRegistration`, `AddToCart`,
   `InitiateCheckout`).

## Pixel + Conversions API (CAPI)

- Send each key event from **both** browser (Pixel) and server (CAPI) with
  the **same `event_id`** and `event_name`, so Meta deduplicates them.
- Server events include `event_time`, `action_source` (`website`/`app`/
  `chat`/…), `event_source_url`, and customer parameters **normalized and
  SHA-256 hashed** (email lowercased/trimmed; phone with country code, digits
  only; `external_id`), plus the `_fbp` / `_fbc` cookie values and client IP
  and user agent when available.
- Check **Event Match Quality** and use **Test Events** (`test_event_code`)
  before going live. Watch for duplicate `Purchase` events: the classic
  ROAS-inflating bug.
- **Consent first:** load the Pixel and send CAPI events only after the user
  agrees to marketing tracking; never send health, financial or other
  sensitive attributes (`data-security`).
- Send server events from a queue with retries; Meta accepts events up to 7
  days old.

## Catalogs

- Feed fields: `id` (stable, matches Pixel `content_ids`), `title`,
  `description`, `availability`, `condition`, `price` (with currency),
  `link`, `image_link`, `brand`. Keep IDs identical across feed, Pixel and
  CAPI, or dynamic ads break.
- Shopify: catalog syncs through the sales channel. Custom: scheduled feed
  file or Catalog Batch API.

## Campaigns and the Marketing API

- **Pin the API version** in config and upgrade on Meta's schedule.
  Marketing API **v26** is current (2026-07). Some restrictions apply to
  **all versions from 2026-10-27** (poll ads, Messenger Stories placement).
- **Legacy Advantage+ shopping/app campaign APIs (ASC/AAC) are retired**:
  creation/updates were blocked for all versions by 2026-05-19, and
  remaining legacy campaigns were scheduled to pause. Advantage+ now comes
  from three levers on normal campaigns: Advantage+ campaign budget,
  audience and placements. Update any automation that still uses the old
  endpoints.
- SDKs: Python `facebook-business` tracks the API (26.x); the Node SDK lags
  (24.x). For Node, consider direct Graph API calls with a pinned version.
- Use a **system user token** for server integrations, stored in a secret
  manager.

## Lead Ads, Click-to-WhatsApp, Instagram

- **Lead Ads:** subscribe to the `leadgen` webhook, fetch the lead by ID
  immediately, push to CRM/WhatsApp within minutes (speed-to-lead wins), and
  store the consent text shown on the form.
- **Click-to-WhatsApp ads:** route into the WhatsApp Business inbox or bot
  (`whatsapp-integration`); conversations from these ads may get a free
  messaging window. Check current pricing rules.
- **Instagram:** content publishing and comment moderation through the
  Instagram API for professional (business/creator) accounts; DMs through the
  messaging APIs.
- **App events:** Meta SDK for the app (Flutter plugins exist) plus
  server-side app events; respect iOS App Tracking Transparency.

## Measurement and policy

- Don't trust platform ROAS alone: compare with your own orders by UTM
  (`marketing`), and use Meta's lift tests for big budgets.
- Ad policies: no personal-attribute targeting language ("Are you
  diabetic?"), restricted categories (credit, employment, housing, social
  issues/politics need special handling and authorizations), and claims must
  be substantiated (ASCI in India).

## Sources

- `research/2026-10-23-marketing-india-compliance.md` → Meta section (Meta
  developer blog posts via search, registries; CAPI details from prior
  knowledge).
