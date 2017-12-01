# -*- coding: utf-8 -*-
# Copyright 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class BusinessRequirementGapAnalysis(models.Model):
    _inherit = 'business.requirement'

    gap_analysis_task_id = fields.Many2one(
        comodel_name='project.task',
        inverse_name='business_requirement_id',
        string='Gap Analysis Task',
        help='Use this task to input all the timesheets for the preparation of'
             ' this BR (meetings, solution design, estimation, etc.)'
    )

    @api.multi
    @api.onchange('project_id')
    def master_project_change(self):
        for rec in self.mapped('gap_analysis_task_id'):
            return {
                'warning': {
                    'title': 'Master Project Changed',
                    'message': 'The master project has been changed,'
                               ' if you want to change the '
                               'master project of gap analysis task, '
                               'you have to change it manually.'
                    }
                }
