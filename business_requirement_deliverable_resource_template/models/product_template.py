# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    resource_lines = fields.One2many(
        comodel_name='business.requirement.resource.template',
        inverse_name='product_template_id',
        string='Business Requirement Resources',
        copy=True,
    )
