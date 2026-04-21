# Agent Install Guide

将 Wave Agent Skills 安装到本地 AI 代理环境的指南。支持 Cursor、Claude Code 和 Codex。

## 快速安装

从 GitHub 克隆并执行安装脚本：

```bash
git clone https://github.com/sensorswave/agent-skills.git
cd agent-skills
./install.sh --all
```

安装脚本会同时安装埋点设计、Tracking Plan 执行、SDK 接入与共享 references。
这是必需的，因为这些 tracking 相关 skill 会跨目录读取 `wave-tracking-common` 中的共享资料。

## 安装目标

脚本根据平台参数自动解析目标目录：

| 参数 | 目标目录 | 说明 |
|------|---------|------|
| `--cursor` | `~/.cursor/skills/` | Cursor 用户级 |
| `--claude` | `~/.claude/skills/` | Claude Code 用户级 |
| `--codex` | `~/.codex/skills/` | Codex 用户级 |
| `--all` | 以上全部 | 安装到所有平台 |
| `--project` | `.cursor/skills/` 等 | 当前项目级 |

如果你的 agent 运行时使用自定义 skills 目录，可手动创建符号链接：

```bash
ln -sf /path/to/agent-skills/skills/wave-tracking-design /your/agent/skills/wave-tracking-design
ln -sf /path/to/agent-skills/skills/wave-tracking /your/agent/skills/wave-tracking
ln -sf /path/to/agent-skills/skills/wave-sdk-integration /your/agent/skills/wave-sdk-integration
ln -sf /path/to/agent-skills/skills/wave-tracking-common /your/agent/skills/wave-tracking-common
ln -sf /path/to/agent-skills/skills/wave-analytics /your/agent/skills/wave-analytics
```

## 安装的 Skills

默认安装以下五个 skill：

| Skill | 功能 |
|-------|------|
| `wave-tracking-design` | 代码/需求分析，输出埋点方案与 plan draft |
| `wave-tracking` | Tracking Plan 写入、发布、看板与质检 |
| `wave-sdk-integration` | SDK、Pipeline、identify、埋点代码接入 |
| `wave-tracking-common` | 共享 references 与统一提示词（内部支撑） |
| `wave-analytics` | 数据分析：事件、漏斗、留存、用户列表、SQL |

## 常用操作

安装到所有平台：

```bash
./install.sh --all
```

仅安装到 Cursor：

```bash
./install.sh --cursor
```

安装到当前项目（项目级）：

```bash
./install.sh --project
```

查看帮助：

```bash
./install.sh --help
```

卸载：

```bash
./install.sh --uninstall --all
```

## 更新

如果本仓库已克隆：

```bash
cd agent-skills
git pull
```

符号链接方式安装无需额外操作，`git pull` 后 skill 内容自动更新。

## 验证

安装完成后，目标目录应包含：

```
~/.cursor/skills/          # 或 ~/.claude/skills/ 或 ~/.codex/skills/
├── wave-tracking-design/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── wave-tracking/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── wave-sdk-integration/
│   ├── SKILL.md
│   └── agents/openai.yaml
├── wave-tracking-common/
│   ├── SKILL.md
│   ├── prompts.md
│   └── agents/openai.yaml
└── wave-analytics/
    ├── SKILL.md
    └── agents/openai.yaml
```

验证符号链接是否正确：

```bash
ls -la ~/.cursor/skills/wave-tracking-design
ls -la ~/.cursor/skills/wave-tracking
ls -la ~/.cursor/skills/wave-sdk-integration
ls -la ~/.cursor/skills/wave-tracking-common
ls -la ~/.cursor/skills/wave-analytics
```

## 前置依赖

所有 Skill 依赖 **Wave MCP Server** 提供的工具集。安装 skill 后，还需要在目标 IDE 中配置 Wave MCP 连接才能正常使用。
