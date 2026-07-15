# 第 12 次学习：多计划持久化

今天修复的问题是：新建计划会覆盖旧计划。

## 问题原因

之前只有一个保存文件：

```text
data/current_plan.json
```

所以每次执行：

```text
/plan <目标>
```

都会把旧计划覆盖掉。

## 新设计

现在每个计划都有独立 ID，并保存为独立文件：

```text
data/plans/<plan_id>.json
```

当前激活计划单独记录在：

```text
data/active_plan.json
```

这意味着：

- 新建计划不会覆盖旧计划。
- `/plans` 可以查看所有计划。
- `/plan-use <id>` 可以切换当前计划。
- `/plan-reset` 只取消当前激活计划，不删除历史计划文件。

## 新增命令

```text
/plans
/plan-use <id>
```

## 本阶段验收

1. 创建第一个计划。
2. 创建第二个计划。
3. 输入 `/plans`，能看到两个计划。
4. 用 `/plan-use <id>` 切回第一个计划。
5. `/plan-show` 能看到第一个计划内容。
