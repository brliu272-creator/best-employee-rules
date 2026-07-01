#!/usr/bin/env python3
"""Validate a best-employee-rules skill file.

Checks:
  - YAML frontmatter with required fields (name, description)
  - Six numbered rules (rule headers matching "## N." or "## N ·")
  - Self-check checklist table (6 rows)
  - No missing or empty sections

Usage:
  python scripts/validate.py best-employee-rules.md
  python scripts/validate.py --quiet best-employee-rules.md
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown text."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not m:
        return {}, text
    raw = m.group(1)
    body = m.group(2)

    # Simple YAML parser for flat key-value and key: | blocks
    fm: dict = {}
    current_key: Optional[str] = None
    current_val: list[str] = []

    for line in raw.split("\n"):
        if current_key is not None:
            if line.startswith("  ") or line.startswith("\t"):
                current_val.append(line.strip())
                continue
            else:
                fm[current_key] = " ".join(current_val)
                current_key = None
                current_val = []

        kv = re.match(r"^(\w+):\s*(.*)", line)
        if kv:
            key = kv.group(1)
            val = kv.group(2).strip()
            if val == "|":
                current_key = key
                current_val = []
            else:
                fm[key] = val

    if current_key is not None:
        fm[current_key] = " ".join(current_val)

    return fm, body


def find_rules(body: str) -> list[str]:
    """Find rule headers like '## 1. RuleName' or '## 1 · RuleName'."""
    return re.findall(r"^##\s*\d+[.·]\s*(.+)", body, re.MULTILINE)


def find_checklist_rows(body: str) -> list[str]:
    """Find checklist table rows (excluding header)."""
    in_table = False
    rows = []
    for line in body.split("\n"):
        if re.match(r"^\|.*\|$", line):
            if re.match(r"^\|[\s-]+\|", line):  # separator line
                in_table = True
                continue
            if in_table:
                rows.append(line)
    return rows


def validate(filepath: Path, quiet: bool = False) -> int:
    """Validate a skill file. Returns 0 on success, 1 on failure."""
    errors: list[str] = []

    if not filepath.exists():
        print(f"ERROR: file not found: {filepath}")
        return 1

    text = filepath.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    # 1. Frontmatter fields
    if not fm:
        errors.append("missing or invalid YAML frontmatter (--- ... ---)")
    else:
        for field in ["name", "description"]:
            if field not in fm or not fm[field].strip():
                errors.append(f"frontmatter missing required field: '{field}'")

    # 2. Six rules
    rules = find_rules(body)
    if len(rules) < 6:
        errors.append(f"expected 6 rules, found {len(rules)}: {rules}")
    elif len(rules) > 6:
        errors.append(f"expected 6 rules, found {len(rules)}: {rules}")

    # 3. Checklist
    checklist_rows = find_checklist_rows(body)
    if len(checklist_rows) < 6:
        errors.append(
            f"self-check checklist: expected >=6 rows, found {len(checklist_rows)}"
        )
    elif len(checklist_rows) > 6:
        errors.append(
            f"self-check checklist: expected 6 rows, found {len(checklist_rows)}"
        )

    # 4. Basic content checks
    if not body.strip():
        errors.append("body is empty")

    # Report
    if errors:
        print(f"FAIL: {filepath.name}")
        for e in errors:
            print(f"  - {e}")
        return 1

    if not quiet:
        print(f"PASS: {filepath.name}")
        print(f"  frontmatter: name='{fm.get('name','?')}'")
        print(f"  rules: {len(rules)} found")
        print(f"  checklist: {len(checklist_rows)} rows")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a best-employee-rules skill file")
    parser.add_argument("file", type=Path, help="path to the skill .md file")
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="only print on failure"
    )
    args = parser.parse_args()
    sys.exit(validate(args.file, quiet=args.quiet))


if __name__ == "__main__":
    main()
