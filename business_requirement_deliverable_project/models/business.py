# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    @api.multi
    def generate_projects_wizard(self):
        res = self.project_id.with_context(
            br_ids=self).generate_project_wizard()
        return res

    linked_project = fields.Many2one(
        string='Linked project',
        comodel_name='project.project',
        groups='project.group_project_user',
        readonly=True,
    )

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='business_requirement_id',
        string='Tasks'
    )
    task_count = fields.Integer(
        string='Total number of tasks related to a business requirement',
        store=True,
        readonly=True,
        compute='_compute_task_count'
    )

    total_hour = fields.Float(
        string='Total Hours in Timesheets related to business requirement',
        compute='_compute_hour'
    )

    total_planned_hour = fields.Float(
        string='Total Planned Hour in RL related to business requirement',
        compute='_compute_planned_hour'
    )

    @api.model
    def read_group(self, domain, fields, groupby, offset=0,
                   limit=None, orderby=False, lazy=True):
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
        else:
            return super(BusinessRequirement, self).\
                read_group(domain, fields, groupby,
                           offset=offset, limit=limit, orderby=orderby)

    @api.multi
    def write(self, vals):
        for r in self:
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
                        raise UserError(_('You can only move to the '
                                          'following stage: draft/confirmed'
                                          '/cancel/drop.'))
                if vals['state'] in ('stakeholder_approval', 'in_progress',
                                     'done'):
                    if br_xml_id.id not in grps:
                        raise UserError(_('You can only move to the'
                                          'following stage: draft/'
                                          'confirmed/cancel/drop.'))
            return super(BusinessRequirement, self).write(vals)

    @api.multi
    @api.depends('task_ids')
    def _compute_task_count(self):
        for r in self:
            r.task_count = len(r.task_ids)

    @api.multi
    def _compute_hour(self):
        for r in self:
            total_hour = 0.0
            if r.task_ids:
                for task in r.task_ids:
                    total_hour += task.effective_hours
            r.total_hour = total_hour

    @api.multi
    def _compute_planned_hour(self):
        for r in self:
            total_planned_hour = 0.0
            if r.deliverable_lines:
                for dl in r.deliverable_lines:
                    if dl.resource_ids:
                        for rl in dl.resource_ids:
                            total_planned_hour += rl.qty
            r.total_planned_hour = total_planned_hour


class BusinessRequirementDeliverable(models.Model):
    _inherit = "business.requirement.deliverable"

    linked_project = fields.Many2one(
        string='Linked project',
        comodel_name='project.project',
        groups='project.group_project_user',
        readonly=True,
        )
