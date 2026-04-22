#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MANIFEST_PATH = SKILLS_DIR / "manifest.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def expect_file(path: Path, context: str) -> None:
    if not path.is_file():
        fail(f"{context} 缺少文件: {path.relative_to(ROOT)}")


def expect_dir(path: Path, context: str) -> None:
    if not path.is_dir():
        fail(f"{context} 缺少目录: {path.relative_to(ROOT)}")


def main() -> None:
    expect_file(MANIFEST_PATH, "manifest")

    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        fail("manifest.skills 不能为空")

    seen_names: set[str] = set()
    seen_dirs: set[str] = set()

    for item in skills:
        for field in ("name", "dir", "skillFile", "description", "type", "visibility"):
            if not item.get(field):
                fail(f"skill 缺少字段 {field}: {item}")

        name = item["name"]
        directory = item["dir"]
        if name in seen_names:
            fail(f"manifest 中存在重复 skill name: {name}")
        if directory in seen_dirs:
            fail(f"manifest 中存在重复 skill dir: {directory}")
        seen_names.add(name)
        seen_dirs.add(directory)

        skill_dir = SKILLS_DIR / directory
        expect_dir(skill_dir, name)
        expect_file(skill_dir / item["skillFile"], name)
        expect_file(skill_dir / "agents" / "openai.yaml", name)

        for ref in item.get("references", []):
            ref_path = skill_dir / ref
            if not ref_path.exists():
                fail(f"{name} 引用缺失: {ref_path.relative_to(ROOT)}")

        for dep in item.get("dependsOn", []):
            if dep not in {skill["name"] for skill in skills}:
                fail(f"{name} 依赖未声明: {dep}")

        visibility = item["visibility"]
        if visibility not in {"public", "internal"}:
            fail(f"{name} visibility 非法: {visibility}")

        skill_type = item["type"]
        if skill_type not in {"router", "workflow", "shared"}:
            fail(f"{name} type 非法: {skill_type}")

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name not in seen_dirs:
            fail(f"skills 目录存在未注册条目: {skill_dir.relative_to(ROOT)}")

    print("OK: manifest 与 skills 目录校验通过")


if __name__ == "__main__":
    main()
