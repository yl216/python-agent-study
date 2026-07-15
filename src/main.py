from deepseek_client import ask_deepseek
from intent_parser import IntentParseError, parse_intent, parse_intent_locally
from planner import clear_saved_plan, create_learning_plan, load_plan, save_plan
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
/tool <命令>       手动调用本地工具，例如 /tool summary README.md
/intent <请求>     让模型输出 JSON 意图并自动调用工具
/plan <目标>       为学习目标生成步骤计划，并自动保存
/plan-show         查看当前计划
/plan-next         标记当前步骤完成，自动保存，并进入下一步
/plan-reset        清空当前计划和保存文件
/exit              退出程序
""".strip()
    )


def handle_tool_command(tool_command: str):
    try:
        result = run_tool(tool_command)
    except (ToolError, SyntaxError, ZeroDivisionError) as error:
        print(f"工具调用失败：{error}")
        return
    print(f"工具结果：\n{result}")


def handle_intent_command(user_request: str, settings):
    if not user_request:
        print("请在 /intent 后面输入你的请求。")
        return

    try:
        parsed = parse_intent(user_request, settings)
    except IntentParseError as error:
        print(f"意图解析失败：{error}")
        return
    except Exception as error:
        print(f"调用 DeepSeek 解析意图失败，改用本地规则解析：{error}")
        parsed = parse_intent_locally(user_request)

    print(f"解析结果：intent={parsed.intent}, argument={parsed.argument or '(空)'}")

    if parsed.intent == "chat":
        print("这个请求更适合普通聊天，请直接输入问题。")
        return

    tool_command = f"{parsed.intent} {parsed.argument}".strip()
    handle_tool_command(tool_command)


def main():
    try:
        settings = load_settings()
    except Exception as error:
        print(f"启动失败：{error}")
        return

    mode = "teacher"
    messages = []
    current_plan = load_plan()

    print("Python Agent 老师已启动。输入 /help 查看命令。")
    print(f"当前模式：{MODE_LABELS[mode]}")
    if current_plan:
        print("已恢复上次未完成的计划。输入 /plan-show 查看。")

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
            handle_tool_command(user_input.removeprefix("/tool").strip())
            continue
        if command.startswith("/intent"):
            handle_intent_command(user_input.removeprefix("/intent").strip(), settings)
            continue
        if command.startswith("/plan "):
            try:
                current_plan = create_learning_plan(user_input.removeprefix("/plan").strip())
                save_plan(current_plan)
            except ValueError as error:
                print(f"计划创建失败：{error}")
                continue
            print(current_plan.show())
            print("\n计划已保存。输入 /plan-next 完成当前步骤并进入下一步。")
            continue
        if command == "/plan-show":
            print(current_plan.show() if current_plan else "当前没有计划。")
            continue
        if command == "/plan-next":
            if not current_plan:
                print("当前没有计划。")
                continue
            print(current_plan.complete_current())
            save_plan(current_plan)
            continue
        if command == "/plan-reset":
            current_plan = None
            clear_saved_plan()
            print("当前计划已清空，保存文件也已删除。")
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
