---
name: wave-skills
description: >-
  Sensors Wave 平台 AI Skills 路由入口。自动分发到埋点设计（wave-tracking-design）、
  Tracking Plan 执行（wave-tracking）、SDK 接入（wave-sdk-integration）或数据分析
  （wave-analytics）子 Skill。Use when working on Wave 埋点设计, tracking
  rollout, sdk integration, instrumentation, analytics, funnel, retention, or
  event tracking implementation.
---

# Wave Skills

这是 Sensors Wave 平台的 AI Skill 集合入口。根据用户意图自动路由到对应的子 Skill。

## 路由规则

根据用户请求的关键词判断应使用哪个 Skill：

### → wave-tracking-design

当用户涉及以下场景时，读取并遵循 [skills/wave-tracking-design/SKILL.md](skills/wave-tracking-design/SKILL.md)：

- 根据当前代码设计埋点计划
- 根据 PRD / 原型 / 页面流程设计埋点方案
- 事件命名规范
- 服务端 vs 客户端选型
- identify / 用户标识方案设计

### → wave-tracking

当用户涉及以下场景时，读取并遵循 [skills/wave-tracking/SKILL.md](skills/wave-tracking/SKILL.md)：

- 把已有草稿写入 Tracking Plan
- 发布 Tracking Plan
- 埋点质检 / 校验
- 创建概览 Dashboard（基于埋点计划）

### → wave-sdk-integration

当用户涉及以下场景时，读取并遵循 [skills/wave-sdk-integration/SKILL.md](skills/wave-sdk-integration/SKILL.md)：

- 创建 / 复用 Pipeline
- SDK 初始化 / 代码生成
- `endpoint` / `source_token`
- identify / reset / 登录态埋点接入
- 客户端或服务端埋点代码集成

### → wave-analytics

当用户涉及以下场景时，读取并遵循 [skills/wave-analytics/SKILL.md](skills/wave-analytics/SKILL.md)：

- 事件分析 / 指标统计
- 漏斗分析 / 转化率
- 留存分析
- 用户列表 / 分群筛选
- 用户行为序列
- 自定义 SQL 查询
- 数据洞察 / 趋势分析

## 歧义处理

- 如果用户同时涉及方案与 SDK 接入，先判断当前卡点：
  - 还在定事件、代码盘点、identify 方案 → `wave-tracking-design`
  - 已有草稿，准备写入 / 发布 Tracking Plan → `wave-tracking`
  - 已经在改代码或接 SDK → `wave-sdk-integration`
- 如果用户同时涉及埋点和分析，优先完成埋点方案/接入，再切换到分析（wave-analytics）。
- 如果不确定，询问用户："你现在是要定埋点方案，还是已经开始接 SDK / 改代码了？"

## 前置依赖

所有子 Skill 均依赖 **Wave MCP Server** 提供的工具集。如当前环境未配置 Wave MCP 连接，请先提示用户完成配置。
