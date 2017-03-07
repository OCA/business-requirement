# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common
from openerp.exceptions import ValidationError


@common.at_install(False)
@common.post_install(True)
class BusinessRequirementTestCase(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementTestCase, self).setUp()
        self.ModelDataObj = self.env['ir.model.data']

        self.ProjectObj = self.env['project.project']

        self.AnalyticAccountObject = self.env['account.analytic.account']

        self.AnalyticAccount = self.AnalyticAccountObject.create(
            {'name': 'AnalyticAccount for Test',
             'state': 'draft'})

        self.projectA = self.ProjectObj.create(
            {'name': 'Test Project A', 'partner_id': 1, 'parent_id': 1,
                'analytic_account_id': self.AnalyticAccount.id})
        self.projectB = self.ProjectObj.create(
            {'name': 'Test Project B', 'partner_id': 1, 'parent_id': 1,
                'analytic_account_id': self.AnalyticAccount.id})

        # Configure unit of measure.
        self.categ_wtime = self.ref('product.uom_categ_wtime')
        self.categ_kgm = self.ref('product.product_uom_categ_kgm')

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

        # Product Created A, B, C, D
        self.ProductObj = self.env['product.product']
        self.productA = self.ProductObj.create(
            {'name': 'Product A', 'uom_id': self.uom_hours.id,
                'uom_po_id': self.uom_hours.id,
                'standard_price': 450})
        self.productB = self.ProductObj.create(
            {'name': 'Product B', 'uom_id': self.uom_hours.id,
                'uom_po_id': self.uom_hours.id,
                'standard_price': 550})
        self.productC = self.ProductObj.create(
            {'name': 'Product C', 'uom_id': self.uom_days.id,
                'uom_po_id': self.uom_days.id,
                'standard_price': 650})
        self.productD = self.ProductObj.create(
            {'name': 'Product D', 'uom_id': self.uom_kg.id,
                'uom_po_id': self.uom_kg.id,
                'standard_price': 750})

        vals = {
            'description': 'test',
            'project_id': self.projectA.id,
            'deliverable_lines': [
                (0, 0, {'name': 'deliverable line1', 'qty': 1.0,
                        'unit_price': 900, 'uom_id': 1,
                        'resource_ids': [
                            (0, 0, {
                                'name': 'Resource Line1',
                                'product_id': self.productA.id,
                                'qty': 100,
                                'uom_id': self.uom_hours.id,
                                'resource_type': 'task',
                            }),
                            (0, 0, {
                                'name': 'Resource Line1',
                                'product_id': self.productB.id,
                                'qty': 100,
                                'uom_id': self.uom_hours.id,
                                'resource_type': 'task',
                            })
                        ]
                        }),
                (0, 0, {'name': 'deliverable line2', 'qty': 1.0,
                        'unit_price': 1100, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line3', 'qty': 1.0,
                        'unit_price': 1300, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line4', 'qty': 1.0,
                        'unit_price': 1500, 'uom_id': 1,
                        }),
            ],
        }

        self.brA = self.env['business.requirement'].create(vals)
        self.brB = self.env['business.requirement'].create(vals)
        self.brC = self.env['business.requirement'].create(vals)

    def test_br_state_generate_project_wizard(self):
        # test when state=draft
        self.brA.state = 'draft'
        self.brB.state = 'draft'
        self.brC.state = 'draft'
        with self.assertRaises(ValidationError):
            self.projectA.generate_project_wizard()

        # test when state=confirmed
        self.brA.state = 'confirmed'
        self.brB.state = 'confirmed'
        self.brC.state = 'confirmed'
        with self.assertRaises(ValidationError):
            self.projectA.generate_project_wizard()

        # test when state=stakeholder_approval
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'confirmed'
        self.brC.state = 'draft'
        with self.assertRaises(ValidationError):
            self.projectA.generate_project_wizard()

        # test when state=stakeholder_approval
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'draft'
        with self.assertRaises(ValidationError):
            self.projectA.generate_project_wizard()

        # test when state=stakeholder_approval
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'confirmed'
        with self.assertRaises(ValidationError):
            self.projectA.generate_project_wizard()

        # test when state=stakeholder_approval
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'stakeholder_approval'
        action = self.projectA.generate_project_wizard()
        self.assertTrue(action)

        # test when state=stakeholder_approval
        self.brA.state = 'done'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'stakeholder_approval'
        action = self.projectA.generate_project_wizard()
        self.assertTrue(action)

        # test when state=stakeholder_approval
        self.brA.state = 'cancel'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'stakeholder_approval'
        action = self.projectA.generate_project_wizard()
        self.assertTrue(action)

    def test_wizard_apply(self):
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'stakeholder_approval'
        action = self.projectA.generate_project_wizard()
        self.assertNotEqual(action, False)
        self.assertNotEqual(action.get('res_id', False), False)
        self.wizard = self.env[
            'br.generate.projects'].browse(action['res_id'])
        self.wizard.for_br = True
        res = self.wizard.apply()
        self.assertEqual(res.get('type', True), 'ir.actions.act_window')

    def test_br_generate_projects_wizard(self):
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'stakeholder_approval'
        action = self.brA.generate_projects_wizard()
        self.assertEqual(
            'ir.actions.act_window',
            action['type'])

    def test_project_generate_project_wizard(self):
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'stakeholder_approval'

        default_uom = self.env[
            'project.config.settings'
        ].get_default_time_unit('time_unit').get('time_unit', False)

        action = self.projectA.generate_project_wizard()
        self.assertEqual(
            action.get('context', False).get('default_uom', False),
            default_uom
        )
        self.assertEqual(
            self.projectA.br_ids,
            self.env[
                'br.generate.projects'].browse(action['res_id']).br_ids
        )
        for br in self.projectA.br_ids:
            self.assertEqual('stakeholder_approval', br.state)

            generated = self.env['project.task'].search(
                [('br_resource_id', '=', br.id)])
            self.assertFalse(generated)

        from_project = self.env[
            'br.generate.projects'].browse(action['res_id']).br_ids
        self.assertTrue(from_project)

        br_ids_a = self.projectA.br_ids
        br_ids_a.filtered(lambda br_ids_a: not br_ids_a.parent_id)

        br_ids_b = from_project
        br_ids_b.filtered(lambda br_ids_b: not br_ids_b.parent_id)

        self.assertEqual(br_ids_a, br_ids_b)

    def test_br_wizard_onchange_for_br(self):
        wizard_obj = self.env['br.generate.projects']
        vals = {
            'partner_id': 1,
            'project_id': self.projectA.id,
            'for_deliverable': False,
            'for_childs': True,
            'br_ids': self.projectA.br_ids,
        }
        wizard = wizard_obj.create(vals)
        wizard.write({'for_br': False})
        wizard._onchange_for_br()
        self.assertEqual(wizard.for_childs, False)

    def test_br_wizard_apply(self):
        vals = {
            'for_br': False,
            'for_deliverable': False,
            'for_childs': False,
        }
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'stakeholder_approval'
        action = self.projectA.generate_project_wizard()
        self.wizard = self.env[
            'br.generate.projects'].browse(action['res_id'])
        self.wizard.write(vals)
        res = self.wizard.apply()
        self.assertEqual(str(res.get('name')), 'Task')

    def test_br_wizard_generate_deliverable_projects(self):
        vals = {
            'for_br': False,
            'for_deliverable': False,
            'for_childs': False,
        }
        self.brA.state = 'stakeholder_approval'
        self.brB.state = 'stakeholder_approval'
        self.brC.state = 'stakeholder_approval'
        action = self.projectA.generate_project_wizard()
        self.wizard = self.env[
            'br.generate.projects'].browse(action['res_id'])
        self.wizard.write(vals)
        res = self.wizard.generate_deliverable_projects(
            self.projectA, self.brA.deliverable_lines, [], [])
        res = res
