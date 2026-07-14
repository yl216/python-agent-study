# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 4，Prompt 设计。

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
/exit              退出程序
```

## 当前模式

- `teacher`：Python 老师
- `explainer`：代码解释器
- `debugger`：错误排查助手
- `planner`：学习计划制定者

## 当前目标

- 理解 system prompt 如何影响模型行为。
- 把 prompt 从 API 调用代码中拆出来。
- 支持不同 Agent 工作模式。
- 切换模式时清空旧上下文，避免旧角色干扰新角色。

## 当前文件

- `src/main.py`：命令行入口和命令处理。
- `src/prompts.py`：管理不同模式的 system prompt。
- `src/settings.py`：读取环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `.env.example`：配置模板。
- `ERROR_MANUAL.md`：错误手册。
