# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 9，简单任务规划。

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
/plan <目标>       为学习目标生成步骤计划
/plan-show         查看当前计划
/plan-next         标记当前步骤完成，并进入下一步
/plan-reset        清空当前计划
/exit              退出程序
```

## 任务规划示例

```text
/plan 学习 Python 函数
/plan-show
/plan-next
```

计划会被拆成：

```text
1. 理解核心概念
2. 运行最小示例
3. 做一个小改造
4. 完成练习题
5. 复盘并记录
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

## 当前文件

- `src/main.py`：命令行入口、命令处理、工具、意图和计划命令路由。
- `src/planner.py`：学习任务规划和步骤推进。
- `src/intent_parser.py`：让模型输出 JSON，并解析为 `intent` 和 `argument`。
- `src/tools.py`：本地工具函数，包含文件读写工具。
- `src/prompts.py`：管理不同模式的 system prompt 和安全规则。
- `src/settings.py`：读取并校验环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `ERROR_MANUAL.md`：错误手册。
- `PROMPT_INJECTION_TESTS.md`：提示词注入测试手册。
