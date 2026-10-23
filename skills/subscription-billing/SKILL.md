---
name: subscription-billing
description: How we implement subscription billing in our apps, covering choosing a provider (Razorpay Subscriptions, Stripe Billing, a merchant of record such as Paddle, App Store and Play billing, Shopify Billing API), the data model, subscription state machine, entitlements, webhooks as the source of truth, upgrades and downgrades, trials, dunning and grace periods, invoices and GST, and reconciliation. Use whenever building or debugging plans, checkout for recurring payments, trials, plan changes, failed-payment handling, feature gating by plan, usage-based billing, or billing webhooks. For deciding prices use the pricing skill.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [payments, billing, saas]
---

# Subscription billing

Billing is a state machine fed by webhooks. The app never asks the payment
provider "is this user paid?" during a request; it reads its own
**entitlements**, which webhooks keep up to date.

## Choose the provider

| Situation | Default |
|---|---|
| Customers mainly in India, UPI/cards/netbanking | Razorpay Subscriptions (see `razorpay` for mandates and RBI limits) |
| Global B2B/B2C SaaS, you handle tax registration | Stripe Billing (check account availability for your entity) |
| Global sales, don't want to handle global sales tax/VAT | Merchant of record (Paddle, Lemon Squeezy and similar) |
| Digital features sold inside iOS/Android apps | App Store / Google Play billing, per current store rules |
| Shopify app | Shopify Billing API (required for App Store apps) |

Multiple providers is normal (web + mobile stores); entitlements unify them.

## Data model

```text
plans / prices      versioned, immutable (price change = new price row)
subscriptions       provider, provider_id, customer/org, price_id, status,
                    current_period_end, cancel_at_period_end, trial_end
entitlements        org_id, feature/limit, value, source_subscription_id
usage_records       org_id, metric, quantity, period (for metered/credit plans)
billing_events      raw provider webhooks (inbox): event_id UNIQUE, payload, processed_at
invoices/payments   provider references, amounts in minor units, tax, GSTIN
```

## State machine

`trialing → active → past_due → (grace) → canceled | expired`, plus
`pending` (awaiting mandate or first payment) and `paused`. Write down which
provider events move which transitions, and what access each status gets
(e.g. `past_due` keeps access for N days, then read-only, then locked).

## Rules that matter

- **Webhook inbox:** verify the signature, insert into `billing_events`
  (unique event ID makes it idempotent), return 2xx, process asynchronously.
  Handle out-of-order events by comparing timestamps or provider state.
- **Entitlements are derived**, not hand-edited: recompute from the
  subscription on every relevant event. Feature checks read entitlements.
- **Plan changes:** upgrades usually take effect now (prorated); downgrades
  at period end. Make the behaviour explicit in the UI.
- **Trials:** collect the payment method up front or not, deliberately;
  send a reminder before the trial converts.
- **Dunning:** provider retries + your emails/WhatsApp notices + a grace
  period. Lock access only after it ends; make "update payment method" one
  click.
- **Cancellation:** default to end of period; capture a reason; keep data
  for a stated retention window.
- **Money:** integer minor units; currency stored with every amount; tax
  shown per jurisdiction (India: GST invoice with GSTIN for B2B).
- **Reconcile daily** against the provider (subscriptions, payments) and
  alert on drift; webhooks get lost.

## Verify loop

- Test-mode scenarios: new subscription, trial → paid, upgrade, downgrade,
  failed renewal → recovery, failed renewal → cancellation, refund, and
  mandate cancelled by the customer from their bank or UPI app.
- Replay duplicate and out-of-order webhooks; entitlements must end the
  same.
- Time-travel renewals with the provider's test clock or simulation tools
  where available.

## Pitfalls

- Gating features on `status == "active"` and forgetting `trialing`,
  `past_due` grace, or canceled-at-period-end-but-still-paid.
- Editing a price in place, which silently changes what existing subscribers
  pay.
- Webhook handler doing slow work inline and timing out, then double
  processing on retry.

## Sources

- Provider docs at implementation time; India specifics in
  `research/2026-10-23-product-platform-baseline.md` → Razorpay.
