# -*- coding: utf-8 -*-
# © 2016 Elico Corp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestReportService(common.TransactionCase):
    def setUp(self):
        super(TestReportService, self).setUp()

    def test_report(self):
        ts1 = self.env.ref('project_completion_report.account_analytic_line_1')
        ts2 = self.env.ref('project_completion_report.account_analytic_line_2')
        ts3 = self.env.ref('project_completion_report.account_analytic_line_3')
        self.brA = self.env.ref('business_requirement.business_requirement_4')
        vals = {
            'for_br': True,
            'for_deliverable': True,
            'for_childs': True,
        }
        self.brA.state = 'stakeholder_approval'
        action = self.brA.project_id.generate_project_wizard()
        self.wizard = self.env['br.generate.projects'].browse(action['res_id'])
        self.wizard.write(vals)
        self.wizard.apply()
        planned_hours = 0
        remaining_hours = 0
        for hours in self.brA.task_ids:
            planned_hours += hours.planned_hours
        remaining_hours += ts1.unit_amount + ts2.unit_amount + ts3.unit_amount
        rl_hours = 0
        for rl in self.brA.deliverable_lines:
            for hours in rl.resource_ids:
                rl_hours += hours.qty
        extra_hours = rl_hours - remaining_hours
        self.assertEqual(extra_hours, 14.0)
        self.assertEqual(planned_hours, 64.0)
