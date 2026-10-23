---
name: brainstorm
description: Structured brainstorming for product ideas, features, technical approaches, growth experiments and names, using a short framing step, wide divergence through several lenses (jobs-to-be-done, constraints, India-market, AI-native, distribution, competitor gaps), then convergence with clustering and ICE scoring down to the riskiest assumption and the cheapest test. Use whenever someone says brainstorm, ideate, "give me ideas", "what could we build", "how might we", "ways to solve X", explores a new product or feature, or is stuck choosing an approach.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [product, ideation, planning]
---

# Brainstorm

Good brainstorming has two separate modes: **diverge** (many options, no
judging) and **converge** (pick, with reasons). Mixing them kills ideas
early or never decides anything.

## 1. Frame (ask at most 3 questions, then go)

- **Goal:** what outcome, for whom? ("Increase repeat orders for our
  Shopify D2C clients.")
- **Constraints:** time, budget, team, stack, compliance, market.
- **Mode:** product idea, feature, technical approach, growth experiment,
  or naming.

Write a one-line "How might we …?" question and confirm it.

## 2. Diverge (aim for 15–25 options)

Run several lenses and label each idea with its lens:

- **Jobs-to-be-done:** what job is the user hiring this for; what do they
  use today?
- **Constraint flip:** what if it had to be free, or built in a week, or
  work offline, or on WhatsApp only?
- **India-first:** UPI, WhatsApp, vernacular languages, low-end Android,
  COD and trust, tier-2/3 cities.
- **AI-native:** what becomes possible if a model does the tedious part
  (extract, draft, classify, converse)?
- **Distribution:** Shopify App Store, WhatsApp, partnerships, SEO,
  marketplaces. Ideas that come with distribution win.
- **Competitor gap:** what do incumbents do badly or ignore?
- **Subtract:** what could we remove or automate away entirely?
- For technical approaches: build vs buy vs integrate, sync vs async,
  rules vs ML, managed vs self-hosted.

Include a few deliberately bold or odd ideas; they often contain the
useful twist.

## 3. Converge

1. **Cluster** similar ideas; merge duplicates.
2. **Score** the clusters with ICE (Impact, Confidence, Ease; 1–10 each) or
   RICE when reach varies a lot. Say what each score assumes.
3. **Pick the top 1–3** and, for each, name the **riskiest assumption** and
   the **cheapest test** (landing page, concierge/manual version, WhatsApp
   prototype, 1-day spike, 5 customer calls).

## Output format

```markdown
# Brainstorm: <how might we …> (<date>)
Constraints: …
## Ideas (by lens)
- [JTBD] …   - [India-first] …   - [AI-native] …
## Shortlist
| Idea | Impact | Confidence | Ease | ICE | Riskiest assumption | Cheapest test |
## Recommendation
<top pick and why> → next: feature-feasibility
```

## Hand-offs

`feature-feasibility` for the shortlist → `ai-feasibility` for AI ideas →
`pricing` if it's monetised → `spec-driven-development` to build.
