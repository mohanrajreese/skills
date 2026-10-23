# Skill lifecycle: learn → research → grow

This library improves itself. Every skill moves through the same loop, and
four meta-skills drive it:

```
        ┌──────────────── skill-gardener (periodic audit) ────────────────┐
        ▼                                                                 │
  idea ──► seed ──► draft ──► stable ──► deprecated                       │
   ▲        │         │          │                                        │
   │   skill-forge  skill-research                                        │
   │                   │          │                                       │
   └── BACKLOG.md ◄────┴── skill-retro (after real use) ──► LEARNINGS.md ─┘
```

| Meta-skill        | When it runs                                   | What it produces                                    |
|-------------------|------------------------------------------------|-----------------------------------------------------|
| `skill-forge`     | "Turn this into a skill", a new idea           | A new `skills/<name>/` from the template            |
| `skill-research`  | A skill is thin, stale, or a topic is new      | Sourced notes in `research/`, references in a skill |
| `skill-retro`     | After a task where a skill was used (or missing) | Dated entries in the skill's `LEARNINGS.md`, backlog ideas |
| `skill-gardener`  | Weekly / before a release                      | Promotions, merges, deprecations, refreshed index   |

## Status levels

Set in each skill's frontmatter under `metadata.status`.

| Status       | Meaning                                                        | Bar to reach it |
|--------------|----------------------------------------------------------------|-----------------|
| `seed`       | Idea captured, outline only. May be wrong.                     | Has a name, a description and the problem it solves. |
| `draft`      | Usable, tried on at least one real task.                       | Steps written, one real use recorded in `LEARNINGS.md`. |
| `stable`     | Trusted default across projects.                               | Used on 3+ tasks in 2+ projects, no open "wrong advice" learnings, sources cited for external facts. |
| `deprecated` | Superseded or no longer true. Kept so links don't break.       | `metadata.replaced-by` names the successor (or says why it's gone). |

## Learnings → skill body

`LEARNINGS.md` is an append-only log. The skill body is the curated result.
A learning gets promoted into `SKILL.md` when any of these hold:

- the same lesson shows up twice,
- it corrects something the skill currently says, or
- it cost real time when it was missing.

When a learning is promoted, mark its entry `→ promoted (YYYY-MM-DD)` rather
than deleting it, so the history of *why* the skill says what it says survives.
A learning that won't be acted on gets `→ rejected (YYYY-MM-DD): reason`.
Entries with `Change suggested: none` are informational and never count as
open; `scripts/skills.py report` counts everything else as open.

## Freshness

`metadata.last-reviewed` records when a human or `skill-gardener` last checked
the skill against reality. Skills that cite tools, APIs or versions go stale
fastest; the gardener flags anything not reviewed in 90 days.
