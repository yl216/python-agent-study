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
python -m py_compile src/main.py src/settings.py src/deepseek_client.py
```

## 常用排查顺序

1. 先运行 `python -m py_compile ...` 检查语法。
2. 再运行 `python src/main.py` 看程序是否启动。
3. 如果没有输出，检查是否调用了 `main()`。
4. 如果报 API 错误，检查 `.env` 和网络/API Key。
5. 如果中文显示乱码，优先确认程序功能，再处理终端编码显示。
