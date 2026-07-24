# Copyright 2026 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from odoo.addons.project.models.project_task import CLOSED_STATES


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
        help="Project where the tasks of this requirement are executed.",
    )
    task_ids = fields.One2many(
        comodel_name="project.task",
        inverse_name="business_requirement_id",
        string="Tasks",
    )
    task_count = fields.Integer(compute="_compute_task_count")
    open_task_count = fields.Integer(compute="_compute_task_count")
    allocated_hours_total = fields.Float(
        string="Allocated Hours",
        compute="_compute_allocated_hours_total",
        help="Sum of the allocated hours of all the tasks of this requirement.",
    )

    @api.depends("task_ids", "task_ids.state")
    def _compute_task_count(self):
        groups = self.env["project.task"]._read_group(
            [("business_requirement_id", "in", self.ids)],
            groupby=["business_requirement_id", "state"],
            aggregates=["__count"],
        )
        total = {}
        open_ = {}
        for br, state, count in groups:
            total[br.id] = total.get(br.id, 0) + count
            if state not in CLOSED_STATES:
                open_[br.id] = open_.get(br.id, 0) + count
        for br in self:
            br.task_count = total.get(br.id, 0)
            br.open_task_count = open_.get(br.id, 0)

    @api.depends("task_ids.allocated_hours")
    def _compute_allocated_hours_total(self):
        groups = self.env["project.task"]._read_group(
            [("business_requirement_id", "in", self.ids)],
            groupby=["business_requirement_id"],
            aggregates=["allocated_hours:sum"],
        )
        data = {br.id: hours for br, hours in groups}
        for br in self:
            br.allocated_hours_total = data.get(br.id) or 0.0

    def action_view_tasks(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Tasks"),
            "res_model": "project.task",
            "view_mode": "tree,kanban,form",
            "domain": [("business_requirement_id", "=", self.id)],
            "context": {
                "default_business_requirement_id": self.id,
                "default_project_id": self.project_id.id,
            },
        }

    def action_create_task(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Create Task"),
            "res_model": "project.task",
            "view_mode": "form",
            "context": {
                "default_business_requirement_id": self.id,
                "default_project_id": self.project_id.id,
                "default_partner_id": self.partner_id.id,
                "default_name": self.description,
            },
        }
