# Copyright 2026 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import psycopg2

from odoo.exceptions import AccessError
from odoo.tests import common, new_test_user
from odoo.tools import mute_logger


class TestBusinessRequirementTask(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create(
            {"name": "BR Project", "privacy_visibility": "followers"}
        )
        cls.other_project = cls.env["project.project"].create(
            {"name": "Other Project", "privacy_visibility": "followers"}
        )
        cls.partner = cls.env["res.partner"].create({"name": "BR Customer"})
        cls.br = cls.env["business.requirement"].create(
            {
                "description": "Test requirement",
                "project_id": cls.project.id,
                "partner_id": cls.partner.id,
            }
        )
        cls.task_model = cls.env["project.task"]
        cls.task_open = cls.task_model.create(
            {
                "name": "Open task",
                "project_id": cls.project.id,
                "business_requirement_id": cls.br.id,
                "allocated_hours": 5.0,
            }
        )
        cls.task_done = cls.task_model.create(
            {
                "name": "Done task",
                "project_id": cls.project.id,
                "business_requirement_id": cls.br.id,
                "allocated_hours": 3.0,
                "state": "1_done",
            }
        )

    def test_task_count(self):
        self.assertEqual(self.br.task_count, 2)
        self.assertEqual(self.br.open_task_count, 1)
        self.task_open.state = "1_canceled"
        self.br.invalidate_recordset()
        self.assertEqual(self.br.task_count, 2)
        self.assertEqual(self.br.open_task_count, 0)

    def test_allocated_hours_total(self):
        self.assertEqual(self.br.allocated_hours_total, 8.0)
        br_empty = self.env["business.requirement"].create({"description": "No tasks"})
        self.assertEqual(br_empty.allocated_hours_total, 0.0)
        self.assertEqual(br_empty.task_count, 0)
        self.assertEqual(br_empty.open_task_count, 0)

    def test_onchange_project_from_requirement(self):
        task = self.task_model.new({"business_requirement_id": self.br.id})
        res = task._onchange_business_requirement_id()
        self.assertFalse(res)
        self.assertEqual(task.project_id, self.br.project_id)

    def test_onchange_project_mismatch_warning(self):
        task = self.task_model.new(
            {
                "project_id": self.other_project.id,
                "business_requirement_id": self.br.id,
            }
        )
        res = task._onchange_business_requirement_id()
        self.assertIn("warning", res)
        self.assertEqual(task.project_id, self.other_project)

    def test_ondelete_restrict(self):
        with self.assertRaises(psycopg2.IntegrityError), mute_logger(
            "odoo.sql_db"
        ), self.env.cr.savepoint():
            self.br.unlink()

    def test_action_view_tasks(self):
        action = self.br.action_view_tasks()
        self.assertEqual(action["res_model"], "project.task")
        self.assertEqual(
            action["domain"], [("business_requirement_id", "=", self.br.id)]
        )
        self.assertEqual(
            action["context"]["default_business_requirement_id"], self.br.id
        )

    def test_action_create_task(self):
        action = self.br.action_create_task()
        ctx = action["context"]
        self.assertEqual(ctx["default_business_requirement_id"], self.br.id)
        self.assertEqual(ctx["default_project_id"], self.project.id)
        self.assertEqual(ctx["default_partner_id"], self.partner.id)
        self.assertEqual(ctx["default_name"], self.br.description)

    def test_portal_user_cannot_read_linked_tasks(self):
        portal_user = new_test_user(
            self.env, login="brt_portal", groups="base.group_portal"
        )
        self.br.write({"portal_published": True})
        self.br.message_subscribe(partner_ids=portal_user.partner_id.ids)
        br_as_portal = self.br.with_user(portal_user)
        # The portal user can read the published requirement it follows...
        self.assertEqual(
            br_as_portal.read(["description"])[0]["description"], "Test requirement"
        )
        # ...but not the linked tasks: the project is not portal-visible.
        with self.assertRaises(AccessError):
            self.task_open.with_user(portal_user).read(["name", "allocated_hours"])
        with self.assertRaises(AccessError):
            br_as_portal.task_ids.with_user(portal_user).read(["name"])
