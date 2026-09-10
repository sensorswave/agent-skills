# Agent Skills 维护约定

`agent-skills/` 是 Wave Skill 的唯一源码目录。Web 通过 `embed.go` 打进 binary；wagent 从 `skills/manifest.json` + `SKILL.md` 构建运行时 Skill Index。

## 语言

所有 `SKILL.md`、reference、`agents/openai.yaml` 的正文用中文。frontmatter 的 `name`、MCP 工具名、参数名（`project_id`、`source_token` 等）、产品术语（Tracking Plan、Pipeline、Campaign、Dashboard、Catalog、identify/reset、5W1H）和 skill 名保持英文。frontmatter `description` 以中文为主、保留英文关键词，方便中英文提问都能命中。

## 项目门禁写法

同一份 skill 要同时服务两种运行环境：外部 Agent（Cursor / Claude Code / Codex 走 MCP，必须先 `list_projects` 让用户选 `project_id`）和 Wagent 产品内（会话已绑定项目，没有 `list_projects`）。为了不让 Go 代码去逐句改写 Markdown，约定如下：

1. 项目级 skill 在 manifest 里声明 `"projectScoped": true`，`SKILL.md` 里有且只有一个 `## 项目门禁` 小节，正文包在标记块里：

   ```markdown
   ## 项目门禁

   <!-- wave:project-gate -->
   在调用其他项目级 MCP 工具前：

   1. 调用 `list_projects`，展示 `project_id | name` 表格。
   2. 等待用户回复数字 `project_id`。
   3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

   禁止静默挑选项目，也禁止在此步骤前调用……
   <!-- /wave:project-gate -->
   ```

   wagent 加载时会把标记块整体替换成一句「当前 Wagent 会话已绑定项目，项目门禁已通过……」（见 `apps/web/wagent/service/skill/wagent_adapt.go`）。标记块内的措辞可以随便改。
2. `list_projects` 只允许出现在标记块内。正文其他地方（工作流、边界、reference）只说「先通过项目门禁」「项目门禁未通过前不要……」，这类话在两种环境里都成立。
3. `wave` 路由和 `wave-product-help` 不是项目级 skill（`projectScoped: false`），不能有标记块。

`scripts/validate_skills.py` 会检查以上三条；wagent 的 `TestProjectScopedSkillsSkipProjectSelectionInWagent` 会检查适配后送给模型的所有 skill 和 reference 都不再含 `list_projects`。

## 什么时候必须改 manifest

`skills/manifest.json` 是安装与 embed 清单，不是每次改 `SKILL.md` 都要动。

| 改动 | `manifest.json` | `apps/web/wagent/service/skill/registry.go` `builtInSkillMappings` |
|---|---|---|
| 只改已有 `SKILL.md` 正文 | 不必 | 不必（SuggestedTools / Triggers 变了才改） |
| 新增 / 删除 reference 文件 | 必须改该 skill 的 `references` | 不必 |
| 改公开描述、tags、install、projectScoped | 必须 | 描述可作为 fallback，建议一起看 |
| 新增 / 下线一个 skill | 必须加/删条目（含 `projectScoped`），并视需要 bump `version` | **必须**，否则 `install: true` 也会被 silently skip |
| 改 Mode / task / 触发词 / SuggestedTools | 不必 | 必须 |

manifest 里有、mapping 里没有的 skill，wagent **不会加载**。

## 改完自检

1. `SKILL.md` 与同目录 reference 路径和 manifest `references` 一致。
2. skill `name` 同时存在于 `manifest.json` 和 `builtInSkillMappings`。
3. 跑 `python3 scripts/validate_skills.py`。
4. 跑 `go test ./apps/web/wagent/service/skill/ -count=1`。
