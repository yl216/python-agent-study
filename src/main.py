from deepseek_client import ask_deepseek
from prompts import MODE_LABELS, format_modes, get_prompt
from settings import load_settings
from tools import ToolError, format_tools, run_tool


def trim_history(messages, max_turns):
    return messages[-max_turns * 2 :]


def print_help():
    print(
        """
命令：
/help              查看帮助
/modes             查看可用模式
/mode <name>       切换模式，例如 /mode debugger
/clear             清空当前对话记忆
/tools             查看可用本地工具
/tool <命令>       调用本地工具，例如 /tool summary README.md
/exit              退出程序
""".strip()
    )


def main():
    try:
        settings = load_settings()
    except Exception as error:
        print(f"启动失败：{error}")
        return

    mode = "teacher"
    messages = []
    print("Python Agent 老师已启动。输入 /help 查看命令。")
    print(f"当前模式：{MODE_LABELS[mode]}")

    while True:
        user_input = input("\n你：").strip()
        command = user_input.lower()

        if command in {"/exit", "exit", "quit"}:
            print("Agent 老师：下次继续，我们会进入更强的 Agent 能力。")
            break
        if command == "/help":
            print_help()
            continue
        if command == "/modes":
            print(format_modes())
            continue
        if command == "/tools":
            print(format_tools())
            continue
        if command.startswith("/tool"):
            tool_command = user_input.removeprefix("/tool").strip()
            try:
                result = run_tool(tool_command)
            except (ToolError, SyntaxError, ZeroDivisionError) as error:
                print(f"工具调用失败：{error}")
                continue
            print(f"工具结果：\n{result}")
            continue
        if command == "/clear":
            messages = []
            print("Agent 老师：当前对话记忆已清空。")
            continue
        if command.startswith("/mode "):
            next_mode = command.split(maxsplit=1)[1]
            if next_mode not in MODE_LABELS:
                print("Agent 老师：没有这个模式。")
                print(format_modes())
                continue
            mode = next_mode
            messages = []
            print(f"Agent 老师：已切换到 {MODE_LABELS[mode]}，并清空旧对话记忆。")
            continue
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        messages = trim_history(messages, settings.max_history_turns)

        try:
            answer = ask_deepseek(messages, settings, get_prompt(mode))
        except Exception as error:
            print(f"调用 DeepSeek 失败：{error}")
            messages.pop()
            continue

        print(f"\n{MODE_LABELS[mode]}：\n{answer}")
        messages.append({"role": "assistant", "content": answer})
        messages = trim_history(messages, settings.max_history_turns)


if __name__ == "__main__":
    main()
