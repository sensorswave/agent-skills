# Skills 安装指南

将 Wave Skills 安装到本地 AI 代理环境的推荐方式，是直接使用 [skills.sh](https://skills.sh/) 官方 CLI。

## 快速安装

推荐一次安装全部公开 skills：

```bash
npx skills add sensorswave/agent-skills --skill '*'
```

说明：

- 这条命令会使用 `skills` 官方 CLI，从 GitHub 仓库拉取 skill。
- 当前仓库是 **多 skill workflow**，`wave` 路由、埋点规划、Tracking Plan 执行、质检、SDK 接入会互相切换，所以推荐直接安装全部公开 skills。
- 默认会按 `skills` CLI 的规则让你选择安装范围；如果当前目录是项目，通常优先项目级安装。

## 常用安装方式

安装全部公开 skills，并让 CLI 交互式选择 agent / 范围：

```bash
npx skills add sensorswave/agent-skills --skill '*'
```

强制全局安装：

```bash
npx skills add sensorswave/agent-skills --skill '*' -g
```

只安装某一个 skill：

```bash
npx skills add sensorswave/agent-skills --skill wave-analytics
npx skills add sensorswave/agent-skills --skill wave-sdk-integration
```

如果你想无提示安装，可在熟悉 `skills` CLI 参数后再补 `-y` 和 `--agent`。

## 仓库包含的公开 Skill

| Skill | 功能 |
|-------|------|
| `wave` | 总入口路由：自动分发到埋点规划、接入、执行、质检或分析 |
| `wave-tracking-plan` | 代码/需求分析，输出埋点方案与 plan draft |
| `wave-tracking` | Tracking Plan 写入、发布与 Dashboard |
| `wave-tracking-qc` | Tracking Plan 质检、计划对照、上线验收 |
| `wave-sdk-integration` | SDK、Pipeline、identify、埋点代码接入 |
| `wave-analytics` | 数据分析：事件、漏斗、留存、用户列表、SQL |

## 更新与移除

查看已安装 skill：

```bash
npx skills list
```

更新全部已安装 skill：

```bash
npx skills update
```

只更新某一个 skill：

```bash
npx skills update wave
```

移除某一个 skill：

```bash
npx skills remove wave-analytics
```

交互式移除：

```bash
npx skills remove
```

## 验证

列出当前项目或全局已安装的 skills：

```bash
npx skills list
npx skills list -g
```

如果你是本仓库维护者，也可以在仓库里运行：

```bash
python3 scripts/validate_skills.py
```

## 前置依赖

所有 Skill 都依赖 **Wave MCP Server** 提供的工具集。安装 skill 之后，还需要在目标 IDE / agent 中配置 Wave MCP 连接，才能真正调用项目、Pipeline、Tracking Plan、Dashboard 和分析能力。
