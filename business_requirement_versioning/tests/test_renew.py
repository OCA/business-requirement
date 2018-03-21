# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestBusinessRequirementRenew(common.TransactionCase):
    def setUp(self):
        super(TestBusinessRequirementRenew, self).setUp()
        self.source = self.env.ref(
            "business_requirement.business_requirement_1")
        self.user = self.env.ref("base.user_demo")
        self.br_1 = self.env['business.requirement'].create({
            'state': 'done',
            'responsible_id': self.user.id,
            'version': 1,
            'source_id': self.source.id,
            'copy_from_id': self.source.id,
            'description': 'test_1',
            'reviewer_ids': [(6, 0, [self.user.id])]
        })
        self.br_2 = self.env['business.requirement'].create({
            'state': 'done',
            'responsible_id': self.user.id,
            'version': 0,
            'description': 'test_2'
        })

    def test_renew_br(self):
        res_1 = self.br_1.renew_br()
        res_2 = self.br_2.renew_br()
        self.assertTrue(self.br_1.state, 'renewed')
        self.assertTrue(self.br_2.state, 'renewed')
        self.assertTrue(res_1['name'], 'New application')
        self.assertTrue(res_2['name'], 'New application')

    def test_related_br(self):
        res = self.br_1.related_br()
        self.assertTrue(res['name'], 'Related Business Requirement')
