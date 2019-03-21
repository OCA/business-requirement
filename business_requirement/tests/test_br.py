# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common
from odoo.exceptions import ValidationError
from odoo import _


@common.at_install(False)
@common.post_install(True)
class BusinessRequirementTestCase(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementTestCase, self).setUp()
        self.ProjectObj = self.env['project.project']

        self.AnalyticAccountObject = self.env['account.analytic.account']
        # Configure unit of measure.
        self.categ_wtime = self.ref('uom.uom_categ_wtime')
        self.categ_kgm = self.ref('uom.product_uom_categ_kgm')
        self.partner1 = self.ref('base.res_partner_1')
        self.UomObj = self.env['uom.uom']
        self.uom_hours = self.ref('uom.product_uom_hour')
        self.uom_days = self.ref('uom.product_uom_day')
        self.uom_kg = self.ref('uom.product_uom_kgm')

        self.AnalyticAccount = self.AnalyticAccountObject.create(
            {'name': 'AnalyticAccount for Test'})

        self.projectA = self.ProjectObj. \
            create({'name': 'Test Project A', 'partner_id': 1,
                    'analytic_account_id': self.AnalyticAccount.id})
        self.br = self.env['business.requirement']
        self.pr_1 = self.env.ref('project.project_project_1')
        self.pr_2 = self.env.ref('project.project_project_2')

        vals = {
            'description': 'test',
            'project_id': self.projectA.id
        }
        # Product Created A, B, C, D
        self.ProductObj = self.env['product.product']
        self.productA = self.ProductObj.create(
            {'name': 'Product A', 'uom_id': self.uom_hours,
             'uom_po_id': self.uom_hours,
             'standard_price': 450})
        self.productB = self.ProductObj. \
            create({'name': 'Product B', 'uom_id': self.uom_hours,
                    'uom_po_id': self.uom_hours,
                    'standard_price': 550})

        vals1 = vals.copy()
        vals2 = vals.copy()
        self.brA = self.env['business.requirement'].create(vals)
        self.brB = self.env['business.requirement'].create(vals1)
        self.brC = self.env['business.requirement'].create(vals2)

    def test_project_id_change(self):
        self.pr_1.write({'partner_id': self.partner1})
        self.brA.project_id_change()
        self.assertEqual(
            self.brA.project_id.partner_id.id, self.brA.partner_id.id
        )

    def test_compute_sub_br_count(self):
        self.brC.write({'parent_id': self.brA.id})
        self.brB.write({'parent_id': self.brA.id})
        self.brA._compute_sub_br_count()
        self.assertEqual(
            self.brA.sub_br_count, len(self.brA.business_requirement_ids)
        )

    def test_message_post(self):
        self.brA.with_context({
            'default_model': 'business.requirement',
            'default_res_id': self.brA.id
        }).message_post(
            body=_('Test Body'),
            message_type='notification',
            subtype='mt_notification',
            parent_id=False,
            attachments=None,
            content_subtype='html',
            **{}
        )

    def test_get_default_company(self):
        self.brA._get_default_company()
        self.env.user.company_id = False
        with self.assertRaises(ValidationError):
            self.brA._get_default_company()

    def test_get_level(self):
        br_vals1 = {
            'name': ' test',
            'description': 'test',
            'ref': '/',
            'parent_id': False,
        }
        br1 = self.br.create(br_vals1)
        br1._compute_get_level()
        level1 = br1.level
        self.assertEqual(level1, 1)

        br_vals2 = {
            'name': ' test',
            'description': 'test',
            'parent_id': br1.id,
        }
        br2 = self.br.create(br_vals2)
        br2._compute_get_level()
        level2 = br2.level
        self.assertEqual(level2, 2)

        br_vals3 = {
            'name': ' test',
            'description': 'test',
            'parent_id': br2.id,
        }
        br3 = self.br.create(br_vals3)
        br3._compute_get_level()
        level3 = br3.level
        self.assertEqual(level3, 3)

    def test_br_name_get(self):
        vals = {
            'name': 'test',
            'description': 'test',
            'ref': 'test'
        }
        br = self.br.create(vals)
        res = br.name_get()
        self.assertEqual('[test][test] test', res[0][1])

        vals_2 = {
            'name': 'test2',
            'description': 'test2'
        }
        br2 = self.br.create(vals_2)
        res2 = br2.name_get()
        self.assertEqual('[test2] test2', res2[0][1])

    def test_br_name_search(self):
        br_vals = {
            'name': ' test',
            'description': 'test',
            'parent_id': False,
        }
        self.br.create(br_vals)

        brs = self.br.name_search(name='test')
        self.assertEqual(bool(brs), True)

    def test_create_name_equal_slash(self):
        name = self.env['ir.sequence'].next_by_code('business.requirement')
        br_vals = {
            'name': '/',
            'description': 'test',
        }
        len_seq = name[2:]
        seq = "BR" + str(int(len_seq) + 1).zfill(int(len(len_seq)))
        res = self.br.create(br_vals)
        self.assertEqual(seq, res.name)

    def test_create_write_project(self):
        br_vals = {
            'name': 'test',
            'description': 'test',
            'project_id': self.pr_1.id
        }
        res = self.br.create(br_vals)
        br_vals1 = {
            'project_id': self.pr_2.id
        }
        res.write(br_vals1)
        self.assertEqual(res.project_id.id, self.pr_2.id)

    def test_br_read_group(self):
        states = self.br._get_states()
        br_vals = {
            'name': 'test',
            'description': 'test',
            'project_id': self.pr_1.id
        }
        res = self.br.create(br_vals)
        groups_1 = self.br.read_group([('id', '=', res.id)], [], ['state'])
        self.assertEqual(len(groups_1), len(states))

        groups_2 = self.br.read_group(
            [('id', '=', res.id)],
            [],
            ['project_id'])
        self.assertEqual(len(groups_2), 1)

        groups_3 = self.br.read_group([], [], [])
        self.assertEqual(len(groups_3), 1)

        br_count = self.br.search_count([])
        self.assertEqual(groups_3[0]['__count'], br_count)

    def test_check_state_workflow(self):
        br_vals = {
            'name': 'test',
            'description': 'test'
        }
        br = self.br.create(br_vals)

        self.assertTrue(br._check_state_workflow('cancel'))
        self.assertTrue(br._check_state_workflow('drop'))
        self.assertTrue(br._check_state_workflow('confirmed'))
        with self.assertRaises(ValidationError):
            br._check_state_workflow('approved')

        br.state = 'confirmed'
        self.assertTrue(br._check_state_workflow('draft'))
        self.assertTrue(br._check_state_workflow('approved'))
        with self.assertRaises(ValidationError):
            br._check_state_workflow('stakeholder_approval')

        br.state = 'approved'
        self.assertTrue(br._check_state_workflow('confirmed'))
        self.assertTrue(br._check_state_workflow('stakeholder_approval'))
        with self.assertRaises(ValidationError):
            br._check_state_workflow('in_progress')

        br.state = 'stakeholder_approval'
        self.assertTrue(br._check_state_workflow('approved'))
        self.assertTrue(br._check_state_workflow('in_progress'))
        with self.assertRaises(ValidationError):
            br._check_state_workflow('done')

        br.state = 'in_progress'
        self.assertTrue(br._check_state_workflow('stakeholder_approval'))
        self.assertTrue(br._check_state_workflow('done'))
        with self.assertRaises(ValidationError):
            br._check_state_workflow('approved')

        br.state = 'done'
        self.assertTrue(br._check_state_workflow('draft'))
        with self.assertRaises(ValidationError):
            br._check_state_workflow('confirmed')

        br_vals2 = {
            'name': 'test',
            'description': 'test'
        }
        br2 = self.br.sudo(self.ref('base.user_demo')).create(br_vals2)
        br2 = br2.sudo(self.ref('base.user_demo'))
        br2.state = 'confirmed'
        with self.assertRaises(ValidationError):
            br2._check_state_workflow('approved')

        br2.sudo().state = 'approved'
        with self.assertRaises(ValidationError):
            br2._check_state_workflow('confirmed')

    def test_br_state_change(self):
        self.brA.state = 'draft'
        self.assertFalse(self.brA.confirmed_id)
        self.assertFalse(self.brA.approved_id)
        self.assertFalse(self.brA.confirmation_date)
        self.assertFalse(self.brA.approval_date)

        self.brA.state = 'confirmed'
        self.assertEqual(self.brA.confirmed_id.id, self.env.uid)

        self.brA.state = 'approved'
        self.assertEqual(self.brA.confirmed_id.id, self.env.uid)

        self.brA.state = 'stakeholder_approval'
        self.assertEqual(self.brA.confirmed_id.id, self.env.uid)
