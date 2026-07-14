# 第 4 次学习：Prompt 设计

今天的目标是让 Agent 不只是一种固定角色，而是能通过 system prompt 切换工作模式。

## 本阶段新增能力

- 新增 `src/prompts.py` 管理 prompt。
- 支持 `/modes` 查看模式。
- 支持 `/mode <name>` 切换模式。
- 支持 `/help` 查看命令。
- 支持 `/clear` 清空对话记忆。

## 当前模式

- `teacher`：适合讲解 Python 和 Agent 概念。
- `explainer`：适合解释代码。
- `debugger`：适合分析错误和修复问题。
- `planner`：适合制定学习计划。

## 关键概念

System prompt 是给模型的“工作说明书”。同一个用户问题，在不同 system prompt 下会得到不同风格和结构的回答。

例如用户问：

```text
这段代码为什么报错？
```

`teacher` 模式可能会先解释概念。

`debugger` 模式会更倾向于按错误现象、原因、检查步骤、修复方式来回答。

## 为什么切换模式时清空记忆

如果不清空历史，模型可能同时受到旧模式和新模式影响。

例如刚才还在 `planner` 模式制定计划，下一轮切到 `debugger`，旧的学习计划上下文可能干扰错误排查。

所以当前实现里，切换模式会自动清空 `messages`。

## 本阶段验收

- `/modes` 能列出所有模式。
- `/mode debugger` 能切换到错误排查助手。
- `/clear` 能清空当前对话记忆。
- 不同模式对同一个问题有不同回答风格。
