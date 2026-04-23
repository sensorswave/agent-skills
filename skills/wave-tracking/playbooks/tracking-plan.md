# Tracking Plan Playbook

用于 Tracking Plan 的起草、扩展、模板选择、写入和发布。

## 什么时候读

- 用户要“做埋点方案”
- 用户要创建 / 更新 / 发布 Tracking Plan
- 用户已经有事件草案，想落到 Wave 平台

如果用户还没有事件草案，或明确要求“根据当前代码 / 需求先设计埋点方案”，先切到 [../../wave-tracking-plan/SKILL.md](../../wave-tracking-plan/SKILL.md)。

## 执行步骤

1. 选择项目
   使用 `list_projects`，让用户明确选择 `project_id`。
   交互模板见 [../prompts/interaction.md](../prompts/interaction.md) 的 `P-项目`。

2. 盘点现有计划
   使用 `list_tracking_plans`。
   用户决定是在已有计划上扩展，还是新建。

3. 需要模板时再看模板
   使用 `list_tracking_plan_templates`，必要时再看 `get_template_detail`。
   不要默认把模板流程强塞给用户。

4. 起草计划
   在写入前，先把计划参数、事件列表、属性列表整理给用户确认。
   除计划名称、目标平台等关键字段外，描述、排序等非关键参数优先按当前项目和场景自动补默认值。
   可用工具包括：
   - `create_tracking_plan`
   - `add_tracking_plan_events`
   - `update_tracking_plan`
   - `update_tracking_plan_event`
   - `update_tracking_plan_property`
   - `sort_tracking_plan_events`

5. 发布前再确认一次
   若用户只是要方案草稿，到草稿态即可停止。
   只有明确要作为质检基线时，才调用 `publish_tracking_plan`。

6. 发布后不要自动继续
   发布成功后，先停下来，明确问用户下一步是否要创建 Dashboard。
   如果用户不想建看板，就停在这里；不要自动切到 Dashboard 或质检。

## 辅助规则

- 如果担心与现有埋点冲突，可先用 `list_events`、`list_event_properties` 对照已有 Catalog。
- 输出给用户时，优先用表格或结构化列表，而不是只回 MCP 原始字段。
- 交付内容至少要能让研发直接实现：事件、触发时机、端、属性定义、是否必填。

## 停止条件

- 用户只需要一版可讨论的草稿：停止在 draft
- 用户明确确认发布：执行 publish
- 发布完成后：先询问是否创建 Dashboard
- 用户转去做 SDK 接入：切换到 [../../wave-sdk-integration/SKILL.md](../../wave-sdk-integration/SKILL.md)
