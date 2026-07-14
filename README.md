# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 7，文件读写能力。

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
/tool <命令>       调用本地工具，例如 /tool summary README.md
/exit              退出程序
```

## 本地工具

```text
/tool calc <表达式>              计算数学表达式
/tool time                      查看当前时间
/tool files                     列出项目根目录文件
/tool note <内容>               保存一条学习笔记到 notes/
/tool read <路径>               读取 Markdown 文件
/tool summary <路径>            总结 Markdown 文件
/tool todos <路径>              提取 TODO 或待办项
/tool save-summary <路径>       保存 Markdown 总结到 notes/summaries/
```

示例：

```text
/tool read notes/07_local_tools.md
/tool summary README.md
/tool todos README.md
/tool save-summary README.md
```

## 文件访问边界

文件工具只能访问项目目录内的 Markdown 文件，不能读取项目外部路径。

这样做是为了避免误读系统文件、密钥文件或其他无关文件。

## 当前模式

- `teacher`：Python 老师
- `explainer`：代码解释器
- `debugger`：错误排查助手
- `planner`：学习计划制定者

## 当前文件

- `src/main.py`：命令行入口、命令处理和工具命令路由。
- `src/tools.py`：本地工具函数，包含文件读写工具。
- `src/prompts.py`：管理不同模式的 system prompt 和安全规则。
- `src/settings.py`：读取并校验环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `.env.example`：配置模板。
- `ERROR_MANUAL.md`：错误手册。
- `PROMPT_INJECTION_TESTS.md`：提示词注入测试手册。
