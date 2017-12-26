# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, api, fields, _


class BusinessRequirementRenew(models.Model):
    _inherit = 'business.requirement'

    @api.multi
    def _get_br_children_count(self):
        for record in self:
            count = len(record.env['business.requirement'].search(
                [('source_id', '=', record.id)]))
            record.br_children_count = count + 1

    source_id = fields.Many2one(
        'business.requirement',
        string="Original Bus.Req",
        readonly=True)
    copy_from_id = fields.Many2one(
        'business.requirement', string="Renewed From", readonly=True)
    version = fields.Integer(string='Version', default=0, invisible=True)
    br_children_count = fields.Integer(
        string='BR children', copy=False, store=False,
        compute='_get_br_children_count'
    )

    @api.model
    def _get_states(self):
        res = super(BusinessRequirementRenew, self)._get_states()
        res.append(('renewed', 'Renewed'))
        return res

    @api.multi
    def copy(self, default=None):
        vals = self.copy_data(default)[0]
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
        new = self.with_context(lang=None).create(vals)
        self.copy_translations(new)
        return new

    @api.multi
    def renew_br(self):
        if '-' in self.name:
            source_id = self.source_id.id
            name = self.source_id.name + '-' + \
                   str(self.source_id.br_children_count)
            version = self.source_id.br_children_count
        else:
            name = self.name + '-' + str(self.br_children_count)
            version = self.br_children_count
            source_id = self.id
        reviewer_list = []
        for reviews in self.reviewer_ids:
            reviewer_list.append(reviews.id)
        new_application = self.with_context(
            renew=True,
            name=name,
            copy_from_id=self.id,
            source_id=source_id,
            change_request=self.change_request,
            partner_id=self.partner_id.id,
            project_id=self.project_id.id,
            ref=self.ref,
            origin=self.origin,
            reviewer_ids=[(6, 0, reviewer_list)],
            version=version
        ).copy()
        self.state = 'renewed'
        return {
            'name': 'New application',
            'type': 'ir.actions.act_window',
            'views': [[False, 'form']],
            'res_model': self._name,
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
