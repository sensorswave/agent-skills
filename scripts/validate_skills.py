#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MANIFEST_PATH = SKILLS_DIR / "manifest.json"

# 项目门禁（先 list_projects 让用户选 project_id）只对外部 Agent 成立；Wagent 产品内
# 会话已绑定项目，运行时会把标记块整体替换掉。所以门禁正文必须包在标记块里，
# 且 list_projects 不能出现在标记块之外，否则 Wagent 侧会出现自相矛盾的指令。
GATE_START = "<!-- wave:project-gate -->"
GATE_END = "<!-- /wave:project-gate -->"
GATE_BLOCK_RE = re.compile(re.escape(GATE_START) + r".*?" + re.escape(GATE_END), re.S)

# 门禁正文里这些措辞同样只对外部 Agent 成立。它们不带 list_projects 字样，所以单靠上面
# 的检查抓不到；出现在标记块之外时 Wagent 侧一样会收到"等用户选项目"的矛盾指令。
# 与 apps/web/wagent/service/skill/registry_test.go 的 externalProjectGatePhrases 保持一致。
GATE_ONLY_PHRASES = (
    "等待用户回复数字",
    "静默挑选项目",
    "`project_id | name`",
    "Wait for the user to reply with a numeric",
    "silently pick a project",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def expect_file(path: Path, context: str) -> None:
    if not path.is_file():
        fail(f"{context} 缺少文件: {path.relative_to(ROOT)}")


def expect_dir(path: Path, context: str) -> None:
    if not path.is_dir():
        fail(f"{context} 缺少目录: {path.relative_to(ROOT)}")


def gate_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    starts = text.count(GATE_START)
    ends = text.count(GATE_END)
    blocks = GATE_BLOCK_RE.findall(text)
    if starts != ends or len(blocks) != starts:
        fail(f"{path.relative_to(ROOT)} 的项目门禁标记不配对: {starts} 个开始、{ends} 个结束")
    return blocks


def check_project_gate(skill_dir: Path, item: dict) -> None:
    name = item["name"]
    blocks = gate_blocks(skill_dir / item["skillFile"])
    if item.get("projectScoped"):
        if len(blocks) != 1:
            fail(f"{name} 是项目级 skill（projectScoped），SKILL.md 必须恰好包含一个 {GATE_START} 标记块，当前 {len(blocks)} 个")
        if "list_projects" not in blocks[0]:
            fail(f"{name} 的项目门禁标记块必须说明如何用 list_projects 选择 project_id")
    elif blocks:
        fail(f"{name} 不是项目级 skill，SKILL.md 不应包含项目门禁标记块")


def check_list_projects_only_inside_gate() -> None:
    for path in sorted(SKILLS_DIR.rglob("*.md")):
        gate_blocks(path)
        outside = GATE_BLOCK_RE.sub("", path.read_text(encoding="utf-8"))
        if "list_projects" in outside:
            fail(
                f"{path.relative_to(ROOT)} 在项目门禁标记块之外提到了 list_projects；"
                f"选择项目的说明只能写在 {GATE_START} … {GATE_END} 之间，其他地方请写「先通过项目门禁」"
            )
        for phrase in GATE_ONLY_PHRASES:
            if phrase in outside:
                fail(
                    f"{path.relative_to(ROOT)} 在项目门禁标记块之外出现了门禁措辞「{phrase}」；"
                    f"请把它移进 {GATE_START} … {GATE_END} 之间，或改写为「先通过项目门禁」"
                )


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
        if not isinstance(item.get("projectScoped"), bool):
            fail(f"skill 缺少布尔字段 projectScoped: {item['name']}")

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

        check_project_gate(skill_dir, item)

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name not in seen_dirs:
            fail(f"skills 目录存在未注册条目: {skill_dir.relative_to(ROOT)}")

    check_list_projects_only_inside_gate()

    print("OK: manifest、skills 目录与项目门禁标记校验通过")


if __name__ == "__main__":
    main()
