import ast
import operator
import re
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = PROJECT_ROOT / "notes"
SUMMARY_DIR = NOTES_DIR / "summaries"


class ToolError(ValueError):
    """Raised when a local tool cannot complete a user request."""


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> str:
    if not expression.strip():
        raise ToolError("请提供要计算的表达式。")
    tree = ast.parse(expression, mode="eval")
    result = _eval_math_node(tree.body)
    return str(result)


def _eval_math_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        left = _eval_math_node(node.left)
        right = _eval_math_node(node.right)
        return ALLOWED_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
        return ALLOWED_OPERATORS[type(node.op)](_eval_math_node(node.operand))
    raise ToolError("表达式只能包含数字和 + - * / // % ** 运算。")


def current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def list_files() -> str:
    entries = []
    for path in sorted(PROJECT_ROOT.iterdir(), key=lambda item: item.name.lower()):
        if path.name in {".env", ".venv", ".git", "__pycache__"}:
            continue
        suffix = "/" if path.is_dir() else ""
        entries.append(f"- {path.name}{suffix}")
    return "\n".join(entries) if entries else "当前目录没有可显示的文件。"


def save_note(content: str) -> str:
    content = content.strip()
    if not content:
        raise ToolError("请提供要保存的笔记内容。")

    NOTES_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    note_path = NOTES_DIR / f"tool_note_{timestamp}.md"
    note_path.write_text(f"# 工具保存的笔记\n\n{content}\n", encoding="utf-8")
    return f"笔记已保存：{note_path.relative_to(PROJECT_ROOT)}"


def read_markdown(relative_path: str) -> str:
    path = _resolve_project_file(relative_path)
    if path.suffix.lower() != ".md":
        raise ToolError("当前只允许读取 Markdown 文件。")
    return path.read_text(encoding="utf-8")


def summarize_markdown(relative_path: str) -> str:
    content = read_markdown(relative_path)
    title = _extract_title(content, relative_path)
    headings = _extract_headings(content)
    bullets = _extract_bullets(content)

    lines = [f"# {title} 摘要", "", f"- 字数约：{len(content)} 个字符"]
    if headings:
        lines.append(f"- 主要章节：{', '.join(headings[:6])}")
    if bullets:
        lines.append("- 重点条目：")
        lines.extend(f"  - {item}" for item in bullets[:8])
    if not headings and not bullets:
        preview = content.strip().replace("\n", " ")[:200]
        lines.append(f"- 内容预览：{preview}")

    return "\n".join(lines)


def extract_todos(relative_path: str) -> str:
    content = read_markdown(relative_path)
    todos = []
    for line in content.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if (
            re.match(r"^- \[[ x]\]", lower)
            or lower.startswith(("todo:", "- todo:", "* todo:"))
            or stripped.startswith(("待办:", "- 待办:", "* 待办:"))
        ):
            todos.append(stripped)
    return "\n".join(todos) if todos else "没有找到 TODO 或待办项。"


def save_summary(relative_path: str) -> str:
    summary = summarize_markdown(relative_path)
    source = _resolve_project_file(relative_path)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = SUMMARY_DIR / f"{source.stem}_summary_{timestamp}.md"
    output_path.write_text(summary + "\n", encoding="utf-8")
    return f"总结已保存：{output_path.relative_to(PROJECT_ROOT)}"


def _resolve_project_file(relative_path: str) -> Path:
    if not relative_path.strip():
        raise ToolError("请提供文件路径。")

    path = (PROJECT_ROOT / relative_path.strip()).resolve()
    if PROJECT_ROOT not in path.parents and path != PROJECT_ROOT:
        raise ToolError("只能访问项目目录内的文件。")
    if not path.exists() or not path.is_file():
        raise ToolError(f"文件不存在：{relative_path}")
    return path


def _extract_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return Path(fallback).name


def _extract_headings(content: str) -> list[str]:
    headings = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(stripped.lstrip("#").strip())
    return headings


def _extract_bullets(content: str) -> list[str]:
    bullets = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped.removeprefix("- ").strip())
    return bullets


def format_tools() -> str:
    return """
可用工具：
- calc <表达式>              计算数学表达式，例如 /tool calc 2 * (3 + 4)
- time                      查看当前时间，例如 /tool time
- files                     列出项目根目录文件，例如 /tool files
- note <内容>               保存一条学习笔记，例如 /tool note 今天学了工具调用
- read <路径>               读取 Markdown 文件，例如 /tool read notes/07_local_tools.md
- summary <路径>            总结 Markdown 文件，例如 /tool summary README.md
- todos <路径>              提取 TODO 或待办项，例如 /tool todos README.md
- save-summary <路径>       保存 Markdown 总结，例如 /tool save-summary README.md
""".strip()


def run_tool(raw_command: str) -> str:
    name, _, argument = raw_command.strip().partition(" ")
    name = name.lower()

    if name == "calc":
        return calculate(argument)
    if name == "time":
        return current_time()
    if name == "files":
        return list_files()
    if name == "note":
        return save_note(argument)
    if name == "read":
        return read_markdown(argument)
    if name == "summary":
        return summarize_markdown(argument)
    if name == "todos":
        return extract_todos(argument)
    if name == "save-summary":
        return save_summary(argument)

    raise ToolError(f"未知工具：{name or '(空)'}")
