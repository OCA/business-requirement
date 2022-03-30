# Copyright 2017 Elico Corp (https://www.elico-corp.com).
# Copyright 2019 Tecnativa - Alexandre Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BusinessRequirement(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]
    _name = "business.requirement"
    _description = "Business Requirement"
    _order = "name desc"

    sequence = fields.Char(readonly=True, copy=False, index=True)
    name = fields.Char(
        readonly=True,
        copy=False,
        states={"draft": [("readonly", False)]},
    )
    description = fields.Char(
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    business_requirement = fields.Html(
        string="Customer Story", readonly=True, states={"draft": [("readonly", False)]}
    )
    scenario = fields.Html(
        readonly=True,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", False)]},
    )
    gap = fields.Html(
        readonly=True,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", False)]},
    )
    test_case = fields.Html(
        readonly=True,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", False)]},
    )
    terms_and_conditions = fields.Html(
        readonly=True,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", False)]},
    )
    category_ids = fields.Many2many(
        comodel_name="business.requirement.category",
        string="Categories",
        relation="business_requirement_category_rel",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("approved", "Approved"),
            ("in_progress", "In progress"),
            ("done", "Done"),
            ("cancel", "Cancel"),
            ("drop", "Drop"),
        ],
        default="draft",
        copy=False,
        readonly=False,
        states={"draft": [("readonly", False)]},
        tracking=True,
    )
    change_request = fields.Boolean(
        string="Change Request?", readonly=True, states={"draft": [("readonly", False)]}
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Stakeholder",
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    priority = fields.Selection(
        selection=[("0", "Low"), ("1", "Normal"), ("2", "High")],
        required=True,
        default="1",
    )
    requested_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Requested by",
        required=True,
        readonly=True,
        default=lambda self: self.env.user,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", False)]},
    )
    confirmation_date = fields.Datetime(copy=False, readonly=True)
    confirmed_user_id = fields.Many2one(
        comodel_name="res.users", string="Confirmed by", copy=False, readonly=True
    )
    responsible_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        copy=False,
        readonly=True,
        default=lambda self: self.env.user,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", False)]},
    )
    reviewer_ids = fields.Many2many(
        comodel_name="res.users",
        string="Reviewers",
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", False)]},
    )
    approval_date = fields.Datetime(copy=False, readonly=True)
    approved_id = fields.Many2one(
        comodel_name="res.users", string="Approved by", copy=False, readonly=True
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self.env.company,
    )
    to_be_reviewed = fields.Boolean()
    kanban_state = fields.Selection(
        selection=[
            ("normal", "In Progress"),
            ("on_hold", "On Hold"),
            ("done", "Ready for next stage"),
        ],
        tracking=True,
        default="normal",
    )
    origin = fields.Char(
        string="Source",
        readonly=True,
        states={"draft": [("readonly", False)], "confirmed": [("readonly", True)]},
    )
    portal_published = fields.Boolean("In Portal", default=False)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Owner",
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
    )
    date = fields.Date(
        default=lambda self: self._context.get("date", fields.Date.context_today(self)),
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "/") == "/":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "business.requirement"
                )
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("state"):
            user = self.env.user
            user_manager = user.has_group(
                "business_requirement.group_business_requirement_manager"
            )
            date = fields.Datetime.now()
            if vals["state"] == "confirmed":
                vals.update({"confirmed_user_id": user.id, "confirmation_date": date})
            if vals["state"] == "draft":
                vals.update(
                    {
                        "confirmed_user_id": False,
                        "approved_id": False,
                        "confirmation_date": False,
                        "approval_date": False,
                    }
                )
            if vals["state"] == "approved":
                if user_manager:
                    vals.update({"approved_id": user.id, "approval_date": date})
                else:
                    raise ValidationError(
                        _(
                            "You can only move to the following stage: "
                            "draft/confirmed /cancel/drop."
                        )
                    )
            if vals["state"] in {"approved", "in_progress", "done"}:
                if not user_manager:
                    raise ValidationError(
                        _(
                            "You can only move to the following stage: "
                            "draft/confirmed/cancel/drop."
                        )
                    )
        return super().write(vals)

    def name_get(self):
        """
        Display display [Name] Description
        """
        result = []
        for br in self:
            formatted_name = "[{}] {}".format(br.name, br.description)
            result.append((br.id, formatted_name))
        return result

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        """Search BR based on Name or Description"""
        # Make a search with default criteria
        names = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        # Make the other search
        descriptions = []
        if name:
            domain = [("description", "=ilike", name + "%")]
            descriptions = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names) | set(descriptions))[:limit]

    @api.returns("mail.message", lambda value: value.id)
    def message_post(
        self,
        body="",
        subject=None,
        message_type="notification",
        email_from=None,
        author_id=None,
        parent_id=False,
        subtype_xmlid=None,
        subtype_id=None,
        partner_ids=None,
        channel_ids=None,
        attachments=None,
        attachment_ids=None,
        add_sign=True,
        record_name=False,
        **kwargs
    ):
        context = self._context or {}
        if context.get("default_model") == "business.requirement" and context.get(
            "default_res_id"
        ):
            br_rec = self.env[context.get("default_model")].browse(
                context["default_res_id"]
            )
            subject = "Re: {}-{}".format(br_rec.name, br_rec.description)
        message = super(
            BusinessRequirement, self.with_context(mail_create_nosubscribe=True)
        ).message_post(
            body=body,
            subject=subject,
            message_type=message_type,
            email_from=email_from,
            author_id=author_id,
            parent_id=parent_id,
            subtype_xmlid=subtype_xmlid,
            subtype_id=subtype_id,
            partner_ids=partner_ids,
            attachments=attachments,
            attachment_ids=attachment_ids,
            add_sign=add_sign,
            record_name=record_name,
            **kwargs
        )
        return message

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        """Read group customization in order to display all the stages in the
        kanban view. if the stages values are there it will group by state.
        """
        if groupby and groupby[0] == "state":
            states = (
                self.env["business.requirement"]
                .fields_get(["state"])
                .get("state")
                .get("selection")
            )
            read_group_all_states = [
                {
                    "__context": {"group_by": groupby[1:]},
                    "__domain": domain + [("state", "=", state_value)],
                    "state": state_value,
                    "state_count": 0,
                }
                for state_value, state_name in states
            ]
            # Get standard results
            read_group_res = super().read_group(
                domain, fields, groupby, offset=offset, limit=limit, orderby=orderby
            )
            # Update standard results with default results
            result = []
            for state_value, _state_name in states:
                res = list(filter(lambda x: x["state"] == state_value, read_group_res))
                if not res:
                    res = list(
                        filter(
                            lambda x: x["state"] == state_value, read_group_all_states
                        )
                    )
                res[0]["state"] = state_value
                result.append(res[0])
            return result
        return super().read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )

    def get_portal_confirmation_action(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "business_requirement.br_portal_confirmation_options", default="none"
            )
        )

    def _compute_access_url(self):
        super()._compute_access_url()
        for br in self:
            br.access_url = "/my/business_requirement/%s" % br.id
        return

    def portal_publish_button(self):
        self.ensure_one()
        return self.write({"portal_published": not self.portal_published})


class BusinessRequirementCategory(models.Model):
    _name = "business.requirement.category"
    _description = "Categories"

    name = fields.Char(required=True)
    parent_id = fields.Many2one(
        comodel_name="business.requirement.category",
        string="Parent Category",
        ondelete="restrict",
    )
