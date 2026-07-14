import ast
import operator
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = PROJECT_ROOT / "notes"


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


def format_tools() -> str:
    return """
可用工具：
- calc <表达式>       计算数学表达式，例如 /tool calc 2 * (3 + 4)
- time               查看当前时间，例如 /tool time
- files              列出项目根目录文件，例如 /tool files
- note <内容>        保存一条学习笔记，例如 /tool note 今天学了工具调用
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

    raise ToolError(f"未知工具：{name or '(空)'}")
