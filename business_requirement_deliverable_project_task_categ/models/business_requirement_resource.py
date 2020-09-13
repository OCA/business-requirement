# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class BusinessRequirementDeliverableCateg(models.Model):
    _inherit = "business.requirement.resource"

    categ_id = fields.Many2one(
        'project.category',
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
