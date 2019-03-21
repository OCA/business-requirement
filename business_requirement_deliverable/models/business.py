# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    deliverable_lines = fields.One2many(
        comodel_name='business.requirement.deliverable',
        inverse_name='business_requirement_id',
        string='Deliverable Lines',
        copy=True,
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]},
    )

    resource_lines = fields.One2many(
        comodel_name='business.requirement.resource',
        inverse_name='business_requirement_id',
        string='Resource Lines',
        copy=True,
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]},
    )

    total_revenue = fields.Float(
        compute='_compute_deliverable_total',
        string='Total Deliverable',
        store=True
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        compute='_compute_get_currency'
    )
    dl_total_revenue = fields.Float(
        string='DL Total Revenue',
        digit=dp.get_precision('Account'),
        compute='_compute_dl_total_revenue'
    )
    dl_count = fields.Integer('DL Count', compute='_compute_dl_count')
    rl_count = fields.Integer('RL Count', compute='_compute_rl_count')
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )

    @api.multi
    def _compute_dl_total_revenue(self):
        for r in self:
            r.dl_total_revenue = sum(dl.price_total for dl in
                                     r.deliverable_lines)

    @api.multi
    def _compute_dl_count(self):
        for r in self:
            r.dl_count = len(r.deliverable_lines.ids)

    @api.multi
    def _compute_rl_count(self):
        for r in self:
            r.rl_count = len(r.resource_lines.ids)

    @api.multi
    def open_deliverable_line(self):
        for self in self:
            domain = [('business_requirement_id', '=', self.id)]
            br_id = 0
            if self.state in ('draft', 'confirmed'):
                br_id = self.id
            return {
                'name': _('Deliverable Lines'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form,graph',
                'res_model': 'business.requirement.deliverable',
                'target': 'current',
                'domain': domain,
                'context': {
                    'tree_view_ref': 'business_requirement_deliverable.' +
                    'view_business_requirement_deliverable_tree',
                    'form_view_ref': 'business_requirement_deliverable.' +
                    'view_business_requirement_deliverable_form',
                    'default_business_requirement_id': br_id
                }}

    @api.multi
    def open_resource_line(self):
        for self in self:
            res_lines = self.env['business.requirement.resource'].\
                search([('business_requirement_id', '=', self.id)])
            br_id = 0
            if self.state in ('draft', 'confirmed'):
                br_id = self.id
            return {
                'name': _('Resource Lines'),
                'view_type': 'form',
                'view_mode': 'tree,graph',
                'res_model': 'business.requirement.resource',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', res_lines.ids)],
                'context': {
                    'tree_view_ref': 'business_requirement_resource.' +
                    'view_business_requirement_resource_tree',
                    'default_business_requirement_id': br_id
                }
            }

    @api.multi
    @api.depends('pricelist_id')
    def _compute_get_currency(self):
        for br in self:
            if br.partner_id and br.pricelist_id.currency_id:
                br.currency_id = br.pricelist_id.currency_id.id
            else:
                br.currency_id = self.env.user.company_id.currency_id.id

    @api.multi
    @api.onchange('partner_id')
    def partner_id_change(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        """
        pricelist = self.partner_id.property_product_estimation_pricelist or \
                    self.partner_id.property_product_pricelist or False
        if self.partner_id:
            self.update({'pricelist_id': pricelist})
        msg = _(
            'You are changing customer, on a business requirement'
            'which already contains deliverable lines.'
            'Pricelist could be different.'
        )
        if self.deliverable_lines:
            return {
                'warning': {'message': msg}
            }

    @api.multi
    @api.depends(
        'deliverable_lines',
        'deliverable_lines.price_total',
        'company_id.currency_id',
    )
    def _compute_deliverable_total(self):
        for br in self:
            if br.deliverable_lines:
                total_revenue_origin = sum(
                    line.price_total
                    for line in br.deliverable_lines
                )
                if br.partner_id.property_product_pricelist.currency_id:
                    c_id = br.partner_id.property_product_pricelist.currency_id
                    br.total_revenue = c_id._convert(
                        total_revenue_origin,
                        br.company_id.currency_id,
                        br.company_id,
                        fields.Date.today()
                    )
                else:
                    br.total_revenue = total_revenue_origin
