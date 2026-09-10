---
name: wave
description: >-
  Sensors Wave 平台路由 skill。用户问题较宽或意图不明确时使用，把请求分发到埋点落地
  （wave-tracking）、埋点质检（wave-tracking-validation）、数据分析（wave-analytics）、
  自定义 SQL（wave-sql-query）、人群挖掘（wave-cohort-mining）、营销自动化
  （wave-marketing-automation）、看板构建（wave-dashboard-builder）、产品帮助
  （wave-product-help）或数据字典治理（wave-catalog-governance）。
---

# Wave

## 目标

把用户路由到恰好一个具体的 Wave skill，然后阅读并遵循该 skill。不要在本路由文件里执行领域工作。

## 路由

- 埋点落地 → 阅读 [../wave-tracking/SKILL.md](../wave-tracking/SKILL.md)
  用于事件方案、代码/需求盘点、客户端与服务端职责、identify/reset 策略、Tracking Plan 草稿/写入/发布、Pipeline 选择或创建、SDK 接入，以及为看板交接准备埋点上下文。已发布的 Tracking Plan 是落地及其他下游环节的基线。
- 埋点质检 → 阅读 [../wave-tracking-validation/SKILL.md](../wave-tracking-validation/SKILL.md)
  仅在事件已经上报，且用户要做 Tracking Plan 质检、上线验收或缺失事件/属性排查时使用。
- 数据分析 → 阅读 [../wave-analytics/SKILL.md](../wave-analytics/SKILL.md)
  用于事件指标、漏斗、留存、用户列表、行为序列、用户档案和分群管理。
- 自定义 SQL → 阅读 [../wave-sql-query/SKILL.md](../wave-sql-query/SKILL.md)
  用户明确要 SQL，或标准分析模型无法表达时使用（多表关联、跨事件对齐同一元素、行为找人、分群交集、临时 SELECT）。
- 人群挖掘 → 阅读 [../wave-cohort-mining/SKILL.md](../wave-cohort-mining/SKILL.md)
  用户给出业务目标但没有明确规则，要「挖掘 / 找人群 / 分群推荐 / 圈人 / 有哪些值得运营的人群」时使用；产出带人数与 lift 证据的候选人群并落为 STATIC 规则分群。
- 营销自动化 → 阅读 [../wave-marketing-automation/SKILL.md](../wave-marketing-automation/SKILL.md)
  用于 5W1H Campaign 设计、复用短信/Webhook 通道、受众规划、活动校验、草稿创建、试发、生命周期操作和效果复盘。
- 看板构建 → 阅读 [../wave-dashboard-builder/SKILL.md](../wave-dashboard-builder/SKILL.md)
  用户要创建、更新、整理或打磨已保存图表、看板、概览页、指标卡、布局或可复用分析资产时使用。
- 产品帮助 → 阅读 [../wave-product-help/SKILL.md](../wave-product-help/SKILL.md)
  用于产品用法、配置步骤、概念、FAQ、页面入口、权限和排障。
- 数据字典治理 → 阅读 [../wave-catalog-governance/SKILL.md](../wave-catalog-governance/SKILL.md)
  用于维护已有 Catalog 的显示名、描述、事件触发时机、平台标签和示例值。

## 歧义处理

- 请求同时涉及埋点和数据分析时，先完成埋点设计或落地，再交给分析。
- 请求同时涉及埋点落地和质检时，落地走 `wave-tracking`；只有用户确认事件已经上报、并明确要求检查时，才做质检。
- 请求先分析数据再保存为图表或看板时，先用 `wave-analytics` 或 `wave-sql-query` 确认指标/查询形态，再交给 `wave-dashboard-builder`。
- 指标、漏斗、留存类问题优先 `wave-analytics`。只有用户要 SQL，或分析模型无法表达时，才走 `wave-sql-query`。
- 用户已经说清一条分群规则要建、改、删时走 `wave-analytics`；只给目标、要 AI 提出该圈谁时走 `wave-cohort-mining`。挖出的候选要建 Campaign 时，再交给 `wave-marketing-automation`。
- 请求同时涉及 Campaign 规划和效果分析时，先在 `wave-marketing-automation` 完成活动上下文和操作门禁，再把已校验的指标形态交给 `wave-analytics`。
- 请求同时涉及 Campaign 规划和保存看板时，先完成活动上下文，再把指标/查询形态交给 `wave-dashboard-builder`。
- 用户要改技术名、改数据类型、删除元数据或合并重复项时，只把请求交给 `wave-catalog-governance` 说明当前 MCP 边界；不要暗示这些操作现在可用。
- 用户问「Wave 怎么用 / 在哪配置 / 为什么看不到」时，优先 `wave-product-help`，不要先走分析或埋点。

## 停止

选定路由后，停止使用本文件，改为阅读并遵循目标 skill。项目级 skill（`wave-tracking`、`wave-tracking-validation`、`wave-analytics`、`wave-sql-query`、`wave-cohort-mining`、`wave-marketing-automation`、`wave-dashboard-builder`、`wave-catalog-governance`）必须先通过各自的「项目门禁」确认项目，再调用其他项目级 MCP 工具。若无法判断路由，只问一句：「你现在要做埋点落地、质检、数据分析、自定义 SQL、人群挖掘、营销自动化、看板构建、产品帮助，还是 Catalog 元数据治理？」
