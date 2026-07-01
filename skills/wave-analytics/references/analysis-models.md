# Analysis Models Reference

Use this file only when building concrete Wave analysis queries or saved chart inputs.

## Event Analysis

Use `query_event_analysis` for event counts, unique users, property aggregations, trends, and breakdowns.

Aggregator mapping:

| User asks | aggregator | property |
|---|---|---|
| total events / PV / count | `count` | no |
| unique users / UV / DAU | `uv` | no |
| per-user frequency | `count_uv` | no |
| sum of property | `sum` | yes |
| per-user sum / ARPU | `sum_uv` | yes |
| average property | `avg` | yes |
| max/min property | `max` / `min` | yes |
| distinct property count | `dis_count` | yes |
| median / percentile | `median` / `p90` / `p99` | yes |

Choose time unit by range: 1-3 days `hour`, 4-30 days `day`, 1-3 months `week`, 3-12 months `month`, longer `quarter` or `year`.

## Funnel

Use `query_funnel` for ordered or unordered conversion across at least two steps.

- Default `funnel_mode`: `in_order`
- Default `measure_type`: `rate`
- Default window: 7 days
- Use `measure_type=time` with `time_agg` when the user asks conversion duration.
- Explain both overall conversion and the largest adjacent drop-off.

## Retention

Use `query_retention` for return behavior after an initial event.

- `init_event`: cohort-forming event
- `return_event`: return behavior, often the same event for active retention
- Default `unit`: `day`
- Default `retention_period`: `{ "type": "in_each" }`
- Default `retention_mode`: `on`
- Compare cohorts or groups only when the user asks or the result needs diagnosis.

## User List And Cohorts

Use `query_user_list` to fetch users matching property or behavior rules. Keep default limit at 100.

Use `query_cohort_user_count` when the user asks for count only and does not need individual users.

Use `get_user_profile` or `query_user_sequence` for one specific user, issue diagnosis, or timeline reconstruction.

## Filters

Filter shape:

```json
{
  "logic": "and",
  "conditions": [
    {
      "type": "condition",
      "condition": {
        "field": { "name": "<property>", "table_type": "event" },
        "operator": "equal",
        "values": ["<value>"]
      }
    }
  ]
}
```

Common operators: `equal`, `not_equal`, `contain`, `greater`, `greater_or_equal`, `less`, `less_or_equal`, `between`, `is_set`, `is_not_set`, `is_true`, `is_false`.

## Custom SQL

Use `get_sql_schema` before `query_custom_sql`.

Rules:
- SELECT only.
- Add `LIMIT` for row-returning queries.
- Filter events by event name and event time using schema-confirmed column names.
- Explain what the SQL measures before interpreting results.

## Saved Charts And Dashboards

If the user asks to save, share, or build a dashboard, hand off to `wave-dashboard-builder` with:

- Analysis model type: event, funnel, retention, or custom SQL
- Validated events/properties/filters/time range
- Recommended chart type
- Any dashboard name or layout preference from the user
