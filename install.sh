#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"
SKILLS=(wave-tracking wave-analytics)

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

将 Wave Agent Skills 安装（符号链接）到指定平台的 skills 目录。

Options:
  --cursor          安装到 Cursor（用户级 ~/.cursor/skills/）
  --claude          安装到 Claude Code（用户级 ~/.claude/skills/）
  --codex           安装到 Codex（用户级 ~/.codex/skills/）
  --project         安装到当前项目（自动检测 .cursor/.claude/.codex 目录）
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
