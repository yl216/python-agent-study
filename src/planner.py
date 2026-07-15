from dataclasses import dataclass


@dataclass
class PlanStep:
    title: str
    goal: str
    exercise: str
    acceptance: str
    done: bool = False


class TaskPlan:
    def __init__(self, goal: str, steps: list[PlanStep]):
        self.goal = goal
        self.steps = steps
        self.current_index = 0

    def show(self) -> str:
        lines = [f"任务目标：{self.goal}", ""]
        for index, step in enumerate(self.steps, start=1):
            status = "完成" if step.done else "进行中" if index - 1 == self.current_index else "待做"
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


def _extract_topic(goal: str) -> str:
    for prefix in ("帮我学习", "学习", "理解", "掌握"):
        if goal.startswith(prefix):
            topic = goal.removeprefix(prefix).strip(" ：:")
            return topic or goal
    return goal
