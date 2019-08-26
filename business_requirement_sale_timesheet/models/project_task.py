# Copyright 2019 Tecnativa - Victor M.M. Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    business_requirement_deliverable_id = fields.Many2one(
        comodel_name='business.requirement.deliverable',
        related='sale_line_id.business_requirement_deliverable_id',
        readonly=True,
        string='Deliverable',
    )

    @api.multi
    def action_view_deliverable(self):
        action = self.env.ref(
            'business_requirement_deliverable.action_deliverable_lines'
        ).read()[0]
        action.update({
            'view_mode': 'form',
            'views': [],
            'view_id': False,
            'res_id': self.business_requirement_deliverable_id.id,
        })
        return action
