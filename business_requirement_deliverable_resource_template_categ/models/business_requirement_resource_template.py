# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class BusinessRequirementResourceTemplate(models.Model):
    _inherit = "business.requirement.resource.template"

    categ_id = fields.Many2one(
        'project.category.main',
        string="Task Category"
    )
