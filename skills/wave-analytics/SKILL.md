---
name: wave-analytics
description: >-
  用 Sensors Wave MCP 的标准分析模型做用户行为分析：事件分析、漏斗分析、留存分析、
  用户列表、用户行为序列和分群管理。适用于数据分析、指标问数、转化分析、
  funnel / retention / event metrics 类问题。需要自定义 SQL 或 Doris SELECT 时交给
  wave-sql-query；要保存图表或 Dashboard 时交给 wave-dashboard-builder。
---

# Wave 分析模型

## 目标

把用户的业务问题转成正确的 Wave 分析查询，用 MCP 工具执行，并用业务语言解释结果。标准分析模型能表达的问题不要改写成 SQL。

## 按需加载

- 筛选与分组：[references/filters.md](references/filters.md)
- 事件分析：[references/event-analysis.md](references/event-analysis.md)
- 漏斗：[references/funnel.md](references/funnel.md)
- 留存：[references/retention.md](references/retention.md)
- 用户列表：[references/user-list.md](references/user-list.md)

## 本轮工具

以当前可见工具为准。SKILL 里列出的分析工具不一定都在本轮可用。

| 问题 | 工具 | 当前没有该工具时 |
|---|---|---|
| 指标、趋势、分组 | `query_event_analysis` | `switch_mode`，`task_type=metric_query` 或 `event_analysis` |
| 步骤转化、流失 | `query_funnel` | `switch_mode`，`task_type=funnel` |
| 首次行为后回访 | `query_retention` | `switch_mode`，`task_type=retention` |
| 找人、分群 | `query_user_list` / `search_users` | `switch_mode`，`task_type=user_query` |

发现工具：`list_events`、`list_event_properties`、`list_user_properties`、`list_metrics`、`list_cohorts`。需要时区或「今天 / 本周」时调用 `get_project_context`。

## 项目门禁

<!-- wave:project-gate -->
在调用其他项目级 MCP 工具前：

1. 调用 `list_projects`，展示 `project_id | name` 表格。
2. 等待用户回复数字 `project_id`。
3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

禁止静默挑选项目，也禁止在此步骤前调用元数据、分析或分群工具。
<!-- /wave:project-gate -->

## 属性

查询前用 `list_event_properties` / `list_user_properties` 确认 `name` 和 `data_type`。查询参数用 `name`，不用显示名。按 `data_type` 选择筛选操作符和分组字段，见 [filters.md](references/filters.md)。

SQL 只用于多表关联、跨事件对齐同一元素、行为条件找人、分群交集、临时探查，或用户明确要 SQL。

## 工作流

1. 先通过项目门禁，再判断请求类型：
   - 指标、趋势、分组对比 → 事件分析
   - 步骤转化、流失 → 漏斗分析
   - 首次行为后的回访 → 留存分析
   - 找人、分群候选 → 用户列表或分群人数
   - 解释单个用户的行为 → 用户序列或用户档案
   - 模型表达不了，或用户明确要 SQL → 交给 `wave-sql-query`
   - 保存可复用资产 → 交给 `wave-dashboard-builder`
2. 查询前先发现数据模型，把业务词映射成真实的事件名和属性名。需要解释日期切分、今天/本周或当前时间时，先调用 `get_project_context`；用 `now_project` 和 `week_starts_on`（周一），结构化分析默认按 `project_timezone` 切日。
3. 用户没指定时使用合理默认值：最近 30 天、按时间范围选择粒度、分组 Top 10、用户列表 100 条、有序漏斗窗口 7 天。
4. 执行对应查询工具。失败时先修正事件名、属性名、操作符、筛选结构或时间范围。筛选或分组失败后，不要改用未筛选的全站结果当作原问题的答案；做不到时直接说明原因。
5. 先给结论，再给数字、趋势或对比、限制条件，以及一到两个后续分析建议。
6. 用户要保存图表或做 Dashboard 时，汇总已验证的查询结构，交给 `wave-dashboard-builder`。

分群生命周期请求：先发现已保存分群；创建或更新前先校验完整规则；复用受众时用 `cohort_id`；删除前先检查引用。

## 边界

- 项目门禁未通过前，禁止查询或改写项目数据。
- 不要在这里设计或落地新埋点，交给 `wave-tracking`。
- 不要在这里做 Tracking Plan 质检，交给 `wave-tracking-validation`。
- 不要在这里改 Catalog 元数据，交给 `wave-catalog-governance`。
- 不要在这里创建已保存图表或 Dashboard，交给 `wave-dashboard-builder`。
- 不要把能用分析模型表达的问题改写成 SQL；需要 SQL 时交给 `wave-sql-query`。

## 输出

返回：

- 简短结论
- 关键数字；需要时用紧凑表格
- 业务语言解读
- 数据范围、筛选或埋点质量方面的限制
- 一到两个后续查询建议

看板请求先给出查询结构和推荐图表类型，再交接。
