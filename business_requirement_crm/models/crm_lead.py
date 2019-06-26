# Copyright 2019 Tecnativa - Victor M.M. Torres
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    business_requirement_ids = fields.One2many(
        comodel_name='business.requirement',
        inverse_name='lead_id',
    )
    business_requirement_count = fields.Integer(
        compute='_compute_business_requirement_count'
    )

    @api.multi
    @api.depends('business_requirement_ids')
    def _compute_business_requirement_count(self):
        groups = self.env['business.requirement'].read_group(
            domain=[('lead_id', 'in', self.ids)],
            fields=['lead_id'],
            groupby=['lead_id'],
        )
        data = {x['lead_id'][0]: x['lead_id_count'] for x in groups}
        for rec in self:
            rec.business_requirement_count = data.get(rec.id, 0)

    @api.multi
    def open_requirements(self):
        action = self.env.ref(
            'business_requirement.action_business_requirement_tree'
        ).read()[0]
        if len(self) == 1:
            action['context'] = {
                'search_default_lead_id': self.id,
            }
        else:
            action['domain'] = [('lead_id', 'in', self.ids)],
        return action
