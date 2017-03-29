# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class BusinessRequirementResource(models.Model):
    _inherit = "business.requirement.resource"

    sale_price_unit = fields.Float(
        string='Sales Price',
        groups='business_requirement_deliverable.'
        'group_business_requirement_estimation',
    )
    sale_price_total = fields.Float(
        compute='_compute_sale_price_total',
        string='Total Revenue',
        groups='business_requirement_deliverable.'
        'group_business_requirement_estimation',
    )
    unit_price = fields.Float(
        string='Cost Price',
        groups='business_requirement_deliverable_cost.'
        'group_business_requirement_cost_control',
    )
    price_total = fields.Float(
        store=False,
        compute='_compute_get_price_total',
        string='Total Cost',
        groups='business_requirement_deliverable_cost.'
        'group_business_requirement_cost_control',
    )

    partner_id = fields.Many2one(
        'res.partner',
        related='business_requirement_deliverable_id.'
        'business_requirement_id.partner_id',
        string='Parter ID Related',
        readonly=True,
    )

    @api.multi
    @api.depends('unit_price', 'qty')
    def _compute_get_price_total(self):
        for resource in self:
            resource.price_total = resource.unit_price * resource.qty

    @api.multi
    @api.depends('sale_price_unit', 'qty')
    def _compute_sale_price_total(self):
        for resource in self:
            resource.sale_price_total = resource.sale_price_unit * resource.qty

    @api.multi
    def _get_pricelist(self):
        self.ensure_one()
        if self.partner_id:
            if self.partner_id.property_product_pricelist:
                return self.partner_id.property_product_pricelist
        else:
            return False

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        super(BusinessRequirementResource, self).product_id_change()
        unit_price = self.product_id.standard_price
        pricelist_id = self._get_pricelist()
        sale_price_unit = self.product_id.list_price
        if pricelist_id and self.partner_id and self.uom_id:
            product = self.product_id.with_context(
                lang=self.partner_id.lang,
                partner=self.partner_id.id,
                quantity=self.qty,
                pricelist=pricelist_id.id,
                uom=self.uom_id.id,
            )
            sale_price_unit = product.list_price
            unit_price = product.standard_price

        self.unit_price = unit_price
        self.sale_price_unit = sale_price_unit

    @api.multi
    @api.onchange('uom_id', 'qty')
    def product_uom_change(self):
        qty_uom = 0
        unit_price = self.unit_price
        sale_price_unit = self.product_id.list_price
        pricelist = self._get_pricelist()
        product_uom = self.env['product.uom']

        if self.qty != 0:
            qty_uom = product_uom._compute_qty(
                self.uom_id.id,
                self.qty,
                self.product_id.uom_id.id
            ) / self.qty

        if pricelist:
            product = self.product_id.with_context(
                lang=self.partner_id.lang,
                partner=self.partner_id.id,
                quantity=self.qty,
                pricelist=pricelist.id,
                uom=self.uom_id.id,
            )
            unit_price = product.standard_price
            sale_price_unit = product.list_price

        self.unit_price = unit_price * qty_uom
        self.sale_price_unit = sale_price_unit * qty_uom


class BusinessRequirementDeliverable(models.Model):
    _inherit = "business.requirement.deliverable"

    unit_price = fields.Float(
        groups='business_requirement_deliverable.'
        'group_business_requirement_estimation',
    )
    price_total = fields.Float(
        groups='business_requirement_deliverable.'
        'group_business_requirement_estimation',
    )

    @api.multi
    def action_button_update_estimation(self):
        for deliverable in self:
            if deliverable.resource_ids:
                for resource in deliverable.resource_ids:
                    pricelist_id = resource._get_pricelist()
                    resource.sale_price_unit = resource.product_id.lst_price
                    if pricelist_id and resource.partner_id \
                            and resource.uom_id:
                        product = resource.product_id.with_context(
                            lang=resource.partner_id.lang,
                            partner=resource.partner_id.id,
                            quantity=resource.qty,
                            pricelist=pricelist_id.id,
                            uom=resource.uom_id.id,
                        )
                        resource.sale_price_unit = product.price


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    total_revenue = fields.Float(
        store=False,
        groups='business_requirement_deliverable_cost.'
        'group_business_requirement_estimation',
    )
    resource_task_total = fields.Float(
        compute='_compute_resource_task_total',
        string='Total tasks',
        store=False,
        groups='business_requirement_deliverable_cost.'
        'group_business_requirement_cost_control',
    )
    resource_procurement_total = fields.Float(
        compute='_compute_resource_procurement_total',
        string='Total procurement',
        store=False,
        groups='business_requirement_deliverable_cost.'
        'group_business_requirement_cost_control',
    )
    gross_profit = fields.Float(
        string='Estimated Gross Profit',
        compute='_compute_gross_profit',
        groups='business_requirement_deliverable_cost.'
        'group_business_requirement_cost_control',
    )

    @api.multi
    @api.depends('deliverable_lines')
    def _compute_resource_task_total(self):
        for br in self:
            if br.deliverable_lines:
                br.resource_task_total = sum(
                    br.mapped('deliverable_lines').mapped(
                        'resource_ids').filtered(
                        lambda r: r.resource_type == 'task').mapped(
                            'price_total'))

    @api.multi
    @api.depends('deliverable_lines')
    def _compute_resource_procurement_total(self):
        for br in self:
            if br.deliverable_lines:
                br.resource_procurement_total = sum(
                    br.mapped('deliverable_lines').mapped(
                        'resource_ids').filtered(
                        lambda r: r.resource_type == 'procurement').mapped(
                        'price_total'))

    @api.multi
    @api.depends(
        'total_revenue',
        'resource_task_total',
        'resource_procurement_total')
    def _compute_gross_profit(self):
        for br in self:
            br.gross_profit = br.total_revenue - \
                br.resource_task_total - br.resource_procurement_total
