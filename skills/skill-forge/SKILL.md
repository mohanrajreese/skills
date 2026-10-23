---
name: skill-forge
description: Create a new skill in the shared dev-skills library from an idea, a workflow just completed, or a repeated set of instructions. Use whenever someone says "make this a skill", "we keep doing this", "save this workflow", "add a skill for X", or when the same multi-step procedure has been explained more than once across sessions, even if they never say the word skill.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [meta, authoring]
---

# Skill Forge

Turns a repeatable piece of know-how into a skill in this repo
(`skills/<name>/`), following the library's conventions so the other
meta-skills can research, learn into and maintain it later.

## When to use

- A workflow was just done in a session and is worth repeating.
- An item from `BACKLOG.md` is being picked up.
- Not for editing an existing skill: append to its `LEARNINGS.md` via
  `skill-retro`, or refresh it via `skill-research`.

## Steps

1. **Check for overlap first.** Read `SKILLS.md` (the generated index). If an
   existing skill covers 70%+ of the idea, extend that one instead; two
   near-duplicate skills compete for triggering and both get worse.
2. **Pin down the intent.** Get answers (from the conversation if possible,
   otherwise ask) to:
   - What should Claude be able to do with this skill?
   - What phrases or situations should trigger it? What should *not*?
   - What does a correct result look like, and how is it verified?
   - Is it project-specific? If so it belongs in that project's
     `.claude/skills/`, not here. This library is for things that apply
     across projects.
3. **Scaffold** with the repo script, which fills the template and today's date:
   ```bash
   python3 scripts/skills.py new <kebab-name> --description "..."
   ```
4. **Write the description carefully.** It is the only part always in context
   and is what decides whether the skill fires. Say what it does *and* when to
   use it, list the trigger phrases, and lean slightly pushy; under-triggering
   is the common failure. Max 1024 chars, no angle brackets.
5. **Write the body** from the template's sections. Prefer explaining *why*
   over ALL-CAPS rules; reasons let the model adapt to a project it hasn't
   seen. Keep `SKILL.md` under ~300 lines and move detail into
   `references/`. Put deterministic, repeated logic into `scripts/`.
6. **Record provenance.** Add the first `LEARNINGS.md` entry: where the
   workflow came from (project, task) and kind `idea` or `worked`.
7. **Set status honestly.** `seed` if it's an outline, `draft` if it was used
   on a real task. Never start at `stable` (see `docs/skill-lifecycle.md`).
8. **Validate and index:**
   ```bash
   python3 scripts/skills.py validate
   python3 scripts/skills.py index
   ```
9. If the idea came from `BACKLOG.md`, remove it from there.

## Pitfalls

- Skills that restate what the model already knows ("write clean code") add
  context cost and no value. Capture what is specific: our conventions, the
  order that avoids a trap, the command that actually works.
- Overly narrow skills, written around one example, don't trigger on the next
  case. Generalise the steps; keep the example in `references/`.
- For a deeper eval-driven loop (test prompts, benchmarks, description
  tuning) use Anthropic's `skill-creator` skill if it is available, then come
  back here for the repo conventions.
