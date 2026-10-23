---
name: skill-evals
description: Write and run tests for the skills in this library using the claude plugin eval format, covering should-fire and should-not-fire trigger cases, outcome graders (regex, file_exists, llm rubrics) in priority order, with-versus-without-skill ablation, minimum runs, interpreting the score delta, and turning failures into description or body fixes and LEARNINGS entries. Use whenever someone asks to test a skill, check whether a skill triggers or helps, write evals for a skill, compare a skill against no skill, gather evidence to promote a skill to stable, or when a skill seems to misfire or never load.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [meta, testing, evals]
---

# Skill evals

A skill is only proven when runs **with** it beat runs **without** it on
realistic prompts, and it stays quiet on prompts it shouldn't touch. This
skill writes those tests in the format `claude plugin eval` runs, so they
work locally and in CI.

## Where tests live

```text
evals/                                # repo root = the plugin's eval dir
  <skill>-<what-it-checks>/
    prompt.md                         # settings block + the user's prompt
    case.yaml                         # schema_version "1.1", name, expected_outcome
    graders/01-<claim>.md             # one checkable claim per file
    files/ + place-files.sh           # only if the case needs input files
```

Name cases `<skill>-<what>` and tag them with the skill name so one
skill's suite can run alone (`--tag razorpay`).

## Writing a suite (per skill: 3–6 cases)

1. **Should-fire cases (2–4):** prompts a real teammate would type, varied
   in wording; at least one doesn't name the technology directly.
2. **At least one should-NOT-fire case:** a nearby prompt that belongs to a
   different skill or none. This catches over-triggering.
3. **Graders: outcome first.** Prefer, in order: verifiable checks (`regex`
   on the answer, `file_exists`) → a binary claim → an `llm` rubric with
   concrete checkable statements. Every case needs at least one **outcome**
   grader.
4. A `tool_used` grader with `tool: Skill` is a **trigger indicator only**.
   It is reported but not scored. For "must not fire", set `min: 0`,
   `max: 0`, `arm: both`.
5. Keep `runs: 3` or more; models vary.

Example `prompt.md` and grader:

```markdown
---
tags: [razorpay]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add a webhook endpoint to our Django app that marks orders paid when Razorpay says so.
```

```markdown
---
type: llm
focus: trace
weight: 1
---

The handler verifies X-Razorpay-Signature with HMAC-SHA256 over the raw request body using the webhook secret before parsing JSON.
```

Scaffold a blank case with `claude plugin eval init --bare <name>`, or run
`claude plugin eval init` for a guided interview.

## Running

```bash
claude plugin eval . --tag <skill> --runs 3 --no-publish
```

- It compares **with plugin vs without** (ablation) and reports the score
  delta per case. A positive delta is the evidence a skill helps.
- **These are real, billed model runs.** Ask before running, and use
  `--max-cost-usd` for a hard ceiling.
- Results land in `evals/results/` (git-ignored).

## Acting on results

| Result | Fix |
|---|---|
| Should-fire case: skill not used | Description lacks the user's words; add trigger phrases (pushy, specific) |
| Should-not-fire case: skill used | Description too broad; add "not for X; use Y" boundaries |
| Skill used, outcome still fails | Body is wrong or unclear; fix the step, add a pitfall |
| With ≈ without | Skill adds nothing the model doesn't already know; sharpen it to our specifics, or deprecate it |

Record each run's outcome in the skill's `LEARNINGS.md` (`skill-retro`).
Passing evals with a positive delta across two projects' prompts is strong
evidence for promoting a skill to `stable` (`docs/skill-lifecycle.md`).

## Sources

- `claude plugin eval --help` and the case schema used by the skill-creator
  skill (checked 2026-10-23, Claude Code 2.1.309).
