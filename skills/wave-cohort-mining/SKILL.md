---
name: wave-cohort-mining
description: >-
  人群挖掘：给定业务目标（转化、复购、召回、激活），基于 Sensors Wave 项目真实数据主动提出
  候选人群，用工具算出人数、相对基线的 lift 和与已有分群的重叠，人工确认后落为 STATIC 规则分群。
  适用于「帮我挖人群」「有哪些值得运营的分群」「找高意向未转化 / 沉默 / 高价值用户」、
  segment discovery、cohort mining。单条明确规则的分群增删改仍走 wave-analytics。
---

# Wave 人群挖掘

## 目标

把「提升 X」变成 3–10 个带证据的候选人群：每个候选有规则、人数、占基线比例、目标指标相对基线的 lift、与已有分群的重叠度和建议动作。评分只能来自工具返回的数字。产出只有一种形态：可解释的 RULE 规则分群。

## 按需加载

- 假设库（模板、事件角色、阈值方法、DSL 骨架）：[references/hypothesis-library.md](references/hypothesis-library.md)
- 评分门槛、排序、报告表、落库参数模板：[references/scoring.md](references/scoring.md)
- 属性筛选写法沿用 wave-analytics 的 [filters.md](../wave-analytics/references/filters.md)

## 本轮工具

以当前可见工具为准。

| 步骤 | 工具 | 当前没有该工具时 |
|---|---|---|
| 盘点 | `get_project_context`、`list_events`、`list_event_properties`、`list_user_properties`、`list_cohorts` | — |
| 维度取值 | `list_property_values` | `query_event_analysis` 按该属性 `group_by`，`limit` 20 |
| 基线与反差 | `query_funnel`、`query_event_analysis`（`group_by`）、`query_retention` | — |
| 评估候选 | `evaluate_cohort_definition` | `query_cohort_user_count(definition)` 算人数，`query_custom_sql` 算 lift 与重叠 |
| 抽样 | `sample_cohort_users(rule_group=完整定义)` | — |
| 落库 | `validate_cohort_definition` → `create_cohort` | — |

`query_cohort_user_count.definition` 与 `sample_cohort_users.rule_group` 接受完整分群 DSL（`user_did` / `user_did_not` / `user_sequence_did` / `in_cohort` / 嵌套子组），不需要先保存分群。`query_user_list` 不接受行为规则，不要用它评估候选。

## 项目门禁

<!-- wave:project-gate -->
在调用其他项目级 MCP 工具前：

1. 调用 `list_projects`，展示 `project_id | name` 表格。
2. 等待用户回复数字 `project_id`。
3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

禁止静默挑选项目，也禁止在此步骤前调用元数据、分析或分群工具。
<!-- /wave:project-gate -->

## 工作流

1. 先通过项目门禁，调用 `get_project_context` 拿时区和当前时间。
2. 盘点：`list_events`、`list_event_properties`、`list_user_properties`、`list_cohorts`。把业务词映射到真实事件名；记下已有分群的名称和规则，用于去重。`filter_by` 只能用用户属性；`platform_type` 这类事件属性写在 `user_did.metric_rule.filter`（`table_type=event`），取值用 `list_property_values`，不要猜。
3. 定目标：用户未说时默认「转化」并在报告中注明。找出目标事件及其上游意向事件。
4. 定基线：用 `query_funnel` / `query_event_analysis` 算全量目标转化率或留存率；再按 platform、channel、city 等维度 `group_by`，记下偏离基线最多的切片作为「反差候选」。
5. 出假设：从假设库挑 6–10 个，用真实事件名实例化。阈值来自分布（`count_uv`、`p90`、`list_property_values`），不拍脑袋。
6. 评估每个候选，门槛见 scoring.md：人数占基线 0.5%–30%；`|lift − 1| ≥ 0.3`；与任一已有分群重叠 ≤ 70%。调用 `evaluate_cohort_definition` 时必须传 `compare_cohort_ids`（第 2 步盘点到的相关已有分群，最多 10 个）；报告里的重叠数字只能来自返回的 `overlap`，收到 `overlap_not_measured` 就不得声称「无重叠」。带 `target_leakage` 警告的 lift 不得采用，先修正定义再评。
7. 按 lift × 规模 × 可运营性排序，定下保留候选；然后对每个保留候选各调用一次 `sample_cohort_users` 抽 20 人，核对属性是否符合假设、无测试账号特征。抽样结论必须和同一条规则对应，不要把一个候选的样本写到另一个候选下。
8. 输出报告表。盘点中发现的已有分群问题（0 人、重叠 > 90%、引用已下线事件）附在末尾，只报告不处置。
9. 用户确认后，对选中候选 `validate_cohort_definition` → `create_cohort`，参数按 scoring.md 模板。

## 边界

- 只产出 RULE 规则分群，不做 SQL 分群、上传分群、聚类或预测评分。
- 自动创建一律 `calc_mode=STATIC`，名称以 `[AI候选] ` 开头，description 首行为 `[ai_mined]`；人工确认后再转 DYNAMIC。
- 评分只能来自工具返回的数字，不得凭印象判断人群价值。
- 不调用 `update_cohort`、`delete_cohort`、`recalculate_cohort`，不改动任何已有分群。
- 单次挖掘候选 ≤ 10、落库 ≤ 3，时间窗默认最近 30 天；先输出完整报告，再逐个落库。
- 用户未确认前不发起任何写调用。

## 输出

报告表列固定为：候选名 | 规则要点 | 人数 | 占活跃比例 | 目标 lift | 建议动作。表后给一到两句结论、数据范围限制，以及下一步：落库哪几个、是否交给 `wave-marketing-automation` 建 Campaign。
