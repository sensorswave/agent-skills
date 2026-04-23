---
name: wave
description: >-
  Sensors Wave 平台总入口。根据用户请求路由到埋点方案规划（wave-tracking-plan）、
  Tracking Plan 执行（wave-tracking）、Tracking Plan 质检（wave-tracking-qc）、
  SDK 接入（wave-sdk-integration）或数据分析（wave-analytics）。
---

# Wave

这是 Sensors Wave 平台的总入口 Skill。它只负责识别当前阶段并路由到对应 workflow，不直接展开具体执行。

## 路由规则

根据用户当前卡点选择对应 Skill：

### → wave-tracking-plan

当用户涉及以下场景时，读取并遵循 [../wave-tracking-plan/SKILL.md](../wave-tracking-plan/SKILL.md)：

- 根据当前代码设计埋点计划
- 根据 PRD / 原型 / 页面流程设计埋点方案
- 事件命名规范
- 服务端 vs 客户端选型
- identify / 用户标识方案设计

### → wave-tracking

当用户涉及以下场景时，读取并遵循 [../wave-tracking/SKILL.md](../wave-tracking/SKILL.md)：

- 把已有草稿写入 Tracking Plan
- 发布 Tracking Plan
- 创建概览 Dashboard（基于埋点计划）

### → wave-tracking-qc

当用户涉及以下场景时，读取并遵循 [../wave-tracking-qc/SKILL.md](../wave-tracking-qc/SKILL.md)：

- 埋点质检 / 校验
- 按已发布 Tracking Plan 做上线验收
- 核对缺失事件、缺失属性或值不符合计划
- 用户已经确认事件开始触发，下一步要做质量检查

### → wave-sdk-integration

当用户涉及以下场景时，读取并遵循 [../wave-sdk-integration/SKILL.md](../wave-sdk-integration/SKILL.md)：

- 创建 / 复用 Pipeline
- SDK 初始化 / 代码生成
- `endpoint` / `source_token`
- identify / reset / 登录态埋点接入
- 客户端或服务端埋点代码集成

### → wave-analytics

当用户涉及以下场景时，读取并遵循 [../wave-analytics/SKILL.md](../wave-analytics/SKILL.md)：

- 事件分析 / 指标统计
- 漏斗分析 / 转化率
- 留存分析
- 用户列表 / 分群筛选
- 用户行为序列
- 自定义 SQL 查询
- 数据洞察 / 趋势分析

## 歧义处理

- 如果用户同时涉及方案与 SDK 接入，先判断当前卡点：
  - 还在定事件、代码盘点、identify 方案 → `wave-tracking-plan`
  - 已有草稿，准备写入 / 发布 Tracking Plan → `wave-tracking`
  - 已经开始对照计划检查线上数据质量 → `wave-tracking-qc`
  - 已经在改代码或接 SDK → `wave-sdk-integration`
- 如果用户同时涉及埋点和分析，优先完成埋点方案/接入，再切换到分析（wave-analytics）。
- 如果不确定，询问用户："你现在是要定埋点方案，还是已经开始接 SDK / 改代码了？"

## 安装前提

- 这组 `wave-*` skill 设计为一起安装，路由、执行、质检与 SDK 接入会互相切换。
- 所有子 Skill 均依赖 **Wave MCP Server** 提供的工具集。如当前环境未配置 Wave MCP 连接，请先提示用户完成配置。
