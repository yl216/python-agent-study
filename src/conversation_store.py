import json
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONVERSATIONS_DIR = PROJECT_ROOT / "data" / "conversations"


def load_conversation(plan_id: str | None, mode: str) -> list[dict[str, str]]:
    if not plan_id:
        return []

    path = _conversation_path(plan_id, mode)
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


def save_conversation(plan_id: str | None, mode: str, messages: list[dict[str, str]]) -> None:
    if not plan_id:
        return

    path = _conversation_path(plan_id, mode)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {"plan_id": plan_id, "mode": mode, "messages": messages},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def clear_conversation(plan_id: str | None, mode: str) -> None:
    if not plan_id:
        return

    path = _conversation_path(plan_id, mode)
    if path.exists():
        path.unlink()


def conversation_summary(plan_id: str) -> dict[str, int]:
    plan_dir = CONVERSATIONS_DIR / plan_id
    if not plan_dir.exists():
        return {}

    summary = {}
    for path in sorted(plan_dir.glob("*.json")):
        summary[path.stem] = len(load_conversation(plan_id, path.stem))
    return summary


def delete_plan_conversations(plan_id: str) -> None:
    path = CONVERSATIONS_DIR / plan_id
    if path.exists():
        shutil.rmtree(path)


def _conversation_path(plan_id: str, mode: str) -> Path:
    return CONVERSATIONS_DIR / plan_id / f"{mode}.json"
