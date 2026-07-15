# 第 11 次学习：计划持久化

今天的目标是解决“计划做到一半，程序退出后丢失”的问题。

## 核心概念

之前的计划保存在内存里：

```text
程序运行中 -> current_plan 存在
程序退出 -> 内存清空 -> current_plan 丢失
```

现在计划会保存到文件：

```text
data/current_plan.json
```

这样程序重启后就可以恢复计划。

## 本阶段新增能力

`src/planner.py` 新增：

- `TaskPlan.to_dict()`：把计划转换成可写入 JSON 的字典。
- `TaskPlan.from_dict()`：从 JSON 数据恢复计划。
- `save_plan()`：保存当前计划。
- `load_plan()`：启动时读取计划。
- `clear_saved_plan()`：清空保存文件。

`src/main.py` 更新：

- 启动时自动 `load_plan()`。
- `/plan` 创建计划后自动保存。
- `/plan-next` 推进后自动保存。
- `/plan-reset` 删除保存文件。

## 为什么用 JSON

Markdown 适合人读，JSON 适合程序恢复状态。

计划恢复需要知道：

- 目标是什么。
- 当前进行到第几步。
- 每一步是否完成。
- 每一步的标题、练习、验收标准。

这些信息用 JSON 表达更稳定。

## 本阶段验收

1. 创建计划。
2. 推进一步。
3. 退出程序。
4. 重新运行程序。
5. 输入 `/plan-show`，能看到之前的计划和进度。
