# 第 14 次学习：按计划和模式保存对话历史

今天的目标是把对话历史从“只属于计划”升级为“属于计划 + mode”。

## 为什么要这样做

同一个计划下，不同 mode 的对话目的不同：

- `teacher`：解释概念。
- `debugger`：排查错误。
- `explainer`：解释代码。
- `planner`：制定计划。

如果它们共用同一份对话历史，上下文会串台。

所以新的结构是：

```text
计划 -> mode -> 对话历史
```

## 新存储结构

```text
data/conversations/<plan_id>/<mode>.json
```

例如：

```text
data/conversations/learn-functions/teacher.json
data/conversations/learn-functions/debugger.json
```

## 行为变化

- `/mode <name>` 不再清空对话。
- 切换 mode 时，会保存旧 mode 的 messages。
- 切换 mode 后，会加载当前计划下新 mode 的 messages。
- `/clear` 只清空当前计划 + 当前 mode 的对话。
- 启动时会恢复上次的 active mode。

## 删除计划

新增：

```text
/plan-delete <id>
/plan-delete <id> --yes
```

删除前需要确认。

确认后会删除：

- 计划文件。
- 该计划下所有 mode 的对话目录。
- 如果它是当前激活计划，也会清空激活状态。

## 本阶段验收

1. 创建计划。
2. 在 `teacher` 模式下聊天。
3. 切到 `debugger`，确认 teacher 对话没有被清空。
4. 切回 `teacher`，能加载 teacher 历史。
5. 删除计划时，一并删除该计划下所有 mode 对话。
