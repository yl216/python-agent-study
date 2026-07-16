from conversation_store import (
    clear_conversation,
    conversation_summary,
    delete_plan_conversations,
    load_conversation,
    rename_plan_conversations,
    save_conversation,
)
from deepseek_client import ask_deepseek
from intent_parser import IntentParseError, parse_intent, parse_intent_locally
from learning_assistant import build_progress, build_quiz, build_review
from planner import (
    clear_active_plan,
    create_learning_plan,
    delete_plan,
    export_plan_markdown,
    format_plan_list,
    get_active_mode,
    load_plan,
    rename_plan_id,
    save_plan,
    set_active_state,
    write_plan,
)
from prompts import MODE_LABELS, format_modes, get_prompt
from settings import load_settings
from tools import ToolError, format_tools, run_tool


def trim_history(messages, max_turns):
    return messages[-max_turns * 2 :]


def active_plan_id(plan):
    return plan.plan_id if plan else None


def print_help():
    print(
        """
命令：
/help                    查看帮助
/modes                   查看可用模式
/mode <name>             切换模式，并加载当前计划下该模式的对话历史
/clear                   清空当前计划 + 当前模式的对话记忆
/tools                   查看可用本地工具
/tool <命令>             手动调用本地工具
/intent <请求>           让模型输出 JSON 意图并自动调用工具
/review                  复习最近学习笔记
/quiz                    根据最近学习笔记生成练习题
/progress                查看计划和笔记进度
/plan <目标>             新建学习计划
/plans                   查看所有保存的计划
/plan-use <id>           切换当前计划
/plan-show               查看当前计划
/plan-next               标记当前步骤完成
/plan-rename <id> <名称> 重命名计划，计划 ID 也会一起改
/plan-done <id>          标记计划完成
/plan-archive <id>       归档计划
/plan-export <id>        导出计划为 Markdown
/plan-reset              取消当前激活计划，不删除历史计划文件
/plan-delete <id>        预览删除计划
/plan-delete <id> --yes  确认删除计划和该计划下所有 mode 对话
/exit                    退出程序
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


def parse_delete_command(user_input: str) -> tuple[str, bool]:
    parts = user_input.split()
    if len(parts) < 2:
        return "", False
    plan_id = parts[1]
    confirmed = len(parts) >= 3 and parts[2] == "--yes"
    return plan_id, confirmed


def parse_id_and_text(user_input: str, command_name: str) -> tuple[str, str]:
    rest = user_input.removeprefix(command_name).strip()
    plan_id, _, text = rest.partition(" ")
    return plan_id.strip(), text.strip()


def describe_delete_impact(plan_id: str) -> str:
    summary = conversation_summary(plan_id)
    lines = [f"将删除计划：{plan_id}", "影响范围：", f"- 计划文件：data/plans/{plan_id}.json"]
    if summary:
        lines.append("- 对话历史：")
        for mode, count in summary.items():
            lines.append(f"  - {mode}: {count} 条消息")
    else:
        lines.append("- 对话历史：无")
    lines.append(f"确认删除请再次输入：/plan-delete {plan_id} --yes")
    return "\n".join(lines)


def main():
    try:
        settings = load_settings()
    except Exception as error:
        print(f"启动失败：{error}")
        return

    mode = get_active_mode()
    if mode not in MODE_LABELS:
        mode = "teacher"
    current_plan = load_plan()
    messages = load_conversation(active_plan_id(current_plan), mode)

    print("Python Agent 老师已启动。输入 /help 查看命令。")
    print(f"当前模式：{MODE_LABELS[mode]}")
    if current_plan:
        print(f"已恢复当前计划：{current_plan.plan_id}。输入 /plan-show 查看。")
        if messages:
            print(f"已恢复该计划在 {MODE_LABELS[mode]} 模式下的 {len(messages)} 条对话消息。")

    while True:
        user_input = input("\n你：").strip()
        command = user_input.lower()

        if command in {"/exit", "exit", "quit"}:
            save_conversation(active_plan_id(current_plan), mode, messages)
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
        if command == "/review":
            print(build_review())
            continue
        if command == "/quiz":
            print(build_quiz())
            continue
        if command == "/progress":
            print(build_progress(current_plan))
            continue
        if command.startswith("/plan "):
            save_conversation(active_plan_id(current_plan), mode, messages)
            try:
                current_plan = create_learning_plan(user_input.removeprefix("/plan").strip())
                save_plan(current_plan, mode)
                messages = load_conversation(current_plan.plan_id, mode)
            except ValueError as error:
                print(f"计划创建失败：{error}")
                continue
            print(current_plan.show())
            print(f"\n计划已保存为独立文件，并设为当前计划。已进入 {MODE_LABELS[mode]} 模式的空对话历史。")
            continue
        if command == "/plans":
            print(format_plan_list())
            continue
        if command.startswith("/plan-use "):
            save_conversation(active_plan_id(current_plan), mode, messages)
            plan_id = user_input.removeprefix("/plan-use").strip()
            selected_plan = load_plan(plan_id)
            if not selected_plan:
                print(f"没有找到计划：{plan_id}")
                continue
            current_plan = selected_plan
            set_active_state(plan_id, mode)
            messages = load_conversation(plan_id, mode)
            print(f"已切换当前计划：{plan_id}")
            print(f"已加载该计划在 {MODE_LABELS[mode]} 模式下的 {len(messages)} 条对话消息。")
            print(current_plan.current_step())
            continue
        if command.startswith("/plan-rename "):
            save_conversation(active_plan_id(current_plan), mode, messages)
            plan_id, new_goal = parse_id_and_text(user_input, "/plan-rename")
            try:
                plan, old_id, new_id = rename_plan_id(plan_id, new_goal)
            except ValueError as error:
                print(f"重命名失败：{error}")
                continue
            rename_plan_conversations(old_id, new_id)
            if current_plan and current_plan.plan_id == old_id:
                current_plan = plan
                messages = load_conversation(new_id, mode)
            print(f"计划已重命名：{old_id} -> {new_id}（{new_goal}）")
            continue
        if command.startswith("/plan-done "):
            plan_id = user_input.removeprefix("/plan-done").strip()
            plan = load_plan(plan_id)
            if not plan:
                print(f"没有找到计划：{plan_id}")
                continue
            plan.mark_done()
            write_plan(plan)
            if current_plan and current_plan.plan_id == plan_id:
                current_plan = plan
            print(f"计划已标记完成：{plan_id}")
            continue
        if command.startswith("/plan-archive "):
            plan_id = user_input.removeprefix("/plan-archive").strip()
            plan = load_plan(plan_id)
            if not plan:
                print(f"没有找到计划：{plan_id}")
                continue
            plan.archive()
            write_plan(plan)
            if current_plan and current_plan.plan_id == plan_id:
                current_plan = plan
            print(f"计划已归档：{plan_id}")
            continue
        if command.startswith("/plan-export "):
            plan_id = user_input.removeprefix("/plan-export").strip()
            plan = load_plan(plan_id)
            if not plan:
                print(f"没有找到计划：{plan_id}")
                continue
            output_path = export_plan_markdown(plan)
            print(f"计划已导出：{output_path.relative_to(output_path.parents[1])}")
            continue
        if command.startswith("/plan-delete "):
            plan_id, confirmed = parse_delete_command(user_input)
            target_plan = load_plan(plan_id)
            if not target_plan:
                print(f"没有找到计划：{plan_id}")
                continue
            if not confirmed:
                print(describe_delete_impact(plan_id))
                continue
            delete_plan(plan_id)
            delete_plan_conversations(plan_id)
            if current_plan and current_plan.plan_id == plan_id:
                current_plan = None
                messages = []
            print(f"已删除计划及其所有 mode 对话历史：{plan_id}")
            continue
        if command == "/plan-show":
            print(current_plan.show() if current_plan else "当前没有激活计划。")
            continue
        if command == "/plan-next":
            if not current_plan:
                print("当前没有激活计划。")
                continue
            print(current_plan.complete_current())
            save_plan(current_plan, mode)
            continue
        if command == "/plan-reset":
            save_conversation(active_plan_id(current_plan), mode, messages)
            current_plan = None
            messages = []
            clear_active_plan()
            print("当前激活计划已取消，历史计划文件和对话文件仍然保留。")
            continue
        if command == "/clear":
            messages = []
            clear_conversation(active_plan_id(current_plan), mode)
            print(f"当前计划在 {MODE_LABELS[mode]} 模式下的对话记忆已清空。")
            continue
        if command.startswith("/mode "):
            next_mode = command.split(maxsplit=1)[1]
            if next_mode not in MODE_LABELS:
                print("Agent 老师：没有这个模式。")
                print(format_modes())
                continue
            save_conversation(active_plan_id(current_plan), mode, messages)
            mode = next_mode
            if current_plan:
                set_active_state(current_plan.plan_id, mode)
            messages = load_conversation(active_plan_id(current_plan), mode)
            print(f"Agent 老师：已切换到 {MODE_LABELS[mode]}。")
            print(f"已加载当前计划在该模式下的 {len(messages)} 条对话消息。")
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
        save_conversation(active_plan_id(current_plan), mode, messages)


if __name__ == "__main__":
    main()
