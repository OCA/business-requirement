# -*- coding: utf-8 -*-
# © 2016 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class BusinessRequirementDeliverableCateg(models.Model):
    _inherit = "business.requirement.resource"

    categ_id = fields.Many2one(
        'project.category.main',
        string="Task Category"
    )

    @api.onchange('resource_type')
    def resource_type_change(self):
        super(BusinessRequirementDeliverableCateg, self).resource_type_change()
        if self.resource_type == 'procurement':
            self.categ_id = False

    @api.multi
    def write(self, vals):
        if vals.get('resource_type', '') == 'procurement':
            vals['categ_id'] = None
        return super(BusinessRequirementDeliverableCateg, self).write(vals)
