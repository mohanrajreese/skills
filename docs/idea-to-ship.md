# Idea to shipped feature

How the product and delivery skills chain together. Each step's output is
the next step's input; skip steps only when the answer is already known.

```
brainstorm ──► feature-feasibility ──► tech-stack-chooser ──► spec-driven-development ──► skill-retro
 (options)      (go / spike / no-go)    (ADR)                  (spec → plan → tasks →        (learnings back
                  │        │                │                    implement → verify)          into skills)
                  │        └► ai-feasibility │                        │
                  └► pricing ◄── cloud-cost-planning ◄────────────────┤
                                                                       └► stack + integration skills
```

| Step | Skill | Output |
|---|---|---|
| Explore options | `brainstorm` | Shortlist with riskiest assumption and cheapest test |
| Check it's worth building | `feature-feasibility` (+ `ai-feasibility` for AI parts) | Verdict: go / spike / no-go |
| Decide the technology | `tech-stack-chooser` | ADR in `docs/adr/` |
| Design the system | `system-design` (+ `algorithms-complexity`, `data-structures` for hot paths) | Design doc with estimates and trade-offs |
| Know what it costs to run | `cloud-cost-planning` | Three-scenario cost model, unit costs |
| Know what to charge | `pricing` → `subscription-billing` | Pricing proposal → billing implementation |
| Build it | `spec-driven-development` | `specs/NNN-feature/{spec,plan,tasks}.md`, code, tests |
| Build it well | `design-principles` (plan), `coding-standards` (write), `code-quality` (review) | Simple design, consistent code, a merge-ready diff |
| Platform foundations | `saas`, `sso`, `security`, `data-security`, `india-it-compliance` | Tenancy, auth, security and India compliance baseline |
| Launch and grow | `marketing`, `meta-marketing` | Campaigns with tracking and compliant messaging |
| Integrations | `razorpay`, `whatsapp-integration`, `shopify`, `figma` | Working, verified integrations |
| AI features | `ai-agents`, `agentic-coding`, `subagent-suggester` | Agents/features with guardrails; agent-ready repo |
| Learn | `skill-retro` → `skill-gardener` | Better skills next time |
