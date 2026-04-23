---
name: wave-tracking-plan
description: >-
  Plan Sensors Wave tracking from code, PRDs, or user flows. Use when
  analyzing the current codebase, pages, business flows, event naming,
  client/server ownership, identify strategy, or producing a tracking plan
  draft before writing anything into Wave.
---

# Wave Tracking Plan

这是埋点方案规划专用 Skill。它负责从当前代码、需求文档或业务流程中反推出埋点方案与 Tracking Plan 草稿，不负责直接写入、发布或 SDK 接入。

## 职责边界

- 先分析现状，再产出方案；不要一上来就调用平台写工具。
- 如果用户明确说“根据当前代码设计埋点计划”，优先结合代码库现状、目录结构和已有实现，不要只凭猜测列事件。
- 默认输出草稿和待确认问题，不自动发布 Tracking Plan。

## 按需读取文件

- **通用交互与安全约束**：
  先读取 [policies/operating-rules.md](policies/operating-rules.md)
- **交互式提问模板**：
  需要复用确认话术时读取 [prompts/interaction.md](prompts/interaction.md)

- **事件命名、客户端 / 服务端归属、事件属性边界**：
  读取 [references/tracking-principles.md](references/tracking-principles.md)
- **登录、注册、登出、匿名转登录、跨设备**：
  读取 [references/user-identification.md](references/user-identification.md)
- **根据代码盘点页面、模块、关键动作**：
  读取 [playbooks/code-discovery.md](playbooks/code-discovery.md)
- **整理最终交付格式与 handoff**：
  读取 [playbooks/draft-output.md](playbooks/draft-output.md)

## 工作流

1. 识别输入来源
   先判断用户给的是：
   - 当前代码库
   - PRD / 原型 / 页面说明
   - 已有埋点表或半成品草稿

2. 盘点现状
   如果是代码库，先按 `code-discovery` playbook 盘点：
   - 页面 / 路由 / 模块入口
   - 关键动作与成功 / 失败分支
   - 登录注册、支付下单、表单提交等关键流程
   - 客户端与服务端边界
   - 已有埋点调用或历史事件命名

3. 设计事件模型
   产出事件名、触发时机、端、属性、是否必填、枚举范围，并标明哪些建议服务端上报、哪些必须客户端上报。

4. 补齐用户标识方案
   只要存在登录态或跨设备，就必须补充 `login_id`、`identify`、`reset`、`anon_id` 透传方案。

5. 输出草稿并停在设计阶段
   默认交付埋点方案草稿、Tracking Plan draft 结构和待确认问题。

## 停止条件

- 用户只想先看方案：停在草稿
- 用户要把草稿写入 / 发布到 Wave：切到 [../wave-tracking/SKILL.md](../wave-tracking/SKILL.md)
- 用户要开始接 SDK / 改埋点代码：切到 [../wave-sdk-integration/SKILL.md](../wave-sdk-integration/SKILL.md)

## 交接规则

- 本 Skill 解决“埋什么、在哪埋、怎么命名、identify 怎么做”。
- 本 Skill 不负责调用 `create_tracking_plan` / `publish_tracking_plan` 等写工具，除非用户明确要求并切到执行 Skill。
- 深度指标分析、漏斗/留存解读、SQL 排查仍切到 `wave-analytics`。
