# Copyright 2026 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    business_requirement_id = fields.Many2one(
        comodel_name="business.requirement",
        string="Business Requirement",
        ondelete="restrict",
        index=True,
        tracking=True,
        copy=True,
    )

    @api.onchange("business_requirement_id")
    def _onchange_business_requirement_id(self):
        br_project = self.business_requirement_id.project_id
        if not br_project:
            return None
        if not self.project_id:
            self.project_id = br_project
        elif self.project_id != br_project:
            return {
                "warning": {
                    "title": _("Different projects"),
                    "message": _(
                        "The task project (%(task_project)s) is not the project "
                        "of the business requirement (%(br_project)s)."
                    )
                    % {
                        "task_project": self.project_id.display_name,
                        "br_project": br_project.display_name,
                    },
                }
            }
        return None
