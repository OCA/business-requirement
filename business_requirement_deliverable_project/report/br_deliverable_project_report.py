# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class BusinessRequirementDeliverableSaleReport(models.Model):
    _inherit = "business.requirement.deliverable.sale.report"
    _auto = False

    linked_project = fields.Many2one('project.project', 'Linked Project',
                                     readonly=True)

    def _select(self):
        return super(BusinessRequirementDeliverableSaleReport, self
                     )._select() + ", br.linked_project as linked_project"
