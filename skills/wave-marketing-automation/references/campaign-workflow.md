# Campaign 操作流程

用能匹配用户请求的最小流程。只读查看、规划、创建或更新 Draft、试发、生命周期操作和效果复盘，各有不同的副作用边界。

## 规划与 Draft 创建/更新

新建 Campaign，或复制/更新且改变业务行为时，在项目门禁通过后按以下顺序执行：

```text
get_ma_design_context
→ 选择一条已有通道
→ get_ma_connection_detail
→ get_ma_sms_assets（仅 SMS）
→ 查看/查询受众，并校验任何要复用的分群定义
→ plan_ma_campaign
→ validate_ma_campaign
→ create_ma_campaign 或 update_ma_campaign
```

传给 `validate_ma_campaign` 和 `create_ma_campaign` / `update_ma_campaign` 的必须是同一份完整方案。简报在写入之前展示；模型不能从查到一个数字 ID 直接跳到创建 Campaign。调用 `create_ma_campaign` 或 `update_ma_campaign` 之前，请用户确认完整的已校验 Draft。仅要求设计 Campaign 不构成保存授权。

新 Draft 用 `create_ma_campaign`（只传 `plan`）。已有 Draft 或已暂停的 Campaign 用 `update_ma_campaign`（`plan` + `campaign_id` + `expected_version`）。

`safe_to_save=false` 阻止保存。`safe_to_launch=false` 阻止启动或恢复。解决具体的校验问题，而不是用文字把它解释掉。

## 配置契约

这些字段要显式写出，不要从已有 Campaign 推断。

- `content_config`（Webhook）：`{"body":"{\"ssid\":\"{{user.ssid}}\"}","variable_defaults":{"user.city":"unknown"}}`。不要把文案放在 `description`。企微/推送的 JSON 属于 `body`。
- `content_config`（SMS）：`{"sign_name":"...","template_id":"...","variable_bindings":{"name":{"mapping":"{{user.name}}","default":"用户"}}}`。
- `trigger_config`：`time_once` 用 `fire_date`；`time_recurring` 用 `granularity`/`n`/`start_date`/`fire_time`/`tz`；`action_done` 用 `trigger_event` + `active_duration`；`action_done_not_done` 还需要 `delay` 和 `cancel_event`。不要传 `frequency` 或 `time`。
- `in_cohort`：`field.name=id`、`table_type=cohort`、`operator=in`、`values=[cohort_id]`。
- `test_ma_content` 变量：只允许 `user.*`、`event.*`、`campaign.id`、`campaign.name`。绝不用 `message.*` 或 `content.*`。
- 空的 `content_config` 可以保存 Draft。`validate` 会把 `content_missing` 报为启动阻塞项（`safe_to_launch=false`）。启动和试发都需要真实的 body。
- `context_id` 是 catalog 的 ETag。分群人数等运行时统计不会让它变化。遇到 `soft_stale` 或 `required_action=reuse_plan` 时复用当前方案；遇到 `stale` / `dep_stale` / `required_action=rebind` 时刷新 `get_ma_design_context` 并只重绑变化的依赖；只有 `required_action=replan` 或 `context_id` 缺失时才重新规划。

没有合适通道时，把 Campaign 规划停在 Where 这一步。用户明确要求创建通道时，执行 `create_ma_connection → test_ma_connection → get_ma_connection_detail`，然后重新获取 MA 设计上下文再做规划/校验，让新通道进入证据快照。

## 精确复制

用户明确要求精确复制时，可以在读取源 Campaign 详情之后使用 `copy_ma_campaign`。用户想改任何行为、受众、时机、内容、通道、频控或目标时，走完整规划流程并校验得到的方案。

## 只读查看

Campaign ID 未知时先 `list_ma_campaigns`，再 `get_ma_campaign_detail`。通道 ID 未知时先 `list_ma_connections`，再 `get_ma_connection_detail`。只读查看不要求完整的 5W1H 简报，但不要臆造缺失的事实。

## 试发与生命周期

- `test_ma_content` 会走真实的 SMS/Webhook 发送路径。调用前说明目的地/副作用，并要求用户明确提出试发请求。
- `transition_ma_campaign` 可以启动、恢复、暂停或停止 Campaign。启动和恢复会造成真实的客户触达；需要用户明确意图和服务端确认流程。
- 用户没要求启动/恢复时，成功的创建/更新保持为 Draft。
- 用 `list_ma_campaign_operation_logs` 解释状态变化或自动暂停。

## 通道生命周期

- 创建/更新：先读已有候选。只有明确的通道管理请求才调用 `create_ma_connection` 或 `update_ma_connection`。更新使用当前 `expected_version`；未传的字段保持不变。
- 测试：说明真实目的地和副作用之后才调用 `test_ma_connection`。通过的结果会更新通道测试状态。
- 删除：读当前安全详情，展示 ID/名称/引用关系，仅在用户明确确认删除后调用 `delete_ma_connection`。绝不从设计或清理 Campaign 的请求中推断出删除权限。

## 效果复盘

1. 读 `get_ma_campaign_dashboard`，拿到归因窗口和查询模板。
2. 需要更深的转化分析时，用返回的查询形态调 `query_event_analysis` 或 `query_funnel`。
3. 综合发送、送达、失败、目标转化、频控治理、操作日志和埋点注意事项。区分送达和转化。

更宽泛的趋势、漏斗、留存或用户行为解读，保留 Campaign 上下文后交给 `wave-analytics`。自定义 SQL 交给 `wave-sql-query`。

## 停止条件

出现以下情况时停下来澄清：关键 5W1H 部分未定；没有匹配的已测试通道；所需 SMS 资产无法绑定；校验不安全；用户尚未授权有副作用的操作。
