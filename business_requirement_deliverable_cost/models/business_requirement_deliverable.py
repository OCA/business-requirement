# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class BusinessRequirementDeliverable(models.Model):
    _inherit = "business.requirement.deliverable"

    @api.multi
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    unit_price = fields.Float('Unit Price')
    price_total = fields.Float('Total Price')
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
            total_revenue_ci = rec.currency_id._convert(
                rec.price_total,
                rec.company_currency_id,
                rec.business_requirement_id.company_id,
                fields.Date.today()
            )
            rec.total_revenue_ci = total_revenue_ci

    @api.multi
    @api.depends('resource_ids', 'resource_ids.price_total')
    def _compute_resource_task_total(self):
        for rec in self:
            resource_task_total = sum(
                rec.mapped('resource_ids').filtered(
                    lambda r: r.resource_type == 'task').mapped(
                    'price_total'))
            rec.resource_task_total = rec.currency_id._convert(
                resource_task_total,
                rec.company_currency_id,
                rec.business_requirement_id.company_id,
                fields.Date.today()
            )

    @api.multi
    @api.depends('resource_ids', 'resource_ids.price_total')
    def _compute_resource_procurement_total(self):
        for rec in self:
            resource_procurement_total = sum(
                rec.mapped('resource_ids').filtered(
                    lambda r: r.resource_type == 'procurement').mapped(
                    'price_total'))
            rec.resource_procurement_total = rec.currency_id._convert(
                resource_procurement_total,
                rec.company_currency_id,
                rec.business_requirement_id.company_id,
                fields.Date.today()
            )

    @api.multi
    @api.depends(
        'price_total',
        'resource_task_total',
        'resource_procurement_total')
    def _compute_gross_profit(self):
        for rec in self:
            gross_profit = rec.price_total - \
                rec.resource_task_total - rec.resource_procurement_total
            rec.gross_profit = rec.currency_id._convert(
                gross_profit,
                rec.company_currency_id,
                rec.business_requirement_id.company_id,
                fields.Date.today()
            )

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
