---
name: python
description: How we write, run, lint, type-check and test Python across our projects, using uv, Ruff, pytest and a type checker, plus what changed recently in Python and its tooling. Use whenever working in a Python codebase or script, setting up a new Python project, adding dependencies, fixing lint or type errors, upgrading Python or Ruff, or when you see pyproject.toml, uv.lock, requirements.txt or .python-version. For Django-specific work also use the django skill.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, python, backend]
---

# Python

Our baseline for Python work: one package manager, one linter/formatter, a
type checker and pytest, all run through the project's lockfile.

## Before you start

1. **Detect what the project already uses and follow it.** Look for
   `uv.lock` (uv), `poetry.lock` (Poetry), `Pipfile.lock` (Pipenv),
   `requirements*.txt` (pip-tools/pip), and tool config in `pyproject.toml`
   (`[tool.ruff]`, `[tool.mypy]`, `[tool.pyright]`, `[tool.pytest.ini_options]`).
   Mixing managers in one repo breaks lockfiles; don't introduce uv into a
   Poetry project as a side effect of another task.
2. Check the Python version: `.python-version`, `requires-python` in
   `pyproject.toml`, the Dockerfile or CI matrix. Write code that runs on the
   *lowest* version the project supports.

## Defaults for new projects

| Concern | Default | Why |
|---|---|---|
| Python | 3.14 | 3.15.0 shipped 2026-10-09; give wheels and platforms (e.g. Lambda) a few months before adopting it. |
| Env + deps + lock | `uv` (`uv init`, `uv add`, `uv sync`) | Fast, one tool for Python installs, venvs and lockfiles. Commit `uv.lock`. |
| Lint + format | `ruff check` + `ruff format` | Replaces flake8/isort/black. Pin the version. |
| Types | mypy or pyright in CI | `ty` is fast but still 0.0.x; fine to try, not yet our only gate. |
| Tests | pytest (+ `pytest-cov`) | |
| Settings / validation | pydantic v2 / pydantic-settings at boundaries | |

## Verify loop

Run these before calling work done (prefix with `uv run` in uv projects):

```bash
uv sync --locked            # env matches the lockfile
uv run ruff check .         # add --fix for safe autofixes
uv run ruff format --check .
uv run mypy .               # or: uv run pyright
uv run pytest -q
```

## Rules that matter

- Type-annotate public functions. Use modern syntax (`list[str]`,
  `X | None`) when the minimum Python allows it.
- Timezone-aware datetimes only: `datetime.now(UTC)`, never
  `datetime.utcnow()` (deprecated since 3.12).
- Validate external input (HTTP, files, env, queues) at the boundary with
  pydantic or dataclasses plus explicit checks; trust typed values inside.
- Use `pathlib`, `logging` (not `print`) and context managers for resources.
- Secrets come from the environment or a secret manager, never from code or
  committed `.env` files.
- Add dependencies with the project's tool (`uv add pkg`, `uv add --dev pkg`)
  so the lockfile updates in the same change.

## Changed recently (checked 2026-10-23)

- **Ruff 0.16** (Jul 2026) turned on 413 default rules (was 59) and formats
  Python blocks in Markdown. Upgrading Ruff in a repo without an explicit
  `select` list can produce hundreds of new findings: pin the version, and
  upgrade in its own PR. **Ruff 0.17** defaults to Python 3.11 when no
  `target-version`/`requires-python` is set, so set `requires-python`.
- **Python 3.15.0** released 2026-10-09. **3.14** made the free-threaded
  (no-GIL) build officially supported, but it is opt-in and many C
  extensions aren't ready; don't assume it.
- **Python 3.10** reaches end of life in October 2026; plan upgrades for
  projects still on it.

## Pitfalls

- `pip install` into the system or global interpreter. Always use the
  project env (`uv run`, or an activated venv).
- Editing `uv.lock`/`poetry.lock` by hand: regenerate with the tool.
- Mutable default arguments, bare `except:`, and catching `Exception` just
  to log and continue. They hide real failures.
- Shadowing stdlib modules with local file names (`json.py`, `types.py`).

## Sources

- `research/2026-10-23-stack-baseline.md` → Python section.
