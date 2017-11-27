# -*- coding: utf-8 -*-
# Copyright 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class BusinessRequirementTestCase(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementTestCase, self).setUp()
        self.ProjectObj = self.env['project.project']

        self.AnalyticAccountObject = self.env['account.analytic.account']
        # Configure unit of measure.
        self.partner1 = self.ref('base.res_partner_1')
        self.AnalyticAccount = self.AnalyticAccountObject.create(
            {'name': 'AnalyticAccount for Test'})

        self.projectA = self.ProjectObj. \
            create({'name': 'Test Project A', 'partner_id': 1,
                    'analytic_account_id': self.AnalyticAccount.id})
        self.br = self.env['business.requirement']
        self.pr_1 = self.env.ref('project.project_project_1')
        self.pr_2 = self.env.ref('project.project_project_2')

        self.ProjectCategObj = self.env['project.category']
        self.category = self.ProjectCategObj.create({'name': 'GAP_test'})

        vals = {
            'description': 'test',
            'project_id': self.projectA.id,
        }
        self.brA = self.env['business.requirement'].create(vals)

        self.WizardObj = self.env['br.gap_analysis_task_id']
        self.ProjectTaskObj = self.env['project.task']

        self.GapConfigObj = self.env[
            'business.requirement.gap.task.config.setting']
        self.gap_category = self.GapConfigObj.create(
            {'gap_task_category_id': self.category.id}
        )
        self.gap_category.set_business_requirement_gap_task_category_default()

    def test_wizard_apply(self):
        self.WizardObj.create({'estimated_time': 40})
        self.WizardObj.with_context({'active_id': self.brA.id}).apply()
        self.assertEqual(
            self.brA.gap_analysis_task_id.name,
            'Gap Analysis for {}'.format(self.brA.name))
        self.assertEqual(
            self.brA.gap_analysis_task_id.categ_id.id, self.category.id
        )
        self.assertEqual(
            self.brA.gap_analysis_task_id.user_id.id, self.env.user.id
        )
        self.assertEqual(
            self.brA.gap_analysis_task_id.project_id.id, self.brA.project_id.id
        )
        self.assertEqual(
            self.brA.gap_analysis_task_id.planned_hours,
            self.WizardObj.estimated_time
        )
        self.assertEqual(
            self.brA.gap_analysis_task_id.id,
            self.ProjectTaskObj.search([]).sorted('create_date')[-1].id
        )
