# Copyright 2019 Tecnativa Victor M.M. Torres>
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BusinessRequirement(models.Model):
    _inherit = 'business.requirement'

    sale_order_ids = fields.One2many(
        comodel_name='sale.order',
        inverse_name='business_requirement_id',
        string='Sales Orders',
    )
    sale_order_count = fields.Integer(
        string='Sales Orders Count',
        compute='_compute_sale_order_count',
    )

    @api.multi
    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        groups = self.env['sale.order'].read_group(
            domain=[('business_requirement_id', 'in', self.ids)],
            fields=['business_requirement_id'],
            groupby=['business_requirement_id'],
        )
        data = {
            x['business_requirement_id'][0]: x['business_requirement_id_count']
            for x in groups
        }
        for rec in self:
            rec.sale_order_count = data.get(rec.id, 0)

    @api.multi
    def open_orders(self):
        action = self.env.ref('sale.action_quotations').read()[0]
        if len(self) == 1:
            action['context'] = {
                'search_default_business_requirement_id': self.id,
            }
        else:
            action['domain'] = [('business_requirement_id', 'in', self.ids)],
        return action
