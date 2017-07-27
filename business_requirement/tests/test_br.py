# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class BusinessRequirementTestCase(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementTestCase, self).setUp()
        self.br = self.env['business.requirement']
        self.pr_1 = self.env.ref('project.project_project_1')
        self.pr_2 = self.env.ref('project.project_project_2')

    def test_get_level(self):
        br_vals1 = {
            'name': ' test',
            'description': 'test',
            'ref': '/',
            'parent_id': False,
        }
        br1 = self.br.create(br_vals1)
        br1._get_level()
        level1 = br1.level
        self.assertEqual(level1, 1)

        br_vals2 = {
            'name': ' test',
            'description': 'test',
            'parent_id': br1.id,
        }
        br2 = self.br.create(br_vals2)
        br2._get_level()
        level2 = br2.level
        self.assertEqual(level2, 2)

        br_vals3 = {
            'name': ' test',
            'description': 'test',
            'parent_id': br2.id,
        }
        br3 = self.br.create(br_vals3)
        br3._get_level()
        level3 = br3.level
        self.assertEqual(level3, 3)

    def test_action_button_confirm(self):
        br_vals = {
            'name': ' test',
            'description': 'test',
            'parent_id': False,
        }
        br = self.br.create(br_vals)
        br.action_button_confirm()
        self.assertEqual(br.state, 'confirmed')

    def test_action_button_back_draft(self):
        br_vals = {
            'name': 'test',
            'description': 'test',
            'parent_id': False,
        }
        br = self.br.create(br_vals)
        br.action_button_back_draft()
        self.assertEqual(br.state, 'draft')

    def test_action_button_approve(self):
        br_vals = {
            'name': ' test',
            'description': 'test',
            'parent_id': False,
        }
        br = self.br.create(br_vals)
        br.action_button_approve()
        self.assertEqual(br.state, 'approved')

    def test_action_button_done(self):
        br_vals = {
            'name': ' test',
            'description': 'test',
            'parent_id': False,
        }
        br = self.br.create(br_vals)
        br.action_button_done()
        self.assertEqual(br.state, 'done')

    def test_br_name_search(self):
        br_vals = {
            'name': ' test',
            'description': 'test',
            'parent_id': False,
        }
        self.br.create(br_vals)
        brs = self.br.name_search(name='test')
        self.assertEqual(bool(brs), True)

    def test_create_sequance(self):
        br_vals = {
            'name': '/',
            'description': 'test',
        }
        self.br.create(br_vals)

    def test_create_write_project(self):
        br_vals = {
            'name': 'test',
            'description': 'test',
            'project_id': self.pr_1.id
        }
        self.br.create(br_vals)
        br_vals1 = {
            'project_id': self.pr_2.id
        }
        self.br.write(br_vals1)
