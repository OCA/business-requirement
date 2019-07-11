# Copyright 2019 Tecnativa - Victor M.M. Torres
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _


class BusinessRequirementCreateSale(models.TransientModel):
    _name = 'business.requirement.create.sale'
    _description = 'Wizard to create new SO from requirement'

    totaled_method = fields.Selection(
        selection=[
            ('standard', 'Quantity and price unit as is'),
            ('totaled', 'Subtotal as price unit and qty = 1'),
        ],
        required=True,
        default='totaled',
    )
    business_requirement_id = fields.Many2one(
        comodel_name='business.requirement',
        string='Business Requirement',
        required=True,
        domain="[('business_requirement_id', '=', business_requirement_id)]",
    )
    deliverable_ids = fields.Many2many(
        comodel_name='business.requirement.deliverable',
        relation='br_create_sale_brd_rel',
        column1='wizard_id',
        column2='deliverable_id',
        string='Business Requirement Deliverables',
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        context = self.env.context
        if ('business_requirement_id' in fields and
                not res.get('business_requirement_id') and
                context.get('active_model') == 'business.requirement' and
                context.get('active_id')):
            res['business_requirement_id'] = context['active_id']
            br = self.env['business.requirement'].browse(context['active_id'])
            if ('deliverable_ids' in fields and
                    not res.get('deliverable_ids') and
                    res.get('business_requirement_id')):
                res['deliverable_ids'] = [(6, 0, br.deliverable_lines.ids)]
        return res

    def _prepare_sale_layout_category_vals(self, deliverable, line_vals):
        return {
            'name': deliverable.section_id.name,
        }

    def _prepare_sale_order_line_vals(self, deliverable, order_vals):
        vals = {
            'name': deliverable.name,
            'product_id': deliverable.product_id.id,
            'business_requirement_deliverable_id': deliverable.id,
        }
        if self.totaled_method == 'standard':
            vals.update({
                'price_unit': deliverable.sale_price_unit,
                'product_uom_qty': deliverable.qty,
            })
        else:
            vals.update({
                'price_unit': deliverable.price_total,
                'product_uom_qty': 1,
            })
        if deliverable.section_id:
            if not deliverable.section_id.sale_layout_category_id:
                layout_categ = self.env['sale.layout_category'].create(
                    self._prepare_sale_layout_category_vals(deliverable, vals),
                )
                deliverable.section_id.sale_layout_category_id = layout_categ
            vals['layout_category_id'] = (
                deliverable.section_id.sale_layout_category_id.id)
        return vals

    def _prepare_sale_order_vals(self):
        br = self.business_requirement_id
        return {
            'origin': br.name,
            'partner_id': br.partner_id.id,
            'business_requirement_id': br.id,
            'order_line': [],
        }

    def _create_sale_order(self):
        self.ensure_one()
        vals = self._prepare_sale_order_vals()
        for deliverable in self.deliverable_ids:
            line_vals = self._prepare_sale_order_line_vals(deliverable, vals)
            vals['order_line'].append((0, 0, line_vals))
        order = self.env['sale.order'].create(vals)
        msg_body = _("Quotation %s created ") % (
            "<a href=# data-oe-model=sale.order data-oe-id=%d>%s</a>" %
            (order.id, order.name)
        )
        br = self.business_requirement_id
        br.message_post(body=msg_body)
        # post message on the order
        order_msg = _("This quotation has been created from:") + " %s" % (
            "<a href=# data-oe-model=business.requirement data-oe-id=%d>%s</a>"
        ) % (br.id, br.name)
        order.message_post(body=order_msg)
        return order

    def button_create(self):
        order = self._create_sale_order()
        action = self.env.ref('sale.action_quotations').read()[0]
        action.update({
            'view_mode': 'form',
            'views': [],
            'view_id': False,
            'res_id': order.id,
        })
        return action
