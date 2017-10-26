# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class BrGenerateProjects(models.TransientModel):
    _inherit = 'br.generate.projects'

    @api.multi
    def _prepare_project_task(self, line, project_id):
        vals = super(BrGenerateProjects, self) \
            ._prepare_project_task(line, project_id)
        if line.categ_id:
            vals.update({
                'tag_ids': [(6, 0, [line.categ_id.id])]
            })
        return vals
