# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestBusinessRequirementRenew(common.TransactionCase):
    def setUp(self):
        super(TestBusinessRequirementRenew, self).setUp()
        self.source = self.env.ref("business_requirement.business_requirement_1")
        self.user = self.env.ref("base.user_demo")
        self.br = self.env['business.requirement'].create({
            'state': 'done',
            'responsible_id': self.user.id,
            'version': 1,
            'source_id': self.source.id,
            'copy_from_id': self.source.id,
        })

    def test_renew_br(self):
        res = self.br.renew_br()
        self.assertTrue(self.br.state, 'renewed')
        self.assertTrue(res['name'], 'New application')

    def test_child_br(self):
        res = self.br.child_br()
        self.assertTrue(res['name'], 'Business Requirement Children')
