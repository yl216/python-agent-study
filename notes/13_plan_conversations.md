# 第 13 次学习：按计划保存对话历史

今天解决的问题是：计划能恢复，但普通对话不能恢复。

## 新设计

每个计划都有独立对话文件：

```text
data/conversations/<plan_id>.json
```

这样不同计划的上下文不会混在一起。

例如：

```text
learn-functions -> data/conversations/learn-functions.json
learn-classes   -> data/conversations/learn-classes.json
```

## 本阶段新增文件

新增 `src/conversation_store.py`，提供：

- `load_conversation(plan_id)`：加载某个计划的对话历史。
- `save_conversation(plan_id, messages)`：保存某个计划的对话历史。
- `clear_conversation(plan_id)`：清空某个计划的对话历史。

## 行为变化

- 程序启动时，如果有当前计划，会加载该计划的对话历史。
- `/plan <目标>` 新建计划时，会切换到这个新计划的空对话历史。
- `/plan-use <id>` 切换计划时，会加载该计划自己的对话历史。
- 普通聊天成功后，会保存到当前计划的对话文件。
- `/clear` 只清空当前计划的对话历史。

## 为什么按计划保存

如果只保存一个全局聊天历史，就会出现上下文串台：

```text
学习函数的对话
学习类的对话
错误排查的对话
```

全混在一起后，模型很容易误解当前任务。

按计划保存对话，能让每个学习任务拥有自己的上下文。

## 本阶段验收

1. 创建一个计划。
2. 在这个计划下聊天。
3. 退出程序。
4. 重新启动程序。
5. 能看到该计划的对话消息数量被恢复。
6. 切换另一个计划时，对话历史也随计划切换。
