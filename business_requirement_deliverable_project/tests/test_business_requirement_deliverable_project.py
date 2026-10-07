# Copyright 2026 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import common, new_test_user


class TestBusinessRequirementDeliverableProject(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_model = cls.env["project.task"]
        cls.partner = cls.env["res.partner"].create({"name": "Customer"})
        cls.project = cls.env["project.project"].create({"name": "Existing"})
        cls.uom_hour = cls.env.ref("uom.product_uom_hour")
        cls.uom_day = cls.env.ref("uom.product_uom_day")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.requirement = cls.env["business.requirement"].create(
            {
                "description": "Customer portal",
                "partner_id": cls.partner.id,
                "deliverable_lines": [
                    Command.create(
                        {"name": "Login", "qty": 8, "uom_id": cls.uom_hour.id}
                    ),
                    Command.create(
                        {
                            "name": "Invoice list\nWith filters\nAnd <b>export</b>",
                            "qty": 2,
                            "uom_id": cls.uom_day.id,
                        }
                    ),
                    Command.create(
                        {"name": "Licence", "qty": 3, "uom_id": cls.uom_unit.id}
                    ),
                ],
            }
        )
        cls.login, cls.invoices, cls.licence = cls.requirement.deliverable_lines

    def _approve(self, requirement=None):
        (requirement or self.requirement).write({"state": "approved"})

    def test_nothing_by_default(self):
        self.assertEqual(self.requirement.task_generation, "none")
        self._approve()
        self.assertFalse(self.requirement.task_ids)
        self.assertFalse(self.requirement.can_generate_tasks)

    def test_create_tasks_in_project(self):
        self.requirement.write(
            {"task_generation": "task", "project_id": self.project.id}
        )
        self._approve()
        tasks = self.requirement.task_ids
        self.assertEqual(len(tasks), 3)
        self.assertEqual(self.requirement.task_count, 3)
        self.assertEqual(tasks.project_id, self.project)
        self.assertEqual(tasks.partner_id, self.partner)
        self.assertFalse(tasks.user_ids)
        self.assertEqual(
            tasks.business_requirement_deliverable_id,
            self.requirement.deliverable_lines,
        )
        self.assertFalse(self.requirement.can_generate_tasks)

    def test_task_values(self):
        self.requirement.write(
            {"task_generation": "task", "project_id": self.project.id}
        )
        self._approve()
        by_deliverable = {
            task.business_requirement_deliverable_id: task
            for task in self.requirement.task_ids
        }
        login = by_deliverable[self.login]
        self.assertEqual(login.name, "Login")
        self.assertEqual(login.allocated_hours, 8)
        invoices = by_deliverable[self.invoices]
        # Only the first line is the name, the rest is the description
        self.assertEqual(invoices.name, "Invoice list")
        self.assertIn("With filters<br>", invoices.description)
        self.assertIn("&lt;b&gt;export&lt;/b&gt;", invoices.description)
        # A day of working time is 8 hours
        self.assertEqual(invoices.allocated_hours, 16)
        # Units aren't time, so no time is allocated
        self.assertEqual(by_deliverable[self.licence].allocated_hours, 0)
        messages = "".join(login.message_ids.mapped("body"))
        self.assertIn(self.requirement.name, messages)

    def test_create_tasks_when_skipping_approval(self):
        """The statusbar allows going straight to a later state"""
        self.requirement.write(
            {"task_generation": "task", "project_id": self.project.id}
        )
        self.requirement.state = "done"
        self.assertEqual(self.requirement.task_count, 3)
        self.assertFalse(self.requirement.can_generate_tasks)

    def test_no_tasks_when_moving_on_from_approval(self):
        """Deliverables added after the approval wait for the button"""
        self.requirement.task_generation = "project"
        self._approve()
        self.env["business.requirement.deliverable"].create(
            {"name": "PDF download", "business_requirement_id": self.requirement.id}
        )
        self.requirement.state = "in_progress"
        self.assertEqual(self.requirement.task_count, 3)
        self.assertTrue(self.requirement.can_generate_tasks)

    def test_create_tasks_without_project(self):
        self.requirement.task_generation = "task"
        with self.assertRaises(UserError):
            self._approve()

    def test_create_new_project(self):
        self.requirement.task_generation = "project"
        self._approve()
        project = self.requirement.project_id
        self.assertTrue(project)
        self.assertNotEqual(project, self.project)
        self.assertEqual(project.name, self.requirement.display_name)
        self.assertEqual(project.partner_id, self.partner)
        self.assertEqual(len(project.type_ids), 4)
        self.assertEqual(self.requirement.task_ids.project_id, project)
        self.assertTrue(all(task.stage_id for task in self.requirement.task_ids))

    def test_changing_option_resets_project(self):
        self.requirement.write(
            {"task_generation": "task", "project_id": self.project.id}
        )
        self.requirement.task_generation = "project"
        self.assertFalse(self.requirement.project_id)

    def test_no_duplicated_tasks(self):
        self.requirement.task_generation = "project"
        self._approve()
        project = self.requirement.project_id
        self.requirement.task_ids[0].active = False
        self.requirement.state = "draft"
        self._approve()
        self.assertEqual(self.requirement.project_id, project)
        all_tasks = self.task_model.with_context(active_test=False).search(
            [("business_requirement_id", "=", self.requirement.id)]
        )
        self.assertEqual(len(all_tasks), 3)

    def test_create_tasks_of_new_deliverables(self):
        self.requirement.task_generation = "project"
        self._approve()
        self.env["business.requirement.deliverable"].create(
            {"name": "PDF download", "business_requirement_id": self.requirement.id}
        )
        self.assertTrue(self.requirement.can_generate_tasks)
        self.requirement.action_generate_tasks()
        self.assertEqual(self.requirement.task_count, 4)
        self.assertEqual(
            self.requirement.task_ids.project_id, self.requirement.project_id
        )
        self.assertFalse(self.requirement.can_generate_tasks)

    def test_copied_requirement_creates_its_own_tasks(self):
        self.requirement.task_generation = "project"
        self._approve()
        copy = self.requirement.copy()
        self.assertFalse(copy.project_id)
        self.assertFalse(copy.task_ids)
        self._approve(copy)
        self.assertEqual(copy.task_count, 3)
        self.assertNotEqual(copy.project_id, self.requirement.project_id)

    def test_action_view_tasks_of_one_requirement(self):
        self.requirement.task_generation = "project"
        self._approve()
        action = self.requirement.action_view_tasks()
        self.assertEqual(action["res_model"], "project.task")
        self.assertEqual(
            action["domain"], [("business_requirement_id", "in", self.requirement.ids)]
        )
        self.assertEqual(
            action["context"],
            {
                "default_business_requirement_id": self.requirement.id,
                "default_project_id": self.requirement.project_id.id,
            },
        )

    def test_action_view_tasks_of_several_requirements(self):
        requirements = self.requirement + self.requirement.copy()
        action = requirements.action_view_tasks()
        self.assertEqual(
            action["domain"], [("business_requirement_id", "in", requirements.ids)]
        )
        self.assertEqual(action["context"], {})

    def test_manager_without_project_access_approves(self):
        """Tasks are created even if the approver can't manage projects"""
        manager = new_test_user(
            self.env,
            login="br_manager",
            groups="base.group_user,"
            "business_requirement.group_business_requirement_manager",
        )
        self.requirement.task_generation = "project"
        self._approve(self.requirement.with_user(manager))
        self.assertEqual(self.requirement.task_count, 3)

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
        self.assertNotIn("project_id", arch)
        requirement.web_read({"description": {}, "can_generate_tasks": {}})
