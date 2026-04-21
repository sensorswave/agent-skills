# SDK Matrix

用户确定技术栈后，再读取本文件；不要在未确定端之前默认展开全部 SDK 细节。

参考链接入口：
[https://sensorswave.com/docs/data-integration/](https://sensorswave.com/docs/data-integration/)

## SDK 索引

| 端 | SDK | 安装方式 | 文档 |
|----|-----|--------|------|
| Web | JavaScript SDK | `npm install @sensorswave/js-sdk` 或 `<script>` 引入 | [JS SDK 文档](https://sensorswave.com/docs/data-integration/javascript-sdk/) |
| Android | Android SDK | Gradle 依赖 | [Android SDK 文档](https://sensorswave.com/docs/data-integration/android-sdk/) |
| iOS | iOS SDK | CocoaPods / SPM | [iOS SDK 文档](https://sensorswave.com/docs/data-integration/ios-sdk/) |
| Flutter | Flutter SDK | `pubspec.yaml` 依赖 | [Flutter SDK 文档](https://sensorswave.com/docs/data-integration/flutter-sdk/) |
| React Native | RN SDK | npm 依赖 | [RN SDK 文档](https://sensorswave.com/docs/data-integration/react-native-sdk/) |
| 鸿蒙 | Harmony SDK | ohpm 依赖 | [Harmony SDK 文档](https://sensorswave.com/docs/data-integration/harmony-sdk/) |
| 小程序 | 微信小程序 SDK | npm 依赖 | [小程序 SDK 文档](https://sensorswave.com/docs/data-integration/wechat-miniprogram-sdk/) |
| 服务端 Go | Go SDK | `go get` | [Go SDK 文档](https://sensorswave.com/docs/data-integration/go-sdk/) |

## 相关文档

- [埋点方案选择](https://sensorswave.com/docs/data-integration/tracking-strategy/)
- [如何正确标识用户](https://sensorswave.com/docs/data-integration/identify/)
- [数据模型](https://sensorswave.com/docs/data-integration/data-model/)
- [事件和属性](https://sensorswave.com/docs/data-integration/events-and-properties/)
- [预置事件和预置属性](https://sensorswave.com/docs/data-integration/preset-events-and-properties/)

## 使用规则

- 先确认技术栈，再给对应文档链接，不要把整张表原样灌给用户。
- SDK 初始化所需的 `endpoint` 和 `source_token` 来自 pipeline 相关 MCP 工具。
- 不要再调用 `get_server_info`；当前流程以 pipeline 返回值为准。
- 如果用户只想要安装文档，不必提前进入 Tracking Plan 或质检流程。
