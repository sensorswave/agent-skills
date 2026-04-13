---
name: wave-tracking
description: >-
  Guide end-to-end Sensors Wave tracking instrumentation via MCP tools:
  event naming conventions, server-vs-client strategy, interactive workflow
  with user confirmation gates (project → pipeline → tracking plan → SDK
  code generation → quality check → dashboard). Use when working on
  埋点方案, Tracking Plan, SDK 集成, 埋点规范, event tracking setup,
  or data collection instrumentation.
---

# Sensors Wave 埋点规范（AI 执行说明）

遵循 Sensors Wave 官方文档站 data-integration 分类下的推荐。向用户解释时用业务语言；技术规则以下文为准。

## 0. 交互式原则（全局）

- **项目必须由用户选定**：任何项目级 MCP 调用前，先 `list_projects`，展示结果，让用户明确选择 `project_id`。禁止静默假定。
- **列选项 → 用户拍板 → 再调工具**：每一步先说明选项与推荐，收到确认后再执行；**写**工具须二次确认。
- **先展示将提交的参数**：创建/更新前列出将写入的字段，避免误操作。
- **用户要求「全自动」时**：仍须至少完成项目选择与首次写操作确认。

提示词模板见 [prompts.md](prompts.md)。

## 1. 埋点方式选型（优先服务端）

- **只要业务上能在服务端产生可靠事实，优先服务端埋点**。
- 客户端易受广告拦截、隐私设置影响，可能丢失 30%–50% 请求；服务端易维护、跨端一致。
- **客户端更适合**：必须依赖 UI 的行为（点击、滑动、停留、浏览路径）。
- **决策顺序**：关键业务结果 → 服务端；必须 UI 行为 → 客户端；不能容忍丢失 → 改服务端或说明风险。

## 2. 事件设计

- 与分析层级匹配；**通用事件名 + 属性区分细节**，避免每按钮一事件或 `Click` 总桶。
- 示例：`PageView` + `page_name`；`ButtonClick` + `button_name`；`VideoPlay` + `video_id`。

## 3. 命名规范

**事件名**：PascalCase，对象 + 动作（`PageView`、`AddToCart`、`OrderCreate`）。已有 snake_case 的项目可统一沿用，但同应用内必须风格一致。预置事件以 `$` 开头。

**属性名**：snake_case（`order_id`、`total_amount`）。禁止 `$` 前缀。布尔用 `is_`/`has_`。

## 4. 事件属性 vs 用户属性

- **事件属性**：描述这一次行为的上下文，随事件写入。
- **用户属性**：描述用户当前/长期状态，可更新。
- 口诀：随动作变 → 事件属性；描述人、跨事件复用 → 用户属性。

## 5. 类型与取值

String、Numeric、Boolean、Datetime、List。同属性全事件类型一致。枚举统一小写 snake 风格。禁止动态属性名。

## 6–8. 全局属性、预置能力、数量限制

- 80%+ 事件都需要的上下文用**全局属性**注册。
- SDK 自动采集 `$…` 预置事件/属性，勿重复造轮子。自定义属性禁止 `$` 前缀。
- 事件种类上限 ~1000，单事件属性建议 5–20 个，总属性各 ~500。

## 9. 隐私与安全

勿上报密码、Token、完整卡号/证件/手机/邮箱；优先 ID、哈希、后四位等脱敏形态。

## 10. 用户属性更新方式

按语义选用：**set** 覆盖、**set_once** 首次、**increment** 累加、**append** 列表追加。

## 11. AI 交付物

输出可研发落地的表格：事件名、中文含义、触发时机、端、属性（名/类型/必填/枚举/说明）、服务端 vs 客户端标注、是否与预置重复。

## 12. MCP 完整闭环流程

按顺序推进，每步结合 §0 与 [prompts.md](prompts.md) 模板确认。

### 12.1 选择项目

`list_projects` → 用户选定 `project_id`。

### 12.2 接入 Pipeline

1. `list_pipelines` → 用户选择复用或新建。
2. 复用：`get_pipeline_detail`（获取 `source_token`）。
3. 新建：确认后 `create_pipeline`（返回 `source_token`）。

### 12.3 创建 Tracking Plan

1. `list_tracking_plans` → 用户选择扩展已有或新建。
2. 可选 `list_tracking_plan_templates` 使用模板。
3. 确认后 `create_tracking_plan` / `add_tracking_plan_events`。
4. 确认后 `publish_tracking_plan`。

### 12.4 获取 SDK 初始化信息

1. `get_server_info` → 获取 `data_collection_url`（SDK server_url 参数）和 `dashboard_url_base`。
2. 结合 `source_token`，生成 SDK 初始化代码片段。

### 12.5 生成 SDK 埋点代码

1. 确认**服务端 vs 客户端**方案。
2. **autoCapture**：SDK 自动采集预置事件，不等于业务事件齐全。
3. 根据栈选择 SDK 文档（JavaScript / Android / iOS / Go / Flutter / Harmony），用 `source_token` + `data_collection_url` 初始化。
4. 按 Tracking Plan 中的事件和属性生成 `trackEvent` 调用代码。

### 12.6 校验埋点

1. 等待数据上报后，`get_tracking_plan_quality_check` 对照计划与实际数据。
2. 可选 `list_events` / `list_event_properties` 交叉验证。

### 12.7 创建 Dashboard

1. 根据 Tracking Plan 中的核心事件，用 `create_chart_for_dashboard` 创建分析图表并关联概览。
2. 可选 `set_dashboard_chart_layouts` 调整布局。
3. 构造概览链接：`{dashboard_url_base}/{dashboard_id}` 返回给用户。

### 12.8 分工

- **AI**：按 §0 交互；编排 MCP 工具；输出埋点表与 SDK 代码；创建概览。
- **用户/研发**：选择项目、确认各步；合入 SDK 代码、发版；敏感环境与合规由团队负责。

## 13. 与「数据分析」的边界

- 本 Skill：采集设计、命名、选型、MCP 落地、SDK 策略、Dashboard 创建。
- 深度分析（漏斗 SQL、`query_*` 系列）：使用 `wave-analytics` Skill。

---

> 若官方文档或 MCP 工具后续变更，以 Sensors Wave 文档站与当前 MCP 工具描述为准。
