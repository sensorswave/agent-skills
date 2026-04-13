# Sensors Wave Agent Skills

[![GitHub](https://img.shields.io/github/license/sensorswave/agent-skills)](https://github.com/sensorswave/agent-skills)

Sensors Wave 平台的 AI Agent Skills 集合，提供埋点方案设计与数据分析能力。兼容 **Cursor**、**Claude Code** 和 **Codex**。

## Skills 一览

| Skill | 说明 |
|-------|------|
| [wave-tracking](skills/wave-tracking/) | 埋点方案设计：事件命名规范、服务端/客户端选型、交互式 MCP 工具流程（项目选择→Pipeline→Tracking Plan→SDK 代码→质检→Dashboard） |
| [wave-analytics](skills/wave-analytics/) | 数据分析：事件分析、漏斗、留存、用户列表、行为序列、自定义 SQL，基于 Wave MCP 工具 |

根目录 [SKILL.md](SKILL.md) 为伞型路由入口，AI 会根据用户意图自动分发到对应子 Skill。

## 一键安装

```bash
# 克隆仓库
git clone https://github.com/sensorswave/agent-skills.git
cd agent-skills

# 安装到所有平台（Cursor + Claude Code + Codex）
./install.sh --all

# 安装到指定平台
./install.sh --cursor
./install.sh --claude
./install.sh --codex

# 安装到当前项目（项目级）
./install.sh --project

# 卸载
./install.sh --uninstall --all
```

### 手动安装

也可以手动创建符号链接：

```bash
# Cursor（用户级）
ln -s /path/to/agent-skills/skills/wave-tracking ~/.cursor/skills/wave-tracking
ln -s /path/to/agent-skills/skills/wave-analytics ~/.cursor/skills/wave-analytics

# Claude Code（用户级）
ln -s /path/to/agent-skills/skills/wave-tracking ~/.claude/skills/wave-tracking
ln -s /path/to/agent-skills/skills/wave-analytics ~/.claude/skills/wave-analytics

# Codex（用户级）
ln -s /path/to/agent-skills/skills/wave-tracking ~/.codex/skills/wave-tracking
ln -s /path/to/agent-skills/skills/wave-analytics ~/.codex/skills/wave-analytics
```

> 将 `/path/to/agent-skills` 替换为本仓库的实际绝对路径。

### AI 一键安装

复制以下提示词发给任意 AI 助手（Cursor / Claude Code / Codex），即可自动完成安装：

> 克隆 https://github.com/sensorswave/agent-skills 仓库，然后读取其 docs/README.install.md，按照指引完成安装。

详细安装文档见 [docs/README.install.md](docs/README.install.md)。

## 前置依赖

所有 Skill 均依赖 **Wave MCP Server** 提供的工具集。确保目标项目或 IDE 已配置 Wave MCP 连接。

## 目录结构

```
agent-skills/
├── SKILL.md                    # 伞型路由入口
├── README.md
├── install.sh                  # 安装脚本
├── .gitignore
├── agents/
│   └── openai.yaml             # Codex agent 配置（伞型）
├── docs/
│   └── README.install.md       # 详细安装指南
└── skills/
    ├── manifest.json            # Skill 注册清单
    ├── wave-tracking/
    │   ├── SKILL.md
    │   ├── prompts.md
    │   └── agents/
    │       └── openai.yaml
    └── wave-analytics/
        ├── SKILL.md
        └── agents/
            └── openai.yaml
```
