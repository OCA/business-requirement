# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, models


class BrGenerateProjects(models.TransientModel):
    _inherit = 'br.generate.projects'

    @api.multi
    def _prepare_project_task(self, line, project_id):
        vals = super(BrGenerateProjects, self) \
            ._prepare_project_task(line, project_id)
        if line.categ_id:
            vals.update({
                'categ_id': line.categ_id.id
            })
        return vals
