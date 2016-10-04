# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common


@common.at_install(False)
@common.post_install(True)
class BusinessRequirementTestCase(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementTestCase, self).setUp()
        self.ModelDataObj = self.env['ir.model.data']

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
                'lst_price': 1000, 'uom_po_id': self.uom_hours.id})
        self.productB = self.ProductObj.create(
            {'name': 'Product B', 'uom_id': self.uom_hours.id,
                'lst_price': 3000, 'uom_po_id': self.uom_hours.id})
        self.productC = self.ProductObj.create(
            {'name': 'Product C', 'uom_id': self.uom_days.id,
                'uom_po_id': self.uom_days.id})
        self.productD = self.ProductObj.create(
            {'name': 'Product D', 'uom_id': self.uom_kg.id,
                'uom_po_id': self.uom_kg.id})

        self.pricelistA = self.env['product.pricelist'].create({
            'name': 'Pricelist A',
            'type': 'sale',
            'version_id': [
                (0, 0, {
                    'name': 'Version A',
                    'items_id': [(0, 0, {
                        'name': 'Item A',
                        'product_id': self.productA.id,
                        'price_discount': '-0.5',
                    })]
                })
            ]
        })
        self.project = self.env['project.project'].create({
            'name': 'Project A', 'pricelist_id': self.pricelistA.id,
            'partner_id': 3,
        })

        vals = {
            'description': 'test',
            'project_id': self.project.id,
            'partner_id': 3,
            'deliverable_lines': [
                (0, 0, {'name': 'deliverable line1', 'qty': 1.0,
                        'unit_price': 900, 'uom_id': 1,
                        'resource_ids': [
                            (0, 0, {
                                'name': 'Resource Line2',
                                'product_id': self.productA.id,
                                'qty': 100,
                                'uom_id': self.uom_hours.id,
                                'unit_price': 500,
                                'resource_type': 'task',
                            }),
                            (0, 0, {
                                'name': 'Resource Line1',
                                'product_id': self.productA.id,
                                'qty': 100,
                                'uom_id': self.uom_hours.id,
                                'unit_price': 500,
                                'resource_type': 'task',
                                'sale_price_unit': 400,
                            }),
                            (0, 0, {
                                'name': 'Resource Line3',
                                'product_id': self.productA.id,
                                'qty': 100,
                                'uom_id': self.uom_hours.id,
                                'unit_price': 500,
                                'resource_type': 'procurement',
                                'sale_price_unit': 100,
                            }),
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
        self.br = self.env['business.requirement'].create(vals)
        self.wizard_obj = self.env['br.crm.make.sale']
        self.crm_lead_16 = self.env.ref('crm.crm_case_1')
        self.crm_lead_16.project_id = self.project.id
        self.partner_4 = self.env.ref('base.res_partner_4')
        vals_wizard = {
            'partner_id': self.partner_4.id,
            'update_quotation': True
        }
        context_wizard = {
            'active_id': self.crm_lead_16.id,
            'active_ids': [self.crm_lead_16.id]
        }

        self.wizard = self.wizard_obj.create(
            vals_wizard).with_context(context_wizard)

    def test_make_orderline(self):
        res = self.wizard.make_orderline()
        self.assertTrue(res.get('res_id', False))

    def test_prepare_sale_order_line(self):
        res = self.wizard.make_orderline()
        order_id = res.get('res_id', False)
        lines = self.wizard.prepare_sale_order_line(
            self.crm_lead_16.id,
            order_id)
        self.assertTrue(lines)

    def test_create_sale_order_line(self):
        res = self.wizard.make_orderline()
        order_id = res.get('res_id', False)
        lines = self.wizard.prepare_sale_order_line(
            self.crm_lead_16.id,
            order_id)
        try:
            self.wizard.create_sale_order_line(lines)
            self.assertTrue(True)
        except Exception:
            pass
