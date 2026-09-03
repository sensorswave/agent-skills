# 留存分析参考

用 `query_retention` 分析初始事件之后的回访。筛选与分组见 [filters.md](filters.md)。

- `init_event`：形成队列的事件
- `return_event`：回访行为；看活跃留存时常常与初始事件相同
- 默认 `unit`：`day`
- 默认 `retention_period`：`{ "type": "in_each" }`
- 默认 `retention_mode`：`on`
- 只有用户要求或结果需要诊断时，才对比队列或分组
