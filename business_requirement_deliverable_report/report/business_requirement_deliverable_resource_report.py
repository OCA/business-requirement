# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class BRDeliverableSourceReport(models.AbstractModel):
    _name = 'business.requirement.deliverable.resource.report'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        br_deliverable_resource_report = report_obj._get_report_from_name(
            '%s.%s' % (
                'business_requirement_deliverable_report',
                'br_deliverable_resource_report'))

        docargs = {
            'doc_ids': self._ids,
            'doc_model': br_deliverable_resource_report.model,
            'docs': self,
        }

        return report_obj.render(
            '%s.%s' % (
                'business_requirement_deliverable_report',
                'br_deliverable_resource_report'),
            docargs)
