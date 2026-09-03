# 事件分析参考

用 `query_event_analysis` 做事件次数、独立用户、属性聚合、趋势和分组。筛选与分组见 [filters.md](filters.md)。

| 用户说法 | aggregator | 是否需要 property |
|---|---|---|
| 总次数 / PV / count | `count` | 否 |
| 独立用户 / UV / DAU | `uv` | 否 |
| 人均次数 | `count_uv` | 否 |
| 属性求和 | `sum` | 是 |
| 人均求和 / ARPU | `sum_uv` | 是 |
| 属性均值 | `avg` | 是 |
| 最大 / 最小 | `max` / `min` | 是 |
| 去重属性个数 | `dis_count` | 是 |
| 中位数 / 分位数 | `median` / `p90` / `p99` | 是 |

数组属性或对象数组子字段要先做行内聚合时，加 `array_aggregator`：`array_sum` / `array_avg` / `array_max` / `array_min` / `array_size`，再由 `aggregator` 做跨事件聚合。嵌套子字段的 `property` 写成 `parent.child`。

`label` 是内部序列键 A/B/C，业务名放在 `name`。已保存指标优先用 `list_metrics` 得到的 `id`。

按时间范围选择粒度：1–3 天用 `hour`，4–30 天用 `day`，1–3 个月用 `week`，3–12 个月用 `month`，更长用 `quarter` 或 `year`。

用户未指定时：时间范围最近 30 天；分组 `limit` 为 10。

交给 `wave-dashboard-builder` 时提供：已验证的事件 / 属性 / 筛选 / 时间范围，以及推荐图表类型。
