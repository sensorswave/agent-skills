#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"
MANIFEST_PATH="$SKILLS_DIR/manifest.json"
SKILLS=()

find_python() {
  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
    return
  fi
  if command -v python >/dev/null 2>&1; then
    echo "python"
    return
  fi
  echo ""
}

load_skills_from_manifest() {
  local python_bin
  local skill

  python_bin="$(find_python)"
  if [ -z "$python_bin" ]; then
    echo "未找到 python3 或 python，无法解析 manifest: $MANIFEST_PATH" >&2
    exit 1
  fi

  while IFS= read -r skill; do
    [ -n "$skill" ] || continue
    SKILLS+=("$skill")
  done < <("$python_bin" - "$MANIFEST_PATH" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)

skills = data.get("skills", [])
skills_by_name = {item["name"]: item for item in skills}
resolved = []
visited = set()
visiting = set()


def visit(name):
    if name in visited:
        return
    if name in visiting:
        raise SystemExit(f"manifest 依赖存在循环: {name}")

    item = skills_by_name.get(name)
    if not item:
        raise SystemExit(f"manifest 依赖未声明: {name}")

    visiting.add(name)
    for dep in item.get("dependsOn", []):
        visit(dep)
    visiting.remove(name)

    visited.add(name)
    resolved.append(item["dir"])


for item in skills:
    if item.get("install", True):
        visit(item["name"])

for directory in resolved:
    print(directory)
PY
)

  if [ "${#SKILLS[@]}" -eq 0 ]; then
    echo "manifest 中未声明可安装的 skills: $MANIFEST_PATH" >&2
    exit 1
  fi

  for skill in "${SKILLS[@]}"; do
    if [ ! -f "$SKILLS_DIR/$skill/SKILL.md" ] || [ ! -f "$SKILLS_DIR/$skill/agents/openai.yaml" ]; then
      echo "skill 目录缺少必需文件: $SKILLS_DIR/$skill" >&2
      exit 1
    fi
  done
}

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

将 Wave Agent Skills 安装（符号链接）到指定平台的 skills 目录。

Options:
  --cursor          安装到 Cursor（用户级 ~/.cursor/skills/）
  --claude          安装到 Claude Code（用户级 ~/.claude/skills/）
  --codex           安装到 Codex（用户级 ~/.codex/skills/）
  --project         安装到当前项目（默认 .cursor/skills/，如存在则追加 .claude/.codex）
  --all             安装到所有已安装的平台（用户级）
  --uninstall       卸载已安装的符号链接
  -h, --help        显示帮助

Examples:
  $(basename "$0") --cursor              # 安装到 Cursor
  $(basename "$0") --claude --codex      # 安装到 Claude Code + Codex
  $(basename "$0") --all                 # 安装到所有平台
  $(basename "$0") --project             # 安装到当前项目
  $(basename "$0") --uninstall --cursor  # 从 Cursor 卸载
EOF
}

link_skills() {
  local target_dir="$1"
  local platform="$2"
  mkdir -p "$target_dir"
  for skill in "${SKILLS[@]}"; do
    local src="$SKILLS_DIR/$skill"
    local dst="$target_dir/$skill"
    if [ -L "$dst" ]; then
      echo "  ⟳ $skill (已存在，跳过)"
    elif [ -e "$dst" ]; then
      echo "  ✗ $skill (目标路径已被占用: $dst)"
    else
      ln -s "$src" "$dst"
      echo "  ✓ $skill"
    fi
  done
  echo "  → $platform 安装完成: $target_dir"
}

unlink_skills() {
  local target_dir="$1"
  local platform="$2"
  for skill in "${SKILLS[@]}"; do
    local dst="$target_dir/$skill"
    if [ -L "$dst" ]; then
      rm "$dst"
      echo "  ✓ 已移除 $skill"
    fi
  done
  echo "  → $platform 卸载完成"
}

if [ $# -eq 0 ]; then
  usage
  exit 0
fi

load_skills_from_manifest

TARGETS=()
UNINSTALL=false
PROJECT=false

while [ $# -gt 0 ]; do
  case "$1" in
    --cursor)  TARGETS+=("cursor");;
    --claude)  TARGETS+=("claude");;
    --codex)   TARGETS+=("codex");;
    --all)     TARGETS+=("cursor" "claude" "codex");;
    --project) PROJECT=true;;
    --uninstall) UNINSTALL=true;;
    -h|--help) usage; exit 0;;
    *) echo "未知选项: $1"; usage; exit 1;;
  esac
  shift
done

if $PROJECT; then
  echo "安装到当前项目..."
  for platform in cursor claude codex; do
    dot_dir=".${platform}"
    if [ -d "$dot_dir" ] || [ "$platform" = "cursor" ]; then
      if $UNINSTALL; then
        unlink_skills "$dot_dir/skills" "$platform (project)"
      else
        link_skills "$dot_dir/skills" "$platform (project)"
      fi
    fi
  done
fi

if [ "${#TARGETS[@]}" -gt 0 ]; then
  for target in "${TARGETS[@]}"; do
    home_dir="$HOME/.${target}/skills"
    echo ""
    if $UNINSTALL; then
      echo "从 $target 卸载..."
      unlink_skills "$home_dir" "$target"
    else
      echo "安装到 $target..."
      link_skills "$home_dir" "$target"
    fi
  done
fi
