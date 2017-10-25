# -*- coding: utf-8 -*-
# © 2016-2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp


class BusinessRequirementResource(models.Model):
    _name = "business.requirement.resource"
    _description = "Business Requirement Resource"
    _order = 'sequence'

    sequence = fields.Integer('Sequence')
    state = fields.Selection(
        related='business_requirement_id.state',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed'),
                   ('approved', 'Approved'),
                   ('stakeholder_approval', 'Stakeholder Approval'),
                   ('in_progress', 'In progress'),
                   ('done', 'Done'),
                   ('cancel', 'Cancel'),
                   ('drop', 'Drop'),
                   ],
        store=True,
    )
    name = fields.Char('Name', required=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=False
    )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
        required=True
    )
    qty = fields.Float(
        string='Quantity',
        default=1,
    )
    resource_type = fields.Selection(
        selection=[('task', 'Task'), ('procurement', 'Procurement')],
        string='Type',
        required=True,
        default='task'
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assign To',
        ondelete='set null',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
            'approved': [('readonly', False)],
            'stakeholder_approval': [('readonly', False)]}
    )
    business_requirement_deliverable_id = fields.Many2one(
        comodel_name='business.requirement.deliverable',
        string='Business Requirement Deliverable',
        ondelete='cascade'
    )
    business_requirement_id = fields.Many2one(
        comodel_name='business.requirement',
        string='Business Requirement',
        required=True,
    )
    business_requirement_partner_id = fields.Many2one(
        comodel_name='res.partner',
        related='business_requirement_id.partner_id',
        string='Stakeholder',
        store=True
    )
    business_requirement_project_id = fields.Many2one(
        comodel_name='project.project',
        related='business_requirement_id.project_id',
        string='Project',
        store=True
    )
    state = fields.Selection(related='business_requirement_id.state',
                             string='State', store=True, readonly=True)

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        description = ''
        uom_id = False
        product = self.product_id
        if product:
            description = product.name_get()[0][1]
            uom_id = product.uom_id.id
        if product.description_sale:
            description += '\n' + product.description_sale
        if not self.name:
            self.name = description
        if uom_id:
            self.uom_id = uom_id

    @api.onchange('resource_type')
    def resource_type_change(self):
        if self.resource_type == 'procurement':
            self.user_id = False
            self.uom_id = self.env.ref('product.product_uom_unit').id
        else:
            self.uom_id = self.env.ref('product.product_uom_hour').id

    @api.multi
    @api.constrains('resource_type', 'uom_id')
    def _check_description(self):
        for resource in self:
            if resource.resource_type == 'task' and (
                    resource.uom_id.category_id != (
                        self.env.ref('product.uom_categ_wtime'))):
                raise ValidationError(_(
                    "When resource type is task, "
                    "the uom category should be time"))

    @api.multi
    def write(self, vals):
        if vals.get('resource_type', '') == 'procurement':
            vals['user_id'] = None
        return super(BusinessRequirementResource, self).write(vals)


class BusinessRequirementDeliverable(models.Model):
    _name = "business.requirement.deliverable"
    _description = "Business Requirement Deliverable"

    sequence = fields.Integer('Sequence')
    state = fields.Selection(
        related='business_requirement_id.state',
        selection=[('draft', 'Draft'),
                   ('confirmed', 'Confirmed'),
                   ('approved', 'Approved'),
                   ('stakeholder_approval', 'Stakeholder Approval'),
                   ('in_progress', 'In progress'),
                   ('done', 'Done'),
                   ('cancel', 'Cancel'),
                   ('drop', 'Drop'),
                   ],
        store=True,
    )
    name = fields.Text('Name', required=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        domain=[('sale_ok', '=', True)],
        required=False
    )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
        required=True,
        default=lambda self: self.env.ref('product.product_uom_unit')
    )
    qty = fields.Float(
        string='Quantity',
        store=True,
        default=1,
    )
    resource_ids = fields.One2many(
        comodel_name='business.requirement.resource',
        inverse_name='business_requirement_deliverable_id',
        string='Business Requirement Resource',
        copy=True,
    )
    business_requirement_id = fields.Many2one(
        comodel_name='business.requirement',
        string='Business Requirement',
        ondelete='cascade',
        required=True
    )
    sale_price_unit = fields.Float(
        string='Sales Price',
        oldname='unit_price'
    )
    price_total = fields.Float(
        compute='_compute_get_price_total',
        string='Total Deliverable',
        store=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
        compute='_compute_get_currency',
    )
    business_requirement_partner_id = fields.Many2one(
        comodel_name='res.partner',
        related='business_requirement_id.partner_id',
        string='Stakeholder',
        store=True
    )
    business_requirement_project_id = fields.Many2one(
        comodel_name='project.project',
        related='business_requirement_id.project_id',
        string='Project',
        store=True
    )
    state = fields.Selection(related='business_requirement_id.state',
                             string='State', store=True, readonly=True)

    @api.multi
    @api.onchange('business_requirement_id')
    def business_requirement_id_change(self):
        for deliverables in self:
            if deliverables.business_requirement_id:
                for resource in deliverables.resource_ids:
                    resource.business_requirement_id =\
                        deliverables.business_requirement_id

    @api.multi
    @api.depends('business_requirement_id.partner_id')
    def _compute_get_currency(self):
        for brd in self:
            currency_id = brd.business_requirement_id.\
                pricelist_id.currency_id.id
            if currency_id:
                brd.currency_id = currency_id
            else:
                brd.currency_id = self.env.user.company_id.currency_id

    @api.multi
    @api.depends('sale_price_unit', 'qty')
    def _compute_get_price_total(self):
        for brd in self:
            brd.price_total = brd.sale_price_unit * brd.qty

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        description = ''
        uom_id = False
        sale_price_unit = 0
        product = self.product_id

        if product:
            description = product.name_get()[0][1]
            uom_id = product.uom_id.id
            sale_price_unit = product.list_price

        if product.description_sale:
            description += '\n' + product.description_sale

        sale_price_unit = self.product_id.list_price

        if self.business_requirement_id and \
                self.business_requirement_id.pricelist_id:
            product = self.product_id.with_context(
                lang=self.business_requirement_id.partner_id.lang,
                partner=self.business_requirement_id.partner_id.id,
                quantity=self.qty,
                pricelist=self.business_requirement_id.pricelist_id.id,
                uom=self.uom_id.id,
            )
            sale_price_unit = product.price

        if not self.name:
            self.name = description
        if uom_id:
            self.uom_id = uom_id
        self.sale_price_unit = sale_price_unit

    @api.onchange('uom_id', 'qty')
    def product_uom_change(self):
        product_uom = self.env['product.uom']

        if self.qty != 0:
            product_uom._compute_quantity(
                self.uom_id.id, self.qty, self.product_id.uom_id.id) / self.qty

        if self.business_requirement_id and \
                self.business_requirement_id.pricelist_id:
            product = self.product_id.with_context(
                lang=self.business_requirement_id.partner_id.lang,
                partner=self.business_requirement_id.partner_id.id,
                quantity=self.qty,
                pricelist=self.business_requirement_id.pricelist_id.id,
                uom=self.uom_id.id,
            )
            self.sale_price_unit = product.price


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
        readonly=True,
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
        states={'draft': [('readonly', False)]},
    )

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        """
        if self.partner_id:
            values = {
                'pricelist_id':
                    self.partner_id.property_product_estimation_pricelist or
                    self.partner_id.property_product_pricelist or False,
            }
            self.update(values)

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
        for record in self:
            if record.deliverable_lines:
                raise UserError(_(
                    'You are changing customer, on a business requirement'
                    'which already contains deliverable lines.'
                    'Pricelist could be different.'))

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
                    br.total_revenue = \
                        br.partner_id.property_product_pricelist.currency_id\
                        .compute(
                            total_revenue_origin, br.company_id.currency_id)
                else:
                    br.total_revenue = total_revenue_origin
