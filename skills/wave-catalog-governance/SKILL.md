---
name: wave-catalog-governance
description: >-
  维护已有事件、事件属性和用户属性的 Catalog 文档信息。用于更新显示名、描述、
  事件触发时机、平台标签或示例值。不要用于改技术名、改数据类型、删除元数据、
  合并重复项或设计新埋点方案。
---

# Wave 数据字典治理

## 目标

用当前 MCP 写入工具，维护已有事件和属性的文档类 Catalog 信息。

## 工具

- 项目：`list_projects`
- 发现：`list_events`、`list_event_properties`、`list_user_properties`
- 更新事件：`update_event_metadata`
- 更新事件属性：`update_event_property_metadata`
- 更新用户属性：`update_user_property_metadata`
- 批量上下文：可用时阅读资源 `wave://catalog/summary`

## 可写字段

- 事件：`display_name`、`description`、`trigger_condition`、`platforms`
- 事件属性：`display_name`、`description`、`example_value`
- 用户属性：`display_name`、`description`、`example_value`

## 项目门禁

在调用其他项目级 MCP 工具前：

1. 调用 `list_projects`，展示 `project_id | name` 表格。
2. 等待用户回复数字 `project_id`。
3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

禁止静默挑选项目，也禁止在此步骤前调用元数据写入工具。

## 工作流

1. 先通过项目门禁，再按 id、技术名或关键词查出当前 Catalog 对象。
2. 整理变更清单：对象类型、id/name、当前值、拟改值和原因。
3. 任何更新调用前先请用户确认。
4. 按 id 或搜索结果更新时带上 `expected_name`，避免改错对象。
5. 调用对应的更新工具。
6. 再查询一次已改对象，汇报确认后的最终值。

## 边界

- 禁止在用户选择 `project_id` 之前查询或改写项目数据。
- 不要改技术名。
- 不要改数据类型。
- 不要删除、归档或合并元数据。
- 不要创建新事件、新属性或 Tracking Plan。
- 在 MCP 尚未提供对应工具前，不要宣称后续治理能力已经可用。

如果用户要求的是当前不可写的操作，说明现有工具边界；需要重做埋点时交给 `wave-tracking`，需要产品用法说明时交给 `wave-product-help`。

## 输出

返回：

- 已应用的变更
- 跳过的对象及原因
- 仍需用户确认的值
- 若当前 MCP 工具无法完成治理请求，给出下一步建议
