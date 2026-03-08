#!/usr/bin/env python3
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ALLOWED_ROOT_FILES = {"SKILL.md"}
ALLOWED_ROOT_DIRS = {"agents", "scripts", "references", "assets"}
EXCLUDED_PARTS = {"__pycache__", "dist"}


def iter_files(skill_dir: Path):
    for path in sorted(skill_dir.rglob("*")):
        if path.is_dir():
            continue
        relative = path.relative_to(skill_dir)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if len(relative.parts) == 1:
            if relative.name not in ALLOWED_ROOT_FILES:
                continue
        elif relative.parts[0] not in ALLOWED_ROOT_DIRS:
            continue
        yield path, relative


def package_skill(skill_dir: Path, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    root_name = skill_dir.name
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, relative in iter_files(skill_dir):
            archive.write(path, arcname=str(Path(root_name) / relative))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package a skill directory into a .skill archive")
    parser.add_argument(
        "--skill-dir",
        default=".",
        help="Path to the skill directory to package",
    )
    parser.add_argument(
        "--output",
        help="Output archive path. Defaults to dist/<skill-name>.skill",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_dir).resolve()
    output_path = (
        Path(args.output).resolve()
        if args.output
        else skill_dir / "dist" / f"{skill_dir.name}.skill"
    )
    package_skill(skill_dir, output_path)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
