---
name: skill-router
description: Pick the right skills from this library for a task and the order to apply them, using the skills guide and index, so multi-step work such as "build a paid WhatsApp feature for our SaaS" loads planning, stack, integration, security and quality skills at the right moments without loading everything. Also spots gaps where no skill fits and sends them to the backlog. Use at the start of any large or cross-cutting task, when someone asks "which skills should I use", "what's the process for X", when a task spans several technologies or phases, or when planning work for subagents that need skill lists.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [meta, routing, workflow]
---

# Skill router

The library has many skills; each session should load the few that matter,
in the order they matter. This skill produces that short plan.

## Steps

1. **Read the map:** `docs/skills-guide.md` (what each skill does) and
   `docs/idea-to-ship.md` (how planning and delivery skills chain).
2. **Break the task into phases:** decide → plan → build → secure → check →
   launch → learn. Skip phases that don't apply.
3. **For each phase pick at most 1–3 skills**, by the most specific match:
   a stack skill beats a general one; an integration skill beats `saas`.
4. **Check the project:** load stack skills only for technologies the repo
   actually uses (`project-onboarding` if unknown).
5. **Note gaps:** a phase with no fitting skill → line in `BACKLOG.md`
   (`skill-retro` format) and continue without one.
6. **Output the routing plan** (format below) and load the first phase's
   skills.

## Output format

```markdown
Task: <one line>
1. Decide → `feature-feasibility` (+ `ai-feasibility` for the AI part)
2. Plan → `spec-driven-development`, `system-design`, `design-principles`
3. Build → `django`, `postgres`, `whatsapp-integration`, `razorpay`
4. Secure → `security`, `data-security`, `india-it-compliance`
5. Check → `code-quality`
6. Learn → `skill-retro`
Gaps: <none | "no skill for GST e-invoicing → BACKLOG">
```

## Common routes

| Task type | Route |
|---|---|
| New product | `brainstorm` → `feature-feasibility` → `tech-stack-chooser` → `saas` → `system-design` → `cloud-cost-planning` → `pricing` → `spec-driven-development` |
| New feature in an existing app | `feature-feasibility` → `spec-driven-development` → stack skills → `code-quality` |
| Payments | `razorpay` / `subscription-billing` → `security` → `data-security` → `india-it-compliance` |
| Messaging / marketing | `whatsapp-integration` / `meta-marketing` → `marketing` (compliance) → `data-security` |
| AI feature | `ai-feasibility` → `ai-agents` → `security` (LLM Top 10) → `skill-evals`-style evals for prompts |
| Performance problem | `algorithms-complexity` → `data-structures` → `postgres` → `system-design` |
| Code review | `code-quality` → `design-principles` → `security` |
| UI from design | `figma` → `nextjs` + `tailwind` or `flutter` |
| Unfamiliar business domain | `domain-learning` → `skill-forge` |

## Pitfalls

- Loading ten skills "just in case". Each costs context and attention.
- Routing to a general skill when a specific one exists.
- Forgetting the learn step; routes end with `skill-retro`.
