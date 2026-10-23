---
name: razorpay
description: How we accept payments in India with Razorpay, covering Orders and Standard Checkout, server-side signature verification, webhooks, refunds, Subscriptions with UPI Autopay, card and eNACH mandates, RBI e-mandate rules, and Route for marketplaces, across Next.js, Django, Go and Flutter. Use whenever adding or debugging Razorpay checkout, verifying payments, handling Razorpay webhooks, building recurring billing or mandates in India, issuing refunds, reconciling settlements, or when you see razorpay SDK imports, rzp_test or rzp_live keys.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [integration, payments, india, razorpay]
---

# Razorpay

The browser can lie and the callback can be lost. **The server decides the
amount, the server verifies the signature, and webhooks are the source of
truth.**

## Before you start

1. Find the integration type: Standard Checkout (web), `razorpay_flutter`
   (mobile), Payment Links, Subscriptions, Route (split payouts). Each has
   different events.
2. Check which keys are configured: `rzp_test_...` vs `rzp_live_...`, plus a
   separate **webhook secret** (not the key secret). Keys live in a secret
   manager or env; the key secret never reaches the client.
3. Check the dashboard's auto-capture setting. Authorized-but-uncaptured
   payments are refunded automatically after the capture window.

## One-time payment flow

1. **Server creates an Order:** amount in **paise (integer)**, `currency`,
   your `receipt` (your internal order ID). Store it as `created`.
2. Client opens Checkout with `key_id` and `order_id` (never an amount it
   chose).
3. Client receives `razorpay_payment_id`, `razorpay_order_id`,
   `razorpay_signature` → sends them to your server.
4. **Server verifies** HMAC-SHA256(`order_id|payment_id`, key secret) with
   the SDK (`validatePaymentVerification` in Node,
   `client.utility.verify_payment_signature` in Python) and checks the
   order belongs to this user.
5. **Webhook** `payment.captured` / `order.paid` marks the order paid,
   idempotently. Steps 3–4 give fast UI feedback; the webhook covers lost
   callbacks and closed tabs.

## Webhooks

- Verify `X-Razorpay-Signature` = HMAC-SHA256(**raw request body**, webhook
  secret) (`Razorpay.validateWebhookSignature(body, signature, secret)`).
  Parsing JSON before verifying breaks the signature.
- Dedupe by event ID (sent as the `x-razorpay-event-id` header; confirm in
  the current webhook docs), falling back to entity ID + event type. Events
  retry and can arrive **out of order**. Apply state transitions only forward.
- Re-check `amount`, `currency` and `order_id` against your record before
  fulfilling.
- Return 2xx quickly; process asynchronously.

## Subscriptions and mandates

- Model: **Plan** (amount, period) → **Subscription** (plan, `total_count`,
  start) → customer authorises a mandate at Checkout using
  `subscription_id`. Verify with HMAC-SHA256(`payment_id|subscription_id`,
  key secret): Node `validatePaymentVerification({subscription_id,
  payment_id}, …)`, Python `client.utility.verify_subscription_payment_signature`.
- Drive state from webhooks: `subscription.authenticated`, `.activated`,
  `.charged`, `.pending`, `.halted`, `.paused`, `.resumed`, `.cancelled`,
  `.completed`. Map them to your entitlements (see `subscription-billing`).
- **RBI e-mandate rules (2026 framework):** recurring debits up to **₹15,000**
  per transaction run without extra authentication (₹1,00,000 for insurance,
  mutual funds and credit-card bills); above that the customer must
  authenticate each debit. Customers get a **pre-debit notification ≥ 24 h**
  before each charge and can cancel the mandate any time. Plans priced above
  the limit need a flow for per-debit authentication, or eNACH.
- Confirmation of recurring debits can lag by days; don't revoke access on
  the due date. Use a grace period.

## Defaults for new work

- One `payments` table keyed by your order ID with Razorpay IDs, amount,
  currency, status, and raw webhook events stored in an inbox table.
- Prices and plans defined server-side; GST handled explicitly (invoice
  shows GSTIN for B2B).
- Daily **reconciliation job**: compare your records with Razorpay
  payments/settlements and alert on mismatches.
- Refunds via API with your own reason codes; partial refunds supported.
- Marketplaces paying sellers: **Route** with linked accounts (KYC needed).
  Don't collect and pay out manually.

## Verify loop

- Test mode end to end: success, failure, user closes Checkout, and UPI
  pending-then-success (webhook arrives after the callback).
- Webhook tests with a tampered body (must reject), a duplicate event (must
  no-op) and out-of-order events.
- Confirm no secret is shipped in the web bundle or the Flutter app.

## Pitfalls

- Trusting the client-side `handler` alone, so payments get lost when the tab
  closes.
- Floating-point rupees; use integer paise everywhere.
- Using the key secret as the webhook secret, or one webhook secret across
  environments.
- Assuming international cards work; they need activation and have
  different rules.

## Sources

- `research/2026-10-23-product-platform-baseline.md` → Razorpay section
  (razorpay-node source, RBI framework reports).
