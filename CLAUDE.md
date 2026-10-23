# CLAUDE.md

This repo is the shared dev-skills library. It is a Claude Code plugin
(`.claude-plugin/`) whose skills live in `skills/<name>/SKILL.md`.

## Working here

- Creating a skill → follow `skills/skill-forge/SKILL.md`.
- Recording what a task taught us → `skills/skill-retro/SKILL.md`.
- Refreshing a skill from sources → `skills/skill-research/SKILL.md`.
- Maintenance pass → `skills/skill-gardener/SKILL.md`.
- Lifecycle rules (status bars, promotion rule, freshness):
  `docs/skill-lifecycle.md`.

## Commands

```bash
python3 scripts/skills.py validate   # must pass before committing
python3 scripts/skills.py index      # rerun after any frontmatter change; commit SKILLS.md
python3 scripts/skills.py report
```

## Conventions

- Frontmatter keys: `name`, `description`, optional `license`,
  `allowed-tools`, `compatibility`, and `metadata` (`status`, `version`,
  `last-reviewed`, `owners`, `tags`, `replaced-by`).
- `name` is kebab-case and equals the folder name.
- Bump `metadata.version` (semver) and `metadata.last-reviewed` whenever a
  skill's guidance changes.
- `LEARNINGS.md` is append-only, newest entry first; mark entries
  `→ promoted (date)` / `→ rejected (date): reason` instead of deleting.
- `SKILLS.md` is generated; never edit it by hand.
