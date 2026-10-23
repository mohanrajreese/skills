---
name: feature-feasibility
description: Check whether a proposed feature or product idea is feasible before committing to it, assessing problem fit, technical feasibility on our stack, dependencies and unknowns, effort range, cost to run, security and compliance (DPDP, RBI, Meta WhatsApp policy, App Store, Shopify rules), platform limits and risks, and ending in a go, spike or no-go verdict with next steps. Use whenever someone asks "is this feasible", "can we build X", "how hard would it be", "should we do this feature", wants an estimate or risk assessment for an idea, or before writing a spec for anything non-trivial.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [planning, feasibility, product]
---

# Feature feasibility

A feasibility check is cheap insurance: an hour of structured checking
before weeks of building. It must end in a **verdict** (go / spike / no-go),
not a list of considerations.

## Steps

1. **Restate the feature** in one paragraph: user, problem, proposed
   solution, success metric. If the problem itself is unclear, run
   `brainstorm` first.
2. **Problem fit:** evidence the problem is real (customer requests, data,
   support tickets) and how big it is. No evidence → cheapest test first.
3. **Technical feasibility on our stack:** which layers change; does the
   stack support it (check the stack skills' "Changed recently" sections
   for version or platform limits); external APIs needed (WhatsApp,
   Razorpay, Shopify, Figma, LLM) and their limits (rate limits, policies,
   approval processes like template review or app review).
4. **AI parts** → run `ai-feasibility` and paste its verdict.
5. **Unknowns:** list what we don't know that could change the answer. Each
   unknown becomes a time-boxed **spike** with a question it must answer.
6. **Effort range:** break into 5–10 chunks; estimate each as a range
   (optimistic / likely / pessimistic, in days); sum the ranges. Wide ranges
   mean unknowns still to resolve.
7. **Cost to run:** new per-unit and fixed costs (`cloud-cost-planning`).
   Does it fit the pricing (`pricing`)?
8. **Risk and compliance:** security (`security` threat-model), personal
   data (DPDP/GDPR), payments (RBI mandate rules), messaging (Meta policy,
   opt-in), app stores and Shopify app review, vendor lock-in, and
   reversibility.
9. **Verdict** and next step.

## Red flags (any one → spike or no-go until resolved)

- Depends on an API capability that's in beta, undocumented, or recently
  changed policy.
- Needs data we don't have or aren't allowed to use.
- Irreversible actions (money movement, deletions, mass messaging) without
  a review step.
- Cost per user is unbounded (LLM loops, marketing messages) with no cap.
- Effort's pessimistic estimate is more than 3× the optimistic one.

## Report format

```markdown
# Feasibility: <feature> (<date>)
Summary: <one paragraph>
| Dimension | Finding | Risk (L/M/H) |
| Problem fit | | |
| Technical (stack, APIs, limits) | | |
| AI (from ai-feasibility) | | |
| Effort (range, days) | | |
| Cost to run (per unit / month) | | |
| Security & compliance | | |
| Dependencies & lock-in | | |
Unknowns → spikes: <question, time box>
Verdict: GO / SPIKE FIRST / NO-GO (alternative: …)
Next: spec via spec-driven-development | spike plan | park in backlog
```
