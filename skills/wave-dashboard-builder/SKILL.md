---
name: wave-dashboard-builder
description: >-
  构建和维护 Sensors Wave 的已保存图表与 Dashboard。适用于用户要创建、更新、整理或
  打磨图表、KPI 卡片、看板、概览页、看板布局或可复用分析资产。使用 Wave MCP 的
  chart / dashboard 工具；探索性的数据解读先交给 wave-analytics，自定义 SQL 交给
  wave-sql-query。
---

# Wave 看板构建

## 目标

创建或更新 Wave 的已保存分析资产：图表、Dashboard 和 Dashboard 布局。

## 工具

- 发现资产：`list_charts`、`list_dashboards`、`get_chart_detail`、`get_dashboard_detail`
- 创建 Dashboard：`create_dashboard`
- 创建图表：`create_event_chart`、`create_event_charts`、`create_funnel_chart`、`create_retention_chart`、`create_custom_sql_chart`
- 需要时验证查询形态：`query_event_analysis`、`query_funnel`、`query_retention`、`get_sql_schema`、`query_custom_sql`
- 整理布局：`set_dashboard_chart_layouts`
- 更新已有资产：`update_dashboard`、`update_chart`

## 项目门禁

<!-- wave:project-gate -->
在调用其他项目级 MCP 工具前：

1. 调用 `list_projects`，展示 `project_id | name` 表格。
2. 等待用户回复数字 `project_id`。
3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

禁止静默挑选项目，也禁止在此步骤前列出、创建、更新或排布图表/Dashboard。
<!-- /wave:project-gate -->

## 工作流

1. 先通过项目门禁，再明确资产目标：独立图表、新 Dashboard、已有 Dashboard，还是刷新 Dashboard。
2. 用户点名某个资产或要求更新时，先发现已有 Dashboard/图表，避免重复创建。用户问「有哪些看板/图表」时，调用 `list_dashboards` / `list_charts` 且不传 `search_key`，展示全部条目（`total` 加分页）。不要用「看板」「dashboard」「概览」「图表」这类类型词去搜索。
3. 确认指标/查询形态。用户没有明确指标时，交给 `wave-analytics` 或 `wave-sql-query`，或者在创建资产前先跑一次轻量验证查询。
4. 有意识地选择图表类型：
   - KPI 汇总值 → `Metric`
   - 时间趋势 → `Line`
   - 分类对比 → `Column` 或 `Bar`
   - 构成占比 → `StackedLine`、`StackedColumn` 或 `Pie`
   - 漏斗转化 → `FunnelColumn`
   - 留存曲线 → `Line`
   - SQL/明细表 → `Table`
5. 为 Dashboard 一次创建多个事件图表时，优先用 `create_event_charts` 批量调用。
6. 图表和 Dashboard 一起创建时用 `new_dashboards`；挂到已有 Dashboard 时用 `dashboard_ids`。
7. Dashboard 上已有图表之后，任何布局改动前先调用 `get_dashboard_detail`。`list_dashboards` / `get_resource(dashboard)` / `list_charts` 不含坐标。

## 布局默认值

遵循 Wave 概览编辑器的快捷布局（Speedy Layout）。所有图表类型高度一致，包括 Metric/KPI 卡片。

- 12 列栅格。始终 `h=7`。`min_w=3`、`min_h=4`。
- 快捷布局是默认的整理方式（单列 / 双列 / 三列 / 整理布局）。优先用 `set_dashboard_chart_layouts` 传 `speedy_columns`，由服务端按视觉顺序（先 `y` 再 `x`）排序并套用：
  - 1 列：`w=12 h=7`
  - 2 列：`w=6 h=7`
  - 3 列：`w=4 h=7`
- 不要给 Metric/KPI 更矮的高度或单独的顶部一行，把它们当普通图表处理。
- 没有布局的新图表：`w=12 h=7`，放在最底部（`x=0`，`y=max(y+h)`）。
- 复制沿用源图表的 `w/h`，追加到最底部。
- 用户要求时，自定义 `layouts` 可以改 `x/w`，但除非用户明确要求其他高度，保持 `h=7`。
- `x+w` 必须落在 12 列栅格内。矩形之间不能重叠，也不能与本次调用未列出的图表重叠。出现重叠时，把受影响的图表全部带上，或改用 `speedy_columns`。

## 边界

- 项目门禁未通过前，不要发现或写入项目资产。
- 指标定义不清楚时不要臆造分析含义；用 `wave-analytics` 或 `wave-sql-query` 验证。
- 不要在这里做 Tracking Plan 质检，交给 `wave-tracking-validation`。
- 不要在这里设计新埋点事件，交给 `wave-tracking`。
- 除非用户明确要求并确认了准确的资产名称，不要删除图表或 Dashboard。优先创建/更新/布局操作。

## 输出

返回：
- 创建或更新的 Dashboard id/名称
- 创建或更新的图表 id/名称/类型
- 应用的布局改动（`speedy_columns` 或逐图表的 `x,y,w,h`）
- 被跳过的图表请求及原因
- 若数据验证或指标定义仍不清楚，给出后续建议
