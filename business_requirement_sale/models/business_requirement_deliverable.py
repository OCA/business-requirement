# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BusinessRequirementDeliverableSection(models.Model):
    _inherit = 'business.requirement.deliverable.section'

    sale_layout_category_id = fields.Many2one(
        comodel_name='sale.layout_category',
        string='Sales Layout Category',
    )
