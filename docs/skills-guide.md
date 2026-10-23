# Skills guide

What each skill in this library does, when it kicks in, and what you get.
For the one-line generated list see [`SKILLS.md`](../SKILLS.md); for how
the planning skills chain together see [`idea-to-ship.md`](idea-to-ship.md).

**How skills load:** Claude reads every skill's short description each
session and loads the full skill when your request matches it. You don't
have to name a skill, but you can ("use the razorpay skill") to force it.
Every skill starts as `seed` and moves to `draft` once it has been used on
real work (see [`skill-lifecycle.md`](skill-lifecycle.md)).

`scripts/skills.py validate` fails if a skill is missing from this guide, so
add an entry whenever you add a skill.

---

## 1. The self-improving loop (meta)

### `skill-forge`
Creates a new skill from an idea or a workflow you just did, using the
repo template, and checks it doesn't duplicate an existing one.
**Kicks in:** "make this a skill", "we keep doing this".
**You get:** `skills/<name>/` with SKILL.md, LEARNINGS.md, validated and indexed.

### `skill-retro`
The **learn** step. After real work it records what worked, what was wrong
and what was missing, in the relevant skill's `LEARNINGS.md`, or adds new
ideas to `BACKLOG.md`.
**Kicks in:** end of a task, after a correction, "retro", "remember this".
**You get:** dated, standalone learning entries; clear-cut fixes applied immediately.

### `skill-research`
The **research** step. Checks a topic against primary sources (docs,
changelogs, registries, source code) and writes a dated research note with
every claim sourced.
**Kicks in:** a skill is stale or wrong, a new technology is adopted, "research X".
**You get:** `research/YYYY-MM-DD-topic.md` plus updated skill guidance.

### `skill-gardener`
The **grow** step. A periodic maintenance pass that promotes repeated
learnings into skill bodies, re-rates status, merges overlaps, deprecates
stale skills and grooms the backlog.
**Kicks in:** "review our skills", weekly or before a release.
**You get:** a healthier, smaller, current library and a summary of changes.

### `project-onboarding`
Gets oriented in an unfamiliar repo: finds the real commands, proves they
run, maps the architecture, loads the matching stack skills, and writes a
`CLAUDE.md`.
**Kicks in:** first session in a repo, "how does this project work".
**You get:** a working dev loop and a `CLAUDE.md` for future sessions.

### `skill-evals`
Tests skills the way `claude plugin eval` runs them: should-fire and
should-not-fire prompts, outcome graders, and a with-vs-without-skill
comparison that shows whether a skill actually helps. Example suite in
`evals/`.
**Kicks in:** "test this skill", a skill misfires or never loads, evidence for promotion.
**You get:** eval cases in `evals/<skill>-<case>/` and fixes to descriptions or bodies.

### `skill-router`
Picks the few skills a big task needs and the order to use them (decide →
plan → build → secure → check → learn), and logs gaps to the backlog.
**Kicks in:** start of large or cross-cutting work, "which skills should I use".
**You get:** a short routing plan instead of loading everything.

### `domain-learning`
Learns a new business domain fast: glossary, entities, workflows,
regulators, India rails (UPI, ONDC, Account Aggregator, GST e-invoicing),
competitors, expert questions, and turns it into a domain brief and seed
skills.
**Kicks in:** a project in an unfamiliar industry, "understand this domain".
**You get:** `docs/domains/<name>.md`, a research note, and new skills when the domain recurs.

---

## 2. Stack skills (one per technology)

Each one checks the project's actual versions first (the project's own
conventions win), then gives defaults for new work, a verify loop of real
commands, the rules that matter, and a dated **Changed recently** section.

### `python`
uv, Ruff, mypy/pyright, pytest; timezone-aware datetimes, validation at
boundaries. Flags Ruff 0.16's jump to 413 default rules and Python 3.15's
release.

### `django`
Safe migrations, query discipline (`select_related`, 6.1 fetch modes),
transactions with `on_commit`, `check --deploy`. Covers 6.0's Tasks
framework (no worker included), CSP, template partials and 6.1's `MAILERS`.

### `typescript`
Strict tsconfig, zod at boundaries, ESLint/Biome, Vitest/Playwright, Node
LTS. Explains the TypeScript 7 native compiler (no stable API yet) and 6.0's
default changes such as `types: []`.

### `nextjs`
App Router, Server Components and Actions (treated as public endpoints),
explicit caching. Lists Next.js 16 breaking changes: `proxy.ts`, async
request APIs, Turbopack by default, `next lint` removed.

### `tailwind`
Tailwind v4 CSS-first config (`@theme`, `@source`), tokens over arbitrary
values, no dynamic class names, the v3→v4 renames that change visuals.

### `golang`
Errors wrapped with context, `context.Context` everywhere, goroutine
ownership, table tests with `-race`, golangci-lint v2, recent Go releases.

### `postgres`
Schema defaults (`uuidv7`, `timestamptz`, FK indexes), a table of
zero-downtime migration patterns, EXPLAIN workflow, pooling caveats. Flags
PG 14 end-of-life in November 2026.

### `shopify`
Apps (React Router template, GraphQL Admin, toml webhooks, Polaris web
components), Functions and themes, quarterly API versions. Flags Scripts
shutdown (2026-06-30) and the deprecated Remix template.

### `supabase`
Grants + RLS as the authorization layer, `(select auth.uid())` and indexes,
migrations and declarative schemas, generated types, SSR auth. Flags the new
publishable/secret keys replacing `anon`/`service_role`.

### `firebase`
Security rules as the backend, rules tests in the emulator, Firestore
modelling for queries and cost, 2nd-gen Functions, App Check. Flags the
Dynamic Links shutdown and the Extensions sunset (2027-03-31).

### `aws`
Confirm the account first, SSO and OIDC (no long-lived keys), CDK/Terraform
with `diff` before `deploy`, least-privilege IAM, S3 lockdown, log retention,
budgets, current Lambda runtimes.

### `gcp`
gcloud + ADC, Workload Identity Federation for CI, Cloud Run with dedicated
service accounts, Artifact Registry (Container Registry is gone), Secret
Manager, Cloud SQL.

### `flutter`
Feature-first layering, one state approach (Riverpod 3 / Bloc 9), go_router,
codegen, `context.mounted` after `await`, no secrets in the app, release
checks.

---

## 3. Plan: from idea to decision

### `brainstorm`
Structured ideation: frame the "how might we" question, diverge through
several lenses (jobs-to-be-done, India-first, AI-native, distribution,
competitor gaps), then converge with ICE scoring.
**You get:** a shortlist, each with its riskiest assumption and cheapest test.
**Try:** "Brainstorm ways to increase repeat orders for our Shopify clients."

### `feature-feasibility`
Checks whether a feature is worth building: problem fit, stack fit, API
limits, unknowns turned into spikes, effort ranges, running cost, compliance
red flags.
**You get:** a report ending in **GO / SPIKE FIRST / NO-GO**.
**Try:** "Is it feasible to add WhatsApp order tracking to our app?"

### `ai-feasibility`
The AI-specific version: does an LLM fit the task, what accuracy is needed,
what data goes in, does it fit our stack (e.g. Flutter has no official
Claude SDK, so calls go through the backend) and policies (WhatsApp AI
rules), with a worked cost-per-request formula.
**You get:** an AI scorecard with an eval plan and a verdict.
**Try:** "Can we use AI to read customer WhatsApp messages and create orders?"

### `tech-stack-chooser`
Picks technology from our standard stack using requirements and weighted
criteria (Supabase vs Firebase, Django vs Go, AWS vs GCP, Shopify vs
custom), and refuses new tech without a reason.
**You get:** an ADR (architecture decision record) in `docs/adr/`.
**Try:** "What stack should we use for a B2B inventory SaaS with a mobile app?"

### `cloud-cost-planning`
Estimates running cost from an explicit workload model, priced from live
sources with dates, in launch / 10× / 100× scenarios, including LLM,
WhatsApp and payment fees.
**You get:** a cost model, unit cost per customer, and guardrails (budgets,
caps, alerts).
**Try:** "Estimate monthly cost for 500 shops using our app on GCP + Supabase."

---

## 4. Build

### `spec-driven-development`
Our SDD workflow: constitution → **spec** (what/why, acceptance criteria) →
clarify → **plan** (how) → **tasks** → implement task by task → verify →
retro, loading the right skills at each phase. Includes templates and maps to
GitHub Spec Kit and Kiro.
**You get:** `specs/NNN-feature/{spec,plan,tasks}.md` and a feature built against them.
**Try:** "Write a spec for COD-to-prepaid conversion via WhatsApp."

### `saas`
Blueprint for multi-tenant SaaS: tenancy model, org/membership/roles,
what's needed on day one vs later, noisy-neighbour limits, launch checklist.
**You get:** an architecture that won't need a painful retrofit.
**Try:** "Plan the foundations for a new multi-tenant SaaS."

### `figma`
Design → code through the Figma MCP server: screenshot as visual target,
reuse our components and tokens, Code Connect, visual verification, and a
handoff checklist (states, breakpoints, accessibility).
**You get:** UI that matches the design and uses our design system.
**Try:** "Implement this Figma frame in our Next.js app: <figma link>"

---

## 5. Engineering quality

### `design-principles`
KISS, YAGNI, DRY with the rule of three, SOLID (pragmatically), separation
of concerns, and **overengineering prevention**: a four-question test before
adding any abstraction, a red-flag list, how to rein in AI agents, and the
list of things you should *not* skip (validation, tenant IDs, idempotency).
**You get:** simpler designs and concrete "make it smaller" review suggestions.
**Try:** "Is this design overengineered?" / "Review this plan for YAGNI."

### `coding-standards`
How we write code in every language: precedence (project first), naming
with units, small functions with guard clauses, errors with context, types at
boundaries, money and time rules, comments that explain *why*, test naming,
Conventional Commits and small PRs.
**You get:** consistent code and commit/PR conventions across all projects.
**Try:** "Set up our coding standards in this new repo."

### `code-quality`
Quality gates per stack (format, lint, types, tests, complexity, diff
coverage, scans), a prioritised review checklist, code smells, extra checks
for AI-written code, refactoring and tech-debt practice.
**You get:** CI that blocks bad merges and review reports with
blocker/major/minor/nit severities.
**Try:** "Review this PR" / "Add quality gates to this repo's CI."

### `security`
OWASP Top 10:2025 and OWASP GenAI LLM Top 10 2026 checklists mapped to our
stack, a 10-minute threat model, baseline controls (secrets, dependencies,
SAST, headers, audit logs), India DPDP/GDPR duties, incident basics.
**You get:** a security review with the risks that matter for this change.
**Try:** "Security review this webhook handler."

### `data-security`
Protects the data itself across its lifecycle: classify it, avoid holding
cards or Aadhaar, encrypt (TLS, KMS, field-level), hash passwords properly,
remove standing production access, mask data for dev, redact logs, enforce
retention and deletion, keep India residency, and respond to leaks.
**You get:** a data map and controls proportional to how sensitive each field is.
**Try:** "We're adding PAN and bank details to onboarding. How do we store them?"

### `india-it-compliance`
Indian tech law as engineering controls: IT Act sections (43A, 66C, 66D,
72A, 79, 85) with the prevention for each, SPDI → DPDP (May 2027), CERT-In's
6-hour reporting and 180-day logs in India, intermediary duties including
the 2026 rules (3-hour takedowns, AI-content labelling), RBI payment rules,
e-commerce rules and banned dark patterns. Not legal advice.
**You get:** a per-release prevention checklist and incident timelines.
**Try:** "Our app lets users post photos and generate AI images. What do we need for India?"

---

## 6. Integrations

### `razorpay`
Server-created orders, server-side signature verification, webhooks as the
source of truth, subscriptions and mandates with RBI limits (₹15,000 per
debit without extra authentication), refunds, Route, reconciliation.
**Try:** "Add Razorpay checkout and webhooks to our Django app."

### `whatsapp-integration`
Cloud API vs BSPs, opt-in, the 24-hour window, templates, signed webhooks
with dedupe, BSUIDs instead of phone numbers, Meta's AI chatbot policy, and
a pointer to live pricing.
**Try:** "Send order updates on WhatsApp and handle replies."

### `sso`
OIDC with PKCE, SAML, SCIM, social login, org-level SSO with domain
verification, role mapping, break-glass admin, and buy vs self-host vs
platform choices.
**Try:** "An enterprise customer wants Okta SSO. How do we add it?"

---

## 7. Money

### `pricing`
What to charge: value metric, three tiers, free plan vs trial, AI credits
with caps, INR/USD and GST display, annual discounts, unit-economics checks,
price-change rollout.
**You get:** a pricing proposal with margins per tier.
**Try:** "Propose pricing for our WhatsApp automation SaaS."

### `subscription-billing`
How billing works in code: provider choice (Razorpay, Stripe, merchant of
record, app stores, Shopify Billing), data model, state machine,
entitlements, webhook inbox, dunning, reconciliation.
**You get:** billing that survives lost and out-of-order webhooks.
**Try:** "Implement monthly and annual plans with a 14-day trial."

---

## 8. AI

### `ai-agents`
Designing AI features: single call vs workflow vs agent, the four ways to
build agents (manual loop, Tool Runner, Managed Agents, Agent SDK), current
model IDs, tools and MCP, guardrails, evals, cost and observability. Hands
SDK details to the `claude-api` skill.
**Try:** "Build a support agent that answers order questions from our DB."

### `agentic-coding`
Working well with coding agents: CLAUDE.md, installing this library,
permissions and hooks, plan-first, verify-before-done, reviewing AI diffs,
parallel worktrees, headless runs in CI.
**Try:** "Set up this repo so Claude Code works well in it."

### `subagent-suggester`
Looks at a repo and its recurring work, then proposes a few subagents worth
having (reviewer, test runner, migration reviewer, …) and writes their
`.claude/agents/*.md` files with minimal tools and the right model.
**Try:** "Which subagents should we create for this project?"

---

## 9. Fundamentals: algorithms, data structures, system design

### `algorithms-complexity`
Time and space complexity (Big-O, amortized, recursion depth), what input
sizes each complexity can handle, hidden quadratic and N+1 traps, ReDoS, a
catalogue of algorithm patterns by problem shape, streaming for memory, and
profiling before optimising. Includes a per-language cheat sheet of built-in
operation costs.
**You get:** a faster, lighter fix backed by a measurement.
**Try:** "This CSV export of 50k orders takes 40 seconds. Why, and how do we fix it?"

### `data-structures`
Choosing structures by the operations you need: arrays, maps, sets, deques,
heaps, sorted maps, tries, graphs, ring buffers, LRU, bloom filters; each
language's built-ins; Postgres index types (B-tree, GIN, GiST, BRIN,
partial, covering); Redis types (sorted sets, streams, HyperLogLog).
**You get:** the right structure or index for the access pattern.
**Try:** "What's the best way to store a live leaderboard for 100k players?"

### `system-design`
Requirements with numbers, back-of-envelope estimates, API and data model,
scaling options cheapest first, queues, idempotency and the outbox pattern,
retries with backoff and jitter, circuit breakers, rate limits, SLOs, and
building blocks mapped to AWS, GCP, Supabase and Firebase. Ends in a design
doc (interview mode too).
**You get:** a design doc with explicit trade-offs and a path to 10×.
**Try:** "Design order notifications for 2,000 Shopify stores during a sale."

---

## 10. Marketing

### `marketing`
Positioning, ICP, picking 1–2 channels (WhatsApp, Meta, Google, SEO, Shopify
App Store, partnerships), funnel metrics and CAC/LTV, tracking plans and UTM
conventions, landing pages, experiments, and India marketing compliance
(TRAI DLT and 140/1600 series, WhatsApp opt-in, DPDP consent, email sender
rules, ASCI, dark patterns).
**You get:** a campaign brief with measurement and a compliance check.
**Try:** "Plan the launch campaign for our clinic billing app in Tamil Nadu."

### `meta-marketing`
Facebook, Instagram and WhatsApp ads engineering: business portfolio
setup, Pixel + Conversions API with deduplication and hashed match keys,
catalogs (Shopify's Meta app or feeds), Advantage+ after the legacy API
retirement, pinned Marketing API versions (v26), Lead Ads and
Click-to-WhatsApp flows, Instagram APIs, measurement and ad policy.
**You get:** accurate, consented conversion data and integrations on supported APIs.
**Try:** "Our Meta ROAS looks doubled. Check our Pixel and CAPI setup."
