# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 10，计划持久化。

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
/plan <目标>       为学习目标生成步骤计划，并自动保存
/plan-show         查看当前计划
/plan-next         标记当前步骤完成，自动保存，并进入下一步
/plan-reset        清空当前计划和保存文件
/exit              退出程序
```

## 计划持久化

计划会自动保存到：

```text
data/current_plan.json
```

这个文件是运行状态，不提交到 GitHub。

当你退出程序再重新运行：

```powershell
python src/main.py
```

程序会自动读取上次未完成的计划，并提示：

```text
已恢复上次未完成的计划。输入 /plan-show 查看。
```

## 当前能力

- 多轮对话记忆
- Prompt 模式切换
- 提示词注入防护
- 配置校验
- 本地工具调用
- Markdown 文件读写
- 结构化 intent 解析
- 简单任务规划
- 计划持久化

## 当前文件

- `src/main.py`：命令行入口、命令处理、工具、意图和计划命令路由。
- `src/planner.py`：学习任务规划、步骤推进、保存和恢复。
- `src/intent_parser.py`：让模型输出 JSON，并解析为 `intent` 和 `argument`。
- `src/tools.py`：本地工具函数，包含文件读写工具。
- `src/prompts.py`：管理不同模式的 system prompt 和安全规则。
- `src/settings.py`：读取并校验环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `ERROR_MANUAL.md`：错误手册。
- `PROMPT_INJECTION_TESTS.md`：提示词注入测试手册。
