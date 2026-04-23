# Sensors Wave Skills

把 Sensors Wave 的埋点规划、Tracking Plan 执行、埋点质检、SDK 接入和数据分析流程，整理成一组可直接安装到 **Cursor**、**Claude Code**、**Codex** 的 Skills。

装好之后，你可以直接让工具围绕 Sensors Wave 项目工作，而不是每次都从零解释流程、命名规范和执行顺序。

## 适合什么场景

- 根据代码、PRD、页面流程整理埋点方案和事件表
- 在项目里创建或更新 Pipeline、Tracking Plan、Dashboard
- 做埋点验收、计划对照和上线质检
- 生成 JavaScript、Android、iOS、服务端等 SDK 接入思路
- 做事件分析、漏斗分析、留存分析和 SQL 查询

## 推荐安装

这是一组会互相切换的多 skill workflow，推荐一次安装全部公开 skills：

```bash
npx skills add sensorswave/agent-skills --skill '*'
```

如果你想明确指定目标工具：

```bash
# Cursor
npx skills add sensorswave/agent-skills --skill '*' --agent cursor

# Claude Code
npx skills add sensorswave/agent-skills --skill '*' --agent claude-code

# Codex
npx skills add sensorswave/agent-skills --skill '*' --agent codex
```

如果你只想装某一个 skill，也可以单独指定：

```bash
npx skills add sensorswave/agent-skills --skill wave-analytics
```

## 这套 Skills 包含什么

- `wave`
  总入口。根据你当前阶段，把任务路由到埋点规划、执行、质检、SDK 接入或数据分析。
- `wave-tracking-plan`
  用于梳理事件设计、端侧归属、属性定义和 identify 方案。
- `wave-tracking`
  用于写入和发布 Tracking Plan，以及按需创建 Dashboard。
- `wave-tracking-qc`
  用于对照已发布 Tracking Plan 做埋点质检、计划对照和上线验收。
- `wave-sdk-integration`
  用于处理 Pipeline、初始化参数、identify / reset 和埋点代码接入。
- `wave-analytics`
  用于做事件、漏斗、留存、用户列表和 SQL 分析。

## 典型用法

安装完成后，可以直接这样描述任务：

- “根据当前项目代码，帮我设计注册到付费的埋点方案”
- “把这版事件草稿写成 Tracking Plan，并发布出来”
- “我已经确认事件开始触发，帮我按计划做一轮质检”
- “我要接 JavaScript SDK，给我初始化代码和 identify 方案”
- “分析最近 30 天新用户的 7 日留存，并解释原因”

## 使用前提

使用前请先完成 **Wave MCP Server** 配置，否则工具只能看到 skill 说明，不能真正调用 Sensors Wave 的项目、Pipeline、Tracking Plan、Dashboard 和分析能力。

## 更多说明

- 安装、更新、移除见 [docs/README.install.md](docs/README.install.md)

## License

本项目采用 [MIT License](LICENSE)。
