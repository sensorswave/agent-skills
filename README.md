# Sensors Wave Skills

把 Sensors Wave 的埋点落地、Tracking Plan 质检、数据分析、营销自动化、图表看板、产品帮助和 Catalog 治理流程，整理成一组可直接安装到 **Cursor**、**Claude Code**、**Codex** 的 Skills。

装好之后，你可以直接让工具围绕 Sensors Wave 项目工作，而不是每次都从零解释流程、命名规范和执行顺序。

## 适合什么场景

- 根据代码、PRD、页面流程整理埋点方案和事件表
- 在项目里创建或更新 Pipeline、Tracking Plan
- 创建事件图表、漏斗图、留存图、SQL 图表和 Dashboard
- 基于真实项目能力设计和编排 MA Campaign，复用已有 SMS/Webhook 通道
- 做埋点验收、计划对照和上线质检
- 生成 JavaScript、Android、iOS、服务端等 SDK 接入思路
- 做事件分析、漏斗分析、留存分析和 SQL 查询
- 补充 Catalog 中已有事件/属性的显示名、描述、触发时机和示例值
- 查询 Wave 产品功能用法、配置步骤、FAQ 和常见排障

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
  总入口。根据你当前阶段，把任务路由到埋点落地、质检、分析、看板构建、产品帮助或 Catalog 治理。
- `wave-tracking`
  用于埋点方案设计、Tracking Plan 写入/发布、Pipeline/SDK 接入。
- `wave-tracking-validation`
  用于对照已发布 Tracking Plan 做埋点质检、计划对照和上线验收。
- `wave-analytics`
  用于做事件、漏斗、留存、用户列表和 SQL 分析。
- `wave-marketing-automation`
  用于 5W1H 营销简报、真实项目资产发现、已有通道复用、Campaign 规划与校验、Draft 创建、测试、启停和效果复盘。
- `wave-dashboard-builder`
  用于创建和更新 Wave 图表、KPI 卡片、Dashboard 和布局。
- `wave-product-help`
  用于回答 Wave 产品功能用法、配置步骤、概念解释、FAQ 和常见排障。
- `wave-catalog-governance`
  用于维护已有 Catalog 元数据的显示名、描述、触发时机、平台标签和示例值。

## 典型用法

安装完成后，可以直接这样描述任务：

- “根据当前项目代码，帮我设计注册到付费的埋点方案”
- “把这版事件草稿写成 Tracking Plan，并发布出来”
- “我已经确认事件开始触发，帮我按计划做一轮质检”
- “我要接 JavaScript SDK，给我初始化代码和 identify 方案”
- “分析最近 30 天新用户的 7 日留存，并解释原因”
- “基于当前项目真实客群和已有通道，设计一个注册唤醒 Campaign，先给我 5W1H 简报并校验后保存 Draft”
- “复盘 Campaign 251 的发送、送达和目标转化，不要直接启动活动”
- “把这些核心指标做成一个增长看板”
- “帮我把这些事件的中文名、描述和触发时机补完整”
- “Wave 里 Pipeline 应该在哪里配置？”

## 使用前提

使用前请先完成 **Wave MCP Server** 配置，否则工具只能看到 skill 说明，不能真正调用 Sensors Wave 的项目、Pipeline、Tracking Plan、Dashboard、Catalog 和分析能力。

## 更多说明

- 安装、更新、移除见 [docs/README.install.md](docs/README.install.md)

## License

本项目采用 [MIT License](LICENSE)。
