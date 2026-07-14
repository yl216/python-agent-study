# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 8，结构化输出。

## 安装依赖

```powershell
pip install -r requirements.txt
```

## 配置 DeepSeek

复制 `.env.example` 为 `.env`，然后把 `DEEPSEEK_API_KEY` 改成你的真实 DeepSeek API Key。

```powershell
Copy-Item .env.example .env
```

## 运行方式

```powershell
python src/main.py
```

## 当前命令

```text
/help              查看帮助
/modes             查看可用模式
/mode <name>       切换模式，例如 /mode debugger
/clear             清空当前对话记忆
/tools             查看可用本地工具
/tool <命令>       手动调用本地工具，例如 /tool summary README.md
/intent <请求>     让模型输出 JSON 意图并自动调用工具
/exit              退出程序
```

## 结构化输出示例

输入：

```text
/intent 帮我计算 2 * (3 + 4)
```

模型应输出类似 JSON：

```json
{
  "intent": "calc",
  "argument": "2 * (3 + 4)"
}
```

程序解析 JSON 后会调用：

```text
/tool calc 2 * (3 + 4)
```

如果 DeepSeek 临时连接失败，程序会尝试使用本地规则解析常见意图，避免简单工具完全不可用。

## 支持的 intent

```text
calc            计算数学表达式
time            查看当前时间
files           查看项目文件
note            保存笔记
read            读取 Markdown 文件
summary         总结 Markdown 文件
todos           提取 TODO 或待办项
save-summary    保存 Markdown 总结
chat            更适合普通聊天，不调用工具
```

## 本地工具

```text
/tool calc <表达式>
/tool time
/tool files
/tool note <内容>
/tool read <路径>
/tool summary <路径>
/tool todos <路径>
/tool save-summary <路径>
```

## 当前文件

- `src/main.py`：命令行入口、命令处理、工具和意图命令路由。
- `src/intent_parser.py`：让模型输出 JSON，并解析为 `intent` 和 `argument`。
- `src/tools.py`：本地工具函数，包含文件读写工具。
- `src/prompts.py`：管理不同模式的 system prompt 和安全规则。
- `src/settings.py`：读取并校验环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `ERROR_MANUAL.md`：错误手册。
- `PROMPT_INJECTION_TESTS.md`：提示词注入测试手册。
