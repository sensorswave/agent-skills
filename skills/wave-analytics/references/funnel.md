# 漏斗分析参考

用 `query_funnel` 分析至少两步的有序或无序转化。筛选与分组见 [filters.md](filters.md)。

- 默认 `funnel_mode`：`in_order`
- 默认 `measure_type`：`conversion`
- 默认窗口：7 天
- 用户问转化时长时用 `measure_type=time_to_convert`；结果单元格包含平均 / 中位 / p25 / p75 / 最小 / 最大，单位毫秒
- 同时解释整体转化和最大相邻流失
- 对象单元格使用稳定键 `overall` / `step_N`

步骤筛选写法与事件分析相同。按某个商品限定漏斗时，每一步都带上该商品条件；不要先跑未筛选的全站漏斗再当作原问题的答案。
