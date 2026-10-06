# Copyright 2026 Binhex - Oliver García
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    task_ids = fields.One2many(
        comodel_name="project.task",
        inverse_name="business_requirement_id",
        string="Tasks",
        groups="project.group_project_user",
    )
    task_count = fields.Integer(
        compute="_compute_task_count",
        groups="project.group_project_user",
    )

    @api.depends("task_ids")
    def _compute_task_count(self):
        groups = self.env["project.task"]._read_group(
            domain=[("business_requirement_id", "in", self.ids)],
            groupby=["business_requirement_id"],
            aggregates=["__count"],
        )
        data = {requirement.id: count for requirement, count in groups}
        for rec in self:
            rec.task_count = data.get(rec.id, 0)

    def action_view_tasks(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "project.action_view_all_task"
        )
        action["name"] = self.env._("Tasks")
        action["domain"] = [("business_requirement_id", "in", self.ids)]
        action["context"] = (
            {"default_business_requirement_id": self.id} if len(self) == 1 else {}
        )
        return action
