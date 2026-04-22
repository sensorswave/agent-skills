# Agent Install Guide

将 Wave Agent Skills 安装到本地 AI 代理环境的指南。支持 Cursor、Claude Code 和 Codex。

## 快速安装

仓库已经补好 GitHub `npx` 入口。推荐直接从 GitHub 仓库安装。Node CLI 默认走复制安装，适合 macOS / Linux / Windows，也不会把目标 skills 目录链接到 npm 缓存：

```bash
npx github:sensorswave/agent-skills --all
npx github:sensorswave/agent-skills --cursor
npx github:sensorswave/agent-skills --codex
npx github:sensorswave/agent-skills --project
npx github:sensorswave/agent-skills --check --codex
npx github:sensorswave/agent-skills --uninstall --all
```

如果你是从 GitHub 克隆仓库做本地开发，或者希望目标目录保持符号链接随 `git pull` 自动更新，再使用仓库内安装脚本：

```bash
git clone https://github.com/sensorswave/agent-skills.git
cd agent-skills
./install.sh --all
```

无论是 `npx` CLI 还是仓库内安装脚本，都会同时安装埋点规划、Tracking Plan 执行、SDK 接入与共享资料包。
同时也会安装 `wave` 这个伞型路由入口，方便用户直接从总入口触发。
这是必需的，因为这些 tracking 相关 skill 会跨目录读取 `wave-tracking-shared` 中的共享资料。
`wave-tracking-shared` 在 manifest 中作为 internal dependency 存在，由安装器自动随依赖一起安装，而不是作为独立公开入口让用户单独选择。

## 安装目标

安装器根据平台参数自动解析目标目录：

| 参数 | 目标目录 | 说明 |
|------|---------|------|
| `--cursor` | `~/.cursor/skills/` | Cursor 用户级 |
| `--claude` | `~/.claude/skills/` | Claude Code 用户级 |
| `--codex` | `~/.codex/skills/` | Codex 用户级 |
| `--all` | 以上全部 | 安装到所有平台 |
| `--project` | `.cursor/skills/`，以及已存在的 `.claude/.codex` 项目目录 | 当前项目级 |

如果你的 agent 运行时使用自定义 skills 目录，推荐直接指定 `--target`：

```bash
npx github:sensorswave/agent-skills --target /your/agent/skills
```

如果你明确要保留符号链接，再手动创建链接，或在本地克隆仓库后使用 `./install.sh`。

## 安装的包

默认安装以下 6 个包，其中 5 个公开 skill、1 个内部 shared 包：

| Skill | 功能 |
|-------|------|
| `wave` | 总入口路由：自动分发到埋点规划、接入、执行或分析 |
| `wave-tracking-plan` | 代码/需求分析，输出埋点方案与 plan draft |
| `wave-tracking` | Tracking Plan 写入、发布、看板与质检 |
| `wave-sdk-integration` | SDK、Pipeline、identify、埋点代码接入 |
| `wave-analytics` | 数据分析：事件、漏斗、留存、用户列表、SQL |
| `wave-tracking-shared` | 内部共享 prompts / policies / references（自动随 tracking 相关 skill 一起安装） |

说明：本地 shared 负责执行层规则；官网 docs 与对应 `llm.txt` 负责知识层长文内容。

## 常用操作

安装到所有平台：

```bash
npx github:sensorswave/agent-skills --all
```

仅安装到 Cursor：

```bash
npx github:sensorswave/agent-skills --cursor
```

安装到当前项目（项目级）：

```bash
npx github:sensorswave/agent-skills --project
```

说明：`--project` 默认会安装到当前仓库的 `.cursor/skills/`，并在检测到已有 `.claude/`、`.codex/` 目录时同步安装到对应项目级目录。

查看帮助：

```bash
npx github:sensorswave/agent-skills --help
```

卸载：

```bash
npx github:sensorswave/agent-skills --uninstall --all
```

校验某个默认平台目录是否安装完整：

```bash
npx github:sensorswave/agent-skills --check --codex
npx github:sensorswave/agent-skills --check --cursor
```

校验 manifest 与目录结构：

```bash
python3 scripts/validate_skills.py
```

校验某个实际安装目录是否完整包含 internal dependency：

```bash
python3 scripts/check_installed_skills.py ~/.codex/skills
python3 scripts/check_installed_skills.py ~/.cursor/skills
python3 scripts/check_installed_skills.py ./.cursor/skills
```

## 更新

如果本仓库已克隆：

```bash
cd agent-skills
git pull
```

符号链接方式安装无需额外操作，`git pull` 后 skill 内容自动更新。
GitHub `npx` 复制安装方式则需要重新执行一次安装命令来更新目标目录。

## 验证

安装完成后，目标目录应包含：

```
~/.cursor/skills/          # 或 ~/.claude/skills/ 或 ~/.codex/skills/
├── wave/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── wave-tracking-plan/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── wave-tracking/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── wave-sdk-integration/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── wave-tracking-shared/
│   ├── SKILL.md
│   ├── policies/
│   ├── prompts/
│   └── agents/openai.yaml
└── wave-analytics/
    ├── SKILL.md
    └── agents/openai.yaml
```

验证目录是否存在：

```bash
ls -la ~/.cursor/skills/wave
ls -la ~/.cursor/skills/wave-tracking-plan
ls -la ~/.cursor/skills/wave-tracking
ls -la ~/.cursor/skills/wave-sdk-integration
ls -la ~/.cursor/skills/wave-tracking-shared
ls -la ~/.cursor/skills/wave-analytics
```

如果你是手动安装或复制目录，建议再补一层依赖自检：

```bash
python3 scripts/check_installed_skills.py ~/.cursor/skills
```

这会按 manifest 解析公开 skill 与 internal dependency，检查是否漏掉 `wave-tracking-shared`、`SKILL.md` 或 `agents/openai.yaml`。

## 前置依赖

所有 Skill 依赖 **Wave MCP Server** 提供的工具集。安装 skill 后，还需要在目标 IDE 中配置 Wave MCP 连接才能正常使用。
