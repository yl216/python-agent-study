# 第 2 次学习：接入 DeepSeek API

今天的目标是把固定 `print()` 回复，升级成 DeepSeek 模型生成的回复。

## 新增文件

- `.env.example`：环境变量示例，不放真实密钥。
- `requirements.txt`：记录项目依赖。
- `src/settings.py`：读取 DeepSeek 配置。
- `src/deepseek_client.py`：封装模型调用。
- `src/main.py`：负责接收用户问题并打印模型回答。

## 当前流程

1. 用户在终端输入问题。
2. `main.py` 调用 `load_settings()` 读取配置。
3. `deepseek_client.py` 创建 OpenAI 兼容客户端。
4. 程序把问题发送给 DeepSeek。
5. 终端打印模型回答。

## 关键概念

- API：程序和远程服务沟通的接口。
- API Key：证明“我是合法调用者”的密钥。
- SDK：别人封装好的调用工具包。
- base_url：API 服务地址。
- model：要调用的模型名称。
- messages：发送给聊天模型的消息列表。

## 本阶段验收

- API Key 没有写死在代码里。
- 没有 `.env` 时会给出清晰提示。
- 安装依赖并配置密钥后，可以得到 DeepSeek 的回答。

