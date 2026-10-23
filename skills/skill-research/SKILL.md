---
name: skill-research
description: Research a topic, tool, library or practice and distill it into sourced notes and skill references in the dev-skills library. Use when a skill is thin, stale or flagged by the gardener, when a new technology is being adopted across projects, when asked to "research X and make it a skill", "what's the current best practice for X", "update our skill on X", or when a skill's advice turned out wrong and needs checking against primary sources.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [meta, research]
---

# Skill Research

Grows the library's knowledge from primary sources instead of memory, and
leaves a trail so the next reader can see where each claim came from and
when it was checked.

## When to use

- Before promoting a skill that makes claims about external tools or APIs.
- When `skill-gardener` flags a skill as stale (90+ days, or versions moved).
- When a `LEARNINGS.md` entry of kind `wrong-advice` needs resolving.

## Steps

1. **Frame the question.** Write 1–3 concrete questions the research must
   answer, e.g. "How do we configure X for monorepos in version N?". Vague
   topics produce vague skills.
2. **Gather from primary sources, in this order:**
   1. Official docs, changelogs and release notes (check the version!).
   2. The source code or its tests, when docs are silent.
   3. Our own projects: how is it actually used today? Search the repos.
   4. Well-regarded secondary sources, only to find leads to 1–3.

   Use web search / fetch tools if available. Note the version and the date
   checked for every fact; tool advice without a version goes stale silently.
3. **Write the research note** at `research/YYYY-MM-DD-<topic>.md`:
   ```markdown
   # <topic>
   Questions: …
   ## Findings
   - Claim. Source: <url or path>, checked YYYY-MM-DD, version N.
   ## Open questions
   ## Recommendation for the library
   ```
4. **Distill into the skill.** Put the actionable result into the target
   skill's `SKILL.md` (steps, pitfalls), and longer reference material into
   `skills/<name>/references/<topic>.md`. Cite the research note. Don't
   paste whole docs; the skill should say what *we* do and why.
5. **Resolve learnings.** Mark any `LEARNINGS.md` entries the research
   answered as `→ promoted (date)` or `→ rejected (date): reason`.
6. **Bump** `metadata.version` (minor for new guidance, patch for fixes) and
   `metadata.last-reviewed`. Run `python3 scripts/skills.py validate`.
7. If the research uncovers a new skill-worthy topic, add it to `BACKLOG.md`
   rather than scope-creeping the current skill.

## Pitfalls

- Recency: model memory lags reality. When a source and memory disagree, the
  source wins; when two sources disagree, prefer the newer official one and
  record the conflict under *Open questions*.
- Don't over-generalise from one project. If only one project does it that
  way, say so in the skill.
