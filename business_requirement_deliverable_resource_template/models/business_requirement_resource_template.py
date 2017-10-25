# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BusinessRequirementDeliverable(models.Model):
    _inherit = "business.requirement.deliverable"

    def _prepare_resource_lines(self):
        rl_data = self.env['business.requirement.resource.template'].search(
            [('product_template_id', '=', self.product_id.product_tmpl_id.id)],
            order='sequence')
        data = []
        for rec in rl_data:
            data.append(rec.copy_data()[0])
        return [(0, 0, item) for index, item in enumerate(data)]

    @api.onchange('product_id')
    def product_id_change(self):
        super(BusinessRequirementDeliverable, self).product_id_change()
        product = self.product_id
        if product:
            self.resource_ids = self._prepare_resource_lines()
        business_requirement = self.business_requirement_id
        if business_requirement:
            for resource in self.resource_ids:
                resource.business_requirement_id = business_requirement


class BusinessRequirementResourceTemplate(models.Model):
    _name = "business.requirement.resource.template"

    product_template_id = fields.Many2one(
        comodel_name='product.template',
        string='Product',
        ondelete='set null',
        copy=False
    )
    sequence = fields.Integer('Sequence')
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
        # FIXME: selection should be on a constant imported
        selection=[('task', 'Task'), ('procurement', 'Procurement')],
        string='Type',
        required=True,
        default='task'
    )

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
        self.name = description
        self.uom_id = uom_id

    @api.multi
    @api.constrains('resource_type', 'uom_id')
    def _check_description(self):
        for resource in self:
            if resource.resource_type == 'task' and (
                    resource.uom_id.category_id != (
                        # FIXME: UoM elegible should be on a list configurable
                        self.env.ref('product.uom_categ_wtime'))):
                raise ValidationError(_(
                    "When resource type is task, "
                    "the UoM category should be time"))
