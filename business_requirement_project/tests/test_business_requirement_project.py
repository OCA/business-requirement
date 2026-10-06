# Copyright 2026 Binhex - Oliver García
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common, new_test_user


class TestBusinessRequirementProject(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.br_model = cls.env["business.requirement"]
        cls.task_model = cls.env["project.task"]
        cls.project = cls.env["project.project"].create({"name": "Test project"})
        cls.requirement = cls.br_model.create({"description": "Customer portal"})
        cls.other_requirement = cls.br_model.create({"description": "Invoicing"})
        cls.tasks = cls.task_model.create(
            [
                {
                    "name": "Login",
                    "project_id": cls.project.id,
                    "business_requirement_id": cls.requirement.id,
                },
                {
                    "name": "Invoice list",
                    "project_id": cls.project.id,
                    "business_requirement_id": cls.requirement.id,
                },
            ]
        )

    def test_task_count(self):
        self.assertEqual(self.requirement.task_ids, self.tasks)
        self.assertEqual(self.requirement.task_count, 2)
        self.assertEqual(self.other_requirement.task_count, 0)

    def test_task_count_ignores_archived_tasks(self):
        self.tasks[0].active = False
        self.requirement.invalidate_recordset(["task_count"])
        self.assertEqual(self.requirement.task_count, 1)

    def test_action_view_tasks_of_one_requirement(self):
        """A single requirement links the new tasks to itself"""
        action = self.requirement.action_view_tasks()
        self.assertEqual(action["res_model"], "project.task")
        self.assertEqual(
            action["domain"], [("business_requirement_id", "in", self.requirement.ids)]
        )
        self.assertEqual(
            action["context"],
            {"default_business_requirement_id": self.requirement.id},
        )
        task = self.task_model.with_context(**action["context"]).create(
            {"name": "PDF download", "project_id": self.project.id}
        )
        self.assertEqual(task.business_requirement_id, self.requirement)
        self.assertEqual(self.requirement.task_count, 3)

    def test_action_view_tasks_of_several_requirements(self):
        """Several requirements don't propose a default one"""
        requirements = self.requirement + self.other_requirement
        action = requirements.action_view_tasks()
        self.assertEqual(
            action["domain"], [("business_requirement_id", "in", requirements.ids)]
        )
        self.assertEqual(action["context"], {})

    def test_unlink_requirement_keeps_tasks(self):
        self.requirement.unlink()
        self.assertTrue(self.tasks.exists())
        self.assertFalse(self.tasks.business_requirement_id)

    def test_requirement_form_without_project_access(self):
        """Users without project rights can still open requirements"""
        user = new_test_user(
            self.env,
            login="br_user",
            groups="base.group_user,"
            "business_requirement.group_business_requirement_user",
        )
        requirement = self.requirement.with_user(user)
        arch = requirement.get_views([(False, "form")])["views"]["form"]["arch"]
        self.assertNotIn("task_count", arch)
        requirement.web_read({"description": {}})
