# -*- coding: utf-8 -*-
# © 2017 Praxya (https://www.praxya.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ProjectIssue(models.Model):
    _inherit = "project.issue"

    business_requirement_id = fields.Many2one(
        comodel_name="business.requirement",
        string="Business Requirement",
        ondelete="set null",
    )
