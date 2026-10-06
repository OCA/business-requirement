# Copyright 2026 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from markupsafe import Markup

from odoo import models


class BusinessRequirementDeliverable(models.Model):
    _inherit = "business.requirement.deliverable"

    def _get_task_allocated_hours(self):
        """Quantity in hours, only when the deliverable is measured in time"""
        self.ensure_one()
        hour_uom = self.env.ref("uom.product_uom_hour")
        if self.uom_id.category_id != hour_uom.category_id:
            return 0.0
        return self.uom_id._compute_quantity(self.qty, hour_uom)

    def _prepare_task_vals(self, project):
        self.ensure_one()
        lines = self.name.strip().splitlines() or [self.display_name]
        return {
            "name": lines[0],
            "description": Markup("<br/>").join(lines[1:]),
            "project_id": project.id,
            "partner_id": self.business_requirement_id.partner_id.id,
            "allocated_hours": self._get_task_allocated_hours(),
            "sequence": self.sequence,
            "business_requirement_id": self.business_requirement_id.id,
            "business_requirement_deliverable_id": self.id,
            # Created as sudo, so they would be assigned to the approver
            "user_ids": False,
        }

    def _create_tasks(self, project):
        tasks = (
            self.env["project.task"]
            .sudo()
            .create([deliverable._prepare_task_vals(project) for deliverable in self])
        )
        for task in tasks:
            task.message_post(
                body=self.env._(
                    "This task has been created from: %(link)s",
                    link=task.business_requirement_id._get_html_link(),
                )
            )
        return tasks
