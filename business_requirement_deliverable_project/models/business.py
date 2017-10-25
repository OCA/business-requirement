# -*- coding: utf-8 -*-
# © 2016-2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    @api.multi
    def generate_projects_wizard(self):
        res = self.project_id.with_context(
            br_ids=self).generate_project_wizard()
        return res

    project_ids = fields.One2many(
        comodel_name='project.project',
        inverse_name='business_requirement_id',
        groups='project.group_project_user',
        readonly=True,
        string='Projects'
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
    linked_project_count = fields.Integer(
        compute='_compute_linked_project_count',
        string="Number of Business Requirements"
    )

    @api.depends('project_ids', 'deliverable_lines')
    def _compute_linked_project_count(self):
        for rec in self:
            rec.linked_project_count = len(rec.project_ids.ids)

    @api.multi
    def action_open_linked_project(self):
        for rec in self:
            domain = ['|',
                      ('business_requirement_id', '=', rec.id),
                      ('business_requirement_deliverable_id', 'in',
                       rec.deliverable_lines.ids)]
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form,graph',
                'res_model': 'project.project',
                'target': 'current',
                'domain': domain
            }

    all_project_generated = fields.Boolean(
        compute='compute_all_project_generated',
        string='All Project Generated'
    )

    @api.depends('business_requirement_ids',
                 'business_requirement_ids.project_ids')
    def compute_all_project_generated(self):
        for rec in self:
            rec.all_project_generated = True
            if rec.business_requirement_ids:
                if rec.business_requirement_ids:
                    for subbr in rec.business_requirement_ids:
                        if not subbr.project_ids and subbr.state == \
                                "stakeholder_approval":
                            rec.all_project_generated = False
            elif rec.project_ids:
                rec.all_project_generated = True
            else:
                rec.all_project_generated = False

    @api.multi
    @api.depends('task_ids')
    def _compute_task_count(self):
        for r in self:
            r.task_count = len(r.task_ids)

    @api.multi
    def _compute_hour(self):
        for r in self:
            total_hour = 0.0
            if r.task_ids:
                for task in r.task_ids:
                    total_hour += task.effective_hours
            r.total_hour = total_hour

    @api.multi
    def _compute_planned_hour(self):
        for r in self:
            total_planned_hour = 0.0
            if r.deliverable_lines:
                for dl in r.deliverable_lines:
                    if dl.resource_ids:
                        for rl in dl.resource_ids:
                            total_planned_hour += rl.qty
            r.total_planned_hour = total_planned_hour


class BusinessRequirementDeliverable(models.Model):
    _inherit = "business.requirement.deliverable"

    project_ids = fields.One2many(
        comodel_name='project.project',
        inverse_name='business_requirement_deliverable_id',
        groups='project.group_project_user',
        readonly=True,
        string='Projects'
    )
    linked_project_count = fields.Integer(
        compute='_compute_linked_project_count',
        string="Number of Business Requirements"
    )

    @api.depends('project_ids')
    def _compute_linked_project_count(self):
        for rec in self:
            rec.linked_project_count = len(rec.project_ids.ids)

    @api.multi
    def action_open_linked_project(self):
        for rec in self:
            domain = [('business_requirement_deliverable_id', '=', rec.id)]
            return {
                'name': _('Projects'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form,graph',
                'res_model': 'project.project',
                'target': 'current',
                'domain': domain
            }
