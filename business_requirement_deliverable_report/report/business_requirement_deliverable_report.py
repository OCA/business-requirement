# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class BRDeliverableReport(models.AbstractModel):
    _name = 'business.requirement.deliverable.report'

    @api.multi
    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        br_deliverable_resource_report = report_obj._get_report_from_name(
            cr, uid,
            'business_requirement_deliverable_report.br_deliverable_report')
        selected_records = self.pool['business.requirement'].browse(
            cr, uid, ids, context=context)

        docargs = {
            'doc_ids': ids,
            'doc_model': br_deliverable_resource_report,
            'docs': selected_records,
        }

        return report_obj.render(
            cr, uid, ids,
            'business_requirement_deliverable_report.br_deliverable_report',
            docargs, context=context)
