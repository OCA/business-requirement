# -*- coding: utf-8 -*-
# © 2016-2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        ondelete='set null',
    )
    resource_cost_total = fields.Float(
        compute='_compute_resource_cost_total',
        string='Total Revenue from BR'
    )

    @api.multi
    def _compute_resource_cost_total(self):
        self.ensure_one()
        self.resource_cost_total = sum(
            [br.total_revenue for br in
                self.project_id and self.project_id.br_ids
                if br.state not in ('drop', 'cancel')])

    @api.multi
    @api.onchange('project_id')
    def project_id_change(self):
        self.ensure_one()
        if self.project_id:
            self.partner_id = self.project_id.partner_id.id
