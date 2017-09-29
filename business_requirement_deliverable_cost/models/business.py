# -*- coding: utf-8 -*-
# © 2016-2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


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
        string='Parter ID Related',
        readonly=True,
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
            qty_uom = 0
            product_uom = self.env['product.uom']
            if resource.qty != 0:
                qty_uom = product_uom._compute_quantity(
                    resource.qty,
                    resource.product_id.uom_id.id
                ) / resource.qty
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
    def _get_pricelist(self):
        self.ensure_one()
        if self.partner_id:
            return (
                self.partner_id.property_product_estimation_pricelist or
                self.partner_id.property_product_pricelist)
        else:
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
        # Calculte the sales_price_unit
        self._set_sales_price()
        # Calculate the unit_price
        self._set_cost_price()


class BusinessRequirementDeliverable(models.Model):
    _inherit = "business.requirement.deliverable"

    @api.multi
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    unit_price = fields.Float()
    price_total = fields.Float()
    resource_task_total = fields.Float(
        compute='_compute_resource_task_total',
        string='Total Tasks',
        store=True
    )
    resource_procurement_total = fields.Float(
        compute='_compute_resource_procurement_total',
        string='Total Procurement',
        store=True
    )
    gross_profit = fields.Float(
        string='Est. Gross Profit',
        compute='_compute_gross_profit',
        store=True
    )
    total_revenue_ci = fields.Float(
        compute='_compute_total_revenue_in_ci',
        string='Total Revenue',
    )
    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=_default_currency,
        help="Company Currency Id"
    )
    currency_status = fields.Boolean(
        compute='_compute_currency_status',
        string='Company Currency'
    )

    @api.depends('business_requirement_id.pricelist_id')
    def _compute_currency_status(self):
        for rec in self:
            if rec.business_requirement_id and \
                    rec.business_requirement_id.pricelist_id:
                pricelist_id = rec.business_requirement_id.pricelist_id
                if pricelist_id and pricelist_id.currency_id \
                        and pricelist_id.currency_id.id == \
                        rec.company_currency_id.id:
                    rec.currency_status = True

    @api.depends('currency_id')
    def _compute_total_revenue_in_ci(self):
        for rec in self:
            total_revenue_ci = self.env['res.currency']._compute(
                rec.currency_id, rec.company_currency_id,
                rec.price_total)
            rec.total_revenue_ci = total_revenue_ci

    @api.multi
    @api.depends('resource_ids', 'resource_ids.price_total')
    def _compute_resource_task_total(self):
        for rec in self:
            resource_task_total = sum(
                rec.mapped('resource_ids').filtered(
                    lambda r: r.resource_type == 'task').mapped(
                    'price_total'))
            rec.resource_task_total = self.env['res.currency']._compute(
                rec.currency_id, rec.company_currency_id,
                resource_task_total)

    @api.multi
    @api.depends('resource_ids', 'resource_ids.price_total')
    def _compute_resource_procurement_total(self):
        for rec in self:
            resource_procurement_total = sum(
                rec.mapped('resource_ids').filtered(
                    lambda r: r.resource_type == 'procurement').mapped(
                    'price_total'))
            rec.resource_procurement_total = self.env['res.currency'].\
                _compute(rec.currency_id,
                         rec.company_currency_id,
                         resource_procurement_total)

    @api.multi
    @api.depends(
        'price_total',
        'resource_task_total',
        'resource_procurement_total')
    def _compute_gross_profit(self):
        for rec in self:
            gross_profit = rec.price_total - \
                rec.resource_task_total - rec.resource_procurement_total
            rec.gross_profit = self.env['res.currency']._compute(
                rec.currency_id, rec.company_currency_id,
                gross_profit)

    @api.multi
    def action_button_update_estimation(self):
        for deliverable in self:
            if deliverable.resource_ids:
                for resource in deliverable.resource_ids:
                    resource._set_sales_price()
                    resource._set_cost_price()

    @api.multi
    def action_button_update_total_revenue(self):
        self.sale_price_unit = sum(self.resource_ids.
                                   mapped('sale_price_total'))


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    @api.multi
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    resource_task_total = fields.Float(
        compute='_compute_resource_task_total',
        string='Total Tasks',
        store=True
    )
    resource_procurement_total = fields.Float(
        compute='_compute_resource_procurement_total',
        string='Total Procurement',
        store=True
    )
    gross_profit = fields.Float(
        string='Est. Gross Profit',
        compute='_compute_gross_profit',
        store=True,
    )
    rl_total_cost = fields.Float(
        'RL Total Cost',
        compute='_compute_rl_total_cost',
        digit=dp.get_precision('Account')
    )
    total_revenue_ci = fields.Float(
        compute='_compute_total_revenue_in_ci',
        string='Total Revenue',
    )
    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=_default_currency,
        help="Company Currency Id"
    )
    currency_status = fields.Boolean(
        compute='_compute_currency_status',
        string='Company Currency'
    )

    @api.depends('pricelist_id')
    def _compute_currency_status(self):
        for rec in self:
            if rec.pricelist_id and rec.pricelist_id.currency_id and \
                    rec.pricelist_id.currency_id.id == \
                    rec.company_currency_id.id:
                rec.currency_status = True

    @api.depends('currency_id')
    def _compute_total_revenue_in_ci(self):
        for rec in self:
            total_revenue_ci = self.env['res.currency']._compute(
                rec.currency_id, rec.company_currency_id,
                rec.total_revenue)
            rec.total_revenue_ci = total_revenue_ci

    @api.multi
    @api.depends('deliverable_lines.resource_ids.price_total')
    def _compute_rl_total_cost(self):
        for r in self:
            for dl in r.deliverable_lines:
                r.rl_total_cost += sum(
                    rl.price_total for rl in dl.resource_ids)

    @api.multi
    @api.depends('deliverable_lines', 'deliverable_lines.resource_ids',
                 'deliverable_lines.resource_ids.price_total')
    def _compute_resource_task_total(self):
        for br in self:
            if br.deliverable_lines:
                resource_task_total =\
                    sum(br.mapped('deliverable_lines').mapped('resource_ids')
                        .filtered(lambda r: r.resource_type == 'task')
                        .mapped('price_total'))
                br.resource_task_total = self.env['res.currency']._compute(
                    br.currency_id, br.company_currency_id,
                    resource_task_total)

    @api.multi
    @api.depends('deliverable_lines', 'deliverable_lines.resource_ids',
                 'deliverable_lines.resource_ids.price_total')
    def _compute_resource_procurement_total(self):
        for br in self:
            if br.deliverable_lines:
                resource_procurement_total =\
                    sum(br.mapped('deliverable_lines').mapped('resource_ids')
                        .filtered(lambda r: r.resource_type == 'procurement')
                        .mapped('price_total'))
                br.resource_procurement_total = self.env['res.currency']\
                    ._compute(br.currency_id,
                              br.company_currency_id,
                              resource_procurement_total)

    @api.multi
    @api.depends(
        'total_revenue',
        'resource_task_total',
        'resource_procurement_total')
    def _compute_gross_profit(self):
        for br in self:
            gross_profit = (
                br.total_revenue -
                br.resource_task_total -
                br.resource_procurement_total)
            br.gross_profit = self.env['res.currency']._compute(
                br.currency_id, br.company_currency_id,
                gross_profit)
