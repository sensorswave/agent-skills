# Tracking Plan Playbook

用于 Tracking Plan 的起草、扩展、模板选择、写入和发布。

## 什么时候读

- 用户要“做埋点方案”
- 用户要创建 / 更新 / 发布 Tracking Plan
- 用户已经有事件草案，想落到 Wave 平台

如果用户还没有事件草案，或明确要求“根据当前代码 / 需求先设计埋点方案”，先读取 [code-discovery.md](code-discovery.md) 和 [draft-output.md](draft-output.md)。

## 执行步骤

1. 选择项目
   使用 `list_projects`，让用户明确选择 `project_id`。
   交互模板见 [../prompts/interaction.md](../prompts/interaction.md) 的 `P-项目`。

2. 盘点现有计划
   使用 `list_tracking_plans`。
   用户决定是在已有计划上扩展，还是新建。
   若用户要继续 Pipeline、SDK、代码改造或 Dashboard 等后续流程：
   - 已发布且本次不修改的计划：读取详情并作为本次实施基线
   - 草稿计划：必须先完成并发布
   - 新建或本次更新的计划：必须在本次流程发布后才能继续

3. 需要模板时再看模板
   使用 `list_templates`，必要时再看 `get_template_detail`。
   不要默认把模板流程强塞给用户。

4. 起草计划
   在写入前，先把计划参数、事件列表、属性列表整理给用户确认。
   除计划名称、目标平台等关键字段外，描述、排序等非关键参数优先按当前项目和场景自动补默认值。
   使用 `create_tracking_plan` 创建新草稿，或用 `update_tracking_plan` 替换已有草稿快照：
   - 新建：调用 `create_tracking_plan`，不要传 `plan_id`
   - 更新：先调用 `get_tracking_plan_detail`，本地合并后再调用 `update_tracking_plan` 并传 `plan_id` 与完整事件/属性快照，避免遗漏项被移除
   - 初次草稿写入不要设置 `publish=true`；草稿创建或更新成功后按步骤 5 单独展示发布摘要并取得发布确认

5. 发布前再确认一次
   若用户只是要方案草稿，到草稿态即可停止。
   若用户要继续 Pipeline、SDK、埋点代码或 Dashboard，已发布的 Tracking Plan 是强制前置条件：
   - 本次新建或更新计划后，立即展示待发布计划摘要，并要求用户明确回复“确认发布”
   - 收到明确确认后调用 `publish_tracking_plan`
   - 发布成功前禁止执行任何后续流程；用户拒绝或推迟发布时停在草稿态
   - 已有计划若已发布且本次未修改，可以直接作为基线，无需重复发布

6. 发布后不要自动继续
   发布成功后，先停下来，明确让用户选择停止、创建 Dashboard，或继续 Pipeline / SDK / 代码改造。
   不要仅凭发布成功自动切到任何后续流程，也不要自动进入质检。

## 辅助规则

- 如果担心与现有埋点冲突，可先用 `list_events`、`list_event_properties` 对照已有 Catalog。
- 输出给用户时，优先用表格或结构化列表，而不是只回 MCP 原始字段。
- 交付内容至少要能让研发直接实现：事件、触发时机、端、属性定义、是否必填。

## 停止条件

- 用户只需要一版可讨论的草稿：停止在 draft
- 用户还要继续实施但计划未发布：请求确认发布，并在获得确认前停止
- 用户明确确认发布：执行 publish；只有发布成功后才解除后续流程门禁
- 发布完成后：先让用户选择停止、Dashboard 或 Pipeline / SDK / 代码改造
- 用户在计划发布后转去做 SDK 接入：读取 [../references/sdk-matrix.md](../references/sdk-matrix.md)
