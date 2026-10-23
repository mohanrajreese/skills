---
name: pricing
description: How we design and change pricing for our SaaS and apps, covering the value metric, tiers and packaging, free plan versus trial, usage-based and credit pricing for AI features, India-first and global price localization including GST display, annual discounts, unit economics checks, price change rollout and the pricing page. Use whenever someone asks what to charge, how to structure plans or tiers, how to price an AI feature, whether to offer a free plan, how to raise prices or grandfather customers, or needs a pricing page or pricing proposal. For implementing billing use the subscription-billing skill.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [business, pricing, saas]
---

# Pricing

Price on the value the customer gets, check it against what it costs us to
serve, and keep it simple enough to fit on one screen.

## Inputs to gather first

- Who buys (individual, SMB, enterprise), who uses, and who pays.
- The customer's alternative and what it costs them (manual work, a
  competitor, an agency).
- **Cost to serve** per customer per month: infra, LLM tokens, WhatsApp
  messages, payment fees, support (`cloud-cost-planning` gives the numbers).
- Market: India-only, global, or both.

## Steps

1. **Pick the value metric**: the unit that grows with value delivered
   (seats, orders processed, messages sent, active locations, AI credits).
   Good metrics are easy to understand, easy to predict, and grow with the
   customer's success.
2. **Package 3 tiers** (good / better / best) by *who* the customer is, not
   by random feature splits. Put the features each segment must have in
   that segment's tier; use limits on the value metric to separate tiers.
   Add "Enterprise: contact us" when SSO, SLAs, audit logs or invoicing
   terms come into play.
3. **Free plan or trial?** Free plan when usage spreads the product (viral
   or collaborative) and serving cost is near zero; time-boxed trial when
   value shows up quickly; reverse trial (full features, then downgrade) is
   often best for B2B SaaS.
4. **AI features:** never unlimited. Bundle a monthly allowance of credits
   per tier, sell top-ups, and set hard caps. Price so the median user's
   token cost stays a small fraction of their plan price, and re-check
   when model prices change.
5. **Localize:** INR pricing for India (`₹999/mo` style, with clear GST
   treatment: B2C prices usually shown inclusive, B2B exclusive + 18% GST with
   GSTIN invoices), USD for global. Price levels can differ by market;
   features shouldn't.
6. **Annual plans:** about two months free (~15–20% off), billed upfront.
7. **Sanity-check unit economics:** gross margin per tier (target ≥ 70–80%
   for plain SaaS; AI-heavy products are lower and need a plan to raise it),
   CAC payback, and the worst-case heavy user.
8. **Write the proposal** (format below) and decide how to test it: new
   signups only, A/B on the pricing page, or sales conversations.

## Proposal format

```markdown
# Pricing proposal: <product> (<date>)
Segments and value metric:
| Tier | Price (INR / USD, monthly · annual) | Limits | Key features | Target customer |
Free plan / trial decision and why:
AI usage policy (allowance, top-ups, caps):
Unit economics per tier (revenue, cost to serve, gross margin):
Risks and what we'll measure (conversion, ARPA, churn, expansion):
Rollout: who sees it, when, grandfathering:
```

## Changing prices

- Grandfather existing customers for a stated period, or give clear notice
  (30–60 days) with the reason. Never surprise-charge.
- Recurring mandates in India have a per-debit limit without
  re-authentication (₹15,000; see `razorpay`); a price increase can push
  customers over it.
- Store prices as versioned, immutable price records so old subscriptions
  keep their price (see `subscription-billing`).

## Pitfalls

- Too many tiers or add-ons; buyers stall.
- Pricing on cost-plus alone, which leaves value on the table, or on value
  alone, which ignores heavy-usage loss-makers.
- Seat pricing for a product where one admin does all the work.
- A free plan with real per-user cost (LLM, WhatsApp) and no cap.

## Sources

- General pricing practice; India GST and mandate notes from
  `research/2026-10-23-product-platform-baseline.md`.
