# SDK Matrix

这是本地精简摘要，用于在确认技术栈后快速定位 Wave SDK 集成入口。

## 本地必须规则

- 未确定端之前，不要把全部 SDK 文档整包倾倒给用户；只给当前技术栈相关的入口。
- SDK 初始化所需的 `endpoint` 和 `source_token` 以 pipeline 相关 MCP 工具返回值为准，不要自行拼接服务地址。
- 只要涉及登录态变化，就要同时补读用户标识资料，而不是只给安装文档。
- 如果用户只想拿 SDK 安装方式或初始化片段，不必提前进入 Tracking Plan 或质检流程。
- 前端 SDK 场景优先给客户端文档；服务端上报再补服务端 SDK 文档和 `anon_id` 透传要求。
- 需要解释自动采集、预置事件和属性边界时，再回看 tracking principles，而不是在 SDK 矩阵里展开。

## 官网权威入口

- 官方文档页 URL：
  [SDK 数据接入](https://sensorswave.cn/docs/data-center/pipeline/sources/sdk/)

## 常用 SDK 文档

- JavaScript SDK：
  [页面](https://sensorswave.cn/docs/data-integration/client-sdks/javascript/)
- Android SDK：
  [页面](https://sensorswave.cn/docs/data-integration/client-sdks/android/)
- iOS SDK：
  [页面](https://sensorswave.cn/docs/data-integration/client-sdks/ios/)
- React Native SDK：
  [页面](https://sensorswave.cn/docs/data-integration/client-sdks/reactnative/)
- Flutter SDK：
  [页面](https://sensorswave.cn/docs/data-integration/client-sdks/flutter/)
- Harmony SDK：
  [页面](https://sensorswave.cn/docs/data-integration/client-sdks/harmony/)
- 微信小程序 SDK：
  [页面](https://sensorswave.cn/docs/data-integration/client-sdks/wechatMini/)
- Go SDK：
  [页面](https://sensorswave.cn/docs/data-integration/server-sdks/go/)
- PHP SDK：
  [页面](https://sensorswave.cn/docs/data-integration/server-sdks/php/)

## 使用说明

- 联网时，SDK 安装、初始化参数和平台差异以官网文档页为准。
- 无法联网时，退回本文件中的本地摘要规则继续推进。
