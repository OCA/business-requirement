# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from openerp.exceptions import ValidationError


@common.at_install(False)
@common.post_install(True)
class BusinessRequirementTestCase(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementTestCase, self).setUp()
        self.ProjectObj = self.env['project.project']

        self.AnalyticAccountObject = self.env['account.analytic.account']
        # Configure unit of measure.
        self.categ_wtime = self.ref('product.uom_categ_wtime')
        self.categ_kgm = self.ref('product.product_uom_categ_kgm')
        self.partner1 = self.ref('base.res_partner_1')
        self.UomObj = self.env['product.uom']
        self.uom_hours = self.UomObj.create({
            'name': 'Test-Hours',
            'category_id': self.categ_wtime,
            'factor': 8,
            'uom_type': 'smaller'})
        self.uom_days = self.UomObj.create({
            'name': 'Test-Days',
            'category_id': self.categ_wtime,
            'factor': 1})
        self.uom_kg = self.UomObj.create({
            'name': 'Test-KG',
            'category_id': self.categ_kgm,
            'factor_inv': 1,
            'factor': 1,
            'uom_type': 'reference',
            'rounding': 0.000001})

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
            {'name': 'Product A', 'uom_id': self.uom_hours.id,
             'uom_po_id': self.uom_hours.id,
             'standard_price': 450})
        self.productB = self.ProductObj. \
            create({'name': 'Product B', 'uom_id': self.uom_hours.id,
                    'uom_po_id': self.uom_hours.id,
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
            body='Test Body',
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
        self.env['business.requirement'].read_group(
            [],
            ['state'], ['state'])[0]
        self.env['business.requirement'].read_group(
            [],
            [], [])[0]

    def test_br_state_generate_project_wizard(self):
        # test when state=draft
        self.brA.state = 'draft'
        self.brB.state = 'draft'
        self.brC.state = 'draft'

        # test when state=confirmed
        self.brA.state = 'confirmed'
        self.brB.state = 'confirmed'
        self.brC.state = 'confirmed'

        self.brB.state = 'confirmed'
        self.brC.state = 'draft'

        # test when state=stakeholder_approval
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'approved'
        self.brC.state = 'approved'

        # test when state=done
        self.brA.state = 'done'
        self.brB.state = 'approved'
        self.brC.state = 'approved'

        # test when state=cancel
        self.brB.state = 'approved'
        self.brC.state = 'approved'
