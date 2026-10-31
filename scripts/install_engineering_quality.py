#!/usr/bin/env python3
"""Install engineering-quality profile without overwriting existing project files."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import sys

FACTORY = Path(__file__).resolve().parents[1]
SOURCE = FACTORY / "policy" / "engineering-quality"


def install(target: Path, project: str, dry_run=False):
    target = Path(target).resolve()
    if not (target / ".git").exists() and not (target / ".git").is_file():
        raise ValueError("Target must be a Git working tree")
    if not project or "/" not in project or any(c.isspace() for c in project):
        raise ValueError("Provide a valid owner/repository project")
    config = {
        "schema": "engineering-quality-v1",
        "project": project,
        "quick": [],
        "full_additional": []
    }
    files = {
        target / "scripts" / "quality_runner.py": (SOURCE / "quality_runner.py").read_bytes(),
        target / "scripts" / "architecture_explorer.py": (SOURCE / "architecture_explorer.py").read_bytes(),
        target / "quality" / "ENGINEERING-STANDARD.md": (SOURCE / "ENGINEERING-STANDARD.md").read_bytes(),
        target / "quality" / "standard.json": (json.dumps(config, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        target / "quality" / ".gitignore": b"/reports/\n",
    }
    conflicts = [str(path) for path, content in files.items()
                 if path.exists() and path.read_bytes() != content]
    if conflicts:
        raise ValueError("Existing quality files differ; manual reconciliation required: " + ", ".join(conflicts))
    if dry_run:
        return ["PLAN " + str(path) for path in files]
    created = []
    for path, content in files.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            created.append("CREATED " + str(path))
        else:
            created.append("UNCHANGED " + str(path))
    return created


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        for line in install(Path(args.target), args.project, args.dry_run):
            print(line)
        return 0
    except (OSError, ValueError) as exc:
        print("ENGINEERING_PROFILE_ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
