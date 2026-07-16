import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

import conversation_store
import planner
from planner import PlanStep, TaskPlan


class PlanManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name) / "data"

        self.original_planner_paths = {
            "DATA_DIR": planner.DATA_DIR,
            "PLANS_DIR": planner.PLANS_DIR,
            "ACTIVE_PLAN_PATH": planner.ACTIVE_PLAN_PATH,
            "EXPORT_DIR": planner.EXPORT_DIR,
        }
        self.original_conversations_dir = conversation_store.CONVERSATIONS_DIR

        planner.DATA_DIR = self.data_dir
        planner.PLANS_DIR = self.data_dir / "plans"
        planner.ACTIVE_PLAN_PATH = self.data_dir / "active_plan.json"
        planner.EXPORT_DIR = self.data_dir / "plan_exports"
        conversation_store.CONVERSATIONS_DIR = self.data_dir / "conversations"

    def tearDown(self):
        planner.DATA_DIR = self.original_planner_paths["DATA_DIR"]
        planner.PLANS_DIR = self.original_planner_paths["PLANS_DIR"]
        planner.ACTIVE_PLAN_PATH = self.original_planner_paths["ACTIVE_PLAN_PATH"]
        planner.EXPORT_DIR = self.original_planner_paths["EXPORT_DIR"]
        conversation_store.CONVERSATIONS_DIR = self.original_conversations_dir
        self.temp_dir.cleanup()

    def test_rename_plan_updates_id_active_state_and_conversations(self):
        plan = self.make_plan("old-plan", "old goal")
        planner.write_plan(plan)
        planner.set_active_state("old-plan", "debugger")
        conversation_store.save_conversation(
            "old-plan",
            "debugger",
            [{"role": "user", "content": "hello"}],
        )

        renamed_plan, old_id, new_id = planner.rename_plan_id("old-plan", "learn functions")
        conversation_store.rename_plan_conversations(old_id, new_id)

        self.assertEqual(old_id, "old-plan")
        self.assertEqual(new_id, "learn-functions")
        self.assertEqual(renamed_plan.plan_id, "learn-functions")
        self.assertEqual(planner.get_active_plan_id(), "learn-functions")
        self.assertIsNone(planner.load_plan("old-plan"))
        self.assertEqual(planner.load_plan("learn-functions").goal, "learn functions")
        self.assertEqual(
            conversation_store.load_conversation("learn-functions", "debugger"),
            [{"role": "user", "content": "hello"}],
        )
        self.assertEqual(conversation_store.conversation_summary("old-plan"), {})

    def test_delete_plan_removes_all_mode_conversations(self):
        plan = self.make_plan("delete-me", "delete goal")
        planner.write_plan(plan)
        planner.set_active_state("delete-me", "teacher")
        conversation_store.save_conversation(
            "delete-me",
            "teacher",
            [{"role": "user", "content": "teacher history"}],
        )
        conversation_store.save_conversation(
            "delete-me",
            "planner",
            [{"role": "assistant", "content": "planner history"}],
        )

        deleted = planner.delete_plan("delete-me")
        conversation_store.delete_plan_conversations("delete-me")

        self.assertTrue(deleted)
        self.assertIsNone(planner.load_plan("delete-me"))
        self.assertIsNone(planner.get_active_plan_id())
        self.assertEqual(conversation_store.conversation_summary("delete-me"), {})

    def test_rename_plan_rejects_empty_name(self):
        plan = self.make_plan("keep-me", "keep goal")
        planner.write_plan(plan)

        with self.assertRaises(ValueError):
            planner.rename_plan_id("keep-me", "   ")

        self.assertEqual(planner.load_plan("keep-me").goal, "keep goal")

    def test_rename_plan_uses_unique_id_when_target_exists(self):
        source = self.make_plan("source-plan", "source goal")
        existing = self.make_plan("learn-functions", "existing goal")
        planner.write_plan(source)
        planner.write_plan(existing)

        renamed_plan, old_id, new_id = planner.rename_plan_id("source-plan", "learn functions")

        self.assertEqual(old_id, "source-plan")
        self.assertEqual(new_id, "learn-functions-2")
        self.assertEqual(renamed_plan.plan_id, "learn-functions-2")
        self.assertEqual(planner.load_plan("learn-functions").goal, "existing goal")
        self.assertEqual(planner.load_plan("learn-functions-2").goal, "learn functions")

    def test_delete_missing_plan_returns_false(self):
        self.assertFalse(planner.delete_plan("missing-plan"))

    def test_conversations_are_isolated_by_mode(self):
        conversation_store.save_conversation(
            "mode-plan",
            "teacher",
            [{"role": "user", "content": "teacher message"}],
        )
        conversation_store.save_conversation(
            "mode-plan",
            "planner",
            [{"role": "assistant", "content": "planner message"}],
        )

        conversation_store.clear_conversation("mode-plan", "teacher")

        self.assertEqual(conversation_store.load_conversation("mode-plan", "teacher"), [])
        self.assertEqual(
            conversation_store.load_conversation("mode-plan", "planner"),
            [{"role": "assistant", "content": "planner message"}],
        )

    def make_plan(self, plan_id, goal):
        return TaskPlan(
            goal=goal,
            plan_id=plan_id,
            steps=[
                PlanStep(
                    title="step",
                    goal="goal",
                    exercise="exercise",
                    acceptance="acceptance",
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
