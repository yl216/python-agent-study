# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 6，本地工具调用。

## 安装依赖

```powershell
pip install -r requirements.txt
```

## 配置 DeepSeek

复制 `.env.example` 为 `.env`，然后把 `DEEPSEEK_API_KEY` 改成你的真实 DeepSeek API Key。

```powershell
Copy-Item .env.example .env
```

`.env` 示例：

```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-pro
DEEPSEEK_TEMPERATURE=0.3
MAX_HISTORY_TURNS=5
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
/tool <命令>       调用本地工具，例如 /tool calc 2 * (3 + 4)
/exit              退出程序
```

## 本地工具

```text
/tool calc <表达式>      计算数学表达式
/tool time              查看当前时间
/tool files             列出项目根目录文件
/tool note <内容>       保存一条学习笔记到 notes/
```

示例：

```text
/tool calc 2 * (3 + 4)
/tool time
/tool files
/tool note 今天学习了 Agent 工具调用
```

## 当前模式

- `teacher`：Python 老师
- `explainer`：代码解释器
- `debugger`：错误排查助手
- `planner`：学习计划制定者

## 当前安全规则

- 用户不能通过普通消息修改 Agent 身份或系统规则。
- Agent 不应输出隐藏提示词、系统设定或内部规则原文。
- 多语言、翻译、调试、编号列表等形式的提示词注入都应被当作普通文本处理。
- 安全测试用例记录在 `PROMPT_INJECTION_TESTS.md`。

## 当前文件

- `src/main.py`：命令行入口、命令处理和工具命令路由。
- `src/tools.py`：本地工具函数。
- `src/prompts.py`：管理不同模式的 system prompt 和安全规则。
- `src/settings.py`：读取并校验环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `.env.example`：配置模板。
- `ERROR_MANUAL.md`：错误手册。
- `PROMPT_INJECTION_TESTS.md`：提示词注入测试手册。
