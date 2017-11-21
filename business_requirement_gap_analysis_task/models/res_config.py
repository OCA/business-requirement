# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class BusinessRequirementConfigSettings(models.TransientModel):
    _name = 'business.requirement.gap.task.config.setting'
    _inherit = 'res.config.settings'

    gap_task_category = fields.Many2one(
        'project.category',
        string='Gap Analysis Task Category',
    )

    @api.multi
    def set_business_requirement_gap_task_category_default(self):
        ir_values = self.env['ir.values']
        gap_task_category = self.gap_task_category
        ir_values.set_default(
            'business.requirement.gap.task.config.setting',
            'gap_task_category',
            [gap_task_category.id]
            if gap_task_category else False,
            company_id=self.env.user.company_id.id
        )

    @api.model
    def get_default_gap_task_category(self, fields):
        ir_vaules = self.env['ir.values']
        gap_task_category = None
        if 'gap_task_category' in fields:
            gap_task_category = ir_vaules.get_default(
                'business.requirement.gap.task.config.setting',
                'gap_task_category',
                company_id=self.env.user.company_id.id
            )
        return {'gap_task_category': gap_task_category}
