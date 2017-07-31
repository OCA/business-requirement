# -*- coding: utf-8 -*-
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
    def make_orderline(self):
        print "111111111111111111111111111111111111111111"
        context = self.env.context
        print "ccccccccc",context
        case_id = context and context.get('active_ids', []) or []
        print "case_idcase_idcase_id",case_id
        case_id = case_id and case_id[0] or False
        crm_id = self.env['crm.lead'].browse(case_id)
        print "resresres",case_id
        if crm_id and crm_id.project_id:
            partner = crm_id.partner_id
            sale_order = self.env['sale.order']
            partner_obj = self.env['res.partner']
            pricelist = partner.property_product_pricelist.id
            partner_addr = partner.address_get(['default', 'invoice', 'delivery', 'contact'])
            payment_term = partner.property_payment_term_id and partner.property_payment_term_id.id or False
            if not partner and crm_id.partner_id:
                partner = crm_id.partner_id
                fpos = partner.property_account_position_id and partner.property_account_position.id or False
                payment_term = partner.property_payment_term_id and partner.property_payment_term_id.id or False
                partner_addr = partner_obj.address_get(
                    [partner.id],
                    ['default', 'invoice', 'delivery', 'contact']
                )
                pricelist = partner.property_product_pricelist.id
            sale_order_vals = {
                'partner_id': partner.id,
                'opportunity_id': crm_id.id,
                # 'categ_ids': [
                #     (6, 0, [categ_id.id for categ_id in crm_id.categ_ids])],
                'pricelist_id': pricelist,
                'partner_invoice_id': partner_addr['invoice'],
                'partner_shipping_id': partner_addr['delivery'],
                'date_order': fields.datetime.now(),
                }

            print "sale_order_vals",sale_order_vals
            order_id = sale_order.create(sale_order_vals)
            print "order_idorder_idorder_id",order_id
            order_lines = self.prepare_sale_order_line(case_id, order_id)
            self.create_sale_order_line(order_lines)
            message = _(
                "Opportunity has been <b>converted</b> to the quotation <em>%s</em>.") % (
                      sale_order.name)
            crm_id.message_post(body=message)
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

    def prepare_sale_order_line(self, case_id, order_id):
        lines = []
        case = self.env['crm.lead'].browse(case_id)
        linked_brs = case.project_id and case.project_id.br_ids or []
        if not linked_brs:
            raise ValidationError(
                _("""There is no available business requirement to
                    make sale order!"""))
        for br in linked_brs:
            if br.state in ('drop', 'cancel'):
                continue
            for br_line in br.deliverable_lines:
                taxes = br_line.product_id.taxes_id
                taxes = taxes.filtered(
                    lambda x: x.company_id == br.company_id)
                vals = {
                    'order_id': order_id and order_id.id,
                    'product_id': br_line.product_id.id,
                    'name': br_line.name,
                    'product_uom_qty': br_line.qty,
                    'product_uos_qty': br_line.qty,
                    'product_uom': br_line.uom_id.id,
                    'product_uos': br_line.uom_id.id,
                    'price_unit': br_line.sale_price_unit,
                    'tax_id': [(6, 0, taxes.ids)],
                }
                lines.append(vals)
        return lines

    def create_sale_order_line(self, order_lines):
        saleorder_line_obj = self.env['sale.order.line']
        for line in order_lines:
            print "linelinelineline",line
            saleorder_line_obj.create(line)
