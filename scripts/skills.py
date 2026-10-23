#!/usr/bin/env python3
"""Tooling for the dev-skills library.

Commands:
  validate          Check every skills/*/SKILL.md against the library rules,
                    and that docs/skills-guide.md has an entry for each skill.
  index             Regenerate SKILLS.md from skill frontmatter.
  new NAME -d DESC  Scaffold skills/NAME/ from templates/skill/.
  report            Show status, review age and open learnings per skill.

Requires PyYAML (pip install pyyaml).
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
TEMPLATE_DIR = ROOT / "templates" / "skill"
INDEX_FILE = ROOT / "SKILLS.md"
GUIDE_FILE = ROOT / "docs" / "skills-guide.md"

ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
STATUSES = ("seed", "draft", "stable", "deprecated")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
ENTRY_RE = re.compile(r"^## \d{4}-\d{2}-\d{2}", re.MULTILINE)
STALE_DAYS = 90
MAX_BODY_LINES = 500


def read_frontmatter(skill_md):
    match = FRONTMATTER_RE.match(skill_md.read_text())
    if not match:
        raise ValueError("missing or malformed YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data


def skill_dirs():
    return sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.exists() else []


def to_date(value):
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def open_learnings(skill_dir):
    """Count LEARNINGS.md entries that suggest a change not yet promoted or rejected."""
    path = skill_dir / "LEARNINGS.md"
    if not path.exists():
        return 0
    text = path.read_text().split("<!-- entries below -->", 1)[-1]
    starts = [m.start() for m in ENTRY_RE.finditer(text)] + [len(text)]
    entries = [text[a:b] for a, b in zip(starts, starts[1:])]
    closed = ("→ promoted", "→ rejected", "Change suggested: none")
    return sum(1 for e in entries if not any(c in e for c in closed))


def validate_skill(skill_dir):
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ["SKILL.md not found"]
    try:
        fm = read_frontmatter(skill_md)
    except (ValueError, yaml.YAMLError) as e:
        return [str(e)]

    unexpected = set(fm) - ALLOWED_KEYS
    if unexpected:
        errors.append(f"unexpected frontmatter keys: {', '.join(sorted(unexpected))}")

    name = fm.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"name {name!r} must be kebab-case, at most 64 chars")
    elif name != skill_dir.name:
        errors.append(f"name {name!r} does not match directory {skill_dir.name!r}")

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append("description is required")
    else:
        if len(desc) > 1024:
            errors.append(f"description is {len(desc)} chars (max 1024)")
        if "<" in desc or ">" in desc:
            errors.append("description cannot contain angle brackets")
        if "{{" in desc:
            errors.append("description still contains a template placeholder")

    meta = fm.get("metadata") or {}
    if not isinstance(meta, dict):
        errors.append("metadata must be a mapping")
        meta = {}
    status = meta.get("status")
    if status not in STATUSES:
        errors.append(f"metadata.status must be one of {', '.join(STATUSES)}")
    if status == "deprecated" and not meta.get("replaced-by"):
        errors.append("deprecated skills need metadata.replaced-by")
    if not to_date(meta.get("last-reviewed")):
        errors.append("metadata.last-reviewed must be a YYYY-MM-DD date")

    nested = [p for p in skill_dir.rglob("SKILL.md") if p != skill_md and "evals" not in p.parts]
    if nested:
        errors.append(f"nested SKILL.md files: {', '.join(str(p.relative_to(skill_dir)) for p in nested)}")

    lines = skill_md.read_text().count("\n")
    if lines > MAX_BODY_LINES:
        errors.append(f"SKILL.md is {lines} lines (max {MAX_BODY_LINES}); move detail to references/")
    return errors


def cmd_validate(_args):
    failed = 0
    for d in skill_dirs():
        errors = validate_skill(d)
        if errors:
            failed += 1
            print(f"FAIL {d.name}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"ok   {d.name}")
    if GUIDE_FILE.exists():
        guide = GUIDE_FILE.read_text()
        missing = [d.name for d in skill_dirs() if f"`{d.name}`" not in guide]
        if missing:
            failed += 1
            print(f"FAIL {GUIDE_FILE.relative_to(ROOT)} has no entry for: {', '.join(missing)}")
    if failed:
        sys.exit(f"{failed} check(s) failed validation")


def cmd_index(_args):
    rows = []
    for d in skill_dirs():
        fm = read_frontmatter(d / "SKILL.md")
        meta = fm.get("metadata") or {}
        desc = " ".join(fm["description"].split()).replace("|", "\\|")
        rows.append(f"| [`{fm['name']}`](skills/{d.name}/SKILL.md) | {meta.get('status', '?')} | {desc} |")
    INDEX_FILE.write_text(
        "# Skills index\n\n"
        "Generated by `python3 scripts/skills.py index`. Do not edit by hand.\n\n"
        "| Skill | Status | Description |\n|---|---|---|\n" + "\n".join(rows) + "\n"
    )
    print(f"wrote {INDEX_FILE.relative_to(ROOT)} ({len(rows)} skills)")


def cmd_new(args):
    name = args.name
    if not NAME_RE.match(name) or len(name) > 64:
        sys.exit(f"{name!r} is not a valid kebab-case name")
    target = SKILLS_DIR / name
    if target.exists():
        sys.exit(f"{target.relative_to(ROOT)} already exists")
    values = {
        "name": name,
        "description": args.description,
        "title": name.replace("-", " ").title(),
        "date": dt.date.today().isoformat(),
    }
    target.mkdir(parents=True)
    for src in TEMPLATE_DIR.iterdir():
        text = src.read_text()
        for key, val in values.items():
            text = text.replace("{{" + key + "}}", val)
        (target / src.name).write_text(text)
    print(f"created {target.relative_to(ROOT)}/ — fill in SKILL.md, then run validate and index")


def cmd_report(_args):
    today = dt.date.today()
    print(f"{'skill':28} {'status':11} {'reviewed':>9} {'open learnings':>15}")
    for d in skill_dirs():
        try:
            fm = read_frontmatter(d / "SKILL.md")
        except (ValueError, yaml.YAMLError, FileNotFoundError):
            print(f"{d.name:28} invalid — run validate")
            continue
        meta = fm.get("metadata") or {}
        reviewed = to_date(meta.get("last-reviewed"))
        age = (today - reviewed).days if reviewed else None
        age_s = f"{age}d ago" if age is not None else "never"
        flag = "  STALE" if age is None or age > STALE_DAYS else ""
        print(f"{d.name:28} {str(meta.get('status')):11} {age_s:>9} {open_learnings(d):>15}{flag}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate").set_defaults(func=cmd_validate)
    sub.add_parser("index").set_defaults(func=cmd_index)
    sub.add_parser("report").set_defaults(func=cmd_report)
    new = sub.add_parser("new")
    new.add_argument("name")
    new.add_argument("-d", "--description", required=True)
    new.set_defaults(func=cmd_new)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
