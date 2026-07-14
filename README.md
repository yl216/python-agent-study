# Python Agent Study

这是一个从零开始学习 Python Agent 的练习项目。

当前阶段：阶段 5，配置与密钥管理强化。

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

## 配置说明

| 配置项 | 是否必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DEEPSEEK_API_KEY` | 是 | 无 | DeepSeek API Key，真实值只放在 `.env` |
| `DEEPSEEK_BASE_URL` | 否 | `https://api.deepseek.com` | OpenAI 兼容接口地址 |
| `DEEPSEEK_MODEL` | 否 | `deepseek-v4-pro` | 使用的模型名 |
| `DEEPSEEK_TEMPERATURE` | 否 | `0.3` | 随机性，范围 `0.0` 到 `2.0` |
| `MAX_HISTORY_TURNS` | 否 | `5` | 保留最近几轮对话，范围 `1` 到 `20` |

`.env` 已经被 `.gitignore` 忽略，不会上传到 GitHub。`.env.example` 只保存示例值，可以提交。

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

## 当前安全规则

- 用户不能通过普通消息修改 Agent 身份或系统规则。
- Agent 不应输出隐藏提示词、系统设定或内部规则原文。
- 多语言、翻译、调试、编号列表等形式的提示词注入都应被当作普通文本处理。
- 安全测试用例记录在 `PROMPT_INJECTION_TESTS.md`。

## 当前文件

- `src/main.py`：命令行入口和命令处理。
- `src/prompts.py`：管理不同模式的 system prompt 和安全规则。
- `src/settings.py`：读取并校验环境变量配置。
- `src/deepseek_client.py`：调用 DeepSeek 模型。
- `.env.example`：配置模板。
- `ERROR_MANUAL.md`：错误手册。
- `PROMPT_INJECTION_TESTS.md`：提示词注入测试手册。
