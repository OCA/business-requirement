# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


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
        store=True
    )
    name = fields.Char('Name', required=True)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='UoM',
        required=True
    )
    qty = fields.Float(
        string='Quantity',
        default=1
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
        self.uom_id = self.env.ref('uom.product_uom_hour').id
        if self.resource_type == 'procurement':
            self.user_id = False
            self.uom_id = self.env.ref('uom.product_uom_unit').id

    @api.multi
    @api.constrains('resource_type', 'uom_id')
    def _check_description(self):
        for resource in self:
            if resource.resource_type == 'task' and (
                    resource.uom_id.category_id != (
                        self.env.ref('uom.uom_categ_wtime'))):
                raise ValidationError(_(
                    "When resource type is task, "
                    "the UoM category should be time"))

    @api.multi
    def write(self, vals):
        if vals.get('resource_type', '') == 'procurement':
            vals['user_id'] = None
        return super(BusinessRequirementResource, self).write(vals)
