---
name: cloud-cost-planning
description: How we estimate, budget and control the running cost of our products across AWS, GCP, Firebase, Supabase, Vercel and third-party usage fees (LLM tokens, WhatsApp messages, payment gateway fees, email and SMS), producing a three-scenario cost model, unit cost per customer, guardrails, and a monthly review against actuals. Use whenever someone asks how much something will cost to run, compares cloud or BaaS options on cost, prices a plan and needs cost to serve, sees a cloud bill spike, sets budgets and alerts, or plans for scale.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [cloud, cost, finops, planning]
---

# Cloud cost planning

Cost estimates go wrong in two ways: prices quoted from memory (they
change), and usage assumptions nobody wrote down. This skill fixes both:
**every number has a date and source, every assumption is explicit.**

## Steps

1. **Model the workload** in plain numbers: monthly active users/orgs,
   requests per user per day, peak RPS, data stored (GB) and growth,
   egress (GB), background jobs, files/media, and per-user usage of paid
   APIs (LLM tokens in/out, WhatsApp messages by category, payments count
   and value, emails/SMS).
2. **Map to services** for the chosen stack (`tech-stack-chooser`): compute
   (Cloud Run / Lambda / ECS / Vercel), database (Cloud SQL / RDS / Supabase
   plan), storage + CDN, logs/monitoring, plus third-party APIs.
3. **Price each line from the live source**: official calculators (AWS
   Pricing Calculator, Google Cloud Pricing Calculator) and pricing pages
   (Supabase, Firebase, Vercel, Meta WhatsApp, Razorpay, LLM provider).
   Record the URL and date next to each price. Never reuse a price from an
   old estimate without re-checking it.
4. **Build three scenarios:** launch, 10×, 100×. Costs often jump at plan
   boundaries (BaaS tiers, DB instance sizes); show where.
5. **Compute unit costs:** cost per active org/user per month, and cost per
   key action (an AI request, a WhatsApp conversation, an order). Feed these
   into `pricing`; check gross margin per tier.
6. **Set guardrails before launch:** budgets with alerts at 50/80/100% on
   every cloud account; hard limits where available (Cloud Run max
   instances, Lambda reserved concurrency, Supabase spend cap, LLM per-org
   token caps, WhatsApp marketing send limits); log retention set.
7. **Review monthly** against actual bills; update the model and note the
   biggest variance.

## Output format

```markdown
# Cost model: <product> (prices checked <date>)
Assumptions: <users, usage per user, growth> (each with a source or "guess")
| Line item | Service | Unit price (source, date) | Launch | 10× | 100× |
| Total / month | | | | | |
Unit cost: per org ₹/$ …, per AI request …, per WhatsApp message …
Plan-boundary jumps: …
Guardrails: budgets, caps, alerts
Biggest risks and how we'd cut cost: …
```

## Common cost traps

- **Data egress and NAT Gateway** processing charges (AWS); cross-region
  traffic.
- **Logs** with no retention or with debug logging left on in prod.
- **Always-on minimums:** Cloud Run min instances, idle RDS/Cloud SQL,
  provisioned concurrency, oversized dev/staging databases.
- **Firestore reads** from listeners on large collections; N+1 reads.
- **LLM tokens:** long system prompts without caching, agent loops without
  limits, the most expensive model used for simple steps (see `ai-feasibility`).
- **Per-message/per-transaction fees:** WhatsApp marketing templates,
  payment gateway percentage fees, SMS OTPs. They scale linearly with
  success.
- Free tiers and startup credits ending; plan the month after.

## Sources

- Prices must come from official pricing pages at estimate time. See
  `research/` notes for the date conventions.
