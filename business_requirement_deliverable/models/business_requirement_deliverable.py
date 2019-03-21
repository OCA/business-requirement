# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _


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
        store=True
    )
    name = fields.Text('Name', required=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        domain=[('sale_ok', '=', True)]
    )
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='UoM',
        required=True,
        default=lambda self: self.env.ref('uom.product_uom_unit')
    )
    qty = fields.Float(
        string='Quantity',
        default=1
    )
    resource_ids = fields.One2many(
        comodel_name='business.requirement.resource',
        inverse_name='business_requirement_deliverable_id',
        string='Business Requirement Resource',
        copy=True
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
        store=True
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
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
        product = self.product_id

        if product:
            description = product.name_get()[0][1]
            uom_id = product.uom_id.id

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

    @api.onchange('qty')
    def qty_change(self):
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

    @api.onchange('uom_id')
    def product_uom_change(self):
        if self.qty != 0:
            self.qty = self._origin.uom_id._compute_quantity(
                self._origin.qty,
                self.uom_id
            )
