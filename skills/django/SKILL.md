---
name: django
description: How we build, migrate, test, secure and upgrade Django apps (including Django REST Framework), with what changed in Django 6.0 and 6.1 such as the Tasks framework, CSP, template partials, fetch modes and MAILERS. Use whenever working in a Django project, writing models, migrations, views, serializers, admin or settings, chasing N+1 queries, adding background jobs, preparing a deploy, or upgrading Django versions, or when you see manage.py or settings.py. Pair with the python skill for tooling and the postgres skill for database work.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [stack, python, django, backend]
---

# Django

Our baseline for Django: safe migrations, query discipline, deploy checks,
and knowing which Django version's features are actually available.

## Before you start

1. Find the Django version (`uv.lock`/`requirements*.txt`/`pyproject.toml`)
   and only use features that version has. 6.0 and 6.1 added a lot (below).
2. Find the settings layout (single `settings.py`, or `settings/base.py` +
   per-environment modules) and how settings read env vars.
3. Note the test runner (`manage.py test` vs `pytest` + `pytest-django`) and
   whether DRF, Celery, Channels or django-tasks are in use.

## Defaults for new projects

- Django 6.1 if the project will upgrade at least yearly; 5.2 LTS
  (supported to April 2028) for low-maintenance apps. Django 6.x needs
  Python 3.12+.
- Postgres as the database (see the `postgres` skill), `BigAutoField` PKs
  (the default since 6.0).
- Settings from environment variables; `DEBUG=False` unless explicitly local.
- `pytest-django`, `django-stubs` for type checking, Ruff for lint.
- APIs: DRF (3.18) or django-ninja, whichever the project already uses.

## Verify loop

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run   # fails if models changed without a migration
uv run python manage.py migrate
uv run pytest -q                                           # or: python manage.py test
uv run python manage.py check --deploy --settings=<prod settings module>   # before a release
```

## Rules that matter

- **Migrations:** one logical change per migration; never edit a migration
  that has been applied anywhere shared; review generated SQL with
  `sqlmigrate` for anything touching large tables. For big tables follow the
  zero-downtime pattern in the `postgres` skill (add nullable → backfill in
  batches → add constraint). Keep data migrations separate from schema ones.
- **Queries:** every list view should have a bounded query count. Use
  `select_related` / `prefetch_related`, and pin it in tests with
  `assertNumQueries` / `django_assert_num_queries`. On 6.1+,
  `QuerySet.fetch_mode(models.FETCH_PEERS)` fixes most N+1 cases and
  `FETCH_RAISE` makes accidental lazy loads fail loudly in hot paths.
- **Transactions:** wrap multi-write operations in `transaction.atomic()`.
  Enqueue background work with `transaction.on_commit(...)` so jobs never see
  uncommitted rows.
- **Security:** keep CSRF on; use the ORM or parameterised `raw()`, never
  string-formatted SQL; validate with forms/serializers; check object-level
  permissions, not just login. Django 6.0+ has built-in CSP support; use it
  instead of a third-party CSP middleware on new work.
- **Settings:** never commit `SECRET_KEY` or credentials; set
  `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` and secure cookie/HSTS settings for
  production (`check --deploy` lists what's missing).

## Changed recently (checked 2026-10-23)

- **6.1 (Aug 2026):** fetch modes (above); database-level `on_delete`
  (`DB_CASCADE`, `DB_SET_NULL`, `DB_SET_DEFAULT`). These run in SQL and
  **don't fire delete signals**. New `MAILERS` setting will replace
  `EMAIL_BACKEND`/`EMAIL_*` in 7.0, and old settings now warn. 6.1 supports
  Python 3.12–3.15 (3.15 from 6.1.3).
- **6.0 (Dec 2025):** built-in **Tasks framework** (`from django.tasks import
  task`, `@task`, `.enqueue()`, `TASKS` setting). The bundled backends are
  for development/testing and Django ships **no worker**, so production needs
  a real backend and worker process. Also template partials
  (`{% partialdef %}`), CSP support, the modern email API, and
  `DEFAULT_AUTO_FIELD` now defaults to `BigAutoField` (set it explicitly in
  old projects to avoid surprise migrations).

## Pitfalls

- Signals for business logic: hard to trace, and skipped by `bulk_*`,
  `update()`, `DB_CASCADE`. Prefer explicit service functions.
- `.save()` in loops; use `bulk_create`/`bulk_update` or `update()`.
- Doing slow work (email, HTTP calls, image processing) inside the request;
  enqueue it.
- `makemigrations` producing a migration you didn't expect: find out why
  (often a default or `choices` change) before committing it.

## Sources

- `research/2026-10-23-stack-baseline.md` → Django section (official 6.0 and
  6.1 release notes).
