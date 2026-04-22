# Sensors Wave Agent Skills

[![GitHub](https://img.shields.io/github/license/sensorswave/agent-skills)](https://github.com/sensorswave/agent-skills)

Sensors Wave 平台的 AI Agent Skills 集合，提供埋点方案设计与数据分析能力。兼容 **Cursor**、**Claude Code** 和 **Codex**。

## 公开 Skills

| Skill | 说明 |
|-------|------|
| [wave](skills/wave/) | 总入口路由：自动分发到埋点规划、Tracking Plan 执行、SDK 接入或数据分析 |
| [wave-tracking-plan](skills/wave-tracking-plan/) | 埋点方案规划：代码/需求分析、事件模型、用户标识方案、Tracking Plan draft |
| [wave-tracking](skills/wave-tracking/) | Tracking Plan 执行与验证：写入、发布、Dashboard 启动版、质检 |
| [wave-sdk-integration](skills/wave-sdk-integration/) | SDK 与 Pipeline 接入：`endpoint` / `source_token`、identify / reset、初始化与埋点代码接入 |
| [wave-analytics](skills/wave-analytics/) | 数据分析：事件分析、漏斗、留存、用户列表、行为序列、自定义 SQL，基于 Wave MCP 工具 |

## 内部 Shared 包

| Package | 说明 |
|---------|------|
| [wave-tracking-shared](skills/wave-tracking-shared/) | 内部共享 prompts / policies / references：供 `wave-tracking-plan`、`wave-tracking`、`wave-sdk-integration` 按需读取 |

默认安装会包含 [wave](skills/wave/) 这个总入口，以及 `wave-tracking-shared` 内部共享包。根目录 [SKILL.md](SKILL.md) 保留为仓库内兼容入口。

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

## 校验

修改 skill 结构、manifest 或共享文件后，建议运行：

```bash
python3 scripts/validate_skills.py
```

### 手动安装

也可以手动创建符号链接：

```bash
# Cursor（用户级）
ln -s /path/to/agent-skills/skills/wave ~/.cursor/skills/wave
ln -s /path/to/agent-skills/skills/wave-tracking-plan ~/.cursor/skills/wave-tracking-plan
ln -s /path/to/agent-skills/skills/wave-tracking ~/.cursor/skills/wave-tracking
ln -s /path/to/agent-skills/skills/wave-sdk-integration ~/.cursor/skills/wave-sdk-integration
ln -s /path/to/agent-skills/skills/wave-tracking-shared ~/.cursor/skills/wave-tracking-shared
ln -s /path/to/agent-skills/skills/wave-analytics ~/.cursor/skills/wave-analytics

# Claude Code（用户级）
ln -s /path/to/agent-skills/skills/wave ~/.claude/skills/wave
ln -s /path/to/agent-skills/skills/wave-tracking-plan ~/.claude/skills/wave-tracking-plan
ln -s /path/to/agent-skills/skills/wave-tracking ~/.claude/skills/wave-tracking
ln -s /path/to/agent-skills/skills/wave-sdk-integration ~/.claude/skills/wave-sdk-integration
ln -s /path/to/agent-skills/skills/wave-tracking-shared ~/.claude/skills/wave-tracking-shared
ln -s /path/to/agent-skills/skills/wave-analytics ~/.claude/skills/wave-analytics

# Codex（用户级）
ln -s /path/to/agent-skills/skills/wave ~/.codex/skills/wave
ln -s /path/to/agent-skills/skills/wave-tracking-plan ~/.codex/skills/wave-tracking-plan
ln -s /path/to/agent-skills/skills/wave-tracking ~/.codex/skills/wave-tracking
ln -s /path/to/agent-skills/skills/wave-sdk-integration ~/.codex/skills/wave-sdk-integration
ln -s /path/to/agent-skills/skills/wave-tracking-shared ~/.codex/skills/wave-tracking-shared
ln -s /path/to/agent-skills/skills/wave-analytics ~/.codex/skills/wave-analytics
```

> 将 `/path/to/agent-skills` 替换为本仓库的实际绝对路径。

### AI 一键安装

复制以下提示词发给任意 AI 助手（Cursor / Claude Code / Codex），即可自动完成安装：

> 克隆 https://github.com/sensorswave/agent-skills 仓库，然后读取其 docs/README.install.md，按照指引完成安装。

详细安装文档见 [docs/README.install.md](docs/README.install.md)。

## 前置依赖

所有 Skill 均依赖 **Wave MCP Server** 提供的工具集。确保目标项目或 IDE 已配置 Wave MCP 连接。

## License

本项目采用 [MIT License](LICENSE)。

## 目录结构

```
agent-skills/
├── SKILL.md                    # 仓库根目录兼容入口
├── README.md
├── install.sh                  # 安装脚本
├── .gitignore
├── agents/
│   └── openai.yaml             # 仓库根目录兼容入口配置
├── docs/
│   └── README.install.md       # 详细安装指南
└── skills/
    ├── manifest.json            # Skill 注册清单
    ├── wave/
    │   ├── SKILL.md
    │   └── agents/
    │       └── openai.yaml
    ├── wave-tracking-plan/
    │   ├── SKILL.md
    │   ├── playbooks/
    │   └── agents/
    │       └── openai.yaml
    ├── wave-tracking/
    │   ├── SKILL.md
    │   └── agents/
    │       └── openai.yaml
    ├── wave-sdk-integration/
    │   ├── SKILL.md
    │   └── agents/
    │       └── openai.yaml
    ├── wave-tracking-shared/
    │   ├── SKILL.md
    │   ├── policies/
    │   ├── prompts/
    │   ├── references/
    │   └── agents/
    │       └── openai.yaml
    └── wave-analytics/
        ├── SKILL.md
        └── agents/
            └── openai.yaml
```
