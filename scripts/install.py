#!/usr/bin/env python3
"""Install best-employee-rules skill to target directory.

Copies the skill .md file to a Reasonix / Kun skills directory.

Usage:
  python scripts/install.py                          # auto-detect target
  python scripts/install.py --target ~/.reasonix/skills/
  python scripts/install.py --variant en             # install English version
  python scripts/install.py --dry-run                # preview only
"""

import argparse
import shutil
import sys
from pathlib import Path

SKILL_FILES = {
    "bilingual": "best-employee-rules.md",
    "en": "best-employee-rules-en.md",
}

AUTO_TARGETS = [
    Path.home() / ".reasonix" / "skills",
    Path.home() / ".codex" / "skills",
    Path.home() / ".kun" / "skills",
]


def find_target() -> Path | None:
    """Auto-detect an existing skills directory."""
    for p in AUTO_TARGETS:
        if p.exists() and p.is_dir():
            return p
    return None


def install(
    source_dir: Path,
    target: Path,
    variant: str = "bilingual",
    dry_run: bool = False,
    force: bool = False,
) -> int:
    filename = SKILL_FILES.get(variant, SKILL_FILES["bilingual"])
    src = source_dir / filename

    if not src.exists():
        print(f"ERROR: source file not found: {src}")
        return 1

    target.mkdir(parents=True, exist_ok=True)
    dst = target / "best-employee-rules.md"

    if dst.exists() and not force:
        print(f"WARNING: {dst} already exists. Use --force to overwrite.")
        return 1

    if dry_run:
        print(f"[DRY RUN] would copy: {src} -> {dst}")
        return 0

    shutil.copy2(src, dst)
    print(f"Installed: {dst}")
    print(f"  source: {src}")
    print(f"  variant: {variant}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install best-employee-rules skill to a skills directory"
    )
    parser.add_argument(
        "-t", "--target", type=Path, default=None, help="target skills directory"
    )
    parser.add_argument(
        "--variant",
        choices=["bilingual", "en"],
        default="bilingual",
        help="which language variant to install (default: bilingual)",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="overwrite existing file"
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="preview without copying"
    )
    args = parser.parse_args()

    # Determine source directory (parent of scripts/)
    script_dir = Path(__file__).resolve().parent
    source_dir = script_dir.parent

    target = args.target or find_target()
    if target is None:
        print("ERROR: no target directory specified and no auto-target found.")
        print(f"  Tried: {', '.join(str(p) for p in AUTO_TARGETS)}")
        print("  Use --target to specify a path.")
        sys.exit(1)

    sys.exit(
        install(
            source_dir=source_dir,
            target=target,
            variant=args.variant,
            dry_run=args.dry_run,
            force=args.force,
        )
    )


if __name__ == "__main__":
    main()
