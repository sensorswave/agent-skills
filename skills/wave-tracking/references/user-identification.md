# User Identification

这是本地精简摘要，用于在登录、注册、登出、匿名转登录、跨设备和共享设备场景下快速收敛用户标识方案。

## 本地必须规则

- `login_id` 必须使用稳定、全局唯一、不可变的业务主键；不要用 session、token 或会变化的手机号。
- 客户端登录成功后先 `identify(login_id)`，再记录登录后的业务事件，避免事件带着旧身份。
- 用户登出通常调用 `reset()`；公共设备场景才考虑 `reset(true)`，以便重置匿名 ID。
- 服务端处理登录关联时，必须明确是否接收并透传客户端 `anon_id`。
- 匿名浏览后注册/登录的链路中，如果不做 identify，登录前行为与登录后行为会断开。
- 多设备登录时，各端必须使用同一套 `login_id`；否则会被识别为不同用户。
- 只要用户数、漏斗或留存明显不准，就要先回头检查 identify、reset、anon_id 透传是否正确。

## 官网权威入口

- 官方文档页 URL：
  [如何正确的标识用户](https://sensorswave.cn/docs/data-integration/user-identification/)

## 相关补充文档

- [埋点方案选择](https://sensorswave.cn/docs/data-integration/tracking-strategy/)
- [事件和属性](https://sensorswave.cn/docs/data-integration/events-and-properties/)

## 使用说明

- 联网时，身份合并、客户端/服务端差异和边界条件以官网文档页为准。
- 无法联网时，退回本文件中的本地摘要规则继续推进。
