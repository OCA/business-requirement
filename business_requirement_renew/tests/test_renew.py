# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestBusinessRequirementRenew(common.TransactionCase):
    def setUp(self):
        super(TestBusinessRequirementRenew, self).setUp()
        self.br = self.env.ref('business_requirement.business_requirement_1')

    def test_renew_br(self):
        res = self.br.renew_br()
        self.assertTrue(self.state,'renewed')
        self.assertTrue(res['name'], 'New application')

    def test_child_br(self):
        res = self.br.child_br()
        self.assertTrue(res['name'], 'Business Requirement Children')
