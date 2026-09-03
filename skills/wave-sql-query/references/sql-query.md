# SQL 查询参考

编写 `query_custom_sql` 前阅读本文。列名和类型以当前项目 `get_sql_schema` 为准。时区、当前时间和周起始以 `get_project_context` 为准。

## 什么时候用 SQL

SQL 用于分析模型覆盖不了的问题：多表关联、跨事件对齐同一元素、行为条件找人、分群交集、临时探查，或用户明确要求 SQL。

不要用 SQL 去「复刻」事件分析、漏斗分析、留存分析。`WINDOW_FUNNEL` / `RETENTION` 是 Doris 函数，和产品分析模型的计算结果不能直接对比。

## 可查询的表

MCP 只能查询下面四张表，禁止写 `project_db.events` 这种库表限定名。

| 表 | 一行代表 | 用途 |
|---|---|---|
| `events` | 一次事件 | 行为明细、事件聚合、事件发生时的用户属性快照 |
| `users` | 一个用户 | 最新用户画像 |
| `cohorts` | 某分群中的一个用户 | 按分群筛选或比较；只有当前活跃版本成员 |
| `query_log` | 一次查询 | 耗时、扫描量、错误诊断 |

`events` 固定列：`time`、`event_id`、`distinct_id`、`trace_id`、`anon_id`、`login_id`、`event`、`ssid`、`received_at`、`created_at`、`updated_at`。其余是动态属性列。

`users` 固定列：`ssid`、`login_id`、`anon_id`、`created_at`、`updated_at`、`aid`。其余是 `u_*`。

`cohorts` 只有 `cohort_id`、`ssid`。

## 从属性找到 SQL 列名

属性名在入库时强制转小写，Catalog 和 Schema 中的属性名都是小写；只差大小写的名字是同一个属性。显示名不能写入 SQL。

用 `list_event_properties` / `list_user_properties` 拿到小写逻辑名后，按固定规则生成列名：

- 系统保留列：列名等于属性名，不加前缀
- 其他事件属性：`e_` + 属性名
- 其他用户属性：`u_` + 属性名

`get_sql_schema` 用来确认列已存在、查看存储类型，并从列反查 Catalog 属性。每列的 `comment` 是本地化展示名；`property` 给出 `name`、`display_name`、`table_type`、`data_type`、`physical_data_type`。`OBJECT` / `OBJECT_ARRAY` 的子属性在 `property.children` 里，不是独立 SQL 列。HTTP 和 MCP 都不返回 `property.description`。

### 哪些列不加 `e_` / `u_`

系统保留列是表结构里的固定字段，列名等于逻辑名，**不要**加前缀。

`events`：`time`、`event_id`、`trace_id`、`anon_id`、`login_id`、`event`、`ssid`、`distinct_id`、`received_at`、`created_at`、`updated_at`。

`users`：`ssid`、`login_id`、`anon_id`、`created_at`、`updated_at`、`aid`。

这些列的查询口径：

| 列 | 含义 | SQL 用法 |
|---|---|---|
| `time` | 事件发生时间 | 时间筛选和按日截断用这一列 |
| `event` | 事件名称 | `WHERE event = 'Purchase'` |
| `ssid` | 服务端用户唯一 ID | 用户去重、关联 `users` / `cohorts` 都用它：`COUNT(DISTINCT ssid)` |
| `login_id` | 登录 ID，匿名用户可为空 | 按账号查人；不要用来做 UV |
| `anon_id` | 匿名 ID，可为空 | 设备 / 浏览器标识，不是 UV 口径 |
| `distinct_id` | 客户端唯一 ID | 入库键的一部分，不是分析 UV 口径 |
| `event_id` | 事件名哈希 | 查询加速，不要当成事件次数 |
| `trace_id` | 客户端事件去重 ID | 事件去重，不是用户 ID |
| `received_at` / `created_at` / `updated_at` | 接收 / 入库 / 更新时间 | 诊断链路用；业务时间范围用 `time` |

### 哪些列要加前缀

埋点上报的动态属性都要加前缀。事件属性加 `e_`，用户属性加 `u_`。以 `$` 开头的预置属性同样加前缀，不是固定列。

| 逻辑属性 | 所在表 | SQL 列 | 说明 |
|---|---|---|---|
| `$os` | `events` | `e_$os` | 预置事件属性 |
| `category` | `events` | `e_category` | 自定义事件属性 |
| `$first_seen_time` | `events` / `users` | `u_$first_seen_time` | 预置用户属性 |
| `vip_level` | `events` / `users` | `u_vip_level` | 自定义用户属性 |

含 `$` 的列名必须用反引号：`` `e_$os` ``、`` `u_$first_seen_time` ``。

### 用户属性：快照优先，最新画像再 JOIN

`events.u_*` 是事件发生时的用户属性快照；`users.u_*` 是用户当前最新画像。同一属性在两张表里的值可能不同。

查用户属性时，默认读 `events.u_*`，与分析模型默认策略一致。只有用户明确要求「当前 / 最新」用户属性时，才 `JOIN users` 并用 `users.u_*`。不要为了读快照去 JOIN `users`。

## 时区

自定义 SQL 同时使用两套时区。MCP 禁止 `SHOW` / `SET`，不要用 `query_custom_sql` 去查会话变量。执行时系统已经把会话 `time_zone` 设为项目时区，因此 `NOW()`、`CURRENT_TIMESTAMP()`、`CURDATE()` 返回的是项目时区的当前时间。

| 时区 | 含义 |
|---|---|
| 存储时区 | 服务端写入 `DATETIME` 的默认时区，由集群决定，不能改。以 `get_project_context` 的 `storage_timezone` 为准 |
| 项目时区 | 用户希望分析使用的默认时区，会话 `time_zone`。以 `get_project_context` 的 `project_timezone` 为准 |

写时区相关 SQL 前调用 `get_project_context`。解释「今天 / 本周」时用 `now_project`；按周聚合时用 `week_starts_on`。

保持存储时区、不会随项目时区自动转换的字段：

- 系统时间列：`events.time`、`events.received_at`、`events.created_at`、`users.created_at`、`users.updated_at`
- 逻辑类型为 `DATETIME` 的属性，例如 `e_paid_at`、`` `u_$first_seen_time` ``

因此 `DATE_TRUNC(time, 'day')` 截断的是存储时区的日历日。`UNIX_TIMESTAMP(time)` 会按项目时区解释存储时区的本地时间，两套时区不一致时会偏移。

项目时区与存储时区一致时，可以直接比较 `time` 和 `NOW()`。不一致时用 `CONVERT_TZ`：第一个时区参数填当前存储时区，第二个填目标时区；项目时区用 `@@session.time_zone`。

按项目时区统计日活（把 `<storage_timezone>` 换成当前存储时区）：

```sql
SELECT
  DATE_TRUNC(CONVERT_TZ(time, '<storage_timezone>', @@session.time_zone), 'day') AS activity_date,
  COUNT(DISTINCT ssid) AS active_users
FROM events
WHERE time >= CONVERT_TZ('2026-08-01 00:00:00', @@session.time_zone, '<storage_timezone>')
  AND time < CONVERT_TZ('2026-09-01 00:00:00', @@session.time_zone, '<storage_timezone>')
GROUP BY activity_date
ORDER BY activity_date;
```

`WHERE` 中的 `time` 不要先套 `CONVERT_TZ` 再过滤。把边界转到存储时区后，再比较原始 `time` 列，才能命中按月分区。

## 逻辑类型与存储类型

Schema 展示的是父属性列的存储类型。比较、分组、聚合前按存储类型处理。

| 逻辑类型 | 存储类型 | 写法 |
|---|---|---|
| `STRING` | `STRING` | 字符串比较 |
| `NUMBER` | `BIGINT` / `DOUBLE` | 直接比较和聚合 |
| `BOOLEAN` | `BOOLEAN` | `TRUE` / `FALSE` |
| `DATETIME` | `DATETIME(3)` | 日期时间函数 |
| `ARRAY` | `ARRAY<...>` | 数组函数或 `EXPLODE` |
| `OBJECT` | `VARIANT` | `col['child']` 后再 `CAST` |
| `OBJECT_ARRAY` | `VARIANT` | 先转 `ARRAY<JSON>`，再提取元素 |

`OBJECT` / `OBJECT_ARRAY` 的子属性不是独立表列。从父列的 `property.children` 读取子属性名和 `physical_data_type`，不要猜测嵌套路径。

## ARRAY

`ARRAY_CONTAINS` 的比较值类型必须与元素类型一致。条件判断用 `ARRAY_MATCH_ANY` / `ARRAY_MATCH_ALL`。分组前先在内层选出数组列，再用 `LATERAL VIEW EXPLODE`；每个元素会变成一行。

## OBJECT

不要直接对 `VARIANT` 子列做数值比较或聚合。先按子属性存储类型 `CAST`：

```sql
CAST(e_profile['city'] AS STRING)
CAST(e_profile['age'] AS BIGINT)
CAST(e_profile['score'] AS DOUBLE)
CAST(e_profile['is_member'] AS BOOLEAN)
CAST(e_profile['registered_at'] AS DATETIME(3))
```

筛选、分组、聚合使用同一套转换表达式。

## OBJECT_ARRAY

不能写 `e_items['sku']`。方括号只适用于单个 `OBJECT`。对象数组按三步处理：

1. `JSON_EXTRACT(e_items, '$')`
2. `CAST(... AS ARRAY<JSON>)`
3. 用 `JSON_EXTRACT_*` 读每个元素的子属性

基础表达式：

```sql
CAST(JSON_EXTRACT(e_items, '$') AS ARRAY<JSON>)
```

| 子属性存储类型 | 提取函数 |
|---|---|
| `STRING` | `JSON_EXTRACT_STRING(item, '$.sku')` |
| `BIGINT` | `JSON_EXTRACT_BIGINT(item, '$.quantity')` |
| `DOUBLE` | `JSON_EXTRACT_DOUBLE(item, '$.price')` |
| `BOOLEAN` | `JSON_EXTRACT_BOOL(item, '$.is_gift')` |
| `DATETIME(3)` | `CAST(JSON_EXTRACT_STRING(item, '$.paid_at') AS DATETIME(3))` |

判断是否存在满足条件的元素用 `ARRAY_MATCH_ANY`；全部满足用 `ARRAY_MATCH_ALL`。需要同时用多个子属性时，只 `EXPLODE` 一次完整对象数组，再从同一个 `item` 提取字段。分别展开多个子属性数组会形成笛卡尔积，统计值会被放大。

`users` 表用法相同，列名换成 `u_*`。

## 虚拟事件和虚拟属性

- 虚拟事件不会在自定义 SQL 中自动展开。`events.event` 存的是实际上报事件名。用 `list_events` 看到 `is_virtual=true` 时，把返回的构成条件写成等价 `event` / 属性过滤，不要把虚拟事件名当成 `event` 值。
- 虚拟属性不会作为列出现在 Schema 中。看到 `is_virtual=true` 后，读取表达式，把 `{event.xxx}` / `{user.xxx}` / `{user.xxx@latest}` / `{user.xxx@snapshot}` 换成实际列，再写入 SQL。不要直接复制带占位符的表达式。
- `{user.xxx@snapshot}` 对应 `events.u_*`；`{user.xxx@latest}` 对应 `users.u_*`。保留用户列如 `ssid` 仍然不加 `u_` 前缀。

## MCP 约束

- 只允许一条 `SELECT` 或 `WITH ... SELECT`。
- 禁止 `INSERT`、`UPDATE`、`DELETE`、`DROP`、`ALTER`、`CREATE`、`SHOW`、`SET`、`EXPLAIN`、`USE`。
- 禁止多语句、表函数和 `db.table` 限定名。
- 允许的表只有 `events`、`users`、`cohorts`、`query_log` 以及本条 SQL 里定义的 CTE 名。
- 明细查询加 `LIMIT`。普通查询最多返回 10,000 行，系统不会把 `LIMIT` 写进 SQL。
- 不要在 SQL 字面量中写入密码、密钥、身份证号等敏感信息。

## 性能

1. 查 `events` 时先限制 `time` 和 `event`。
2. 不要 `SELECT *`，尤其不要一次拉回大型数组或 `VARIANT` 列。
3. 先过滤再 `EXPLODE`。
4. 可用 `query_log` 看 `cost_time_ms`、`scan_rows`、`scan_bytes`、`peak_memory_bytes`。`status` 实际值为 `Running`、`Completed`、`Failed`、`Canceled`。

## 常见失败

- 把显示名或逻辑属性名当成列名，漏了 `e_` / `u_`，或给 `time` / `event` / `ssid` 加了前缀。
- 用 `login_id`、`anon_id` 或 `distinct_id` 做用户去重。UV 必须是 `COUNT(DISTINCT ssid)`。
- 查用户属性时默认 JOIN 了 `users`。快照在 `events.u_*`，只有明确要最新画像才 JOIN。
- `$` 列没有反引号。
- 把 `OBJECT_ARRAY` 写成 `e_items['sku']`。
- 对 `VARIANT` 子列直接比较，没有 `CAST`。
- 把虚拟事件名、虚拟属性名当成物理列。
- 在 `WHERE time` 上套 `CONVERT_TZ`，导致无法命中分区。
- 项目时区与存储时区不同时，按天聚合结果与事件分析不一致。
