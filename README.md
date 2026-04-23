# Sensors Wave Agent Skills

[![GitHub](https://img.shields.io/github/license/sensorswave/agent-skills)](https://github.com/sensorswave/agent-skills)

这是给 **Cursor**、**Claude Code**、**Codex** 用的一组 Sensors Wave Skills。

装好以后，你可以直接让 AI：

- 根据代码、PRD、页面流程设计埋点方案
- 生成 SDK 接入思路和初始化代码
- 补 identify / reset / 用户标识方案
- 按已发布 Tracking Plan 做埋点质检
- 做事件分析、漏斗、留存和 SQL 查询

## 快速安装

推荐直接在你的 IDE 或项目环境里运行：

```bash
# 安装到当前项目
npx github:sensorswave/agent-skills --project

# 或安装到本机用户目录
npx github:sensorswave/agent-skills --cursor
npx github:sensorswave/agent-skills --claude
npx github:sensorswave/agent-skills --codex
```

如果想一次装到全部平台：

```bash
npx github:sensorswave/agent-skills --all
```

安装完成后，可用下面命令做一次检查：

```bash
npx github:sensorswave/agent-skills --check --codex
```

默认是复制安装，适合 macOS / Linux / Windows。

## 怎么开始用

安装完成后，直接在 AI 工具里描述业务目标就行，例如：

- “根据当前项目代码，帮我设计注册到付费的埋点方案”
- “我现在要接 JavaScript SDK，给我初始化代码和 identify 方案”
- “帮我分析最近 30 天新用户的 7 日留存，并解释原因”

你通常不需要手动挑具体 skill，`wave` 会按当前阶段自动路由到埋点规划、Tracking Plan 执行、质检、SDK 接入或数据分析流程。

## 前置条件

使用前请先完成 **Wave MCP Server** 配置，否则 AI 只能看到技能说明，不能调用 Wave 工具能力。

## 详细说明

- 详细安装、更新、手动安装见 [docs/README.install.md](docs/README.install.md)
- 仓库兼容入口见 [SKILL.md](SKILL.md)

## License

本项目采用 [MIT License](LICENSE)。
