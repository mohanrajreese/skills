---
name: skill-gardener
description: Audit and maintain the dev-skills library as a whole by promoting recurring learnings into skill bodies, advancing or demoting skill status, merging overlapping skills, deprecating stale ones and regenerating the index. Use for periodic maintenance, before tagging a release, when asked to "review our skills", "clean up the skills repo", "which skills are stale", "groom the backlog", or when skill triggering seems to overlap or misfire.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [meta, maintenance]
---

# Skill Gardener

The "grow" half of the loop: keeps the library small, current and
trustworthy, so the skills that load are the ones worth loading.

## When to use

- On a schedule (weekly is a good default) or before a release.
- When `python3 scripts/skills.py report` shows stale skills or unpromoted
  learnings piling up.

## Steps

1. **Get the state:**
   ```bash
   python3 scripts/skills.py validate
   python3 scripts/skills.py report
   ```
   The report lists each skill's status, last review age and count of
   unpromoted learnings.
2. **Promote learnings.** For each skill with open entries, apply the rule in
   `docs/skill-lifecycle.md` (repeated, corrective, or costly → promote).
   Edit `SKILL.md`, mark entries `→ promoted (date)` or `→ rejected (date):
   reason`, bump the version.
3. **Re-rate status** against the bars in `docs/skill-lifecycle.md`:
   - `seed` with a real use logged → `draft`.
   - `draft` meeting the `stable` bar → `stable`.
   - `stable` with open `wrong-advice` entries → back to `draft` until fixed.
4. **Find overlap.** Read all descriptions side by side (`SKILLS.md`). Two
   skills that would both fire on the same request should be merged or have
   their descriptions sharpened to say when to use the other one.
5. **Freshness.** Anything with `last-reviewed` older than 90 days that cites
   tools, versions or APIs → run `skill-research` on it, or mark it
   `deprecated` with `metadata.replaced-by` if it's no longer relevant.
6. **Groom `BACKLOG.md`.** Drop ideas that no longer matter, merge
   duplicates, and pick the top one or two to hand to `skill-forge`.
7. **Regenerate the index** with `python3 scripts/skills.py index` and
   summarise what changed (promoted, merged, deprecated, new) in the commit
   message or PR description.

## Pitfalls

- Don't delete deprecated skills outright; other projects may reference
  them. Deprecate, point to the replacement, remove a release later.
- Fewer, sharper skills beat many overlapping ones; every description costs
  context in every session.
