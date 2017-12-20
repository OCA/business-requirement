# -*- coding: utf-8 -*-
# © 2016 Elico Corp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, tools, _


class BusinessRequirementInherit(models.Model):
    _inherit = "business.requirement"

    @api.multi
    def br_open_project_completion_report(self):
        for self in self:
            domain = [('br_id', '=', self.id)]
            return {
                'name': _('BR_Project_completion_report'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'graph',
                'res_model': 'project.completion.report',
                'target': 'current',
                'domain': domain,
            }


class ProjectInherit(models.Model):
    _inherit = "project.project"

    @api.multi
    def project_open_pro_com_trp(self):
        for self in self:
            domain = [('project_id', '=', self.id)]
            return {
                'name': _('Project_project_completion_report'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'graph',
                'res_model': 'project.completion.report',
                'target': 'current',
                'domain': domain,
            }
