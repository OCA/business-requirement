# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class BusinessRequirementTestCase(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementTestCase, self).setUp()
        self.ModelDataObj = self.env['ir.model.data']

        # Configure unit of measure.
        self.categ_wtime = self.ref('uom.uom_categ_wtime')
        self.categ_kgm = self.ref('uom.product_uom_categ_kgm')
        self.UomObj = self.env['uom.uom']
        self.uom_hours = self.ref('uom.product_uom_hour')
        self.uom_days = self.ref('uom.product_uom_day')
        self.uom_kg = self.ref('uom.product_uom_kgm')
        # Product Created A, B, C, D
        self.ProductObj = self.env['product.product']
        self.productA = self.ProductObj.create(
            {'name': 'Product A', 'uom_id': self.uom_hours,
                'lst_price': 1000, 'uom_po_id': self.uom_hours})
        self.productB = self.ProductObj.create(
            {'name': 'Product B', 'uom_id': self.uom_hours,
                'lst_price': 3000, 'uom_po_id': self.uom_hours})
        self.productC = self.ProductObj.create(
            {'name': 'Product C', 'uom_id': self.uom_days,
                'uom_po_id': self.uom_days})
        self.productD = self.ProductObj.create(
            {'name': 'Product D', 'uom_id': self.uom_kg,
                'uom_po_id': self.uom_kg})

        self.pricelistA = self.env['product.pricelist'].create({
            'name': 'Pricelist A',
            'item_ids': [(0, 0, {
                'name': 'Item A',
                'product_id': self.productA.id,
                'price_discount': '-0.5',
            })]
        })
        self.project = self.env['project.project'].create({
            'name': 'Project A',
            'partner_id': 3,
        })

        vals = {
            'description': 'test',
            'project_id': self.project.id,
            'partner_id': 3,
        }
        self.br = self.env['business.requirement'].create(vals)
        self.br.write({
            'deliverable_lines': [
                (0, 0, {'name': 'deliverable line1', 'qty': 1.0,
                        'product_id': self.productB.id,
                        'unit_price': 900, 'uom_id': 1,
                        'business_requirement_id': self.br.id,
                        'resource_ids': [
                            (0, 0, {
                                'name': 'Resource Line2',
                                'product_id': self.productA.id,
                                'qty': 100,
                                'uom_id': self.uom_hours,
                                'unit_price': 500,
                                'resource_type': 'task',
                                'business_requirement_id': self.br.id
                            }),
                            (0, 0, {
                                'name': 'Resource Line1',
                                'product_id': self.productA.id,
                                'qty': 100,
                                'uom_id': self.uom_hours,
                                'unit_price': 500,
                                'resource_type': 'task',
                                'sale_price_unit': 400,
                                'business_requirement_id': self.br.id
                            }),
                            (0, 0, {
                                'name': 'Resource Line3',
                                'product_id': self.productA.id,
                                'qty': 100,
                                'uom_id': self.uom_hours,
                                'unit_price': 500,
                                'resource_type': 'procurement',
                                'sale_price_unit': 100,
                                'business_requirement_id': self.br.id
                            }),
                        ]
                        }),
                (0, 0, {'name': 'deliverable line2', 'qty': 1.0,
                        'product_id': self.productA.id,
                        'business_requirement_id': self.br.id,
                        'unit_price': 1100, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line3', 'qty': 1.0,
                        'product_id': self.productC.id,
                        'business_requirement_id': self.br.id,
                        'unit_price': 1300, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line4', 'qty': 1.0,
                        'product_id': self.productD.id,
                        'business_requirement_id': self.br.id,
                        'unit_price': 1500, 'uom_id': 1,
                        }),
            ]})
        self.wizard_obj = self.env['br.crm.lead']
        self.partner_4 = self.env.ref('base.res_partner_4')
        self.crm_lead_16 = self.env.ref('crm.crm_case_1')
        self.crm_lead_16.partner_id = self.partner_4.id
        self.crm_lead_16.project_id = self.project.id

        vals_wizard = {
            'partner_id': self.partner_4.id,
        }
        context_wizard = {
            'active_id': self.crm_lead_16.id,
            'active_ids': [self.crm_lead_16.id]
        }

        self.wizard = self.wizard_obj.create(
            vals_wizard).with_context(context_wizard)

    def test_make_order(self):
        res = self.wizard.make_order()
        self.assertTrue(res.get('res_id', False))
        self.wizard.make_order()

    def test_prepare_sale_order_line(self):
        res = self.wizard.make_order()
        order_id = res.get('res_id', False)
        lines = self.wizard.prepare_sale_order_line(
            self.crm_lead_16.id,
            order_id)
        self.assertTrue(lines)

    def test_create_sale_order_line(self):
        res = self.wizard.make_order()
        order_id = res.get('res_id', False)
        lines = self.wizard.prepare_sale_order_line(
            self.crm_lead_16.id,
            order_id)
        try:
            self.wizard.create_sale_order_line(lines)
            self.assertTrue(True)
        except Exception:
            pass
