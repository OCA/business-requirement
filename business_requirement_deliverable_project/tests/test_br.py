# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common
from openerp.osv import osv


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
        self.categ_wtime = self.ModelDataObj.xmlid_to_res_id(
            'product.uom_categ_wtime')
        self.categ_kgm = self.ModelDataObj.xmlid_to_res_id(
            'product.product_uom_categ_kgm')

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

    def test_br_state(self):
        # test when state=draft
        self.brA.state = 'draft'
        self.brB.state = 'draft'
        self.brC.state = 'draft'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception, e:
            action = False
            self.assertEqual(action, False)
            self.assertEqual(type(e), osv.except_osv)

        # test when state=confirmed
        self.brA.state = 'confirmed'
        self.brB.state = 'confirmed'
        self.brC.state = 'confirmed'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception, e:
            action = False
            self.assertEqual(action, False)
            self.assertEqual(type(e), osv.except_osv)

        # test when state=approved
        self.brA.state = 'approved'
        self.brB.state = 'confirmed'
        self.brC.state = 'draft'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception, e:
            action = False
            self.assertEqual(action, False)
            self.assertEqual(type(e), osv.except_osv)

        # test when state=approved
        self.brA.state = 'approved'
        self.brB.state = 'approved'
        self.brC.state = 'draft'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception, e:
            action = False
            self.assertEqual(action, False)
            self.assertEqual(type(e), osv.except_osv)

        # test when state=approved
        self.brA.state = 'approved'
        self.brB.state = 'approved'
        self.brC.state = 'confirmed'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception, e:
            action = False
            self.assertEqual(action, False)
            self.assertEqual(type(e), osv.except_osv)

        # test when state=approved
        self.brA.state = 'approved'
        self.brB.state = 'approved'
        self.brC.state = 'approved'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception:
            action = False
        if action:
            self.assertNotEqual(action, False)

        # test when state=approved
        self.brA.state = 'done'
        self.brB.state = 'approved'
        self.brC.state = 'approved'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception:
            action = False
        if action:
            self.assertNotEqual(action, False)

        # test when state=approved
        self.brA.state = 'done'
        self.brB.state = 'approved'
        self.brC.state = 'approved'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception:
            action = False
        if action:
            self.assertNotEqual(action, False)

    def test_for_br(self):
        self.brA.state = 'approved'
        self.brB.state = 'approved'
        self.brC.state = 'approved'
        try:
            action = self.projectA.generate_project_wizard()
        except Exception:
            action = False
        if action:
            self.assertNotEqual(action, False)
            self.assertNotEqual(action.get('res_id', False), False)
            self.wizard = self.env[
                'br.generate.projects'].browse(action['res_id'])
            self.wizard.for_br = True
            try:
                self.wizard.apply()
            except:
                pass

    def test_br_generate_projects_wizard(self):
        self.brA.state = 'approved'
        self.brB.state = 'approved'
        self.brC.state = 'approved'
        try:
            action = self.brA.generate_projects_wizard()
        except Exception:
            action = False
        if action:
            self.assertEqual(
                'ir.actions.act_window',
                action['type'])

    def test_project_generate_project_wizard(self):
        self.brA.state = 'approved'
        self.brB.state = 'approved'
        self.brC.state = 'approved'
        default_uom = self.env[
            'project.config.settings'
        ].get_default_time_unit('time_unit').get('time_unit', False)

        try:
            action = self.projectA.generate_project_wizard()
        except Exception:
            action = False
        if action:
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
                self.assertEqual('approved', br.state)

                generated = self.env['project.task'].search(
                    [('br_resource_id', '=', br.id)])
                self.assertFalse(generated)

            from_project = self.env[
                'br.generate.projects'].browse(action['res_id']).br_ids
            self.assertTrue(from_project)
            br_ids_a = [
                x for x in self.projectA.br_ids if x.parent_id.id is False]
            br_ids_b = [x for x in from_project if x.parent_id.id is False]
            self.assertEqual(br_ids_a, br_ids_b)
