# -*- coding: utf-8 -*-
# © 2017 Praxya (https://www.praxya.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models, api


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    issue_ids = fields.One2many(
        comodel_name="project.issue",
        inverse_name="business_requirement_id",
        string="Related issues",
        help="Issues related to this BR, click to view",
    )

    issue_count = fields.Integer(
        string='Total number of issues related to a business requirement',
        store=True,
        readonly=True,
        compute='_compute_issue_count'
    )

    @api.multi
    @api.depends('issue_ids')
    def _compute_issue_count(self):
        for r in self:
            r.issue_count = len(r.issue_ids)
