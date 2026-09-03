# 用户列表参考

`query_user_list` 默认 `limit` 为 100，`with_total` 默认 true。`rule_group` 支持用户属性 `filter_by` 和已保存分群 `in_cohort`（`field.name=id`、`table_type=cohort`、`values=[cohort_id]`）。用户属性上的 OBJECT / OBJECT_ARRAY 筛选与分析模型相同，见 [filters.md](filters.md)：OBJECT 用 `parent.child`；OBJECT_ARRAY 用父属性 + `array_match_any/all` + `obj_filter`。

```json
{
  "logic": "and",
  "rules": [
    {
      "field": { "name": "country", "table_type": "user" },
      "operator": "eq",
      "values": ["US"]
    }
  ]
}
```

不要把 `user_did` / 行为序列硬塞进 `rule_group`，先存成分群或交给 `wave-sql-query`。

已保存分群优先用 `cohort_id` 调 `query_cohort_user_count`。只要人数、不要名单时不要拉用户列表。

定位具体用户：先 `search_users`，再 `get_user_profile` 或 `query_user_sequence`。

创建或更新分群前，用 `validate_cohort_definition` 校验完整规则。删除前用 `prepare_delete_cohort` 检查引用。
