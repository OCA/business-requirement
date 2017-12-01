# -*- coding: utf-8 -*-
# Copyright 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'br.gap_analysis_task_id'

    estimated_time = fields.Float(string='estimated hours',
                                  widget='float_time')

    def _get_br_id(self):
        return self.env['business.requirement'].browse(
            self._context.get('active_id'))

    @api.multi
    def _get_analysis_br(self):
        br = self._get_br_id()
        name = 'Gap Analysis for {}'.format(br.name)
        category = self.env[
            'business.requirement.gap.task.config.setting'
        ].get_default_gap_task_category(
            ['gap_task_category_id'])['gap_task_category_id']
        category_id = category[0] if category else None
        project_id = br.project_id
        assigned_to = self.env.user
        vals = {'business_requirement_id': br.id,
                'name': name,
                'categ_id': category_id,
                'user_id': assigned_to.id,
                'project_id': project_id.id,
                }
        return vals

    @api.multi
    def apply(self):
        vals = self._get_analysis_br()
        vals.update({'planned_hours': self.estimated_time})
        task = self.env['project.task'].create(vals)
        br = self.env['business.requirement'].browse(
            vals.get('business_requirement_id'))
        br.write({'gap_analysis_task_id': task.id})
