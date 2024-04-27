# Copyright 2016-2019 Elico Corp (https://www.elico-corp.com).
# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class BusinessRequirementDeliverable(models.Model):
    _name = "business.requirement.deliverable"
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]
    _description = "Business Requirement Deliverable"
    _order = "business_requirement_id, section_id, sequence, id"

    sequence = fields.Integer(string="Sequence")
    state = fields.Selection(related="business_requirement_id.state", store=True)
    name = fields.Text(string="Name", required=True)
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
        readonly=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        readonly=True,
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
        super()._compute_access_url()
        for brd in self:
            brd.access_url = "/my/brd/%s" % brd.id

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

    @api.onchange("product_id")
    def product_id_change(self):
        description = ""
        if self.product_id:
            description = self.product_id.name_get()[0][1]
            self.uom_id = self.product_id.uom_id.id
        if self.product_id.description_sale:
            description += "\n" + self.product_id.description_sale
        if not self.name:
            self.name = description
        if self.product_id and self.business_requirement_id.pricelist_id:
            product = self.product_id.with_context(
                lang=self.business_requirement_id.partner_id.lang,
                partner=self.business_requirement_id.partner_id.id,
                quantity=self.qty,
                pricelist=self.business_requirement_id.pricelist_id.id,
                uom=self.uom_id.id,
            )
            self.sale_price_unit = product.price
        elif self.product_id:
            self.sale_price_unit = self.product_id.uom_id._compute_price(
                self.product_id.lst_price, self.uom_id
            )

    @api.onchange("product_id", "uom_id", "qty")
    def product_uom_change(self):
        if self.product_id and self.business_requirement_id.pricelist_id:
            product = self.product_id.with_context(
                lang=self.business_requirement_id.partner_id.lang,
                partner=self.business_requirement_id.partner_id.id,
                quantity=self.qty,
                pricelist=self.business_requirement_id.pricelist_id.id,
                uom=self.uom_id.id,
            )
            self.sale_price_unit = product.price
        elif self.product_id:
            self.sale_price_unit = self.product_id.uom_id._compute_price(
                self.product_id.lst_price, self.uom_id
            )

    def portal_publish_button(self):
        self.ensure_one()
        return self.write({"portal_published": not self.portal_published})

    def name_get(self):
        result = []
        for rec in self:
            name = "#{0}: {1}"
            args = [rec.sequence, rec.name]
            if rec.section_id:
                name = "[{2}] #{0}: {1}"
                args.append(rec.section_id.name)
            result.append((rec.id, name.format(*args)))
        return result


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    deliverable_lines = fields.One2many(
        comodel_name="business.requirement.deliverable",
        inverse_name="business_requirement_id",
        string="Deliverable Lines",
        copy=True,
        readonly=True,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", False)]},
    )
    total_revenue = fields.Float(
        compute="_compute_deliverable_total", string="Total Deliverable", store=True
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        readonly=True,
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
        readonly=True,
        states={"draft": [("readonly", False)]},
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
        for self in self:
            domain = [("business_requirement_id", "=", self.id)]
            br_id = 0
            if self.state in ("draft", "confirmed"):
                br_id = self.id
            return {
                "name": _("Deliverable Lines"),
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "tree,form,graph",
                "res_model": "business.requirement.deliverable",
                "target": "current",
                "domain": domain,
                "context": {
                    "tree_view_ref": "business_requirement_deliverable."
                    + "view_business_requirement_deliverable_tree",
                    "form_view_ref": "business_requirement_deliverable."
                    + "view_business_requirement_deliverable_form",
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
                    _(
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
                lambda x: x.section_id == section
            )
            brd_section_total = sum(brd_lines.mapped("price_total"))
            sections_total.append((section.name, brd_section_total))
        # No Section
        brd_lines = self.deliverable_lines.filtered(lambda x: not x.section_id)
        if any(brd_lines):
            brd_section_total = sum(brd_lines.mapped("price_total"))
            sections_total.append((_("Others"), brd_section_total))
        return sections_total

    def map_deliverable(self, new_br_id):
        """ copy and map deliverable from old to new requirement """
        deliverables = self.env["business.requirement.deliverable"]
        deliverable_ids = (
            self.env["business.requirement.deliverable"]
            .search([("business_requirement_id", "=", self.id)])
            .ids
        )
        for deliverable in self.env["business.requirement.deliverable"].browse(
            deliverable_ids
        ):
            # preserve deliverable name, normally altered during copy
            defaults = {"name": deliverable.name}
            deliverables += deliverable.copy(defaults)
        return self.browse(new_br_id).write(
            {"deliverable_lines": [(6, 0, deliverables.ids)]}
        )

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get("name"):
            default["name"] = _("%s (copy)") % (self.name)
        br = super(BusinessRequirement, self).copy(default)
        for follower in self.message_follower_ids:
            br.message_subscribe(
                partner_ids=follower.partner_id.ids,
                subtype_ids=follower.subtype_ids.ids,
            )
        if "deliverable_lines" not in default:
            self.map_deliverable(br.id)
        return br

    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        """Subscribe to all existing active deliverables when subscribing
        to a requirement
        """
        res = super().message_subscribe(
            partner_ids=partner_ids, channel_ids=channel_ids, subtype_ids=subtype_ids
        )
        has_subtype = False
        for subtype in self.env["mail.message.subtype"].browse(subtype_ids):
            subtype_ids.append(subtype.id)
            if subtype.parent_id.res_model == ("business.requirement.deliverable"):
                has_subtype = True
                continue
        if not subtype_ids or has_subtype:
            for partner_id in partner_ids or []:
                self.mapped("deliverable_lines").filtered(
                    lambda deliver: (partner_id not in deliver.message_partner_ids.ids)
                ).message_subscribe(
                    partner_ids=[partner_id], channel_ids=None, subtype_ids=None
                )
            for channel_id in channel_ids or []:
                self.mapped("deliverable_lines").filtered(
                    lambda deliver: (channel_id not in deliver.message_channel_ids.ids)
                ).message_subscribe(
                    partner_ids=None, channel_ids=[channel_id], subtype_ids=None
                )
        return res

    def message_unsubscribe(self, partner_ids=None, channel_ids=None):
        """Unsubscribe from all deliverables
        when unsubscribing from a requirement
        """
        self.mapped("deliverable_lines").message_unsubscribe(
            partner_ids=partner_ids, channel_ids=channel_ids
        )
        return super().message_unsubscribe(
            partner_ids=partner_ids, channel_ids=channel_ids
        )
