# Copyright 2026 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command, api, fields, models
from odoo.exceptions import UserError

# The statusbar is clickable, so approval may be skipped to a later state
APPROVED_STATES = ("approved", "in_progress", "done")


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    task_generation = fields.Selection(
        selection=[
            ("none", "Nothing"),
            ("task", "Create tasks in a project"),
            ("project", "Create a new project with tasks"),
        ],
        string="On Approval",
        required=True,
        default="none",
        help="Tasks to create from the deliverables when the requirement is "
        "approved.",
    )
    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
        compute="_compute_project_id",
        store=True,
        readonly=False,
        copy=False,
        domain="[('company_id', 'in', [company_id, False])]",
    )
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
    can_generate_tasks = fields.Boolean(compute="_compute_can_generate_tasks")

    @api.depends("task_generation")
    def _compute_project_id(self):
        """The project chosen for one option doesn't apply to the other one"""
        self.project_id = False

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

    @api.depends("state", "task_generation", "deliverable_lines")
    def _compute_can_generate_tasks(self):
        pending = self._get_deliverables_without_task()
        for rec in self:
            rec.can_generate_tasks = (
                rec.state in APPROVED_STATES
                and rec.task_generation != "none"
                and bool(rec.deliverable_lines & pending)
            )

    def write(self, vals):
        to_generate = self.browse()
        if vals.get("state") in APPROVED_STATES:
            to_generate = self.filtered(lambda rec: rec.state not in APPROVED_STATES)
        res = super().write(vals)
        to_generate._generate_tasks()
        return res

    def _get_deliverables_without_task(self):
        deliverables = self.deliverable_lines
        # Archived tasks still count, so that they aren't created again
        tasks = (
            self.env["project.task"]
            .sudo()
            .with_context(active_test=False)
            .search([("business_requirement_deliverable_id", "in", deliverables.ids)])
        )
        done_ids = set(tasks.business_requirement_deliverable_id.ids)
        return deliverables.filtered(lambda deliverable: deliverable.id not in done_ids)

    def _prepare_project_vals(self):
        self.ensure_one()
        return {
            "name": self.display_name,
            "partner_id": self.partner_id.id,
            "company_id": self.company_id.id,
            # Avoid new tasks to go to an undefined stage
            "type_ids": [
                Command.create({"name": name, "sequence": sequence, "fold": fold})
                for name, sequence, fold in [
                    (self.env._("To Do"), 5, False),
                    (self.env._("In Progress"), 10, False),
                    (self.env._("Done"), 15, False),
                    (self.env._("Cancelled"), 20, True),
                ]
            ],
        }

    def _get_task_project(self):
        self.ensure_one()
        if self.project_id:
            return self.project_id
        if self.task_generation == "task":
            raise UserError(
                self.env._(
                    "Select the project in which to create the tasks of "
                    "%(requirement)s.",
                    requirement=self.display_name,
                )
            )
        project = (
            self.env["project.project"].sudo().create(self._prepare_project_vals())
        )
        self.project_id = project
        return project

    def _generate_tasks(self):
        for requirement in self.filtered(lambda rec: rec.task_generation != "none"):
            deliverables = requirement._get_deliverables_without_task()
            if deliverables:
                deliverables._create_tasks(requirement._get_task_project())
        # The created tasks aren't among the dependencies of this field
        self.invalidate_recordset(["can_generate_tasks"])

    def action_generate_tasks(self):
        self._generate_tasks()
        return True

    def action_view_tasks(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "project.action_view_all_task"
        )
        action["name"] = self.env._("Tasks")
        action["domain"] = [("business_requirement_id", "in", self.ids)]
        action["context"] = {}
        if len(self) == 1:
            action["context"] = {"default_business_requirement_id": self.id}
            if self.project_id:
                action["context"]["default_project_id"] = self.project_id.id
        return action
