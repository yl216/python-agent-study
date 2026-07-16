# 第 16 次学习：修复计划重命名

今天修复的问题是：`/plan-rename` 只改了计划标题，没有改计划 ID。

## 问题表现

执行：

```text
/plan-rename 20260716013923-learn-functions learn
```

再执行：

```text
/plans
```

列表里仍然看到：

```text
20260716013923-learn-functions | active | 第 1/5 步 | learn
```

这说明 `goal` 改了，但 `plan_id` 没改。

## 修复方式

现在重命名会同时更新：

- `goal`
- `plan_id`
- 计划 JSON 文件名
- 对话历史目录
- 当前激活计划指针

## 新行为

```text
/plan-rename 20260716013923-learn-functions learn
```

会把计划 ID 改成：

```text
learn
```

如果已经存在同名计划，会自动使用：

```text
learn-2
learn-3
...
```

避免覆盖已有计划。
