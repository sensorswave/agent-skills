---
name: wave-sdk-integration
description: >-
  Handle Sensors Wave SDK and pipeline integration. Use when working on SDK
  初始化, source_token / endpoint, Pipeline 复用或创建, identify / reset,
  埋点代码接入, client/server instrumentation integration, or event tracking
  implementation in code.
---

# Wave SDK Integration

这是 SDK / Pipeline 接入专用 Skill。只处理“怎么接入并让代码具备上报能力”，不负责完整 Tracking Plan 生命周期。

## 全局原则

- 项目必须由用户明确选择，先用 `list_projects`。
- 写操作前必须展示参数并二次确认。
- 统一复用共享提示词 [../wave-tracking-common/prompts.md](../wave-tracking-common/prompts.md)。
- 不要替用户重启本地项目、移动端 App、前端 Dev Server、后端服务或部署环境。
- 如果代码要靠重启 / 编译 / 发布后才会生效，只能让用户自行完成。

## 按需读取共享参考

- 事件设计、客户端 / 服务端边界：
  读取 [../wave-tracking-common/references/tracking-principles.md](../wave-tracking-common/references/tracking-principles.md)
- 登录态、identify、reset、匿名转登录：
  读取 [../wave-tracking-common/references/user-identification.md](../wave-tracking-common/references/user-identification.md)
- 不同 SDK 的安装方式和文档入口：
  读取 [../wave-tracking-common/references/sdk-matrix.md](../wave-tracking-common/references/sdk-matrix.md)

## 工作流

1. 选择项目
   如果当前项目未明确，先调用 `list_projects`。

2. 处理 Pipeline
   先调用 `list_pipelines`，让用户决定：
   - 复用已有 Pipeline：调用 `get_pipeline_detail`
   - 新建 Pipeline：确认参数后调用 `create_pipeline`

3. 获取初始化参数
   Pipeline 相关工具返回的 `source_token` 与 `endpoint` 是 SDK 初始化的权威来源。
   不要自行拼接服务地址。

4. 判断是否需要补充 identify 方案
   只要涉及：
   - 登录 / 注册
   - 登出
   - 匿名用户转登录用户
   - 跨设备
   - 公共设备
   就必须补读用户标识参考，并明确 `login_id`、`identify`、`reset`、服务端是否透传 `anon_id`。

5. 给对应端的 SDK 文档入口
   技术栈确定后，只给当前端需要的文档和安装方式，不要把所有 SDK 文档整包倾倒给用户。

6. 生成代码草稿
   输出内容通常包括：
   - SDK 初始化代码
   - identify / reset 代码
   - 关键事件的 `trackEvent` 或对应 SDK 调用示例

## 停止条件

- 用户只要 `endpoint` / `source_token`：返回参数即可
- 用户只要最小初始化代码：返回初始化片段即可
- 用户还没准备好发布或重启：停在代码草稿，不继续假设事件已生效
- 用户其实还在定事件模型 / identify 方案：切到 `wave-tracking-design`
- 用户要做 Tracking Plan 起草 / 发布：切到 `wave-tracking`

## 结果边界

- 本 Skill 只负责“代码怎么接进去”。
- 是否真的已经生效，要等用户自行重启 / 编译 / 发布并确认。
- 用户确认事件已开始正常触发后，如需质检，再回到 `wave-tracking` 流程。
