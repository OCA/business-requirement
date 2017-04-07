# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class BrGenerateProjects(models.TransientModel):
    _inherit = 'br.generate.projects'

    @api.multi
    def _prepare_project_task(self, line, project_id):
        vals = super(BrGenerateProjects, self) \
            ._prepare_project_task(line, project_id)
        vals.update({'categ_id': line.categ_id.id})
        return vals
