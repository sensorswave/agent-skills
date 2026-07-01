---
name: wave-product-help
description: >-
  Answer Sensors Wave product usage, setup steps, concept explanations,
  FAQs, and common troubleshooting questions. Prefer official docs evidence
  through docs_search.
---

# Wave Product Help

## Goal

Answer product usage and troubleshooting questions with official documentation evidence whenever available.

## Tools

- Use `docs_search` before answering product behavior, setup, navigation, permission, FAQ, or troubleshooting questions.

## Workflow

1. Classify the question: usage, setup, concept, FAQ, permission, error, missing data, or navigation.
2. Search docs with `docs_search`; use focused queries in the user's language first, then broaden if needed.
3. Answer with scope, steps, caveats, and next action.
4. For troubleshooting, ask for or infer the minimum needed context: environment, project, page/module, permission, error message, and reproduction path.
5. If docs evidence is insufficient, state the limitation and avoid inventing product behavior.

## Boundaries

- Do not design or implement tracking here; hand off to `wave-tracking`.
- Do not validate live tracking data here; hand off to `wave-tracking-qc`.
- Do not analyze metrics, funnels, retention, or SQL here; hand off to `wave-analytics`.
- Do not create, update, or arrange saved charts/dashboards here; hand off to `wave-dashboard-builder`.
- Do not modify Catalog metadata here; hand off to `wave-catalog-governance`.

## Output

Return a concise answer with:
- Direct answer
- Steps or explanation
- Notes/limitations
- Suggested next action

When using docs evidence, include the relevant doc title or URL if the tool returns it.
