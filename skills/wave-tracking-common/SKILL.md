---
name: wave-tracking-common
description: >-
  Internal shared reference bundle for Wave tracking skills. Not intended for
  direct user invocation. Contains common prompts and reference docs for event
  design, user identification, and SDK selection.
---

# Wave Tracking Common

这是 `wave-tracking-design`、`wave-tracking` 与 `wave-sdk-integration` 的共享资料目录。
它不是面向终端用户直接触发的工作流 Skill。

当其他 Skill 明确引用时，按需读取下列文件：

- [prompts.md](prompts.md)
- [references/tracking-principles.md](references/tracking-principles.md)
- [references/user-identification.md](references/user-identification.md)
- [references/sdk-matrix.md](references/sdk-matrix.md)

如果用户直接命中这个 Skill，不要在这里展开执行，改为将任务导向：

- 埋点方案设计 / 代码盘点 / identify 方案：`wave-tracking-design`
- Tracking Plan / 发布后质检：`wave-tracking`
- SDK / Pipeline / 代码接入：`wave-sdk-integration`
