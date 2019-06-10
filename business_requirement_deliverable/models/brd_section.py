# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class BusinessRequirementDeliverableSection(models.Model):
    _name = "business.requirement.deliverable.section"

    name = fields.Char('Name', required=True)
