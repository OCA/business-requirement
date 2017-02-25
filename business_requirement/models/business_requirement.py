# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class BusinessRequirement(models.Model):
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _name = "business.requirement"
    _description = "Business Requirement"
    _order = 'id desc'

    sequence = fields.Char(
        readonly=True,
        copy=False,
        index=True,
    )
    name = fields.Char(
        required=False,
        readonly=True,
        copy=False,
        states={'draft': [('readonly', False)]}
    )
    description = fields.Char(
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    ref = fields.Char(
        'Reference',
        required=False,
        readonly=True,
        copy=False,
        states={'draft': [('readonly', False)]}
    )
    business_requirement = fields.Html(
        'Customer Story',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    scenario = fields.Html(
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    gap = fields.Html(
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    test_case = fields.Html(
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    category_ids = fields.Many2many(
        'business.requirement.category',
        string='Categories',
        relation='business_requirement_category_rel',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    state = fields.Selection(
        selection="_get_states",
        string='State',
        default='draft',
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange'
    )
    business_requirement_ids = fields.One2many(
        comodel_name='business.requirement',
        inverse_name='parent_id',
        string='Sub Business Requirement',
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    parent_id = fields.Many2one(
        comodel_name='business.requirement',
        string='Parent',
        ondelete='set null',
        domain="[('id', '!=', id)]",
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)]}
    )
    level = fields.Integer(
        compute='_get_level',
        string='Level',
        store=True
    )
    change_request = fields.Boolean(
        string='Change Request?',
        default=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Master Project',
        ondelete='set null',
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        store=True,
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    sub_br_count = fields.Integer(
        string='Count',
        compute='_compute_sub_br_count'
    )
    priority = fields.Selection(
        [('0', 'Low'), ('1', 'Normal'), ('2', 'High')],
        required=True,
        default='1'
    )
    requested_id = fields.Many2one(
        'res.users',
        string='Requested by',
        required=True,
        readonly=True,
        default=lambda self: self.env.user,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)]}
    )
    confirmation_date = fields.Datetime(
        copy=False,
        readonly=True
    )
    confirmed_id = fields.Many2one(
        'res.users', string='Confirmed by',
        copy=False,
        readonly=True
    )
    reviewed_date = fields.Datetime(
        copy=False,
        readonly=True
    )
    reviewed_id = fields.Many2one(
        'res.users',
        string='Reviewed by',
        copy=False,
        readonly=True
    )
    approval_date = fields.Datetime(
        copy=False,
        readonly=True
    )
    approved_id = fields.Many2one(
        'res.users',
        string='Approved by',
        copy=False,
        readonly=True
    )
    company_id = fields.Many2one(
        'res.company', string='Company',
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id,
    )

    @api.multi
    @api.onchange('project_id')
    def project_id_change(self):
        for br in self:
            if br.project_id and br.project_id.partner_id:
                br.partner_id = br.project_id.partner_id

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].\
                next_by_code('business.requirement')
        return super(BusinessRequirement, self).create(vals)

    @api.multi
    @api.depends('parent_id')
    def _get_level(self):
        for br in self:
            level = br.parent_id and br.parent_id.level + 1 or 1
            br.level = level

    @api.multi
    @api.depends('business_requirement_ids')
    def _compute_sub_br_count(self):
        for br in self:
            br.sub_br_count = len(br.business_requirement_ids)

    @api.model
    def _get_states(self):
        states = [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('approved', 'Approved'),
            ('stakeholder_approval', 'Stakeholder Approved'),
            ('in_progress', 'In progress'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
            ('drop', 'Drop'),
        ]
        return states

    @api.multi
    def name_get(self):
        """
        Display [Reference] Description if reference is defined
        otherwise display [Name] Description
        """
        result = []
        for br in self:
            if br.ref:
                formatted_name = '[{}] {}'.format(br.ref, br.description)
            else:
                formatted_name = '[{}] {}'.format(br.name, br.description)
            result.append((br.id, formatted_name))
        return result

    @api.multi
    def action_button_confirm(self):
        self.state = 'confirmed'
        self.confirmed_id = self.env.user
        self.confirmation_date = fields.Datetime.now()

    @api.multi
    def action_button_back_draft(self):
        self.state = 'draft'
        self.confirmed_id = self.approved_id = []
        self.confirmation_date = self.approval_date = ''

    @api.multi
    def action_button_approve(self):
        self.state = 'approved'
        self.approved_id = self.env.user
        self.approval_date = fields.Datetime.now()

    @api.multi
    def action_button_stakeholder_approval(self):
        self.state = 'stakeholder_approval'

    @api.multi
    def action_button_in_progress(self):
        self.state = 'in_progress'

    @api.multi
    def action_button_done(self):
        self.state = 'done'

    @api.multi
    def action_button_cancel(self):
        self.state = 'cancel'

    @api.multi
    def action_button_drop(self):
        self.state = 'drop'

    @api.cr_uid_ids_context
    def message_post(self, cr, uid, thread_id, body='', subject=None,
                     subtype=None, parent_id=False,
                     attachments=None, context=None,
                     content_subtype='html', **kwargs):
        subject = None
        if context.get(
                'default_model'
        ) == 'business.requirement' and context.get('default_res_id'):
            br_rec = self.pool.get(
                context.get('default_model')
            ).browse(cr, uid, context['default_res_id'])
            subject = 'Re: %s-%s' % (br_rec.name, br_rec.description)
        res = super(BusinessRequirement, self).message_post(
            cr, uid, thread_id, body='', subject=subject,
            subtype=None, parent_id=False,
            attachments=None, context=None,
            content_subtype='html', **kwargs
        )
        return res
