---
name: skill-retro
description: Capture what was learned during a task into the dev-skills library so skills improve from real use. Use at the end of any substantial task, after a mistake was corrected, when a skill gave wrong or incomplete advice, when the user says "remember this", "note that for next time", "we should have known that", "retro", or "what did we learn", and whenever a workflow was needed that no skill covered.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [meta, learning]
---

# Skill Retro

The "self-learn" half of the loop. Turns experience from real projects into
dated, attributable entries that the gardener later promotes into skill
bodies.

## When to use

- After finishing a task where a library skill was used, or should have
  existed.
- Immediately after the user corrects an approach; corrections are the most
  valuable signal and the easiest to lose.

## Steps

1. **List the moments that mattered.** Scan the session for: corrections from
   the user, dead ends, commands that failed then worked, surprises, and
   steps that had to be figured out from scratch. Skip the routine.
2. **Classify each one** as `worked`, `wrong-advice`, `missing-step`,
   `gotcha` or `idea` (see `templates/skill/LEARNINGS.md`).
3. **Route it:**
   - It relates to an existing skill → append an entry to that skill's
     `LEARNINGS.md` (newest at top, under `<!-- entries below -->`).
   - No skill covers it, and it applies across projects → add a line to
     `BACKLOG.md` with the context.
   - It is specific to one project → it belongs in that project's
     `CLAUDE.md` or `.claude/skills/`, not here. Say so to the user.
4. **Write entries that stand alone.** Someone reading in three months has no
   session context. Include the project, what the skill said, what was
   actually needed, and a concrete suggested change.
5. **Fix right away when it's clear-cut.** If an entry is `wrong-advice` and
   the correct behaviour is unambiguous and verified, edit `SKILL.md` now,
   mark the entry `→ promoted (date)`, and bump the patch version. Otherwise
   leave promotion to `skill-gardener`.
6. If you are working in a project repo rather than this one, write the
   entries to a checkout of this repo if one is available; if not, output the
   entries in the reply so they can be pasted in, rather than dropping them.

## Pitfalls

- Logging everything makes the log useless. One sharp entry beats five vague
  ones.
- Never record secrets, credentials, customer data or internal hostnames in
  learnings; this repo is shared across projects.
