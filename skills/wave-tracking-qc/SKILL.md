---
name: wave-tracking-qc
description: >-
  Run Sensors Wave tracking quality checks after events are already firing. Use
  when validating a published Tracking Plan against actual data, checking
  missing events or properties, or handling rollout acceptance. For Tracking
  Plan write/publish, route to wave-tracking. For SDK or code fixes, route to
  wave-sdk-integration.
---

# Wave Tracking QC

这是独立的 `wave-tracking-qc` 质检入口。它只负责在事件已经开始触发之后，对照已发布 Tracking Plan 做质量检查、计划对照和上线验收。

## 职责边界

- 本 Skill 负责 Tracking Plan 质检、缺失事件/属性排查、值与计划不一致的问题定位。
- Tracking Plan 写入 / 发布、Dashboard 创建，不在本 Skill 内展开，统一交给 `wave-tracking`。
- SDK 初始化、埋点代码修改、identify / reset 接入，不在本 Skill 内展开，统一交给 `wave-sdk-integration`。
- 深度数据分析、漏斗/留存解读、用户查询、SQL 探查，切换到 `wave-analytics`。

## 先读取的共享文件

- **通用交互与安全约束**：
  先读取 [../wave-tracking-shared/policies/operating-rules.md](../wave-tracking-shared/policies/operating-rules.md)
- **交互式提问模板**：
  需要复用确认话术时读取 [../wave-tracking-shared/prompts/interaction.md](../wave-tracking-shared/prompts/interaction.md)

## 按需读取文件

- **Tracking Plan 质检 / 计划对照 / 上线验收**：
  读取 [playbooks/tracking-qc.md](playbooks/tracking-qc.md)
- **Tracking Plan 写入 / 发布 / Dashboard**：
  用户还没准备好质检基线时，读取 [../wave-tracking/SKILL.md](../wave-tracking/SKILL.md)
- **SDK / Pipeline 接入、初始化代码、示例埋点代码**：
  用户需要补代码或修接入时，读取 [../wave-sdk-integration/SKILL.md](../wave-sdk-integration/SKILL.md)
- **埋点方案规划 / 代码盘点 / identify 方案**：
  用户暴露出事件命名、埋点归属或 identify 策略问题时，读取 [../wave-tracking-plan/SKILL.md](../wave-tracking-plan/SKILL.md)

## 工作流

1. 先确认用户要的是质检，不要把“刚改完代码”或“事件已触发”自动当成开始质检。
2. 只在用户明确要求开始质检后，读取 `playbooks/tracking-qc.md`。
3. 如果前置条件不满足，先停下来，让用户手动完成重启 / 重新部署 / 重新编译和基本验证。
4. 质检结果输出后，按问题类型交接到对应 Skill：
   - 需要补埋点代码 / SDK 接入：`wave-sdk-integration`
   - 需要改事件设计 / identify 方案：`wave-tracking-plan`
   - 需要补发布 Tracking Plan 或 Dashboard：`wave-tracking`

## 停止条件

- **用户还没完成手动验证**：
  不进入质检，先等待用户确认“已重启并验证”。
- **Tracking Plan 还没发布**：
  先说明限制；若用户要补发布，切到 `wave-tracking`。
- **质检结果已给出**：
  停在问题清单或验收结论，不默认继续改代码或重新跑质检。

## 交接规则

- 不要尝试替用户重启本地项目、前端 Dev Server、移动端 App、后端服务或部署环境。
- 只有在用户明确说“开始质检”后，才调用质检相关工具。
- 输出优先给“是否通过 + 具体问题清单 + 下一步建议”，不要只贴原始工具返回。
