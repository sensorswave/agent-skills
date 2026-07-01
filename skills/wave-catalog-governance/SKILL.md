---
name: wave-catalog-governance
description: >-
  Maintain low-risk Sensors Wave Catalog metadata for existing events, event
  properties, and user properties. Use when updating display names,
  descriptions, event trigger conditions, platform tags, or example values.
  Do not use for renaming technical names, changing data types, deleting
  metadata, merging duplicates, or designing new tracking plans.
---

# Wave Catalog Governance

## Goal

Maintain documentation-grade Catalog metadata for existing events and properties using the current MCP write tools.

## Tools

- Discover current values: `list_projects`, `list_events`, `list_event_properties`, `list_user_properties`
- Update events: `update_event_metadata`
- Update event properties: `update_event_property_metadata`
- Update user properties: `update_user_property_metadata`
- Bulk context: read resource `wave://catalog/summary` when available

## Writable Fields

- Event: `display_name`, `description`, `trigger_condition`, `platforms`
- Event property: `display_name`, `description`, `example_value`
- User property: `display_name`, `description`, `example_value`

## Workflow

1. Confirm project before project-level MCP calls unless the user explicitly fixes the current project.
2. Query the current Catalog objects by id, technical name, or search keyword.
3. Prepare a change list with object type, id/name, current value, proposed value, and reason.
4. Ask for confirmation before any update call.
5. Include `expected_name` when updating by id or search-derived match to prevent wrong-object edits.
6. Run the correct update tool.
7. Re-query the changed object and report confirmed final values.

## Boundaries

- Do not rename technical names.
- Do not change data types.
- Do not delete, archive, or merge metadata.
- Do not create new events/properties or Tracking Plans.
- Do not claim future governance operations are available until the MCP exposes corresponding tools.

If the user asks for a non-writable operation, explain the current tool boundary and, if appropriate, route to `wave-tracking` for redesign or to `wave-product-help` for product guidance.

## Output

Return:
- Changes applied
- Objects skipped and why
- Any values that still need user confirmation
- Suggested next step, if the requested governance cannot be completed with current MCP tools
