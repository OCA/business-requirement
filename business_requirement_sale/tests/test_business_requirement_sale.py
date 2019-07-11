# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestBusinessRequirementSale(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.br_model = cls.env['business.requirement']
        cls.brd_model = cls.env['business.requirement.deliverable']
        cls.brds_model = cls.env['business.requirement.deliverable.section']
        cls.product_model = cls.env['product.product']
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test BR partner',
        })
        cls.business_requirement = cls.br_model.create({
            'name': 'Test BR',
            'description': 'Test BR',
            'partner_id': cls.partner.id,
        })
        cls.product1 = cls.product_model.create({
            'name': 'Test product BR 1',
        })
        cls.product2 = cls.product_model.create({
            'name': 'Test product BR 2',
        })
        cls.section = cls.brds_model.create({
            'name': 'Test BRD section',
        })
        cls.deliverable1 = cls.brd_model.create({
            'name': 'Test deliverable 1',
            'business_requirement_id': cls.business_requirement.id,
            'product_id': cls.product1.id,
            'section_id': cls.section.id,
            'sale_price_unit': 80,
            'qty': 3,
        })
        cls.deliverable2 = cls.brd_model.create({
            'name': 'Test deliverable 2',
            'business_requirement_id': cls.business_requirement.id,
            'product_id': cls.product2.id,
            'sale_price_unit': 20,
            'qty': 5,
        })
        cls.wizard = cls.env['business.requirement.create.sale'].with_context(
            active_model=cls.br_model._name,
            active_id=cls.business_requirement.id,
        ).create({})

    def test_full_flow(self):
        action = self.wizard.button_create()
        # Sales order
        self.assertTrue(action['res_id'])
        order = self.env['sale.order'].browse(action['res_id'])
        self.assertEqual(order.partner_id, self.partner)
        self.assertEqual(len(order.order_line), 2)
        self.assertEqual(self.business_requirement.sale_order_count, 1)
        self.assertEqual(
            order.business_requirement_id, self.business_requirement,
        )
        action = self.business_requirement.open_orders()
        self.assertTrue(
            action['context']['search_default_business_requirement_id'],
        )
        br2 = self.business_requirement.copy()
        action = (self.business_requirement + br2).open_orders()
        self.assertTrue(action['domain'])
        # Line 1
        line1 = order.order_line.filtered(
            lambda x: x.product_id == self.product1)
        self.assertTrue(line1)
        self.assertAlmostEqual(line1.product_uom_qty, 1)
        self.assertAlmostEqual(line1.price_unit, 240)
        self.assertEqual(
            line1.business_requirement_deliverable_id, self.deliverable1,
        )
        # Section
        self.assertTrue(self.section.sale_layout_category_id)
        self.assertTrue(
            self.section.sale_layout_category_id.name, self.section.name,
        )
        self.assertTrue(line1.layout_category_id)
        # Line 2
        line2 = order.order_line.filtered(
            lambda x: x.product_id == self.product2)
        self.assertTrue(line2)
        self.assertAlmostEqual(line2.product_uom_qty, 1)
        self.assertAlmostEqual(line2.price_unit, 100)
        self.assertFalse(line2.layout_category_id)
        self.assertEqual(
            line2.business_requirement_deliverable_id, self.deliverable2,
        )

    def test_flow_one_line_non_totaled(self):
        self.wizard.deliverable_ids = [(6, 0, self.deliverable1.ids)]
        self.wizard.totaled_method = 'standard'
        action = self.wizard.button_create()
        self.assertTrue(action['res_id'])
        order = self.env['sale.order'].browse(action['res_id'])
        self.assertEqual(len(order.order_line), 1)
        self.assertAlmostEqual(order.order_line.product_uom_qty, 3)
        self.assertAlmostEqual(order.order_line.price_unit, 80)
