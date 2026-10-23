---
name: system-design
description: How we design systems and services, covering requirements and non-functional targets (latency, availability, consistency, compliance such as India data residency), back-of-the-envelope capacity estimates, API and data model design, scaling reads and writes (indexes, caching, CDN, replicas, queues, partitioning), async processing with idempotency and the outbox pattern, reliability (timeouts, retries with backoff and jitter, circuit breakers, rate limiting), observability and SLOs, and mapping building blocks onto AWS, GCP, Supabase and Firebase, ending in a design doc. Use whenever designing a new system or major feature, preparing for scale or a traffic spike, choosing sync versus async, adding a queue, cache or replica, reviewing an architecture, writing a design doc, or practicing system design interviews.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [architecture, system-design, scalability, reliability]
---

# System design

Design for the load you have plus a clear path to 10×, not for imagined
millions. The default architecture, a **modular monolith + Postgres +
object storage + CDN + a job queue**, carries most of our products a long
way. Every additional component must earn its operational cost
(`design-principles`).

## 1. Requirements

- **Functional:** the core user journeys and APIs (3–5, not everything).
- **Non-functional, with numbers:** p95 latency per journey, availability
  target (99.9% ≈ 43 min downtime/month), durability, consistency needs
  (money and inventory: strong; feeds and analytics: eventual), peak vs
  average traffic (Indian sale days, festivals, month-end), data growth.
- **Constraints:** India data residency (CERT-In logs, RBI payment data:
  `india-it-compliance`), budget (`cloud-cost-planning`), team size, deadlines.

## 2. Estimate (back of the envelope)

```text
requests/sec (avg) = daily active users × actions per user per day ÷ 86,400
peak RPS          ≈ avg × 3–10 (spiky consumer traffic: higher)
storage/year      = records/day × bytes/record × 365 (× replicas, + indexes ~30–50%)
bandwidth         = peak RPS × response size
```

Useful magnitudes: memory access ~100 ns; SSD read ~0.1 ms; same-region
network round trip ~0.5–1 ms; India ↔ US round trip ~200 ms+ (so put
servers near users: Mumbai/Delhi regions); a single well-indexed Postgres
handles thousands of simple queries/sec.

## 3. Interfaces and data

- **API:** resource-oriented REST (or GraphQL where clients need it),
  versioned when public, cursor pagination, **idempotency keys** on create
  and payment endpoints, consistent error shape.
- **Data model:** start relational (`postgres`); define ownership
  (`org_id`, `saas`), access patterns, indexes, and what's derived/cached.

## 4. High-level design, then deep dives

Draw the request path (client → CDN → API → DB/cache/queue → workers →
third parties) and then go deep only where requirements demand it:

| Pressure | Options, cheapest first |
|---|---|
| Slow reads | Fix queries/indexes → cache (CDN for public, Redis for hot keys, short TTLs) → read replicas → denormalized read models |
| Heavy writes | Batch writes → async via queue → partition/shard by tenant or time (last resort) |
| Slow or flaky work in the request (emails, WhatsApp, PDFs, AI calls, webhooks out) | **Queue + workers** with retries and a dead-letter queue |
| Realtime updates | Polling at first → SSE/WebSockets → Supabase Realtime / Firestore listeners / Pub/Sub fan-out |
| Search | Postgres full-text/trigram → dedicated search engine when relevance or scale needs it |
| Files and media | Object storage + signed URLs + CDN; process async |

## 5. Correctness in distributed flows

- **Idempotency everywhere** messages can repeat: webhooks (Razorpay,
  Shopify, WhatsApp), queue consumers, retries. Use unique keys plus an
  inbox/dedupe table.
- **Outbox pattern:** write the state change and an "event to publish" row
  in one DB transaction; a relay publishes it. This avoids "saved but never
  sent" and "sent but not saved".
- **No distributed transactions:** use sagas/compensations for multi-step
  flows (order → payment → inventory → notification).
- **Exactly-once is an illusion:** design for at-least-once + idempotent
  handlers.

## 6. Reliability

- **Timeouts** on every network call; **retries with exponential backoff
  and jitter**, capped, only for retryable errors; **circuit breakers**
  around flaky dependencies; **bulkheads** (separate pools/queues) so one
  slow integration can't starve everything.
- **Rate limiting** (token bucket) per user/tenant/IP, at the edge and on
  expensive endpoints; graceful degradation (serve cached or partial
  results).
- Health checks, zero-downtime deploys, backward-compatible migrations
  (`postgres`), feature flags for risky changes.

## 7. Observability

Structured logs with request and tenant IDs; metrics (RED: rate, errors,
duration for services; USE: utilisation, saturation, errors for resources);
distributed traces across queues; **SLOs** with alerts on burn rate, not on
every blip.

## 8. Building blocks on our stack

| Need | AWS | GCP | Supabase / Firebase |
|---|---|---|---|
| Compute | Lambda, ECS Fargate | Cloud Run (services/jobs/functions) | Edge Functions / Cloud Functions |
| Queue / events | SQS, SNS, EventBridge | Cloud Tasks, Pub/Sub | Supabase Queues (pgmq), `pg_cron` / Pub/Sub triggers |
| Cache | ElastiCache (Redis/Valkey) | Memorystore | — |
| Database | RDS / Aurora Postgres | Cloud SQL / AlloyDB | Supabase Postgres / Firestore |
| Files + CDN | S3 + CloudFront | Cloud Storage + Cloud CDN | Supabase Storage / Firebase Storage |
| Realtime | API Gateway WebSockets, AppSync | Pub/Sub + Cloud Run WebSockets | Supabase Realtime / Firestore listeners |

## Design doc format

```markdown
# Design: <system> (<date>, author)
Context & goals / non-goals
Requirements: functional; non-functional with numbers
Estimates: RPS (avg/peak), storage/year, bandwidth
API & data model
Architecture (diagram) and request flow
Deep dives: scaling, consistency, failure modes
Security, privacy, compliance (residency, logs)
Observability & SLOs
Cost estimate (cloud-cost-planning)
Alternatives considered & why not
Rollout & migration plan; open questions
```

Interview mode: same steps, time-boxed: requirements (5 min) → estimates →
API/data → high-level → 1–2 deep dives → bottlenecks and trade-offs.
