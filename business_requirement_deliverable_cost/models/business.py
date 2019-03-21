# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


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
            total_revenue_ci = rec.currency_id._convert(
                rec.total_revenue,
                rec.company_currency_id,
                rec.company_id,
                fields.Date.today()
            )
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
                br.resource_task_total = br.currency_id._convert(
                    resource_task_total,
                    br.company_currency_id,
                    br.company_id,
                    fields.Date.today()
                )

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
                br.resource_procurement_total = br.currency_id._convert(
                    resource_procurement_total,
                    br.company_currency_id,
                    br.company_id,
                    fields.Date.today()
                )

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
            br.gross_profit = br.currency_id._convert(
                    gross_profit,
                    br.company_currency_id,
                    br.company_id,
                    fields.Date.today()
                )
