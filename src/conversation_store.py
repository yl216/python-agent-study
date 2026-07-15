import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONVERSATIONS_DIR = PROJECT_ROOT / "data" / "conversations"


def load_conversation(plan_id: str | None) -> list[dict[str, str]]:
    if not plan_id:
        return []

    path = _conversation_path(plan_id)
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    messages = data.get("messages", [])
    if not isinstance(messages, list):
        return []
    return [
        message
        for message in messages
        if isinstance(message, dict)
        and message.get("role") in {"user", "assistant"}
        and isinstance(message.get("content"), str)
    ]


def save_conversation(plan_id: str | None, messages: list[dict[str, str]]) -> None:
    if not plan_id:
        return

    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
    _conversation_path(plan_id).write_text(
        json.dumps({"plan_id": plan_id, "messages": messages}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_conversation(plan_id: str | None) -> None:
    if not plan_id:
        return

    path = _conversation_path(plan_id)
    if path.exists():
        path.unlink()


def _conversation_path(plan_id: str) -> Path:
    return CONVERSATIONS_DIR / f"{plan_id}.json"
