---
name: wave-tracking
description: >-
  根据代码、PRD 或用户流程设计并落地 Sensors Wave 埋点。适用于设计事件与属性、
  划分客户端/服务端职责、制定 identify/reset 策略、写入或发布 Tracking Plan、
  创建/复用 Pipeline，以及生成 SDK 接入指引。线上埋点质检交给
  wave-tracking-validation；保存图表或 Dashboard 交给 wave-dashboard-builder。
---

# Wave 埋点落地

## 目标

产出或执行一套产品/研发团队可以直接使用的埋点落地方案：以 Tracking Plan 为主线，已发布的计划是进入 Pipeline/SDK 接入、代码改动或看板交接之前的强制基线。

## 先加载

- 任何项目级 MCP 调用或写操作之前，先读 [policies/operating-rules.md](policies/operating-rules.md)。
- 需要统一确认措辞时，读 [prompts/interaction.md](prompts/interaction.md)。

## 按需加载

- 代码或 PRD 盘点：[playbooks/code-discovery.md](playbooks/code-discovery.md)
- 草稿输出格式：[playbooks/draft-output.md](playbooks/draft-output.md)
- 事件/属性设计规则：[references/tracking-principles.md](references/tracking-principles.md)
- 登录、登出、匿名转登录、跨设备：[references/user-identification.md](references/user-identification.md)
- Pipeline/SDK 配置与文档链接：[references/sdk-matrix.md](references/sdk-matrix.md)
- Tracking Plan 写入/发布：[playbooks/tracking-plan.md](playbooks/tracking-plan.md)

## 工具

- 发现：`list_events`、`list_event_properties`、`list_user_properties`
- Tracking Plan：`list_tracking_plans`、`get_tracking_plan_detail`、`list_templates`、`get_template_detail`、`create_tracking_plan`、`update_tracking_plan`、`publish_tracking_plan`
- Pipeline/SDK：`list_pipelines`、`get_pipeline_detail`、`create_pipeline`

## 项目门禁

<!-- wave:project-gate -->
在调用其他项目级 MCP 工具前：

1. 调用 `list_projects`，展示 `project_id | name` 表格。
2. 等待用户回复数字 `project_id`。
3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

禁止静默挑选项目，也禁止在此步骤前调用 Catalog、Tracking Plan、Pipeline 或 SDK 工具。
<!-- /wave:project-gate -->

## 工作流

1. 判断请求是「仅设计」还是「落地」。Pipeline/SDK 接入、代码改动和看板交接都属于 Tracking Plan 之后的落地阶段。
2. 先通过项目门禁，再调用任何其他项目级 MCP 工具。
3. 在发明新名字或新建计划之前，先盘点已有 Catalog 和 Tracking Plan。
4. 设计类工作：产出包含事件、触发时机、平台/客户端/服务端归属、属性、是否必填以及 identify/reset 处理方式的草稿。
5. 写入 Tracking Plan 时，调用 `create_tracking_plan` 或 `update_tracking_plan` 之前先展示完整的草稿快照。新草稿用 `create_tracking_plan`，不传 `plan_id`；已有草稿用 `update_tracking_plan`，传 `plan_id` 和完整的事件/属性快照，未包含的事件/属性可能被移除。
6. 已发布的 Tracking Plan 是每个后续落地阶段的硬门禁。若选中的是一份已发布且本次不改动的计划，读取详情并作为基线。若选中的是草稿，或本次流程新建/更新了计划，先持久化完整草稿，随即请求用户明确确认发布，并在本次流程中完成发布后再继续。
7. 基线计划未发布时，禁止调用 Pipeline 工具、提供项目专属的 SDK 接入或埋点代码、修改埋点代码，或交接给看板构建。用户拒绝或推迟发布时，停在草稿态并说明后续工作被未发布的计划阻塞。
8. 只有在用户明确确认后才发布。不要把「继续实施」的请求当作发布确认。
9. 发布后的 SDK/Pipeline 工作，使用 MCP 返回的 `endpoint` 和 `source_token`，不要手工拼。
10. 发布后如果用户要图表或看板，把相关事件、属性和预期指标交给 `wave-dashboard-builder`。

## 边界

- 项目门禁未通过前，不要调用 Catalog、Tracking Plan、Pipeline 或 SDK 工具。
- 不要在这里做线上埋点质检。只有用户确认事件已经上报并要求检查时，才交给 `wave-tracking-validation`。
- 不要在这里维护已有 Catalog 的文档字段，交给 `wave-catalog-governance`。
- 不要在这里做深度数据解读，交给 `wave-analytics` 或 `wave-sql-query`。
- 不要在这里创建已保存图表或 Dashboard，交给 `wave-dashboard-builder`。
- 不要替用户重启、重新部署、重新构建或操作其应用/设备/服务器。告诉用户需要手动执行什么。

## 输出

- 设计草稿：事件表、属性表、identify/reset 方案、待确认问题。
- 写入/发布结果：计划 id/名称/状态，以及改了什么。
- SDK 结果：选定的 Pipeline、endpoint/source_token 来源、SDK 文档链接、初始化与 identify/reset 的放置位置。
- 看板交接：为 `wave-dashboard-builder` 汇总目标事件、指标和建议图表类型。

## 停止

除非用户明确确认发布且发布成功，否则停在未发布的草稿。代码/SDK 改动之后，请用户手动重启/重新部署并验证事件已上报，然后才考虑交接质检。
