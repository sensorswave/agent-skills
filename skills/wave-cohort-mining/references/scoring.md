# 评分与落库参数

## 保留门槛

| 判断 | 指标 | 保留条件 |
|---|---|---|
| Signal | 目标指标相对基线的 lift | `\|lift − 1\| ≥ 0.3`；lift 为 null（空候选或零基线）直接丢弃 |
| Actionability | 人数占基线比例；规则可读 | 0.5%–30%，且一句话能说清规则 |
| Value | 与已有分群的重叠 | `share_of_candidate ≤ 70%`，否则视为重复 |
| Verifiability | 成功指标与观察窗 | 报告里必须写出 |

lift < 1 同样有价值：这群人「卡住了」，是干预对象；lift > 1 说明值得放大。带 `target_leakage` 警告的结果不可解释，先修正定义再重评。

样本量守门：预期转化数 = 候选人数 × 基线发生率。预期转化不足 10 人时 lift 只是噪声，只能标为「样本不足，观察」，可以进报告但不得落库、不得作为保留依据。`evaluate_cohort_definition` 直接返回 `target.expected_conversions`，并用 `warnings` 里的 `low_expected_conversions`、`small_candidate`、`target_leakage`（定义窗内排除或要求目标事件，lift 不可解释）、`definition_overlaps_observation`（定义窗与观察窗重叠，lift 只是同期共现）、`empty_candidate`、`zero_baseline` 标出问题；带前两类警告的候选先把定义窗整体挪到观察窗之前再重评。`overlap[].share_of_candidate` 就是重叠门槛用的值；报告里的「最大重叠」必须取 `overlap[]` 中最大的 `share_of_candidate` 并写明分群名，不能挑一个小的。

基线默认是「候选定义窗内做过 `$AnyEvent` 的用户」；lift = 候选中目标事件发生率 ÷ 基线中目标事件发生率，观察窗默认 `last_7_days`。基线和候选必须在同一时刻「活着」：候选按前 7 天定义、后 7 天观察时，基线也要是前 7 天活跃的用户，不能用近 30 天活跃——那会混进只在观察窗才出现的新用户，他们在观察窗内转化是必然的，会把所有候选的 lift 都压到 1 以下。候选定义里有排除条件（如「定义窗内未支付」）时，基线还要镜像同样的排除（定义窗活跃 + 定义窗内未支付），否则基线里混着刚支付过的复购用户。不传 `baseline_definition` 时 `evaluate_cohort_definition` 自动做这两件事，`baseline.derived_from` 与 `baseline.activity_window` 回显用了哪个窗口；自己传基线时要自己对齐窗口并镜像排除。只有属性条件、没有行为窗口的候选（反差切片）要加一条 `user_did $AnyEvent count gte 1 <定义窗>`，工具才能对齐基线窗口，否则基线退回近 30 天活跃。用 SQL 自算时，定义窗要落在观察窗之前（如定义用前 7 天，观察用后 7 天），否则就是用结果定义原因；SQL 里没有 `$AnyEvent` 这个事件值，算活跃用户直接不加 `event` 过滤。

## 排序

`|lift − 1| × 人数占比 × 可运营性`。可运营性：1 = 有现成通道与动作；0.5 = 需新建通道；0 = 只能报告。

## 报告表

`候选名 | 规则要点 | 人数 | 占活跃比例 | 目标 lift | 建议动作`。数字来自工具返回，无法计算填 `—`；样本不足的候选在「建议动作」里写明「样本不足，观察」。

## 落库参数模板

```text
name        = "[AI候选] " + 候选短名（含前缀 ≤ 100 字）
calc_mode   = "STATIC"
description = "[ai_mined]
假设：<模板名>。<规则一句话>。人数 <size>（占基线 <share>%），<目标事件> <观察窗> 发生率 <rate>% vs 基线 <baseline_rate>%（lift <lift>）。与 <分群名> 重叠 <overlap>%。挖掘于 <date>。"
```

`[ai_mined]` 是统计标记，必须独占 description 第一行。转正时只去掉名称前缀、改 DYNAMIC，保留这一行。
