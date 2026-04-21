# Dashboard Bootstrap Playbook

这是可选步骤。只有在用户明确希望基于埋点计划顺手生成图表或概览时才读取。

## 什么时候读

- 用户要“顺便建个 Dashboard”
- 用户要把核心埋点事件做成首版看板

## 执行步骤

1. 明确目标
   先确认是要：
   - 一个总览 Dashboard
   - 若干核心 KPI 图表
   - 漏斗 / 留存等结构化分析图

2. 选择最小可用图表集
   首版建议 3–5 个图，不要一次把所有事件都做成图表。
   常见优先级：
   - 核心事件量 / UV
   - 转化漏斗
   - 关键留存
   - 关键属性分布

3. 创建资产前先确认
   典型工具包括：
   - `create_dashboard`
   - `create_event_chart`
   - `create_funnel_chart`
   - `create_retention_chart`
   - `create_custom_sql_chart`
   - `set_dashboard_chart_layouts`

4. 返回结果
   输出 `dashboard_id`、图表名称、图表类型。
   不需要自己再拼接 URL。

5. 创建后先停下
   Dashboard 创建完成后，不要自动切质检。
   先明确告诉用户：
   - 由用户自己重启 / 部署相关项目
   - 由用户自己验证关键事件已经正常触发
   用户确认完成后，再询问是否进入质检流程

## 辅助规则

- Dashboard 是埋点闭环的可选后续动作，不是必经步骤。
- 如果用户真正需要的是分析问题定义或图表指标口径，优先切到 `wave-analytics`。
- 创建 Dashboard 只代表分析资产已建好，不代表埋点数据一定已经正常流入。
