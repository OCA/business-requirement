# Copyright 2019 Tecnativa Victor M.M. Torres>
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    sale_order_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="business_requirement_id",
        string="Sales Orders",
    )
    sale_order_count = fields.Integer(
        string="Sales Orders Count", compute="_compute_sale_order_count"
    )

    @api.depends("sale_order_ids")
    def _compute_sale_order_count(self):
        groups = self.env["sale.order"]._read_group(
            domain=[("business_requirement_id", "in", self.ids)],
            groupby=["business_requirement_id"],
            aggregates=["__count"],
        )
        data = {
            business_requirement.id: count for business_requirement, count in groups
        }
        for rec in self:
            rec.sale_order_count = data.get(rec.id, 0)

    def open_orders(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("sale.action_quotations")
        if len(self) == 1:
            action["context"] = {"search_default_business_requirement_id": self.id}
        else:
            action["domain"] = [("business_requirement_id", "in", self.ids)]
        return action
