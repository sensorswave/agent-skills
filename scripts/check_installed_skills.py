#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MANIFEST_PATH = SKILLS_DIR / "manifest.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_manifest() -> list[dict]:
    if not MANIFEST_PATH.is_file():
        fail(f"manifest 缺失: {MANIFEST_PATH}")

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        fail("manifest.skills 不能为空")
    return skills


def resolve_install_set(skills: list[dict]) -> list[dict]:
    by_name = {item["name"]: item for item in skills}
    resolved: list[dict] = []
    visited: set[str] = set()
    visiting: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in visiting:
            fail(f"manifest 依赖存在循环: {name}")

        item = by_name.get(name)
        if item is None:
            fail(f"manifest 依赖未声明: {name}")

        visiting.add(name)
        for dep in item.get("dependsOn", []):
            visit(dep)
        visiting.remove(name)

        visited.add(name)
        resolved.append(item)

    for item in skills:
        if item.get("install", True):
            visit(item["name"])

    return resolved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="校验目标 skills 目录是否已安装完整的 Wave Skill 集合（含内部依赖）。"
    )
    parser.add_argument(
        "target_dir",
        help="目标 skills 目录，例如 ~/.codex/skills 或 .cursor/skills",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_dir = Path(args.target_dir).expanduser().resolve()

    if not target_dir.exists():
        fail(f"目标目录不存在: {target_dir}")
    if not target_dir.is_dir():
        fail(f"目标路径不是目录: {target_dir}")

    install_set = resolve_install_set(load_manifest())
    missing: list[str] = []

    for item in install_set:
        skill_dir = target_dir / item["dir"]
        if not skill_dir.is_dir():
            missing.append(f"{item['dir']}: 缺少目录 {skill_dir}")
            continue

        skill_file = skill_dir / item["skillFile"]
        if not skill_file.is_file():
            missing.append(f"{item['dir']}: 缺少文件 {skill_file}")

        agent_file = skill_dir / "agents" / "openai.yaml"
        if not agent_file.is_file():
            missing.append(f"{item['dir']}: 缺少文件 {agent_file}")

    if missing:
        print(f"目标目录校验失败: {target_dir}", file=sys.stderr)
        for line in missing:
            print(f"- {line}", file=sys.stderr)
        print(
            "\n建议：使用 ./install.sh 重新安装，或手动补齐缺失 skill 与其 internal dependency。",
            file=sys.stderr,
        )
        raise SystemExit(1)

    installed = ", ".join(item["dir"] for item in install_set)
    print(f"OK: 目标目录安装完整: {target_dir}")
    print(f"已校验技能集: {installed}")


if __name__ == "__main__":
    main()
