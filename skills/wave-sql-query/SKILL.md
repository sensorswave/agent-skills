---
name: wave-sql-query
description: >-
  Query Sensors Wave project data with read-only Apache Doris SQL when
  standard analysis models cannot express the question. Use for 自定义 SQL,
  SQL 查询, schema 探查, 多表关联, 行为找人, 分群交集, and ad-hoc SELECT
  on events/users/cohorts/query_log.
---

# Wave SQL 查询

## 目标

把无法用事件分析、漏斗分析、留存分析表达的问题，写成当前项目可执行的只读 SQL，查出结果并给出业务解释。列名和类型以 Wave 的表结构为准；时区、当前时间和周起始以 `get_project_context` 为准。

## 按需加载

构造 SQL、映射列名、处理时区或复杂类型前，阅读 [references/sql-query.md](references/sql-query.md)。

## 工具

- 项目：`list_projects`
- 项目上下文：`get_project_context`
- 表结构：`get_sql_schema`
- 查询：`query_custom_sql`
- 口径对齐：`list_events`、`list_event_properties`、`list_user_properties`、`list_cohorts`

## 项目门禁

在调用其他项目级 MCP 工具前：

1. 调用 `list_projects`，展示 `project_id | name` 表格。
2. 等待用户回复数字 `project_id`。
3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

禁止静默挑选项目，也禁止在此步骤前调用 schema、SQL 或元数据工具。

## 工作流

1. 先通过项目门禁，再判断请求类型：
   - 用户明确要 SQL，或分析模型覆盖不了（多表关联、跨事件对齐同一元素、行为找人、分群交集、临时探查）→ 继续本 skill
   - 分析模型能表达 → 交给 `wave-analytics`
   - 要把 SQL 存成图表或 Dashboard → 先验证查询，再交给 `wave-dashboard-builder`
2. 先发现口径，再写 SQL。用 `list_events` / `list_event_properties` / `list_user_properties` 把业务词映射成逻辑事件名和属性名；不要用显示名当列名。
3. 按固定规则把小写逻辑属性名转成列名：保留列用原名，其他事件属性加 `e_`，其他用户属性加 `u_`。用户去重和表关联用 `ssid`。用户属性默认用 `events.u_*`（事件发生时的快照）；只有明确要最新画像时才 `JOIN users`。再用 `get_sql_schema` 确认列存在、存储类型，以及 `property` / `children` 关联。涉及时间筛选或按日/周聚合时，先调用 `get_project_context`，用返回的 `storage_timezone`、`project_timezone`、`now_project` 和 `week_starts_on` 写 `CONVERT_TZ`。
4. 写出一条只读 `SELECT` 或 `WITH ... SELECT`。查 `events` 时优先加 `time` 和 `event` 条件；返回明细时加 `LIMIT`。
5. 先用一句话说明这条 SQL 在算什么，再解读结果。失败时先改列名、前缀、引号、类型转换、时区或 LIMIT，不要换一张不存在的表。

## 边界

- 禁止在用户选择 `project_id` 之前查询项目数据。
- 只查询 `events`、`users`、`cohorts`、`query_log`。MCP 只接受单条只读 `SELECT` / CTE，禁止 `INSERT` / `UPDATE` / `DELETE` / DDL，也禁止 `SHOW`、`SET`、`EXPLAIN` 和库表限定名。
- 不要为了「看起来更灵活」把事件分析、漏斗分析、留存分析改写成 SQL。这些模型与 `WINDOW_FUNNEL` / `RETENTION` 的计算结果不能直接对比。
- 虚拟事件不会在 SQL 中自动展开；虚拟属性不会作为列出现在 Schema 中。
- 普通查询最多返回 10,000 行，这个上限不会自动改写 SQL。需要更多明细时，让用户在产品里下载，并继续收紧时间范围。

## 交接

- 标准分析模型能表达的问题，交给 `wave-analytics`。
- 保存图表或 Dashboard 时，把已验证的 SQL、推荐图表类型和 Dashboard 名称交给 `wave-dashboard-builder`。
- 缺事件或属性、需要补埋点时，交给 `wave-tracking`。
- 产品用法、入口或权限问题，交给 `wave-product-help`。

## 输出

返回：

- 简短结论
- 关键数字；明细或按日聚合结果用紧凑表格
- 这条 SQL 实际在度量什么
- 口径、时区、筛选或埋点质量方面的限制
- 一到两个后续查询建议
