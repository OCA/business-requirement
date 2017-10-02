# -*- coding: utf-8 -*-
# © 2016-2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class CrmMakeSale(models.TransientModel):
    _name = "br.crm.lead"

    @api.multi
    def default_partner(self):
        context = self.env.context
        case_id = context and context.get('active_ids', []) or []
        case_id = case_id and case_id[0] or False
        crm_id = self.env['crm.lead'].browse(case_id)
        return crm_id and crm_id.partner_id.id or ''

    partner_id = fields.Many2one(
        'res.partner',
        'Customer',
        default=default_partner
    )
    update_quotation = fields.Boolean('Update existing quotation')

    @api.multi
    def make_order(self):
        context = self.env.context
        case_id = context and context.get('active_ids', []) or []
        case_id = case_id and case_id[0] or False
        crm_id = self.env['crm.lead'].browse(case_id)
        if self.update_quotation and crm_id and crm_id.order_ids:
            for order in crm_id.order_ids:
                if order.order_line:
                    order.order_line.unlink()
        if crm_id and crm_id.project_id:
            partner = crm_id.partner_id
            sale_order = self.env['sale.order']
            pricelist = partner.property_product_pricelist.id
            partner_addr = partner.address_get(
                ['default', 'invoice', 'delivery', 'contact']
            )
            sale_order_vals = {
                'partner_id': partner.id,
                'opportunity_id': crm_id.id,
                'partner_invoice_id': partner_addr['invoice'],
                'partner_shipping_id': partner_addr['delivery'],
                'date_order': fields.datetime.now(),
                }
            for br in crm_id.project_id.br_ids:
                sale_order_vals.update({
                    'client_order_ref': br.name,
                })
                if br and br.pricelist_id:
                    sale_order_vals.update({
                        'pricelist_id': br.pricelist_id.id
                    })
                else:
                    sale_order_vals.update({
                        'pricelist_id': pricelist
                    })
            order_id = sale_order.create(sale_order_vals)
            order_lines = self.prepare_sale_order_line(case_id, order_id.id)
            self.create_sale_order_line(order_lines)
            return {
                'domain': str([('id', 'in', [order_id.id])]),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'name': _('Quotation'),
                'res_id': order_id.id
            }
        if crm_id and crm_id.order_ids:
            return {
                'domain': str([('id', 'in', crm_id.order_ids.ids)]),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'name': _('Quotation'),
                'res_ids': crm_id.order_ids.ids
            }

    def prepare_sale_order_line(self, case_id, order_id):
        lines = []
        case = self.env['crm.lead'].browse(case_id)
        order_id = self.env['sale.order'].browse(order_id)
        linked_brs = case.project_id and case.project_id.br_ids or []
        if not linked_brs:
            raise ValidationError(
                _("""There is no available business requirement to
                    make sale order!"""))
        for br in linked_brs:
            if br.state in ('drop', 'cancel'):
                continue
            for br_line in br.deliverable_lines:
                vals = {
                    'order_id': order_id and order_id.id,
                    'product_id': br_line.product_id.id,
                    'name': br_line.name,
                    'product_uom_qty': br_line.qty,
                    'product_uom': br_line.uom_id.id,
                    'price_unit': br_line.sale_price_unit,
                }
                lines.append(vals)
        return lines

    def create_sale_order_line(self, order_lines):
        saleorder_line_obj = self.env['sale.order.line']
        for line in order_lines:
            saleorder_line_obj.create(line)
