# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common


class TestReportService(common.TransactionCase):
    def setUp(self):
        super(TestReportService, self).setUp()
        self.br = self.env.ref('business_requirement.business_requirement_4')
        self.project = self.env.ref('project.project_project_4')

    def test_br_open_project_completion_report(self):
        res = self.br.br_open_project_completion_report()
        self.assertTrue(res['name'], 'BR Project completion report')

    def test_project_open_pro_com_trp(self):
        res = self.project.project_open_pro_com_trp()
        self.assertTrue(res['name'], 'Project project completion report')
