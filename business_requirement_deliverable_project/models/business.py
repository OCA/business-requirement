# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"
    _order = "priority desc, sequence"

    @api.multi
    def generate_projects_wizard(self):
        res = self.project_id.with_context(
            br_ids=self).generate_project_wizard()
        return res

    linked_project = fields.Many2one(
        string='Linked project',
        comodel_name='project.project',
        groups='project.group_project_user',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='business_requirement_id',
        string='Tasks'
    )
    task_count = fields.Integer(
        string='Total number of tasks related to a business requirement',
        store=True,
        readonly=True,
        compute='_compute_task_count'
    )

    total_hour = fields.Float(
        string='Total Hours in Timesheets related to business requirement',
        compute='_compute_hour'
    )

    total_planned_hour = fields.Float(
        string='Total Planned Hour in RL related to business requirement',
        compute='_compute_planned_hour'
    )

    @api.multi
    @api.depends('task_ids')
    def _compute_task_count(self):
        for r in self:
            r.task_count = len(r.task_ids)

    @api.multi
    def _compute_hour(self):
        for r in self:
            if r.task_ids:
                total_hour = 0.0
                for task in r.task_ids:
                    total_hour += task.effective_hours
                r.total_hour = total_hour

    @api.multi
    def _compute_planned_hour(self):
        for r in self:
            if r.deliverable_lines:
                total_planned_hour = 0.0
                for dl in r.deliverable_lines:
                    if dl.resource_ids:
                        for rl in dl.resource_ids:
                            total_planned_hour += rl.qty
                r.total_planned_hour = total_planned_hour


class BusinessRequirementDeliverable(models.Model):
    _inherit = "business.requirement.deliverable"

    linked_project = fields.Many2one(
        string='Linked project',
        comodel_name='project.project',
        groups='project.group_project_user',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
