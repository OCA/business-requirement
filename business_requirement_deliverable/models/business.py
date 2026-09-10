# Copyright 2016-2019 Elico Corp (https://www.elico-corp.com).
# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import Command, api, fields, models
from odoo.exceptions import UserError


class BusinessRequirementDeliverable(models.Model):
    _name = "business.requirement.deliverable"
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]
    _description = "Business Requirement Deliverable"
    _order = "business_requirement_id, section_id, sequence, id"

    sequence = fields.Integer()
    name = fields.Text(required=True)
    user_case = fields.Html()
    proposed_solution = fields.Html()
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        domain=[("sale_ok", "=", True)],
        required=False,
    )
    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="UoM",
        required=True,
        default=lambda self: self.env.ref("uom.product_uom_unit"),
    )
    qty = fields.Float(string="Quantity", store=True, default=1)
    business_requirement_id = fields.Many2one(
        comodel_name="business.requirement",
        string="Business Requirement",
        ondelete="cascade",
        required=True,
    )
    dependency_ids = fields.Many2many(
        comodel_name="business.requirement.deliverable",
        relation="business_requirement_deliverable_dependency_rel",
        column1="parent_id",
        column2="dependency_id",
        string="Dependencies",
    )
    sale_price_unit = fields.Float(string="Sales Price")
    price_total = fields.Float(
        compute="_compute_price_total",
        string="Total Deliverable",
        store=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        compute="_compute_currency_id",
    )
    business_requirement_partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="business_requirement_id.partner_id",
        string="Stakeholder",
        readonly=False,
        store=True,
    )
    state = fields.Selection(
        related="business_requirement_id.state", string="State", store=True
    )
    portal_published = fields.Boolean(string="In Portal", default=True)
    section_id = fields.Many2one(
        comodel_name="business.requirement.deliverable.section", string="Section"
    )

    def _compute_access_url(self):
        res = super()._compute_access_url()
        for brd in self:
            brd.access_url = f"/my/brd/{brd.id}"
        return res

    @api.depends(
        "business_requirement_id.partner_id", "business_requirement_id.currency_id"
    )
    def _compute_currency_id(self):
        for brd in self:
            br = brd.business_requirement_id
            if br.pricelist_id.currency_id:
                brd.currency_id = br.pricelist_id.currency_id
            else:
                brd.currency_id = br.currency_id

    @api.depends("sale_price_unit", "qty")
    def _compute_price_total(self):
        for brd in self:
            brd.price_total = brd.sale_price_unit * brd.qty

    def _get_sale_price_unit(self):
        """Unit price of the product, from the requirement pricelist if any"""
        self.ensure_one()
        pricelist = self.business_requirement_id.pricelist_id
        if pricelist:
            return pricelist._get_product_price(
                product=self.product_id,
                quantity=self.qty or 1.0,
                uom=self.uom_id,
                date=fields.Date.context_today(self),
            )
        return self.product_id.uom_id._compute_price(
            self.product_id.lst_price, self.uom_id
        )

    @api.onchange("product_id")
    def product_id_change(self):
        description = ""
        if self.product_id:
            description = self.product_id.display_name
            self.uom_id = self.product_id.uom_id.id
        if self.product_id.description_sale:
            description += "\n" + self.product_id.description_sale
        if not self.name:
            self.name = description
        if self.product_id:
            self.sale_price_unit = self._get_sale_price_unit()

    @api.onchange("product_id", "uom_id", "qty")
    def product_uom_change(self):
        if self.product_id:
            self.sale_price_unit = self._get_sale_price_unit()

    def portal_publish_button(self):
        self.ensure_one()
        return self.write({"portal_published": not self.portal_published})

    @api.depends("sequence", "name", "section_id")
    def _compute_display_name(self):
        for rec in self:
            name = f"#{rec.sequence}: {rec.name}"
            if rec.section_id:
                name = f"[{rec.section_id.name}] {name}"
            rec.display_name = name


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    deliverable_lines = fields.One2many(
        comodel_name="business.requirement.deliverable",
        inverse_name="business_requirement_id",
        copy=True,
    )
    total_revenue = fields.Float(
        compute="_compute_deliverable_total", string="Total Deliverable", store=True
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        compute="_compute_currency_id",
    )
    dl_total_revenue = fields.Float(
        string="DL Total Revenue", digits="Account", compute="_compute_dl_total_revenue"
    )
    dl_count = fields.Integer(string="DL Count", compute="_compute_dl_count")
    dl_count_portal_published = fields.Integer(
        string="DL Count Portal pubished", compute="_compute_dl_count_portal_published"
    )
    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Pricelist",
    )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        """
        if self.partner_id:
            values = {
                "pricelist_id": self.partner_id.property_product_estimation_pricelist
                or self.partner_id.property_product_pricelist
                or False
            }
            self.update(values)

    def _compute_dl_total_revenue(self):
        for r in self:
            r.dl_total_revenue = sum(r.deliverable_lines.mapped("price_total"))

    def _compute_dl_count(self):
        for r in self:
            r.dl_count = len(r.deliverable_lines.ids)

    def _compute_dl_count_portal_published(self):
        for r in self:
            r.dl_count_portal_published = len(
                r.deliverable_lines.filtered("portal_published").ids
            )

    def open_deliverable_line(self):
        self.ensure_one()
        br_id = 0
        if self.state in ("draft", "confirmed"):
            br_id = self.id
        return {
            "name": self.env._("Deliverable Lines"),
            "type": "ir.actions.act_window",
            "view_mode": "list,form,graph",
            "res_model": "business.requirement.deliverable",
            "target": "current",
            "domain": [("business_requirement_id", "=", self.id)],
            "context": {
                "list_view_ref": "business_requirement_deliverable."
                "view_business_requirement_deliverable_tree",
                "form_view_ref": "business_requirement_deliverable."
                "view_business_requirement_deliverable_form",
                "default_business_requirement_id": br_id,
            },
        }

    @api.depends("pricelist_id", "company_id")
    def _compute_currency_id(self):
        for br in self:
            if br.partner_id and br.pricelist_id.currency_id:
                br.currency_id = br.pricelist_id.currency_id
            else:
                br.currency_id = br.company_id.currency_id

    @api.onchange("partner_id")
    def partner_id_change(self):
        for record in self:
            if record.deliverable_lines:
                raise UserError(
                    self.env._(
                        "You are changing customer, on a business requirement"
                        "which already contains deliverable lines."
                        "Pricelist could be different."
                    )
                )

    @api.depends(
        "deliverable_lines", "deliverable_lines.price_total", "company_id.currency_id"
    )
    def _compute_deliverable_total(self):
        for br in self:
            if br.deliverable_lines:
                total_revenue_origin = sum(
                    line.price_total for line in br.deliverable_lines
                )
                if br.partner_id.property_product_pricelist.currency_id:
                    curr = br.partner_id.property_product_pricelist.currency_id
                    br.total_revenue = curr._convert(
                        total_revenue_origin,
                        br.company_id.currency_id,
                        br.company_id,
                        br.confirmation_date or fields.Datetime.today(),
                    )
                else:
                    br.total_revenue = total_revenue_origin

    def get_portal_confirmation_action(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "business_requirement_deliverable.br_portal_confirmation_options",
                default="none",
            )
        )

    def get_total_by_section(self):
        sections_total = []
        sections = self.deliverable_lines.mapped("section_id")
        for section in sections:
            brd_lines = self.deliverable_lines.filtered(
                lambda x, section=section: x.section_id == section
            )
            brd_section_total = sum(brd_lines.mapped("price_total"))
            sections_total.append((section.name, brd_section_total))
        # No Section
        brd_lines = self.deliverable_lines.filtered(lambda x: not x.section_id)
        if any(brd_lines):
            brd_section_total = sum(brd_lines.mapped("price_total"))
            sections_total.append((self.env._("Others"), brd_section_total))
        return sections_total

    def map_deliverable(self, new_br_id):
        """copy and map deliverable from old to new requirement"""
        deliverables = self.env["business.requirement.deliverable"]
        for deliverable in self.deliverable_lines:
            # preserve deliverable name, normally altered during copy
            deliverables += deliverable.copy({"name": deliverable.name})
        return self.browse(new_br_id).write(
            {"deliverable_lines": [Command.set(deliverables.ids)]}
        )

    def copy_data(self, default=None):
        vals_list = super().copy_data(default=default)
        if not (default or {}).get("name"):
            for br, vals in zip(self, vals_list, strict=True):
                vals["name"] = self.env._("%s (copy)", br.name)
        return vals_list

    def copy(self, default=None):
        new_brs = super().copy(default)
        for br, new_br in zip(self, new_brs, strict=True):
            for follower in br.message_follower_ids:
                new_br.message_subscribe(
                    partner_ids=follower.partner_id.ids,
                    subtype_ids=follower.subtype_ids.ids,
                )
            if "deliverable_lines" not in (default or {}):
                br.map_deliverable(new_br.id)
        return new_brs

    def message_subscribe(self, partner_ids=None, subtype_ids=None):
        """Subscribe to all existing active deliverables when subscribing
        to a requirement
        """
        res = super().message_subscribe(
            partner_ids=partner_ids, subtype_ids=subtype_ids
        )
        has_subtype = any(
            subtype.parent_id.res_model == "business.requirement.deliverable"
            for subtype in self.env["mail.message.subtype"].browse(subtype_ids or [])
        )
        if not subtype_ids or has_subtype:
            for partner_id in partner_ids or []:
                self.deliverable_lines.filtered(
                    lambda deliver, partner_id=partner_id: (
                        partner_id not in deliver.message_partner_ids.ids
                    )
                ).message_subscribe(partner_ids=[partner_id])
        return res

    def message_unsubscribe(self, partner_ids=None):
        """Unsubscribe from all deliverables
        when unsubscribing from a requirement
        """
        self.deliverable_lines.message_unsubscribe(partner_ids=partner_ids)
        return super().message_unsubscribe(partner_ids=partner_ids)
