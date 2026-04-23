---
name: wave-tracking-shared
description: >-
  Internal shared bundle for Wave tracking skills. Not intended for direct
  user invocation. Contains shared prompts, policies, and references for
  tracking planning, rollout, and SDK integration.
---

# Wave Tracking Shared

这是 `wave-tracking-plan`、`wave-tracking`、`wave-tracking-qc` 与 `wave-sdk-integration` 的内部共享资料目录。
它不是面向终端用户直接触发的 workflow Skill。

## 知识分层

- **本地 shared**：负责 workflow、安全边界、确认话术和精简规则摘要。
- **官网 docs + `llm.txt`**：负责长文知识和权威产品口径。
- 如果本地摘要与官网长文出现冲突，以官网文档页和对应 `llm.txt` 为准。

当其他 Skill 明确引用时，按需读取下列文件：

- [policies/operating-rules.md](policies/operating-rules.md)
- [prompts/interaction.md](prompts/interaction.md)
- [references/tracking-principles.md](references/tracking-principles.md)
- [references/user-identification.md](references/user-identification.md)
- [references/sdk-matrix.md](references/sdk-matrix.md)

如果用户直接命中这个 Skill，不要在这里展开执行，改为将任务导向：

- 埋点方案规划 / 代码盘点 / identify 方案：`wave-tracking-plan`
- Tracking Plan 写入 / 发布 / Dashboard：`wave-tracking`
- 发布后质检 / 计划对照 / 上线验收：`wave-tracking-qc`
- SDK / Pipeline / 代码接入：`wave-sdk-integration`
