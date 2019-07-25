# Copyright 2019 Tecnativa - Victor M.M. Torres
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class CrmLeadCreateRequirement(models.TransientModel):
    _name = "crm.lead.create.requirement"
    _description = "Crm Lead Create Requirement"

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Opportunity',
        readonly=True,
        domain=[('type', '=', 'opportunity')])
    description = fields.Char(
        'Description',
        required=True,
    )
    customer_history = fields.Html('Customer history')

    @api.model
    def default_get(self, fields):
        result = super(CrmLeadCreateRequirement, self).default_get(fields)
        lead = self.env['crm.lead'].browse(
            [self.env.context.get('active_id')])
        if lead:
            result.update({
                'lead_id': lead.id,
                'description': lead.name,
                'customer_history': lead.description,
            })
        return result

    def _prepare_business_requirement_vals(self):
        return {
            "business_requirement": (
                self.customer_history or self.lead_id.description
            ) or self.lead_id.name,
            "description": self.description or (
                self.lead_id.description or self.lead_id.name),
            "partner_id": self.lead_id.partner_id.id,
            "user_id": self.lead_id.user_id.id or self.lead_id.create_uid.id,
            "lead_id": self.lead_id.id,
        }

    @api.multi
    def action_lead_to_business_requirement(self):
        """Procedure to allow create Business Requirement
        for Leads with prefeched information such as
        user, customer history, partner
        """
        self.ensure_one()
        requirement = self.env['business.requirement'].create(
            self._prepare_business_requirement_vals()
        )
        # Chatter reflects new Requierement on both ways
        msg_body = _(
            "Requirement %s created"
        ) % (
            "<a href=# data-oe-model=business.requirement data-oe-id=%d>%s</a>"
            % (requirement.id, requirement.name)
        )
        lead = self.lead_id
        lead.message_post(body=msg_body)
        requirement_msg = _(
            "This business requirement has been created from:"
        ) + " %s" % (
            "<a href=# data-oe-model=crm.lead data-oe-id=%d>%s</a>"
        ) % (lead.id, lead.name)
        requirement.message_post(body=requirement_msg)
        return self.env[
            'business.requirement'
        ].browse(requirement.id).get_formview_action()
