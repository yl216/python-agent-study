# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 11，按计划保存对话历史。

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
/clear             清空当前计划的对话记忆
/tools             查看可用本地工具
/tool <命令>       手动调用本地工具，例如 /tool summary README.md
/intent <请求>     让模型输出 JSON 意图并自动调用工具
/plan <目标>       新建学习计划，保存为独立文件，并设为当前计划
/plans             查看所有保存的计划
/plan-use <id>     切换当前计划，并加载该计划的对话历史
/plan-show         查看当前计划
/plan-next         标记当前步骤完成，自动保存，并进入下一步
/plan-reset        取消当前激活计划，不删除历史计划文件
/exit              退出程序
```

## 多计划与对话历史

每个计划都有独立文件：

```text
data/plans/<plan_id>.json
```

每个计划也有自己的对话历史：

```text
data/conversations/<plan_id>.json
```

当前激活计划保存在：

```text
data/active_plan.json
```

当你执行：

```text
/plan-use <id>
```

程序会切换当前计划，并加载这个计划对应的对话历史。

这些 `data/` 下的运行状态文件不会提交到 GitHub。

## 当前能力

- 多轮对话记忆
- Prompt 模式切换
- 提示词注入防护
- 配置校验
- 本地工具调用
- Markdown 文件读写
- 结构化 intent 解析
- 简单任务规划
- 多计划持久化
- 按计划保存对话历史

## 当前文件

- `src/main.py`：命令行入口、命令处理、工具、意图、计划和对话历史路由。
- `src/planner.py`：学习任务规划、步骤推进、多计划保存和恢复。
- `src/conversation_store.py`：按计划保存和加载对话历史。
- `src/intent_parser.py`：让模型输出 JSON，并解析为 `intent` 和 `argument`。
- `src/tools.py`：本地工具函数，包含文件读写工具。
- `src/prompts.py`：管理不同模式的 system prompt 和安全规则。
- `src/settings.py`：读取并校验环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `ERROR_MANUAL.md`：错误手册。
- `PROMPT_INJECTION_TESTS.md`：提示词注入测试手册。
