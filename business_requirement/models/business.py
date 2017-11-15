# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BusinessRequirement(models.Model):
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _name = "business.requirement"
    _description = "Business Requirement"
    _order = 'name desc'

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
        required=False,
        readonly=True,
        copy=False,
        states={'draft': [('readonly', False)]}
    )
    description = fields.Char(
        'Description', required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    ref = fields.Char(
        'WBS',
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
        selection="_get_states",
        string='State',
        default='draft',
        copy=False,
        readonly=False,
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
        string='Stakeholder',
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
        'Priority',
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
        string='Confirmation Date',
        copy=False,
        readonly=True
    )
    confirmed_id = fields.Many2one(
        'res.users', string='Confirmed by',
        copy=False,
        readonly=True
    )
    responsible_id = fields.Many2one(
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
        required=False,
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

    @api.multi
    @api.onchange('project_id')
    def project_id_change(self):
        if self.project_id and self.project_id.partner_id:
            self.partner_id = self.project_id.partner_id.id

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'business.requirement')
        if vals.get('project_id'):
            project_id = self.env['project.project']. \
                browse(vals.get('project_id'))
            if project_id and project_id.message_follower_ids:
                msg_followers = []
                for project in project_id.message_follower_ids:
                    msg_vals = {
                        'channel_id': project.channel_id.id,
                        'display_name': project.display_name,
                        'partner_id': project.partner_id.id,
                        'res_model': self._name,
                        'subtype_ids': project.subtype_ids.ids
                    }
                    msg_followers.append((0, 0, msg_vals))
                if msg_followers:
                    vals['message_follower_ids'] = msg_followers
        return super(BusinessRequirement, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('project_id'):
            project_id = self.env['project.project']. \
                browse(vals.get('project_id'))
            if project_id and project_id.message_follower_ids:
                msg_followers = []
                for followers in self.message_follower_ids:
                    msg_followers.append((2, followers.id))
                for project in project_id.message_follower_ids:
                    msg_vals = {
                        'channel_id': project.channel_id.id,
                        'display_name': project.display_name,
                        'partner_id': project.partner_id.id,
                        'res_model': self._name,
                        'subtype_ids': project.subtype_ids.ids
                    }
                    msg_followers.append((0, 0, msg_vals))
                if msg_followers:
                    vals['message_follower_ids'] = msg_followers
        if vals.get('state'):
            ir_obj = self.env['ir.model.data']
            br_xml_id = ir_obj.\
                get_object('business_requirement',
                           'group_business_requirement_manager')
            user = self.env['res.users']
            grps = [grp.id for grp in user.browse(self._uid).groups_id]
            date = fields.Datetime.now()
            if vals['state'] == 'confirmed':
                vals.update({'confirmed_id': user,
                             'confirmation_date': date})
            if vals['state'] == 'draft':
                vals.update({'confirmed_id': False,
                             'approved_id': False,
                             'confirmation_date': False,
                             'approval_date': False
                             })
            if vals['state'] == 'approved':
                if br_xml_id.id in grps:
                    vals.update({'approved_id': user,
                                 'approval_date': date})
                else:
                    raise ValidationError(_(
                        'You can only move to the following stage: '
                        'draft/confirmed /cancel/drop.'))
            if vals['state'] == 'stakeholder_approval':
                if br_xml_id.id in grps:
                    vals.update({
                        'approved_id': user,
                        'approval_date': date
                    })
                else:
                    raise ValidationError(_(
                        'You can only move to the following stage: '
                        'draft/confirmed /cancel/drop.'))

            if vals['state'] in ('stakeholder_approval', 'in_progress',
                                 'done'):
                if br_xml_id.id not in grps:
                    raise ValidationError(_(
                        'You can only move to the following stage: '
                        'draft/confirmed/cancel/drop.'))
        return super(BusinessRequirement, self).write(vals)

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
            ('stakeholder_approval', 'Stakeholder Approval'),
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
                formatted_name = u'[{}][{}] {}'.format(br.ref, br.name,
                                                       br.description)
            else:
                formatted_name = u'[{}] {}'.format(br.name, br.description)
            result.append((br.id, formatted_name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """
        Search BR based on Name or Description
        """
        # Make a search with default criteria
        names = super(BusinessRequirement, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        # Make the other search
        descriptions = []
        if name:
            domain = [('description', '=ilike', name + '%')]
            descriptions = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names) | set(descriptions))[:limit]

    @api.multi
    @api.returns('self', lambda value: value.id)
    def message_post(self, body='', subject=None, message_type='notification',
                     subtype=None, parent_id=False, attachments=None,
                     content_subtype='html', **kwargs):
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
            content_subtype=content_subtype,
            **kwargs)
        return message

    @api.model
    def read_group(self, domain, fields, groupby, offset=0,
                   limit=None, orderby=False, lazy=True):
        """ Read group customization in order to display all the stages in the
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
            read_group_res = super(BusinessRequirement, self).\
                read_group(domain, fields, groupby, offset=offset,
                           limit=limit, orderby=orderby)
            # Update standard results with default results
            result = []
            for state_value, state_name in states:
                res = filter(lambda x: x['state'] == state_value,
                             read_group_res)
                if not res:
                    res = filter(lambda x: x['state'] == state_value,
                                 read_group_all_states)
                res[0]['state'] = [state_value, state_name]
                result.append(res[0])
            return result
        return super(BusinessRequirement, self).\
            read_group(domain, fields, groupby,
                       offset=offset, limit=limit, orderby=orderby, lazy=lazy)


class BusinessRequirementCategory(models.Model):
    _name = "business.requirement.category"
    _description = "Categories"

    name = fields.Char(string='Name', required=True)
    parent_id = fields.Many2one(
        comodel_name='business.requirement.category',
        string='Parent Category',
        ondelete='restrict'
    )
