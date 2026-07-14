# 第 8 次学习：文件读写能力

今天的目标是让 Agent 能围绕本地 Markdown 文件工作。

## 本阶段新增工具

- `read`：读取 Markdown 文件。
- `summary`：基于标题、章节和列表条目生成简单总结。
- `todos`：提取 TODO、待办项和 Markdown 任务列表。
- `save-summary`：把总结保存到 `notes/summaries/`。

## 使用示例

```text
/tool read notes/07_local_tools.md
/tool summary README.md
/tool todos README.md
/tool save-summary README.md
```

## 路径安全

文件工具会把用户提供的路径解析到项目目录内，并检查：

- 路径不能为空。
- 文件必须存在。
- 文件必须是 Markdown 文件。
- 文件不能位于项目目录之外。

这一步很重要，因为 Agent 一旦具备文件能力，就必须有清晰边界。

## 当前总结方式

当前 `summary` 工具不调用模型，而是用简单规则：

- 提取一级标题作为标题。
- 提取 Markdown 标题作为主要章节。
- 提取列表项作为重点条目。
- 如果没有标题和列表，就截取前 200 个字符作为预览。

后续可以升级为“读取文件后交给模型总结”。

## 本阶段验收

- 能读取 `README.md`。
- 能总结 `README.md`。
- 能提取待办项。
- 能把总结保存到 `notes/summaries/`。
- 不能读取项目外部文件。
