# Dev Skills

A shared library of [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
for all our projects, built to **learn, research and grow itself**. Skills
start as seeds, get exercised on real work, collect learnings from every use,
get checked against primary sources, and are promoted, merged or retired by a
regular maintenance pass.

See [`SKILLS.md`](SKILLS.md) for the current catalogue.

## How the library grows

Four meta-skills run the loop (details in
[`docs/skill-lifecycle.md`](docs/skill-lifecycle.md)):

| Skill | Role | Say something like |
|---|---|---|
| [`skill-forge`](skills/skill-forge/SKILL.md) | Create a skill from an idea or a workflow just done | "Make this a skill" |
| [`skill-retro`](skills/skill-retro/SKILL.md) | **Self-learn**: log what worked and what didn't after real use | "Retro: what did we learn?" |
| [`skill-research`](skills/skill-research/SKILL.md) | **Research**: check a topic against primary sources, cite them | "Research X and update our skill" |
| [`skill-gardener`](skills/skill-gardener/SKILL.md) | **Grow**: promote learnings, re-rate status, merge, deprecate | "Review our skills" |

Skills move `seed → draft → stable → deprecated`; each level has an explicit
bar so "stable" means something.

## Stack skills

One skill per technology we use. Each one starts by detecting the project's
versions (the project's conventions win), then gives defaults for new
work, a verify loop of real commands, the rules that matter, and a dated
**"Changed recently"** section backed by
[`research/2026-10-23-stack-baseline.md`](research/2026-10-23-stack-baseline.md).

| Area | Skills |
|---|---|
| Backend | `python`, `django`, `golang` |
| Web | `typescript`, `nextjs`, `tailwind`, `shopify` |
| Data | `postgres`, `supabase` |
| Cloud | `aws`, `gcp`, `firebase` |
| Mobile | `flutter` |

Version facts go stale. `skill-gardener` flags skills not reviewed in 90
days, and `skill-research` refreshes them from primary sources.

## Product, platform and AI skills

| Area | Skills |
|---|---|
| Plan | `brainstorm`, `feature-feasibility`, `ai-feasibility`, `tech-stack-chooser`, `cloud-cost-planning` |
| Build | `spec-driven-development` (spec → plan → tasks, templates included), `saas`, `figma` |
| Integrations | `razorpay`, `whatsapp-integration`, `sso` |
| Money | `pricing`, `subscription-billing` |
| Security | `security` (OWASP Top 10:2025, OWASP GenAI LLM Top 10 2026, DPDP) |
| AI | `ai-agents`, `agentic-coding`, `subagent-suggester` |

[`docs/idea-to-ship.md`](docs/idea-to-ship.md) shows how they chain from an
idea to a shipped feature. Evidence lives in
[`research/2026-10-23-product-platform-baseline.md`](research/2026-10-23-product-platform-baseline.md).

## Use the skills in a project

**Claude Code (plugin marketplace)**, once per machine:

```
/plugin marketplace add mohanrajreese/skills
/plugin install dev-skills@mohanrajreese-skills
```

**Claude Code, for everyone on a project**: commit this to the project's
`.claude/settings.json` so teammates get prompted to install it:

```json
{
  "extraKnownMarketplaces": {
    "mohanrajreese-skills": {
      "source": { "source": "github", "repo": "mohanrajreese/skills" }
    }
  },
  "enabledPlugins": { "dev-skills@mohanrajreese-skills": true }
}
```

**Manual**: copy or symlink a skill folder into `~/.claude/skills/` (personal)
or `<project>/.claude/skills/` (one project). For claude.ai, zip a single skill
folder and upload it under Settings → Capabilities → Skills.

## Repository layout

```
.claude-plugin/        plugin.json + marketplace.json (installable as a plugin)
skills/<name>/         one folder per skill
  SKILL.md             frontmatter (name, description, metadata) + instructions
  LEARNINGS.md         append-only log of real uses; feeds improvements
  references/          optional deep-dive docs, loaded on demand
  scripts/             optional deterministic helpers
templates/skill/       what `scripts/skills.py new` copies
research/              sourced research notes behind skill guidance
docs/                  library conventions
BACKLOG.md             skill ideas not built yet
SKILLS.md              generated index — don't edit by hand
```

## Contributing

```bash
pip install pyyaml
python3 scripts/skills.py new my-skill -d "What it does. Use when ..."  # scaffold
python3 scripts/skills.py validate   # frontmatter, naming, status, size
python3 scripts/skills.py index      # regenerate SKILLS.md
python3 scripts/skills.py report     # status, staleness, open learnings
```

CI runs `validate` and checks `SKILLS.md` is current on every PR.

Ground rules:

- **Cross-project only.** Knowledge specific to one repo goes in that repo's
  `CLAUDE.md` or `.claude/skills/`.
- **Descriptions decide triggering.** Say what the skill does *and* when to
  use it, with the phrases people actually type.
- **Explain why, not just what.** Reasons let a skill adapt to projects it
  wasn't written for.
- **Cite and date external facts.** Tools change; undated advice rots
  silently.
- **No secrets** — no credentials, customer data or internal hostnames
  anywhere in this repo, including learnings.

## License

[MIT](LICENSE)
