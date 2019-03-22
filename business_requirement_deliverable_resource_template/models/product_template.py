# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    resource_lines = fields.One2many(
        comodel_name='business.requirement.resource.template',
        inverse_name='product_template_id',
        string='Business Requirement Resources',
        copy=True,
    )
