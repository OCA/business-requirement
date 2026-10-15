# Copyright 2026 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    business_requirement_id = fields.Many2one(
        comodel_name="business.requirement",
        string="Business Requirement",
        index="btree_not_null",
        ondelete="set null",
        tracking=True,
    )
    business_requirement_deliverable_id = fields.Many2one(
        comodel_name="business.requirement.deliverable",
        string="Deliverable",
        index="btree_not_null",
        ondelete="set null",
        copy=False,
    )
