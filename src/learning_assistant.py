from pathlib import Path

from planner import TaskPlan, list_plans


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = PROJECT_ROOT / "notes"


def build_review(limit: int = 5) -> str:
    notes = recent_notes(limit)
    if not notes:
        return "还没有找到学习笔记。先完成一个阶段，或在 notes/ 里保存 Markdown 笔记。"

    lines = ["# 最近学习复习", ""]
    for path in notes:
        content = path.read_text(encoding="utf-8")
        lines.append(f"## {extract_title(content, path)}")
        bullets = extract_bullets(content)
        headings = extract_headings(content)
        if headings:
            lines.append(f"- 主要章节：{', '.join(headings[:4])}")
        if bullets:
            lines.append("- 重点：")
            lines.extend(f"  - {item}" for item in bullets[:5])
        if not headings and not bullets:
            lines.append(f"- 内容预览：{compact_preview(content)}")
        lines.append("")

    lines.append("复习建议：先用自己的话复述每个标题，再挑一个重点写 3 行小结。")
    return "\n".join(lines).strip()


def build_quiz(limit: int = 5) -> str:
    notes = recent_notes(limit)
    if not notes:
        return "还没有足够的学习笔记生成练习题。先完成一个阶段，或在 notes/ 里保存 Markdown 笔记。"

    topics = []
    for path in notes:
        content = path.read_text(encoding="utf-8")
        title = extract_title(content, path)
        headings = extract_headings(content)
        topics.append(f"{title}：{headings[0]}" if headings else title)

    lines = ["# 练习题", ""]
    for index, topic in enumerate(topics[:3], start=1):
        lines.append(f"{index}. 请用自己的话解释：{topic}")
    lines.extend(
        [
            "",
            "加练：从上面任选一题，写一个最小代码例子或命令例子。",
            "完成后把答案直接发给 Agent，让它帮你检查。",
        ]
    )
    return "\n".join(lines)


def build_progress(plan: TaskPlan | None) -> str:
    notes = recent_notes(3)
    all_notes = recent_notes(1000)
    plans = list_plans()
    done_plans = [item for item in plans if item.status == "done"]
    active_plans = [item for item in plans if item.status == "active"]

    lines = ["# 学习进度", ""]
    lines.append(f"- 保存的计划数：{len(plans)}")
    lines.append(f"- 进行中的计划：{len(active_plans)}")
    lines.append(f"- 已完成的计划：{len(done_plans)}")
    lines.append(f"- 学习笔记数：{len(all_notes)}")

    if plan:
        lines.extend(
            [
                "",
                "## 当前计划",
                f"- ID：{plan.plan_id}",
                f"- 目标：{plan.goal}",
                f"- 状态：{plan.status}",
                f"- 进度：{plan.progress_label()}",
            ]
        )
    else:
        lines.extend(["", "## 当前计划", "- 当前没有激活计划。"])

    if notes:
        lines.extend(["", "## 最近笔记"])
        for path in notes:
            content = path.read_text(encoding="utf-8")
            lines.append(f"- {path.relative_to(PROJECT_ROOT)}：{extract_title(content, path)}")

    return "\n".join(lines)


def recent_notes(limit: int) -> list[Path]:
    if not NOTES_DIR.exists():
        return []
    notes = [
        path
        for path in NOTES_DIR.glob("*.md")
        if path.is_file() and not path.name.startswith("tool_note_")
    ]
    return sorted(notes, key=lambda path: path.stat().st_mtime, reverse=True)[:limit]


def extract_title(content: str, path: Path) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return path.stem


def extract_headings(content: str) -> list[str]:
    headings = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            headings.append(stripped.removeprefix("## ").strip())
    return headings


def extract_bullets(content: str) -> list[str]:
    bullets = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped.removeprefix("- ").strip())
    return bullets


def compact_preview(content: str, limit: int = 140) -> str:
    return " ".join(content.split())[:limit]
