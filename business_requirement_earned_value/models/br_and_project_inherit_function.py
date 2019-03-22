# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, api, _


class BusinessRequirementInherit(models.Model):
    _inherit = "business.requirement"

    @api.multi
    def br_open_project_completion_report(self):
        for self in self:
            domain = [('br_id', '=', self.id)]
            return {
                'name': _('BR Project completion report'),
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
                'name': _('Project project completion report'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'graph',
                'res_model': 'project.completion.report',
                'target': 'current',
                'domain': domain,
            }
