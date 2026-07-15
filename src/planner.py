import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PLANS_DIR = DATA_DIR / "plans"
ACTIVE_PLAN_PATH = DATA_DIR / "active_plan.json"
DEFAULT_MODE = "teacher"


@dataclass
class PlanStep:
    title: str
    goal: str
    exercise: str
    acceptance: str
    done: bool = False


class TaskPlan:
    def __init__(
        self,
        goal: str,
        steps: list[PlanStep],
        current_index: int = 0,
        plan_id: str | None = None,
        created_at: str | None = None,
    ):
        self.goal = goal
        self.steps = steps
        self.current_index = current_index
        self.plan_id = plan_id or _make_plan_id(goal)
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")

    def show(self) -> str:
        lines = [f"计划 ID：{self.plan_id}", f"任务目标：{self.goal}", ""]
        for index, step in enumerate(self.steps, start=1):
            if step.done:
                status = "完成"
            elif index - 1 == self.current_index and not self.is_complete():
                status = "进行中"
            else:
                status = "待做"
            lines.extend(
                [
                    f"{index}. [{status}] {step.title}",
                    f"   目标：{step.goal}",
                    f"   练习：{step.exercise}",
                    f"   验收：{step.acceptance}",
                ]
            )
        return "\n".join(lines)

    def current_step(self) -> str:
        if self.is_complete():
            return "计划已经完成。"

        step = self.steps[self.current_index]
        return "\n".join(
            [
                f"当前步骤：{step.title}",
                f"目标：{step.goal}",
                f"练习：{step.exercise}",
                f"验收：{step.acceptance}",
            ]
        )

    def complete_current(self) -> str:
        if self.is_complete():
            return "计划已经完成。"

        self.steps[self.current_index].done = True
        self.current_index += 1

        if self.is_complete():
            return "很好，这个计划已经全部完成。"
        return self.current_step()

    def is_complete(self) -> bool:
        return self.current_index >= len(self.steps)

    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id,
            "goal": self.goal,
            "created_at": self.created_at,
            "current_index": self.current_index,
            "steps": [asdict(step) for step in self.steps],
        }

    @classmethod
    def from_dict(cls, data: dict):
        steps = [PlanStep(**step) for step in data["steps"]]
        return cls(
            goal=data["goal"],
            steps=steps,
            current_index=int(data.get("current_index", 0)),
            plan_id=data.get("plan_id"),
            created_at=data.get("created_at"),
        )


def create_learning_plan(goal: str) -> TaskPlan:
    goal = goal.strip()
    if not goal:
        raise ValueError("请提供要规划的学习目标。")

    topic = _extract_topic(goal)
    steps = [
        PlanStep(
            title="理解核心概念",
            goal=f"先用自己的话说清楚「{topic}」是什么。",
            exercise=f"让 Agent 用 3 句话解释「{topic}」，然后你复述一遍。",
            acceptance=f"你能不用照抄，说出「{topic}」解决什么问题。",
        ),
        PlanStep(
            title="运行最小示例",
            goal="看到一个最小可运行版本，并确认它真的能跑。",
            exercise=f"写一个不超过 15 行的小例子来演示「{topic}」。",
            acceptance="代码能运行，且你能指出输入、处理、输出分别在哪里。",
        ),
        PlanStep(
            title="做一个小改造",
            goal="把示例从照着写，推进到能主动修改。",
            exercise="改一个参数、输出格式或分支逻辑，观察结果变化。",
            acceptance="你能解释改动前后程序行为有什么不同。",
        ),
        PlanStep(
            title="完成练习题",
            goal="用一个小任务检验自己是否真的理解。",
            exercise=f"让 Agent 出 2 道关于「{topic}」的练习题，并自己作答。",
            acceptance="至少完成 1 道题，并能说明卡住的地方。",
        ),
        PlanStep(
            title="复盘并记录",
            goal="把短期练习沉淀成后续可复习的笔记。",
            exercise="写下今天学到的 3 个概念、1 个错误、1 个下一步问题。",
            acceptance="笔记保存到 notes/，以后能根据它继续学习。",
        ),
    ]
    return TaskPlan(goal=goal, steps=steps)


def save_plan(plan: TaskPlan, mode: str = DEFAULT_MODE) -> None:
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    _plan_path(plan.plan_id).write_text(
        json.dumps(plan.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    set_active_state(plan.plan_id, mode)


def load_plan(plan_id: str | None = None) -> TaskPlan | None:
    target_id = plan_id or get_active_plan_id()
    if not target_id:
        return None

    path = _plan_path(target_id)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return TaskPlan.from_dict(data)


def delete_plan(plan_id: str) -> bool:
    path = _plan_path(plan_id)
    if not path.exists():
        return False
    path.unlink()
    if get_active_plan_id() == plan_id:
        clear_active_plan()
    return True


def list_plans() -> list[TaskPlan]:
    if not PLANS_DIR.exists():
        return []
    plans = []
    for path in sorted(PLANS_DIR.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        data = json.loads(path.read_text(encoding="utf-8"))
        plans.append(TaskPlan.from_dict(data))
    return plans


def format_plan_list() -> str:
    plans = list_plans()
    if not plans:
        return "当前没有保存的计划。"

    active_id = get_active_plan_id()
    lines = ["保存的计划："]
    for plan in plans:
        marker = "*" if plan.plan_id == active_id else " "
        status = "完成" if plan.is_complete() else f"第 {plan.current_index + 1}/{len(plan.steps)} 步"
        lines.append(f"{marker} {plan.plan_id} | {status} | {plan.goal}")
    lines.append("")
    lines.append("使用 /plan-use <id> 切换当前计划。")
    lines.append("使用 /plan-delete <id> --yes 删除计划和该计划下所有 mode 对话。")
    return "\n".join(lines)


def set_active_state(plan_id: str, mode: str) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    ACTIVE_PLAN_PATH.write_text(
        json.dumps(
            {"active_plan_id": plan_id, "active_mode": mode},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def set_active_plan_id(plan_id: str) -> None:
    set_active_state(plan_id, get_active_mode())


def set_active_mode(mode: str) -> None:
    plan_id = get_active_plan_id()
    if plan_id:
        set_active_state(plan_id, mode)
    else:
        DATA_DIR.mkdir(exist_ok=True)
        ACTIVE_PLAN_PATH.write_text(
            json.dumps({"active_plan_id": None, "active_mode": mode}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def get_active_state() -> dict:
    if not ACTIVE_PLAN_PATH.exists():
        return {"active_plan_id": None, "active_mode": DEFAULT_MODE}
    data = json.loads(ACTIVE_PLAN_PATH.read_text(encoding="utf-8"))
    return {
        "active_plan_id": data.get("active_plan_id"),
        "active_mode": data.get("active_mode") or DEFAULT_MODE,
    }


def get_active_plan_id() -> str | None:
    return get_active_state().get("active_plan_id")


def get_active_mode() -> str:
    return get_active_state().get("active_mode") or DEFAULT_MODE


def clear_active_plan() -> None:
    if ACTIVE_PLAN_PATH.exists():
        ACTIVE_PLAN_PATH.unlink()


def _plan_path(plan_id: str) -> Path:
    return PLANS_DIR / f"{plan_id}.json"


def _make_plan_id(goal: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", goal.lower()).strip("-")
    if not slug:
        slug = "plan"
    slug = slug[:32].strip("-") or "plan"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{timestamp}-{slug}"


def _extract_topic(goal: str) -> str:
    for prefix in ("帮我学习", "学习", "理解", "掌握"):
        if goal.startswith(prefix):
            topic = goal.removeprefix(prefix).strip(" ：:")
            return topic or goal
    return goal
