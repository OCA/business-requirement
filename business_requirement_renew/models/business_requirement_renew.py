# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, api, fields, _


class BusinessRequirementRenew(models.Model):
    _inherit = 'business.requirement'

    @api.multi
    def _compute_br_children_count(self):
        for record in self:
            count = len(record.env['business.requirement'].search(
                [('source_id', '=', record.id)]))
            record.br_children_count = count + 1

    source_id = fields.Many2one(
        'business.requirement',
        string="Original Bus.Req",
        readonly=True)
    copy_from_id = fields.Many2one(
        'business.requirement', string="Renewed From")
    version = fields.Integer(string='Version', default=0)
    br_children_count = fields.Integer(
        string='BR children', copy=False, store=False,
        compute='_compute_br_children_count'
    )

    @api.model
    def _get_states(self):
        res = super(BusinessRequirementRenew, self)._get_states()
        res.append(('renewed', 'Renewed'))
        return res

    @api.multi
    def copy(self, default=None):
        vals = dict(default or {})
        if self._context.get('renew'):
            vals.update(
                name=self._context.get('name'),
                copy_from_id=self._context.get('copy_from_id'),
                source_id=self._context.get('source_id'),
                change_request=self._context.get('change_request'),
                partner_id=self._context.get('partner_id'),
                project_id=self._context.get('project_id'),
                ref=self._context.get('ref'),
                origin=self._context.get('origin'),
                reviewer_ids=self._context.get('reviewer_ids'),
                version=self._context.get('version')
            )
        return super(BusinessRequirementRenew, self).copy(vals)

    @api.multi
    def renew_br(self):
        for rec in self:
            if rec.source_id:
                source_id = rec.source_id.id
                name = rec.source_id.name + '-' + str(
                    rec.source_id.br_children_count)
                count = rec.source_id.br_children_count
            else:
                name = rec.name + '-' + str(rec.br_children_count)
                count = rec.br_children_count
                source_id = rec.id
            reviewer_list = []
            for reviews in rec.reviewer_ids:
                reviewer_list.append(reviews.id)
            new_application = rec.with_context(
                renew=True,
                name=name,
                copy_from_id=rec.id,
                source_id=source_id,
                change_request=rec.change_request,
                partner_id=rec.partner_id.id,
                project_id=rec.project_id.id,
                ref=rec.ref,
                origin=rec.origin,
                reviewer_ids=[(6, 0, reviewer_list)],
                version=count
            ).copy()
            rec.state = 'renewed'
            return {
                'name': 'New application',
                'type': 'ir.actions.act_window',
                'views': [[False, 'form']],
                'res_model': rec._name,
                'res_id': new_application.id,
                'flags': {'initial_mode': 'edit'},
            }

    @api.multi
    def child_br(self):
        for rec in self:
            domain = ['|', ('source_id', '=', rec.id), ('id', '=', rec.id)]
            return {
                'name': _('Business Requirement Children'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'business.requirement',
                'target': 'current',
                'domain': domain,
            }

    @api.model
    def create(self, vals):
        if self._context.get('renew'):
            br_id = self.env['business.requirement']. \
                browse(vals.get('copy_from_id'))
            if br_id and br_id.message_follower_ids:
                msg_followers = []
                for project in br_id.message_follower_ids:
                    if project.partner_id != self.env.user.partner_id:
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
        return super(BusinessRequirementRenew, self).create(vals)
