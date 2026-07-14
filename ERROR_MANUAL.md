# Python Agent 错误手册

这份手册记录本项目学习过程中遇到的错误、原因和解决方法。以后每遇到一个典型问题，都把它补进来。

## 001：运行 `python src/main.py` 无反应

### 现象

在终端运行：

```powershell
python src/main.py
```

程序没有打印任何内容，也没有进入输入等待状态。

### 原因

`src/main.py` 里虽然定义了 `main()` 函数，但文件末尾没有调用它。

Python 不会自动执行你定义的函数。下面这段代码只是“声明一个函数”：

```python
def main():
    print("hello")
```

必须显式调用：

```python
main()
```

真实项目里通常使用这个入口写法：

```python
if __name__ == "__main__":
    main()
```

### 解决方法

在 `src/main.py` 文件末尾添加：

```python
if __name__ == "__main__":
    main()
```

### 如何避免

每次写命令行脚本时，都检查文件末尾有没有入口调用。

## 002：`Settings(...)` 参数之间少逗号

### 现象

运行或语法检查时可能出现 `SyntaxError`。

问题代码类似：

```python
return Settings(
    temperature=float(os.getenv("DEEPSEEK_TEMPERATURE", "0.3"))
    max_history_turns=int(os.getenv("MAX_HISTORY_TURNS", "5")),
)
```

### 原因

Python 函数调用里，每个参数之间都需要逗号。上面代码在 `temperature=...` 后面少了一个逗号。

### 解决方法

改成：

```python
return Settings(
    temperature=float(os.getenv("DEEPSEEK_TEMPERATURE", "0.3")),
    max_history_turns=int(os.getenv("MAX_HISTORY_TURNS", "5")),
)
```

### 如何避免

修改代码后运行语法检查：

```powershell
python -m py_compile src/main.py src/settings.py src/deepseek_client.py src/prompts.py
```

## 003：缺少 `DEEPSEEK_API_KEY`

### 现象

程序启动失败，并提示：

```text
请先在 .env 里设置 DEEPSEEK_API_KEY。
```

### 原因

`.env` 里没有填写真实 API Key，或者仍然保留了示例值：

```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 解决方法

打开 `.env`，把 `DEEPSEEK_API_KEY` 改成你的真实 DeepSeek API Key。

### 如何避免

只把 `.env.example` 提交到 GitHub，不要提交 `.env`。

## 004：`DEEPSEEK_TEMPERATURE` 不是数字

### 现象

程序启动失败，并提示：

```text
DEEPSEEK_TEMPERATURE 必须是数字，当前值是：abc
```

### 原因

`.env` 里把温度写成了非数字内容。

### 解决方法

把它改成 `0.0` 到 `2.0` 之间的数字，例如：

```text
DEEPSEEK_TEMPERATURE=0.3
```

## 005：`MAX_HISTORY_TURNS` 超出范围

### 现象

程序启动失败，并提示：

```text
MAX_HISTORY_TURNS 必须在 1 到 20 之间，当前值是：0
```

### 原因

历史轮数必须是合理的正整数。太小没有记忆，太大可能让请求变慢、变贵、变乱。

### 解决方法

改成 `1` 到 `20` 之间的整数，例如：

```text
MAX_HISTORY_TURNS=5
```

## 006：`DEEPSEEK_BASE_URL` 缺少协议

### 现象

程序启动失败，并提示：

```text
DEEPSEEK_BASE_URL 必须以 http:// 或 https:// 开头，当前值是：api.deepseek.com
```

### 原因

URL 必须包含协议，否则 SDK 不知道该用什么方式访问。

### 解决方法

改成完整 URL：

```text
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## 常用排查顺序

1. 先运行 `python -m py_compile src/main.py src/settings.py src/deepseek_client.py src/prompts.py` 检查语法。
2. 再运行 `python src/main.py` 看程序是否启动。
3. 如果没有输出，检查是否调用了 `main()`。
4. 如果提示配置错误，检查 `.env`。
5. 如果报 API 错误，检查 API Key、模型名、余额、网络和 DeepSeek 服务状态。
6. 如果中文显示乱码，优先确认程序功能，再处理终端编码显示。
