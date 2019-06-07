# Copyright 2019 Tecnativa Victor M.M. Torres>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _


class ConvertRequirementSale(models.TransientModel):
    """Wizard to guide create new SO from requirement"""

    _name = 'business.convert.requirement.sale'
    _description = 'Create Quotation'

    totaled_method = fields.Selection([
        ('standard', _('Quantity and price unit as is')),
        ('totaled', _('Sub total as price unit and qty = 1'))],
        required=True,
        default='standard',
    )
    br_id = fields.Many2one(
        comodel_name='business.requirement',
        string='Business requirement',
    )
    brd_ids = fields.Many2many(
        comodel_name='business.requirement.deliverable',
        relation='wizard_brd_rel',
        column1='wizard_id',
        column2='brd_id',
        string='Business requirement Deliverables',
    )

    # @api.onchange('totaled_method')
    # def onchage_totaled_method(self):
    #     if self.totaled_method == 'totaled':
    #         for brd in self.brd_ids:
    #             brd.product_uom_qty = 1

    @api.model
    def default_get(self, fields):
        res = super(ConvertRequirementSale, self).default_get(fields)
        if 'br_id' in fields and not res.get(
            'br_id') and self._context.get(
                'active_model'
        ) == 'business.requirement' and self._context.get('active_id'):
            res.update({
                'br_id': self._context['active_id']
            })
        if 'brd_ids' in fields and not res.get('brd_ids') and res.get('br_id'):
            res.update({'brd_ids': [(6, 0, self.env[
                'business.requirement'].browse(
                    res['br_id']).deliverable_lines.ids)]})
        return res

    @api.multi
    def wizard_view(self):
        view = self.env['ir.model.data'].get_object_reference(
            'business_requirement_sale',
            'view_convert_requirement_sale')
        action = {
            'name': _('Create Quotation'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'views': [(view[1], 'form')],
            'view_id': view[1],
            'target': 'new',
            'res_id': self.ids[0],
            'context': self.env.context,
        }
        return action

    def _prepare_sale_order_line_values(self, br_id, so_id, brd):
        if br_id and so_id and brd:
            values = {
                'name': br_id.name,
                'order_id': so_id.id,
                'product_id': brd.product_id.id,
                'product_uom_qty': brd.qty,
                'price_unit': brd.sale_price_unit,
                'business_requirement_deliverable_id': brd.id,
            }
            if values:
                return values
        return False

    def _prepare_sale_order_values(self, br_id):
        if br_id:
            values = {
                'origin': br_id.name,
                'partner_id': br_id.partner_id.id,
                'business_requirement_id': br_id.id,
            }
            return values
        return False

    def _create_sale_order(self, br_id):
        if br_id:
            vals = self._prepare_sale_order_values(br_id)
            if vals:
                order = self.env['sale.order'].create(vals)
                msg_body = _("""Order Created (%s):
                    <a href=# data-oe-model=sale.order data-oe-id=%d>%s</a>
                """) % (br_id.name, order.id, order.name)
                br_id.message_post(body=msg_body)
                # post message on the order
                order_msg = _("""This order has been created from:
            <a href=# data-oe-model=business.requirement data-oe-id=%d>%s</a>
            (%s)""") % (br_id.id, br_id.name, order.name)
                order.message_post(body=order_msg)
                return order
        return False

    def _create_sale_order_section(self, brd_section):
        if brd_section:
            line_section = self.env['sale.order.line.section'].create({
                'name': brd_section.name,
            })
            return line_section
        return False

    def _create_sale_order_line(self, br_id, so_id, brd_ids):
        if br_id and so_id and brd_ids:
            for brd in brd_ids:
                vals = self._prepare_sale_order_line_values(br_id, so_id, brd)
                if vals:
                    sol = self.env['sale.order.line'].create(vals)
                    if brd.business_requirement_deliverable_section_id:
                        line_section = self._create_sale_order_section(
                            brd.business_requirement_deliverable_section_id
                        )
                        if line_section and sol:
                            sol.write({
                                'line_section_id': line_section.id
                            })
                    if sol and self.totaled_method == 'totaled':
                        sol._totaled_method()
                    brd.write({
                        'sale_order_line_id': sol.id,
                    })

    @api.multi
    def apply(self):
        """Create SO and get to right view"""
        so_id = self._create_sale_order(self.br_id)
        brd_ids = self.brd_ids
        if so_id:
            self._create_sale_order_line(self.br_id, so_id, brd_ids)
        res_model = 'sale.order'
        name = 'Sale Order'
        action = {
            'name': _(name),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': res_model,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'res_id': so_id.id,
        }
        return action
