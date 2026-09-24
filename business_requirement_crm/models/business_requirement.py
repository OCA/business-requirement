# Copyright 2019 Tecnativa - Victor M.M. Torres
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    lead_id = fields.Many2one(
        comodel_name="crm.lead", string="Lead", ondelete="restrict"
    )
