# Copyright 2017 Elico Corp (https://www.elico-corp.com).
# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BusinessRequirement(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]
    _name = "business.requirement"
    _description = "Business Requirement"
    _order = "name desc"

    @api.model
    def _get_default_company(self):
        if not self.env.user.company_id:
            raise ValidationError(
                _('There is no default company for the current user!'))
        return self.env.user.company_id.id

    sequence = fields.Char(
        'Sequence',
        readonly=True,
        copy=False,
        index=True,
    )
    name = fields.Char(
        'Name',
        readonly=True,
        copy=False,
        states={'draft': [('readonly', False)]}
    )
    description = fields.Char(
        'Description', required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    business_requirement = fields.Html(
        'Customer Story',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    scenario = fields.Html(
        'Scenario',
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
    )
    gap = fields.Html(
        'Gap',
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
    )
    test_case = fields.Html(
        'Test Case',
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
    )
    terms_and_conditions = fields.Html(
        'Terms and Conditions',
        readonly=True,
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
    )
    category_ids = fields.Many2many(
        'business.requirement.category',
        string='Categories',
        relation='business_requirement_category_rel',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('approved', 'Approved'),
            ('in_progress', 'In progress'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
            ('drop', 'Drop'),
        ],
        string='State',
        default='draft',
        copy=False,
        readonly=False,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange'
    )
    change_request = fields.Boolean(
        string='Change Request?',
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Stakeholder',
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    priority = fields.Selection(
        [('0', 'Low'), ('1', 'Normal'), ('2', 'High')],
        'Priority',
        required=True,
        default='1'
    )
    requested_user_id = fields.Many2one(
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
        string='Confirmation Date',
        copy=False,
        readonly=True
    )
    confirmed_user_id = fields.Many2one(
        'res.users', string='Confirmed by',
        copy=False,
        readonly=True
    )
    responsible_user_id = fields.Many2one(
        'res.users', string='Responsible',
        copy=False,
        readonly=True,
        default=lambda self: self.env.user,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)]
        }
    )
    reviewer_ids = fields.Many2many(
        'res.users', string='Reviewers',
        copy=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)]
        }
    )
    approval_date = fields.Datetime(
        string='Approval Date',
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
        default=_get_default_company,
    )
    to_be_reviewed = fields.Boolean(
        string='To be Reviewed'
    )
    kanban_state = fields.Selection(
        [
            ('normal', 'In Progress'),
            ('on_hold', 'On Hold'),
            ('done', 'Ready for next stage')
        ],
        'Kanban State',
        track_visibility='onchange',
        default='normal'
    )
    origin = fields.Char(
        string='Source',
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', True)]
        }
    )
    portal_published = fields.Boolean('In Portal', default=False)
    user_id = fields.Many2one(
        'res.users',
        string='Owner',
        default=lambda self: self.env.user,
        required=True,
        track_visibility='always',
    )
    date = fields.Date(
        'Date',
        default=lambda self: self._context.get(
            'date', fields.Date.context_today(self)),
        required=True
    )

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'business.requirement')
        return super().create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('state'):
            user = self.env.user
            user_manager = user.has_group(
                'business_requirement.group_business_requirement_manager')
            date = fields.Datetime.now()
            if vals['state'] == 'confirmed':
                vals.update({'confirmed_user_id': user.id,
                             'confirmation_date': date})
            if vals['state'] == 'draft':
                vals.update({'confirmed_user_id': False,
                             'approved_id': False,
                             'confirmation_date': False,
                             'approval_date': False
                             })
            if vals['state'] == 'approved':
                if user_manager:
                    vals.update({
                        'approved_id': user.id, 'approval_date': date})
                else:
                    raise ValidationError(_(
                        'You can only move to the following stage: '
                        'draft/confirmed /cancel/drop.'))
            if vals['state'] in {'approved', 'in_progress',
                                 'done'}:
                if not user_manager:
                    raise ValidationError(_(
                        'You can only move to the following stage: '
                        'draft/confirmed/cancel/drop.'))
        return super().write(vals)

    @api.multi
    def name_get(self):
        """
        Display display [Name] Description
        """
        result = []
        for br in self:
            formatted_name = u'[{}] {}'.format(br.name, br.description)
            result.append((br.id, formatted_name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Search BR based on Name or Description"""
        # Make a search with default criteria
        names = super().name_search(
            name=name, args=args, operator=operator, limit=limit)
        # Make the other search
        descriptions = []
        if name:
            domain = [('description', '=ilike', name + '%')]
            descriptions = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names) | set(descriptions))[:limit]

    @api.multi
    @api.returns('mail.message', lambda value: value.id)
    def message_post(
        self, body='', subject=None,
        message_type='notification', subtype=None,
        parent_id=False, attachments=None,
        notif_layout=False, add_sign=True, model_description=False,
        mail_auto_delete=True, **kwargs
    ):
        context = self._context or {}
        if context.get('default_model') ==\
                'business.requirement' and context.get('default_res_id'):
            br_rec = self.env[context.get('default_model')]. \
                browse(context['default_res_id'])
            subject = 'Re: %s-%s' % (br_rec.name, br_rec.description)
        message = super(BusinessRequirement, self.with_context(
            mail_create_nosubscribe=True)).message_post(
            body=body,
            subject=subject,
            message_type=message_type,
            subtype=subtype,
            parent_id=parent_id,
            attachments=attachments,
            notif_layout=notif_layout,
            add_sign=add_sign,
            model_description=model_description,
            mail_auto_delete=mail_auto_delete,
            **kwargs)
        return message

    @api.model
    def read_group(self, domain, fields, groupby, offset=0,
                   limit=None, orderby=False, lazy=True):
        """Read group customization in order to display all the stages in the
        kanban view. if the stages values are there it will group by state.
        """
        if groupby and groupby[0] == "state":
            states = self.env['business.requirement'].\
                fields_get(['state']).get('state').get('selection')
            read_group_all_states = [{'__context': {'group_by': groupby[1:]},
                                      '__domain': domain + [('state', '=',
                                                             state_value)],
                                      'state': state_value,
                                      'state_count': 0}
                                     for state_value, state_name in states]
            # Get standard results
            read_group_res = super().\
                read_group(domain, fields, groupby, offset=offset,
                           limit=limit, orderby=orderby)
            # Update standard results with default results
            result = []
            for state_value, state_name in states:
                res = list(
                    filter(
                        lambda x: x['state'] == state_value,
                        read_group_res))
                if not res:
                    res = list(
                        filter(
                            lambda x: x['state'] == state_value,
                            read_group_all_states))
                res[0]['state'] = state_value
                result.append(res[0])
            return result
        return super().\
            read_group(domain, fields, groupby,
                       offset=offset, limit=limit, orderby=orderby, lazy=lazy)

    def get_portal_confirmation_action(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'business_requirement.br_portal_confirmation_options',
            default='none')

    def _compute_access_url(self):
        super()._compute_access_url()
        for br in self:
            br.access_url = '/my/business_requirement/%s' % br.id

    @api.multi
    def portal_publish_button(self):
        self.ensure_one()
        return self.write({'portal_published': not self.portal_published})


class BusinessRequirementCategory(models.Model):
    _name = "business.requirement.category"
    _description = "Categories"

    name = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one(
        comodel_name='business.requirement.category',
        string='Parent Category',
        ondelete='restrict'
    )
