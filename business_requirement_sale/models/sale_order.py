# Copyright 2019 Tecnativa Victor M.M. Torres>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    business_requirement_id = fields.Many2one(
        comodel_name='business.requirement',
        string='Business requirement',
    )


class SaleOrderLineSection(models.Model):
    _name = 'sale.order.line.section'
    _description = 'Sale Order Line Section'

    name = fields.Char('Name', required=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    line_section_id = fields.Many2one(
        comodel_name='sale.order.line.section',
        string='Section')
    business_requirement_deliverable_id = fields.Many2one(
        comodel_name='business.requirement.deliverable',
        string='Deliverable')

    @api.multi
    def _totaled_method(self):
        for rec in self:
            rec.write({
                'product_uom_qty': 1,
                'price_unit': rec.price_total,
            })
