# 假设库

先用 `list_events` 给项目事件分配角色：激活（首次关键动作）、核心（日常主行为）、意向（转化前一步，如加购 / 报价 / 试用）、转化（下单 / 支付 / 签约）、付费。模板里的事件名都是角色占位符，实例化时换成真实 `name`。阈值一律先查分布再定：次数用 `query_event_analysis` 的 `count_uv` / `p75` / `p90`，属性取值用 `list_property_values`。

| 模板 | 目标 | 规则骨架 | 阈值方法 | 成功指标 | 泄漏风险 |
|---|---|---|---|---|---|
| 注册未激活 | 激活 | `filter_by` 注册时间在近 N 天 + `user_did_not` 激活 | N = 注册到激活的中位时长 | 7 日激活率 | 目标即激活时，观察窗后移 |
| 完成 A 未完成 B | 转化 | `user_did` A ≥ 1 + `user_did_not` B，同一时间窗 | A、B 取漏斗相邻步骤 | B 完成率 | 目标即 B 时，观察窗后移 |
| 高意向未转化 | 转化 | `user_did` 意向 ≥ N + `user_did_not` 转化 | N 高于人均次数，常取 p75 | 转化率 | 同上 |
| 沉默风险 | 召回 | `user_did` 核心 ≥ 1（前窗）+ `user_did_not` 核心（后窗） | 后窗 = 正常访问周期 × 2 | 回访率 | 无 |
| 频次下降 | 召回 | `user_did` 核心（后窗）count < 阈值，前后窗对比用 SQL 判定 | 阈值取前窗 p50 的一半 | 回访率 | 无 |
| 付费后沉默 | 复购 | `user_did` 支付 ≥ 1（近 90 天）+ `user_did_not` 核心（近 14 天） | — | 复购率 | 目标即支付时，观察窗后移 |
| RFM 分位 | 复购 / 价值 | `user_did` 支付 `sum(金额) ≥ p90`，或 `count` 分层 | p50 / p90 | ARPU、复购率 | 无 |
| 功能采用 vs 未采用 | 激活 / 升级 | `user_did` 功能事件 ≥ N + `user_did_not` 付费 | N 取 p50 | 付费转化 | 目标即付费时，观察窗后移 |
| 回流 | 留存 | 前窗 `user_did_not` 核心 + 后窗 `user_did` 核心 | 沉默 ≥ 30 天 | 30 日留存 | 无 |
| 抑制 / 排除 | 所有 | `in_cohort` `not_in` 已转化分群；`user_did` `$MaMessageSent`（近 7 天）作为排除分群 | — | — | 无 |
| 反差切片 | 所有 | 事件维（platform 等）写在 `user_did.metric_rule.filter`；用户属性才用 `filter_by`。再加 `user_did $AnyEvent gte 1` 对齐定义窗，取 `group_by` 中偏离基线最多的取值 | 切片人数 ≥ 基线 0.5% | 该切片目标率 | 无 |

## DSL 骨架

行为规则放 `metric_rule`，属性规则放 `property_rule`，分群成员用 `in_cohort`（`operator` 可为 `in` / `not_in`）。`time_range` 用 `{"period":"last_7_days"}` 或 `from_date` / `to_date`。事件属性（如 `platform_type`）写在 `metric_rule.filter`，不要写成 `filter_by`。

`user_did_not` 的语义是「**不满足**该指标条件的用户」。「窗口内没做过 X」必须写成 `user_did_not X count gte 1`；写成 `user_did_not X count lt 1` 等于不排除任何人（没有人能满足 count < 1），`user_did X count lt 1` 则匹配不到任何人。`evaluate_cohort_definition` 遇到这两种写法会返回 `ineffective_rule` 警告，看到就改。

```json
{"logic":"and","rules":[
 {"type":"rule","rule":{"rule_type":"user_did","metric_rule":{"event":"<意向>","aggregator":"count","operator":"gte","values":[2],"time_range":{"period":"last_7_days"}}}},
 {"type":"rule","rule":{"rule_type":"user_did_not","metric_rule":{"event":"<转化>","aggregator":"count","operator":"gte","values":[1],"time_range":{"period":"last_7_days"}}}},
 {"type":"rule","rule":{"rule_type":"in_cohort","property_rule":{"field":{"name":"id","table_type":"cohort"},"operator":"not_in","values":[<已转化分群 id>]}}}
]}
```

顶层 `or` 且含 `sub_group` 的定义评估工具不接受；需要「或」时把 `or` 写成 `and` 下的一个 `sub_group`。
