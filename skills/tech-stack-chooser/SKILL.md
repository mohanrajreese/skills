---
name: tech-stack-chooser
description: Choose the technology stack for a new product, service or feature from our standard stack (Next.js, TypeScript, Tailwind, Django, Python, Go, Flutter, Postgres, Supabase, Firebase, AWS, GCP, Shopify) plus integrations (Razorpay, WhatsApp, SSO, AI), using explicit requirements, weighted criteria and an architecture decision record. Use whenever starting a new project, asking "what should we build this with", choosing between Supabase and Firebase, Django and Go, AWS and GCP, web and mobile, Shopify versus a custom store, or before adding any technology outside our stack.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [architecture, planning, decision]
---

# Tech stack chooser

Default to the stack we already know. A new technology must beat the
default on a requirement that matters, not on novelty. Every choice ends in
an ADR (architecture decision record) so the next person knows why.

## Steps

1. **Capture requirements** (ask if missing): users and platforms (web,
   iOS/Android, WhatsApp, Shopify admin/storefront), scale and latency,
   realtime/offline needs, data shape (relational, documents, files),
   compliance and data residency (India DPDP, enterprise SSO), team skills,
   time to market, budget, expected lifetime.
2. **Start from the defaults below**; for each layer, change the default
   only if a requirement forces it.
3. **For real choices, score the options** on weighted criteria (fit to
   requirements, team familiarity, time to market, cost at 10×, operational
   load, lock-in, hiring) and note the deciding factor.
4. **Check feasibility edges:** run `ai-feasibility` for AI parts,
   `cloud-cost-planning` for cost at scale, and the stack skills' "Changed
   recently" sections for version or policy constraints.
5. **Write the ADR** (format below) into the project's `docs/adr/`.

## Defaults by layer

| Layer | Default | Switch when |
|---|---|---|
| Web app | Next.js + TypeScript + Tailwind | Mostly static content → simpler static site; heavy admin/CRUD with server-rendered forms → Django templates may be faster |
| Backend API | Django (+ DRF/ninja) for data-heavy business apps with admin | Go for high-throughput services, workers, CLIs, low-latency or concurrency-heavy work |
| Mobile | Flutter | A web app/PWA is enough; deep native-only features |
| Database | Postgres | (rarely) document-only, offline-first mobile → Firestore |
| BaaS | **Supabase** for Postgres/SQL/RLS-centric apps and B2B SaaS | **Firebase** for realtime/offline-first mobile, Google ecosystem, FCM-heavy apps |
| Cloud | GCP (Cloud Run) for simple container apps | AWS when the customer/credits/required services are on AWS, or for breadth (queues, analytics, enterprise) |
| Commerce | Shopify (+ app/theme) for stores | Custom checkout only for flows Shopify can't support |
| Payments | Razorpay (India) | Global customers → Stripe or a merchant of record (`subscription-billing`) |
| Messaging | WhatsApp Cloud API / BSP + email | |
| Auth | Platform auth (Supabase/Firebase) or managed provider | Enterprise SSO/SCIM needs (`sso`) |
| AI | Claude via our backend (`ai-agents`) | Customer requires a specific cloud → Claude on Bedrock/Vertex |

## ADR format

```markdown
# ADR-NNN: <decision> (<date>)
Status: proposed | accepted | superseded by ADR-MMM
Context: <requirements and constraints that matter>
Options considered: <A, B, C>
| Criterion (weight) | A | B | C |
Decision: <choice> because <deciding factor>
Consequences: <what gets easier, harder; what we must now do>
Revisit when: <trigger, e.g. >50k MAU, enterprise customer needs data residency>
```

## Pitfalls

- Microservices on day one; start with a modular monolith.
- Two BaaS platforms (Supabase *and* Firebase) in one product without a hard
  reason.
- Choosing for a hypothetical scale 100× beyond the business plan.
- Adding a technology outside this list with no ADR. If it becomes common,
  add a stack skill for it (`skill-forge`).
