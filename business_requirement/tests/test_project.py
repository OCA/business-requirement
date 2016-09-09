# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common


@common.at_install(False)
@common.post_install(True)
class ProjectTestCase(common.TransactionCase):
    def setUp(self):
        super(ProjectTestCase, self).setUp()
        self.br = self.env['business.requirement']
        self.pr_5 = self.env.ref('project.project_project_5')

        br_vals1 = {
            'name': ' test',
            'description': 'test',
            'parent_id': False,
            'project_id': self.pr_5.id
        }
        br1 = self.br.create(br_vals1)
        br1._get_level()
        level1 = br1.level
        self.assertEqual(level1, 1)

        br_vals2 = {
            'name': ' test',
            'description': 'test',
            'parent_id': br1.id,
            'project_id': self.pr_5.id
        }
        br2 = self.br.create(br_vals2)
        br2._get_level()
        level2 = br2.level
        self.assertEqual(level2, 2)

        br_vals3 = {
            'name': ' test',
            'description': 'test',
            'parent_id': br2.id,
            'project_id': self.pr_5.id
        }
        br3 = self.br.create(br_vals3)
        br3._get_level()
        level3 = br3.level
        self.assertEqual(level3, 3)

    def test_compute_br_count(self):
        self.pr_5._compute_br_count()
        self.assertEqual(self.pr_5.br_count, len(self.pr_5.br_ids))
