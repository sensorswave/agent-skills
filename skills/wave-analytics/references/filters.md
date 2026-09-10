# 筛选与分组

构造事件分析、漏斗、留存的 `filter` / `group_by`，以及用户列表 `rule_group` 时阅读本文。先用 `list_event_properties` / `list_user_properties` 确认属性的 `name` 和 `data_type`，查询参数用 `name`，不用显示名。`list_*` 与 `get_resource` 会在 `usage_hint` 中给出同一套规则：OBJECT 筛选用 `parent.child`；OBJECT_ARRAY 筛选只用父属性 + `array_match_any/all` + `obj_filter`；分组才写 `parent.child`。

## 通用形态

筛选：

```json
{
  "logic": "and",
  "conditions": [
    {
      "type": "condition",
      "condition": {
        "field": { "name": "<property>", "table_type": "event" },
        "operator": "eq",
        "values": ["<value>"]
      }
    }
  ]
}
```

分组：

```json
"group_by": [{ "name": "<property>", "table_type": "event" }]
```

每条 condition 都要带 `type: "condition"`。`table_type` 为 `event` 或 `user`。下面示例只写出 `condition` 或分组字段；嵌进上面的结构即可。`equal`、`contain`、`is_set` 等别名也可以，服务端会规范化。

操作符或字段写错时，按 `data_type` 修正后重试。不要去掉筛选后再把全站结果当作原问题的答案。

## STRING

操作符：`eq`、`ne`、`in`、`not_in`、`contains`、`not_contains`、`is_empty`、`is_not_empty`、`is_null`、`is_not_null`。

筛选：

```json
{
  "field": { "name": "$os", "table_type": "event" },
  "operator": "eq",
  "values": ["iOS"]
}
```

分组：

```json
{ "name": "$os", "table_type": "event" }
```

## NUMBER

操作符：`eq`、`ne`、`gt`、`gte`、`lt`、`lte`、`between`、`in`、`not_in`、`is_null`、`is_not_null`。

筛选：

```json
{
  "field": { "name": "price", "table_type": "event" },
  "operator": "gte",
  "values": [100]
}
```

分组：

```json
{ "name": "price", "table_type": "event" }
```

## BOOLEAN

操作符：`is_true`、`is_false`、`is_null`、`is_not_null`。

筛选：

```json
{
  "field": { "name": "is_vip", "table_type": "user" },
  "operator": "is_true"
}
```

分组：

```json
{ "name": "is_vip", "table_type": "user" }
```

## DATETIME

操作符：`eq`、`gt`、`gte`、`lt`、`lte`、`between`、`is_null`、`is_not_null`。日期值用 `YYYY-MM-DD` 或带时间的字符串。

筛选：

```json
{
  "field": { "name": "paid_at", "table_type": "event" },
  "operator": "between",
  "values": ["2026-08-01", "2026-08-31"]
}
```

分组：

```json
{ "name": "paid_at", "table_type": "event" }
```

## ARRAY

筛选操作符与字符串/数值不同：用 `contains`、`not_contains`、`contains_all`、`set_eq`、`is_empty`、`is_not_empty`。不要用 `eq`。

筛选：

```json
{
  "field": { "name": "tags", "table_type": "event" },
  "operator": "contains",
  "values": ["new"]
}
```

分组用数组属性名，服务端会按元素展开：

```json
{ "name": "tags", "table_type": "event" }
```

元素级条件也可用 `array_match_any` / `array_match_all`；此时 `obj_filter` 里子字段名留空。

## OBJECT

筛选和分组都写到子字段，字段名为 `parent.child`，操作符按子字段的 `data_type` 选择。

筛选：

```json
{
  "field": { "name": "address.city", "table_type": "user" },
  "operator": "eq",
  "values": ["Shanghai"]
}
```

分组：

```json
{ "name": "address.city", "table_type": "user" }
```

## OBJECT_ARRAY

筛选写父属性，用 `array_match_any`（任一元素满足）或 `array_match_all`（全部元素满足），子字段条件放在 `obj_filter`。`obj_filter` 里的 `field.name` 只写子字段名，例如 `item_name`。不要用 `eq` / `contains` 筛父属性，也不要把 `items.item_name` 当作筛选字段。

筛选：

```json
{
  "field": { "name": "items", "table_type": "event" },
  "operator": "array_match_any",
  "obj_filter": {
    "logic": "and",
    "conditions": [
      {
        "type": "condition",
        "condition": {
          "field": { "name": "item_name" },
          "operator": "eq",
          "values": ["SKU-1"]
        }
      }
    ]
  }
}
```

分组写 `parent.child`，不要对父属性分组：

```json
{ "name": "items.item_name", "table_type": "event" }
```

## 分群 DSL

`filter_by` / `filter_by_not` 只接受用户属性（`list_user_properties`，`table_type=user`）。事件属性（如 `platform_type`）写在 `user_did.metric_rule.filter`，`table_type=event`；取值用 `list_property_values`，不要猜。
