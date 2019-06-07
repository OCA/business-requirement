# Copyright 2019 Tecnativa Victor M.M. Torres>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang


class BusinessRequirement(models.Model):
    _inherit = 'business.requirement'

    sale_order_ids = fields.One2many(
        comodel_name='sale.order',
        inverse_name='business_requirement_id',
        string='Orders',
    )
    order_count = fields.Integer(
        string='Count',
        compute='_compute_order_count',
    )
    detailed_order = fields.Boolean(
        help='Check this if need generated a detailed order'
    )

    @api.multi
    @api.depends('sale_order_ids')
    def _compute_order_count(self):
        aux_count = 0
        fetch_data = self.env['sale.order'].read_group(
            domain=[('business_requirement_id', 'in', self.ids)],
            fields=['business_requirement_id'],
            groupby=['business_requirement_id'],
        )
        if fetch_data:
            aux_count = fetch_data[0].get(
                'business_requirement_id_count', 0)
        for rec in self:
            rec.order_count = aux_count

    @api.multi
    def convert_requirement_sale(self):
        vals = {
            'br_id': self.id,
            'brd_ids': [(6, 0, self.deliverable_lines.ids)]
        }
        wizard_obj = self.env['business.convert.requirement.sale']
        wizard = wizard_obj.create(vals)
        action = wizard.wizard_view()
        return action

    @api.multi
    def launch_convert_wizard(self):
        vals = {
            'br_id': self.id,
            'brd_ids': [(6, 0, self.deliverable_lines.ids)],
        }
        wizard_obj = self.env['business.convert.requirement.sale']
        wizard = wizard_obj.create(vals)
        action = wizard.wizard_view()
        return action

    @api.multi
    def open_orders(self):
        for self in self:
            domain = [('business_requirement_id', '=', self.id)]
            br_id = 0
            if self.state in ('draft', 'confirmed'):
                br_id = self.id
            return {
                'name': _('Sale Orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form,graph',
                'res_model': 'sale.order',
                'target': 'current',
                'domain': domain,
                'context': {
                    'tree_view_ref': 'sale_order.' +
                    'view_sale_order_tree',
                    'form_view_ref': 'sale_order.' +
                    'view_sale_order_form',
                    'default_sale_order_id': br_id
                }}


class BusinessRequirementDeliverable(models.Model):
    _inherit = 'business.requirement.deliverable'

    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Order Line',
        track_visibility='onchange',)

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            name = '{} - {} '.format(rec.sequence, rec.name,)
            name += ' - (' + formatLang(
                self.env, rec.price_total,
                currency_obj=rec.currency_id)
            name += ')'
            result.append((rec.id, name))
        return result
