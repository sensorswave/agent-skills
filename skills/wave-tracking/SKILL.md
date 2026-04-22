---
name: wave-tracking
description: >-
  Execute Sensors Wave tracking rollout steps after the design is ready. Use
  when writing or publishing a Tracking Plan, creating a dashboard, running
  tracking QC, or handling rollout checkpoints. For design work, route to
  wave-tracking-plan. For SDK / Pipeline integration, route to
  wave-sdk-integration.
---

# Wave Tracking

这是 `wave-tracking` 的执行与验证入口。它默认承接“方案已经基本确定”之后的步骤：写入 / 发布 Tracking Plan、可选 Dashboard、以及后续质检。
如果用户还在做事件设计、代码盘点、identify 方案，先切到 `wave-tracking-plan`。涉及接入代码、`endpoint` / `source_token`、identify / reset 落点实现时，改为读取 `wave-sdk-integration`。

## 职责边界

- 本 Skill 负责 Tracking Plan 写入 / 发布、埋点质检、可选的 Dashboard 启动版。
- 事件规划和用户标识设计不在本 Skill 内展开，统一交给 `wave-tracking-plan`。
- 深度数据分析、漏斗/留存解读、用户查询、SQL 探查，切换到 `wave-analytics`。

## 先读取的共享文件

- **通用交互与安全约束**：
  先读取 [../wave-tracking-shared/policies/operating-rules.md](../wave-tracking-shared/policies/operating-rules.md)
- **交互式提问模板**：
  需要复用确认话术时读取 [../wave-tracking-shared/prompts/interaction.md](../wave-tracking-shared/prompts/interaction.md)

## 按需读取文件

- **埋点方案规划 / 代码盘点 / 事件命名 / identify 方案**：
  读取 [../wave-tracking-plan/SKILL.md](../wave-tracking-plan/SKILL.md)
- **SDK / Pipeline 接入、初始化代码、示例埋点代码**：
  读取 [../wave-sdk-integration/SKILL.md](../wave-sdk-integration/SKILL.md)
- **Tracking Plan 草稿、模板、发布**：
  读取 [playbooks/tracking-plan.md](playbooks/tracking-plan.md)
- **埋点验收 / 计划对照 / 质量检查**：
  读取 [playbooks/tracking-qc.md](playbooks/tracking-qc.md)
- **基于埋点计划顺手创建看板**：
  仅在用户明确提出时读取 [playbooks/dashboard-bootstrap.md](playbooks/dashboard-bootstrap.md)

## 工作流

1. 先识别用户当前阶段，不要默认跑完整闭环。
2. 只读取当前阶段需要的 reference / playbook。
3. 当前阶段完成后，如果用户继续推进，再加载下一阶段文件。
4. 若用户同时提到多个阶段，优先顺序通常是：
   埋点方案规划（转到 `wave-tracking-plan`）→ Tracking Plan 写入 / 发布 → SDK / Pipeline 接入（转到 `wave-sdk-integration`）→ 发布后询问是否创建 Dashboard → 用户自行重启并验证 → 质检。

## 停止条件

- **只想接 SDK / 只想拿初始化代码**：
  直接转到 `wave-sdk-integration`，不在当前 Skill 里展开。
- **只想出埋点方案**：
  直接转到 `wave-tracking-plan`，停在方案草稿，不自动发布。
- **发布了计划**：
  发布完成后先问用户是否要创建 Dashboard，不默认继续。
- **创建了 Dashboard**：
  先让用户自己重启 / 部署并验证事件确实触发，再询问是否进入质检。

## 交接规则

- 不要尝试替用户重启本地项目、前端 Dev Server、移动端 App、后端服务或部署环境。
- 如果为了让埋点代码生效需要重启 / 重新部署，只能明确告诉用户由其自行完成，并等待用户确认。
- “看到事件已正常触发”是进入质检前的推荐前置条件，不要默认跳过。
- 如果用户既要埋点又要分析，先把埋点流程收敛到可实施状态，再切换分析。

若产品能力或工具边界后续变更，以当前可用工具和现行产品行为为准。
