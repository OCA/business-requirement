# Copyright 2019 Tecnativa - Victor M.M. Torres
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    business_requirement_ids = fields.One2many(
        comodel_name="business.requirement", inverse_name="lead_id"
    )
    business_requirement_count = fields.Integer(
        compute="_compute_business_requirement_count"
    )

    @api.depends("business_requirement_ids")
    def _compute_business_requirement_count(self):
        groups = self.env["business.requirement"]._read_group(
            domain=[("lead_id", "in", self.ids)],
            groupby=["lead_id"],
            aggregates=["__count"],
        )
        data = {lead.id: count for lead, count in groups}
        for rec in self:
            rec.business_requirement_count = data.get(rec.id, 0)

    def open_requirements(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "business_requirement.action_business_requirement_tree"
        )
        if len(self) == 1:
            action["context"] = {"search_default_lead_id": self.id}
        else:
            action["domain"] = [("lead_id", "in", self.ids)]
        return action
