# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class BusinessRequirementResourceTemplate(models.Model):
    _inherit = "business.requirement.resource.template"

    categ_id = fields.Many2one(
        'project.category',
        string="Task Category"
    )
