# -*- coding: utf-8 -*-
from openerp import api, fields, models
# from openerp.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class BrIssue(models.TransientModel):
    _name = "br.issue"

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
        help="Customer who has to approve the BR before it goes to development",
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
        _logger.debug("Creando BR")

        # context = self.env.context
        # case_id = context and context.get('active_ids', []) or []
        # case_id = case_id and case_id[0] or False

        # fields to fill in the BR
        _logger.debug("Fin de create_br, hasta luego")
