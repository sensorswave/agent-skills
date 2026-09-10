---
name: wave-marketing-automation
description: >-
  基于真实项目资产规划和操作 Sensors Wave 营销自动化。适用于 5W1H Campaign 简报、
  复用已有 SMS/Webhook 通道、受众规划、Campaign 校验、Draft 创建、试发、生命周期操作
  和 Campaign 效果复盘。通用数据分析交给 wave-analytics，自定义 SQL 交给 wave-sql-query，
  产品用法问题交给 wave-product-help。
---

# Wave 营销自动化

## 目标

把营销需求转成有证据支撑、可执行的 Wave Campaign 方案，并且只执行用户要求的那一步生命周期操作。以当前项目的事件、属性、指标、分群、Campaign、治理规则和已有通道为唯一事实来源。不要用泛泛的营销建议或臆造的配置替代 MA 操作。

## 按需加载

- 各类操作的工具顺序、确认边界和复盘流程：[references/campaign-workflow.md](references/campaign-workflow.md)
- 设计、创建、带改动复制或更新 Campaign 之前：[references/5w1h-brief.md](references/5w1h-brief.md)
- 选通道、配内容、试发、创建/更新 Campaign 之前：[references/channel-reuse.md](references/channel-reuse.md)

## 工具

- 设计上下文：`get_ma_design_context`
- 已有资产：`list_cohorts`、`get_cohort_detail`、`list_ma_connections`、`get_ma_connection_detail`、`get_ma_sms_assets`、`list_ma_campaigns`、`get_ma_campaign_detail`、`get_ma_governance`
- 通道管理：`create_ma_connection`、`update_ma_connection`、`test_ma_connection`、`delete_ma_connection`
- 受众检查：`validate_cohort_definition`、`query_cohort_user_count`、`sample_cohort_users`、`inspect_ma_audience`、`create_cohort`、`update_cohort`、`recalculate_cohort`、`get_cohort_run_status`
- Campaign 规划：`plan_ma_campaign`、`validate_ma_campaign`、`create_ma_campaign`、`update_ma_campaign`、`copy_ma_campaign`
- 生命周期与内容：`test_ma_content`、`transition_ma_campaign`、`list_ma_campaign_operation_logs`
- 复盘：`get_ma_campaign_dashboard`、`query_event_analysis`、`query_funnel`

## 项目门禁

<!-- wave:project-gate -->
在调用其他项目级 MCP 工具前：

1. 调用 `list_projects`，展示 `project_id | name` 表格。
2. 等待用户回复数字 `project_id`。
3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

禁止静默挑选项目，也禁止在此步骤前开始任何 MA 发现、规划或写入。
<!-- /wave:project-gate -->

## 工作流

1. 先通过项目门禁，再判断请求类型：
   - 设计 / 创建 / 带改动复制 / 更新：走 5W1H 规划流程；
   - 读取 / 列表 / 详情 / 状态：直接查看目标资产，不强行要求新简报；
   - 试发 / 启动 / 恢复 / 暂停：先查看当前 Campaign 和通道，说明副作用，再走生命周期流程；
   - 效果复盘：用 Campaign dashboard，需要时把已校验的指标形态交给 `wave-analytics`。
2. 设计 Campaign 时先调用 `get_ma_design_context`。在提出任何配置之前，先发现真实的事件、属性、指标、分群、Campaign、已有通道、治理规则以及返回的 `context_id`。
3. 产出结构化的 `wave-ma-brief`，六个部分齐全：Why、Who、When、Where、What、How。证据状态保持可见；当某个关键决策仍会改变受众、时机、通道、内容、频控或成功衡量时，只问一个聚焦的澄清问题。
4. 优先复用匹配的已有通道。按 `connection_id` 选择，读取其安全详情，使用真实的 channel/provider/测试状态。没有合适通道时记录 `channel_strategy.mode=new`。只有在用户明确要求、已提供完整通道配置和只写凭证、并接受确认边界时，才用 `create_ma_connection` 创建。保存后用 `test_ma_connection` 测试，再读一次详情，然后回到 Campaign 规划。不要仅因为候选通道未测试就重复创建。
5. 用 `plan_ma_campaign` 构建 Campaign 方案，再用 `validate_ma_campaign` 校验完整方案。Webhook 的 `body` 或 SMS 的 `sign_name`/`template_id`/`variable_bindings` 写进 `content_config`，不要把文案留在 `description`。遵循 `required_action`：`soft_stale` / `reuse_plan` 时复用方案；`rebind` 时刷新 `get_ma_design_context` 并只重绑变化的依赖；只有 `replan` 或 `context_missing` 才重新规划。校验之后不要重建或悄悄改动方案。`safe_to_save` 为 false 时，先澄清或修复方案再创建或更新。内容为空可以保存 Draft，但不能启动。
6. 调用 `create_ma_campaign` 或 `update_ma_campaign` 之前，展示完整的 5W1H 简报和已校验方案，请用户明确确认保存 Draft。新 Draft 只用已校验的 `plan` 调 `create_ma_campaign`；已有 Draft 或已暂停的 Campaign 用同一份 plan 加 `get_ma_campaign_detail` 返回的 `campaign_id` 和 `expected_version` 调 `update_ma_campaign`。只保存与校验完全一致的方案。宿主或服务端另有确认流程时遵循它。用户要求设计 Campaign 不等于授权保存、发送或启动。
7. 只有用户明确要求该操作、且即时确认边界已满足时，才调用 `test_ma_content`、用于启动/恢复/暂停的 `transition_ma_campaign`，或其他有副作用的操作。用户没要求启动时，结果保持为 Draft。
8. 只有用户明确要求通道管理操作时，才更新或删除通道。先读当前详情；更新用 `connection_id` 加 `expected_version`，删除用 `connection_id` 加当前准确的 `expected_name`。绝不能把删除通道当作 Campaign 规划的清理步骤。
9. 复盘时先确定归因窗口和 Campaign 状态，再综合 dashboard 结果、操作日志、送达状态、频控治理和目标转化。说明数据范围和尚未解决的埋点注意事项。

## 不可逾越的边界

- 项目门禁未通过前，不要开始任何 MA 发现、规划或写入。
- 不要臆造事件名、属性、指标定义、分群 ID、Campaign ID、通道 ID、短信签名/模板、Webhook body 或 provider 细节。
- `connection_id` 和 `Connection` 仍是 MA 代码/API 契约。面向用户的表述用「通道」，但不要重命名或重新解释契约。
- `channel` 是通道类型；被选中的 connection 是项目中已有的实体。不要仅因为请求的类型是 SMS 或 Webhook 就新建通道。
- 绝不把 Webhook 的 URL/method/header/secret 或 SMS provider 凭证放进 Campaign 的 `content_config`。使用已选通道和已审核的 SMS 资产。
- 通道凭证是 `create_ma_connection` 和 `update_ma_connection` 的只写输入。绝不在摘要、工具输出、示例或后续消息中复述。
- `use_project_frequency` 保持显式。启用时读取治理规则，并在 How 里解释适用的项目/通道规则。
- 分群是可复用的受众状态；简单的一次性筛选用内联受众即可。不要为了实现实时触发而创建分群。
- 不要因为方案看起来有效就调用启动/恢复或发送/试发工具。有效不等于用户授权。
- `test_ma_connection` 测试的是已保存的通道本身并更新其最新测试状态；`test_ma_content` 测试的是 Campaign 内容和变量绑定，不能证明通道已可启动。

## 交接

- Campaign 上下文建立之后的指标、漏斗、留存或用户行为解读，交给 `wave-analytics`。
- 自定义 SQL 或分析模型无法表达的查询，交给 `wave-sql-query`。
- 已保存图表或 Dashboard，把已校验的指标/查询形态交给 `wave-dashboard-builder`。
- 埋点落地或埋点质检，使用对应的埋点 skill，不要把缺失事件当成 Campaign 问题处理。
- Wave 页面入口、权限或功能解释，用 `wave-product-help`。

## 输出

- 规划：简洁的 5W1H 简报、证据状态、选中/淘汰的通道候选、假设、待确认问题，以及下一个需要确认的操作。
- 创建/更新：Campaign 名称/id/状态、校验结果、确认状态，以及是否真的发送或启动了什么。
- 生命周期：操作、操作前后的 Campaign 状态、副作用摘要和服务端结果。
- 复盘：目标与受众、触发、通道/内容、频控/静默、发送/送达/失败/转化数字、归因窗口和注意事项。

## 停止

遇到以下情况停下来问用户：关键 5W1H 决策未定；没有合适的已测试通道且用户未授权创建/测试；校验不安全；请求的操作会在没有明确授权的情况下保存凭证、调用外部通道、删除、发送或启动；所需的 MCP 工具不可用。
