# Agent Skills 维护约定

`agent-skills/` 是 Wave Skill 的唯一源码目录。Web 通过 `embed.go` 打进 binary；wagent 从 `skills/manifest.json` + `SKILL.md` 构建运行时 Skill Index。

## 什么时候必须改 manifest

`skills/manifest.json` 是安装与 embed 清单，不是每次改 `SKILL.md` 都要动。

| 改动 | `manifest.json` | `apps/web/wagent/service/skill/registry.go` `builtInSkillMappings` |
|---|---|---|
| 只改已有 `SKILL.md` 正文 | 不必 | 不必（SuggestedTools / Triggers 变了才改） |
| 新增 / 删除 reference 文件 | 必须改该 skill 的 `references` | 不必 |
| 改公开描述、tags、install | 必须 | 描述可作为 fallback，建议一起看 |
| 新增 / 下线一个 skill | 必须加/删条目，并视需要 bump `version` | **必须**，否则 `install: true` 也会被 silently skip |
| 改 Mode / task / 触发词 / SuggestedTools | 不必 | 必须 |

manifest 里有、mapping 里没有的 skill，wagent **不会加载**。

## 改完自检

1. `SKILL.md` 与同目录 reference 路径和 manifest `references` 一致。
2. skill `name` 同时存在于 `manifest.json` 和 `builtInSkillMappings`。
3. 跑 `go test ./apps/web/wagent/service/skill/ -count=1`。
