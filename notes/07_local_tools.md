# 第 7 次学习：本地工具调用

今天的目标是让 Agent 从“只会回答文字”升级成“可以调用本地 Python 函数做事”。

## 本阶段新增能力

新增 `src/tools.py`，包含四个工具：

- `calculate()`：安全计算数学表达式。
- `current_time()`：返回当前时间。
- `list_files()`：列出项目根目录文件。
- `save_note()`：把学习笔记保存到 `notes/`。

`src/main.py` 新增命令：

```text
/tools
/tool <命令>
```

## 使用示例

```text
/tool calc 2 * (3 + 4)
/tool time
/tool files
/tool note 今天学习了工具调用
```

## 为什么计算器不能直接用 `eval()`

`eval()` 会执行任意 Python 表达式，风险很高。

例如用户输入恶意代码，程序可能执行不该执行的操作。

当前实现使用 `ast` 解析表达式，只允许数字和这些运算符：

```text
+ - * / // % **
```

这是一种更安全的做法。

## 当前边界

现在是“用户显式调用工具”：

```text
/tool calc 1 + 2
```

还不是“模型自动决定调用工具”。

下一步可以让模型输出结构化 JSON，例如：

```json
{
  "tool": "calc",
  "input": "1 + 2"
}
```

再由程序执行对应工具。
