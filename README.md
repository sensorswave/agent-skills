# Sensors Wave Agent Skills

Sensors Wave 平台的 AI Agent Skills 集合，提供埋点方案设计与数据分析能力。兼容 **Cursor**、**Claude Code** 和 **Codex**。

## Skills 一览

| Skill | 说明 |
|-------|------|
| [wave-tracking](skills/wave-tracking/) | 埋点方案设计：事件命名规范、服务端/客户端选型、交互式 MCP 工具流程（项目选择→Pipeline→Tracking Plan→SDK 代码→质检→Dashboard） |
| [wave-analytics](skills/wave-analytics/) | 数据分析：事件分析、漏斗、留存、用户列表、行为序列、自定义 SQL，基于 Wave MCP 工具 |

## 一键安装

```bash
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

**安装到所有平台：**

> 读取 /Users/unclezs/coder/sensorsol/agent-skills/README.md ，按照「AI 自动安装指引」完成安装。

---

<!-- AI-INSTALL-START -->
## AI 自动安装指引

> 以下内容供 AI 助手读取并自动执行，用户无需关心。

检测当前运行环境并创建符号链接：

1. 确定本仓库的绝对路径（即本 README.md 所在目录）
2. 检测当前 AI 平台：
   - Cursor → 目标目录 `~/.cursor/skills/`
   - Claude Code → 目标目录 `~/.claude/skills/`
   - Codex → 目标目录 `~/.codex/skills/`
3. 对以下每个 skill 创建符号链接：
   - `wave-tracking`
   - `wave-analytics`
4. 执行命令（以 Cursor 为例）：
   ```bash
   mkdir -p ~/.cursor/skills
   ln -sf <本仓库路径>/skills/wave-tracking ~/.cursor/skills/wave-tracking
   ln -sf <本仓库路径>/skills/wave-analytics ~/.cursor/skills/wave-analytics
   ```
5. 安装完成后告知用户结果。
<!-- AI-INSTALL-END -->

## 前置依赖

两个 Skill 均依赖 **Wave MCP Server** 提供的工具集。确保目标项目或 IDE 已配置 Wave MCP 连接。

## 目录结构

```
agent-skills/
├── README.md
├── .gitignore
└── skills/
    ├── wave-tracking/
    │   ├── SKILL.md        # 埋点规范与 MCP 流程
    │   └── prompts.md      # 交互式提示词模板
    └── wave-analytics/
        └── SKILL.md        # 数据分析工作流
```
