# -*- coding: utf-8 -*-
# © 2017 Praxya (https://www.praxya.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class BrIssue(models.TransientModel):
    _name = "br.issue"

    name = fields.Char()
    issue_id = fields.Many2one(
        comodel_name="project.issue",
        string="Related Issue",
        help="The issue that originated or made this BR relevant.",
    )
    requested_id = fields.Many2one(
        comodel_name="res.users",
        string="Requested by",
        help="Odoo user who requests this issue to be converted to BR.",
    )
    responsible_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        help="Odoo user who will be in charge of this BR.",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        help="Customer who has to approve the BR before it goes to development"
    )
    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
    )
    to_be_reviewed = fields.Boolean(
        string="To be Reviewed",
        help="Check if this BR has to be reviewed by a consultant or a PM",
    )
    priority = fields.Selection(
        [("0", "Low"),
         ("1", "Normal"),
         ("2", "High")],
        string="Priority",
    )
    reviewer_ids = fields.Many2many(
        comodel_name="res.users",
        string="Reviewers",
        help="Users to review the BR",
    )
    business_requirement = fields.Html(
        string="Customer Story",
    )

    @api.multi
    def create_br(self):
        vals = {
            'description': self.name,
            "requested_id": self.requested_id.id,
            "responsible_id": self.responsible_id.id,
            "partner_id": self.partner_id.id,
            "project_id": self.project_id.id,
            "to_be_reviewed": self.to_be_reviewed,
            "priority": self.priority,
            "business_requirement": self.business_requirement,
            "change_request": True,
        }
        if self.to_be_reviewed:
            vals.update({"reviewer_ids": [(6, 0, self.reviewer_ids.ids)]})
        created_br = self.env['business.requirement'].create(vals)
        if created_br:
            self.env['project.issue'].search(
                [('id', '=', self.issue_id.id)]
            ).write(
                {'business_requirement_id': created_br.id}
            )
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'business.requirement',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': created_br.id,
            'context': {}
        }
