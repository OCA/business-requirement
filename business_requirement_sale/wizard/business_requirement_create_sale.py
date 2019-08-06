# Copyright 2019 Tecnativa - Victor M.M. Torres
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


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
    applicable_section_ids = fields.Many2many(
        comodel_name='business.requirement.deliverable.section',
        relation='br_create_sale_applicable_section_rel',
        column1='wizard_id',
        column2='section_id',
        string='Existing Sections',
    )
    section_ids = fields.Many2many(
        comodel_name='business.requirement.deliverable.section',
        relation='br_create_sale_brd_section_rel',
        column1='wizard_id',
        column2='section_id',
        string='Deliverables Sections',
    )
    has_undefined_section = fields.Boolean()
    undefined_section = fields.Boolean()
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
                context.get('active_model') == 'business.requirement' and
                context.get('active_id')):
            res['business_requirement_id'] = context['active_id']
            br = self.env['business.requirement'].browse(context['active_id'])
            if 'deliverable_ids' in fields:
                if not br.deliverable_lines:
                    raise exceptions.UserError(_(
                        'No deliverables found for this business requirement.'
                    ))
            if 'has_undefined_section' in fields:
                res['has_undefined_section'] = any(
                    not x.section_id for x in br.deliverable_lines
                )
            if 'section_ids' in fields:
                sections = br.mapped('deliverable_lines.section_id')
                res['applicable_section_ids'] = [(6, 0, sections.ids)]
        return res

    @api.onchange('section_ids')
    def _onchange_section_ids(self):
        self.ensure_one()
        br = self.business_requirement_id
        new_deliverable_ids = []
        for section in self.applicable_section_ids:
            deliverables = br.deliverable_lines.filtered(
                lambda x: x.section_id == section
            )
            if section in self.section_ids:
                new_deliverable_ids += deliverables.ids
        self.deliverable_ids = [(6, 0, new_deliverable_ids)]

    @api.onchange('undefined_section')
    def _onchange_undefined_section(self):
        self.ensure_one()
        deliverables = self.business_requirement_id.deliverable_lines.filtered(
            lambda x: not x.section_id
        )
        command = 4 if self.undefined_section else 3
        self.deliverable_ids = [(command, x) for x in deliverables.ids]

    def _prepare_sale_order_line_section_vals(
            self, section, sequence):
        vals = {
            'br_deliverable_section_id': section.id,
            'display_type': 'line_section',
            'name': section.name,
            'sequence': sequence,
        }
        return vals

    def _prepare_sale_order_line_vals(
            self, deliverable, sequence):
        vals = {
            'business_requirement_deliverable_id': deliverable.id,
            'name': deliverable.name,
            'product_id': deliverable.product_id.id,
            'sequence': sequence,
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
        previous_section = False
        sequence = 0
        for deliverable in self.deliverable_ids.sorted('section_id'):
            if deliverable.section_id != previous_section:
                if deliverable.section_id:
                    sequence += 1
                    line_vals = self._prepare_sale_order_line_section_vals(
                        deliverable.section_id, sequence)
                    vals['order_line'].append((0, 0, line_vals))
                previous_section = deliverable.section_id
            sequence += 1
            line_vals = self._prepare_sale_order_line_vals(
                deliverable, sequence)
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
        self.ensure_one()
        if not self.deliverable_ids:
            raise exceptions.UserError(_(
                'At least one deliverable must be selected to create the '
                'quotation'
            ))
        order = self._create_sale_order()
        action = self.env.ref('sale.action_quotations').read()[0]
        action.update({
            'view_mode': 'form',
            'views': [],
            'view_id': False,
            'res_id': order.id,
        })
        return action
