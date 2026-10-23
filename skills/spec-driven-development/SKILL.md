---
name: spec-driven-development
description: Our spec-driven and skill-driven development workflow (SDD) for building features with AI coding agents, going from constitution to spec, clarify, plan, tasks, implement, verify and retro, with the matching skills loaded at each phase and learnings fed back into the library. Ships spec, plan and tasks templates and maps to GitHub Spec Kit and Kiro. Use whenever starting a non-trivial feature, turning an idea or ticket into a spec, asking an agent to build something bigger than a quick fix, writing acceptance criteria, breaking work into tasks, or when someone mentions SDD, spec-driven, skill-driven, Spec Kit or specs.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [workflow, specs, agentic-coding, planning]
---

# Spec-driven and skill-driven development (SDD)

**Spec-driven:** decide *what* and *why* in writing before code, so agents
and humans build the same thing and can check it. **Skill-driven:** every
phase pulls in the library's skills for *how*, and every delivery feeds new
lessons back into those skills. Together they make each feature build on the
last.

## Where things live

```text
specs/
  constitution.md            # once per project: principles (or point to CLAUDE.md)
  NNN-<feature>/
    spec.md                  # what & why: stories, acceptance criteria
    plan.md                  # how: stack, data model, APIs, risks
    tasks.md                 # ordered, testable tasks with IDs
```

Templates: `assets/spec-template.md`, `assets/plan-template.md`,
`assets/tasks-template.md` in this skill folder.

## Phases

| Phase | Output | Skills to load | Gate |
|---|---|---|---|
| 0. Constitution (once) | Principles: quality bar, testing, security, UX, "we use our stack" | `project-onboarding`, `agentic-coding` | Team agrees |
| 1. Specify | `spec.md`: problem, users, stories, **acceptance criteria**, non-goals | `brainstorm`, `feature-feasibility`, `ai-feasibility`, `pricing` if monetised | No implementation details; every story testable |
| 2. Clarify | Open questions answered or recorded as assumptions | — | No `[NEEDS CLARIFICATION]` left that blocks the plan |
| 3. Plan | `plan.md`: architecture, data model, API contracts, migrations, security and cost notes, test strategy | `tech-stack-chooser`, stack skills, `security`, `cloud-cost-planning`, `saas`, integration skills | Plan respects the constitution; risks have mitigations |
| 4. Tasks | `tasks.md`: small tasks (T001…), dependencies, `[P]` for parallel, each with its check | `subagent-suggester` for parallel work | Every acceptance criterion maps to ≥1 task |
| 5. Implement | Code + tests, task by task | stack skills, `figma` for UI | Each task's check passes before the next |
| 6. Verify | Acceptance criteria demonstrated (tests, screenshots, demo) | `security`, `/code-review` | All criteria pass; no unplanned scope |
| 7. Retro | Learnings logged; specs updated to match what shipped | `skill-retro` | Library improved |

## Writing good specs

- Acceptance criteria in **Given / When / Then**, or EARS style ("When
  <trigger>, the system shall <response>"). Include error and edge cases:
  payment fails, webhook duplicates, empty states, permission denied.
- Non-goals are as important as goals; they stop agent scope creep.
- Keep specs about behaviour. Tables, endpoints and libraries belong in the
  plan.
- Size: if `tasks.md` has more than ~15–20 tasks, split the feature.

## With tools

- **GitHub Spec Kit:** `uv tool install specify-cli`, `specify init <project>
  --integration <agent>`, then `/speckit-constitution` → `/speckit-specify` →
  `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` →
  `/speckit-converge` (repeat until converged). Its files live under
  `.specify/` and `specs/`. Use our skills inside its phases as above.
- **Kiro:** requirements / design / tasks per feature map to our spec / plan
  / tasks.
- **Plain Claude Code:** plan mode for phases 1–4 with the templates, then
  implement task by task.

## Pitfalls

- Specs written after the code to satisfy the process.
- Letting the agent implement the whole `tasks.md` in one go without checks
  between tasks.
- Specs that drift from reality; update them in the retro or mark them
  superseded.

## Sources

- GitHub Spec Kit README (checked 2026-10-23); see
  `research/2026-10-23-product-platform-baseline.md` → Spec-driven development.
