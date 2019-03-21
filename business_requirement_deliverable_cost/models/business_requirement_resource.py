# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class BusinessRequirementResource(models.Model):
    _inherit = "business.requirement.resource"

    sale_price_unit = fields.Float(
        string='Sales Price'
    )
    sale_price_total = fields.Float(
        compute='_compute_sale_price_total',
        string='Total Revenue',
        store=True
    )
    unit_price = fields.Float(
        string='Cost Price'
    )
    price_total = fields.Float(
        store=True,
        compute='_compute_get_price_total',
        string='Total Cost'
    )
    partner_id = fields.Many2one(
        'res.partner',
        related='business_requirement_deliverable_id.'
        'business_requirement_id.partner_id',
        string='Parter ID Related'
    )

    @api.multi
    def _set_sales_price(self):
        for resource in self:
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

    @api.multi
    def _set_cost_price(self):
        for resource in self:
            if not resource.product_id:
                continue
            qty_uom = 0
            if resource.qty != 0:
                qty_uom = resource.uom_id._compute_quantity(
                    resource.qty,
                    resource.product_id.uom_id
                )
            resource.unit_price = resource.product_id.standard_price * qty_uom

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
    def _get_partner(self):
        self.ensure_one()
        br_id = br_deliverable = False
        if self.business_requirement_deliverable_id.id:
            br_deliverable = self.business_requirement_deliverable_id
        if self.business_requirement_deliverable_id.\
                business_requirement_id.partner_id:
            br_id = br_deliverable.business_requirement_id
        if br_id and br_id.partner_id:
            return br_id.partner_id
        else:
            return False

    @api.multi
    def _get_pricelist(self):
        self.ensure_one()
        partner_id = self._get_partner()
        if partner_id:
            return (
                partner_id.property_product_estimation_pricelist or
                partner_id.property_product_pricelist)
        return False

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        self.ensure_one()
        super(BusinessRequirementResource, self).product_id_change()
        self._set_sales_price()
        self._set_cost_price()

    @api.multi
    @api.onchange('uom_id', 'qty')
    def product_uom_change(self):
        self.ensure_one()
        # Calculate the sales_price_unit
        self._set_sales_price()
        # Calculate the unit_price
        self._set_cost_price()
