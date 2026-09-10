# 通道复用与内容规则

## 选择顺序

1. 读 `get_ma_design_context`，查看其 `connections` 能力。
2. 需要时带上请求的 channel/provider 筛选条件调用 `list_ma_connections`。
3. 按 `connection_id` 选定一条项目中已有的通道。
4. 规划 Campaign 内容之前调用 `get_ma_connection_detail`。
5. SMS 场景调用 `get_ma_sms_assets`，选择变量能被完整绑定的已审核签名/模板。

UI 把这些资源叫「通道」。MA API 和代码继续使用 `Connection`、`connection_id` 和 `ConnectionService`。在工具输入输出中保留这些名字，即便向用户解释时也是如此。

## 匹配标准

优先选择满足以下条件的通道：

- 所需的 channel（`sms` 或 `webhook`）；
- SMS 所需的 provider；
- 最新测试状态（启动前要求 `passed`）；
- 兼容的限速和项目频控治理；
- 所需的模板变量或 payload 形态；
- 已有 Campaign 的引用只作为规划信号，不作为暴露密钥的理由。

多个候选都匹配时，用工具证据简短说明选择理由。当 provider、测试状态或版本会改变执行结果时，不要只凭名字选。

## 新建通道路径

`channel_strategy.mode = "new"` 可以记录「没有已有通道匹配」，但不构成创建授权。用户明确要求创建通道并提供完整配置和凭证时，在确认边界之后调用 `create_ma_connection`，然后在用户另行明确提出测试请求后调用 `test_ma_connection`。回到 Campaign 规划之前，再读一次新通道详情，使用其真实的 `connection_id`、版本和测试状态。

不要臆造 `connection_id`，不要把 Webhook URL 内联进 Campaign 内容，也不要把 SMS provider 凭证嵌进 Campaign 配置。不要仅因为匹配的已有通道未测试就新建一条；先提议测试已有实体。

## 通道管理

- `create_ma_connection` 创建新通道。`update_ma_connection` 需要 `connection_id + expected_version`，更新前先读详情。
- 所有凭证都视为只写。工具调用之后绝不复述。
- `test_ma_connection` 测试已保存的 URL/鉴权/provider 配置并更新 `test_status`；它会发出真实的外部请求或短信。
- `test_ma_content` 测试 Campaign 内容/变量绑定，不会更新通道的启动门禁状态。
- `delete_ma_connection` 需要当前 `connection_id` 和准确的 `expected_name`。仅在明确的删除请求下调用。已有 Campaign 引用会阻止删除；绝不为了让新的 Campaign 方案更简单而删除通道。

## 内容边界

- Webhook Campaign 只保存所选通道需要的 body/默认值。URL、method、header、鉴权和密钥留在通道里。
- SMS Campaign 保存已审核的签名、模板和完整的变量绑定。provider 凭证、回调 URL 和回调 token 不进入 Campaign。
- 所需模板变量无法从真实项目属性或受支持的绑定中获得时，把 What 标为 `needs_confirmation`，在校验或创建/更新之前停下。

## 启动门禁

所选通道的最新测试未通过时，绝不启动或恢复 Campaign。SMS 资产由服务端在启动时重新检查。通道有效不等于允许发送：启动和试发仍然需要用户明确的操作请求和服务端确认流程。
