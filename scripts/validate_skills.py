#!/usr/bin/env python3
"""Validate the standalone ABI skills catalog without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    try:
        block = text.split("---", 2)[1]
    except IndexError as exc:
        raise ValueError(f"{path}: unterminated YAML frontmatter") from exc
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if line.startswith(("name:", "description:", "compatibility:")):
            key, _, value = line.partition(":")
            fields[key] = value.strip()
    return fields


def validate_skill(skill_dir: Path) -> str:
    skill_path = skill_dir / "SKILL.md"
    fields = read_frontmatter(skill_path)
    name = fields.get("name", "")
    description = fields.get("description", "")

    if not NAME_PATTERN.fullmatch(name):
        raise ValueError(f"{skill_path}: invalid name {name!r}")
    if name != skill_dir.name:
        raise ValueError(f"{skill_path}: name must match parent directory")
    if not description:
        raise ValueError(f"{skill_path}: missing description")
    if len(description) > 1024:
        raise ValueError(f"{skill_path}: description exceeds 1024 characters")
    return name


def main() -> int:
    errors: list[str] = []
    names: list[str] = []

    for skill_dir in sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir()):
        try:
            names.append(validate_skill(skill_dir))
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    if len(names) != len(set(names)):
        errors.append("duplicate skill names")

    try:
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read manifest: {exc}")
    else:
        entries = {entry["name"]: entry for entry in marketplace.get("plugins", [])}
        if plugin.get("name") not in entries:
            errors.append("plugin name is not listed in marketplace.json")
        elif entries[plugin["name"]].get("source") != "./":
            errors.append("marketplace plugin source must be ./")
        if mcp.get("mcpServers", {}).get("abi") != {
            "command": "abi-mcp",
            "args": ["--profile", "safe"],
        }:
            errors.append("unexpected ABI MCP configuration")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(names)} skills: {', '.join(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
