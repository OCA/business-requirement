# Copyright 2019 Tecnativa - Victor M.M. Torres
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    business_requirement_id = fields.Many2one(
        comodel_name='business.requirement',
        string='Business requirement',
    )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    business_requirement_deliverable_id = fields.Many2one(
        comodel_name='business.requirement.deliverable',
        string='Deliverable')
