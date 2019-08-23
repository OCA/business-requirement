# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo import exceptions


class TestBusinessRequirementSaleBase(common.SavepointCase):
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
        cls.brd_section1 = cls.brds_model.create({
            'name': 'Test BRD section 1',
            'sequence': 20,
        })
        cls.brd_section2 = cls.brds_model.create({
            'name': 'Test BRD section 2',
            'sequence': 10,  # lower sequence on purpose for checking order
        })
        cls.deliverable1 = cls.brd_model.create({
            'name': 'Test deliverable 1',
            'business_requirement_id': cls.business_requirement.id,
            'product_id': cls.product1.id,
            'section_id': cls.brd_section1.id,
            'sale_price_unit': 80,
            'qty': 3,
        })
        cls.deliverable2 = cls.brd_model.create({
            'name': 'Test deliverable 2',
            'business_requirement_id': cls.business_requirement.id,
            'product_id': cls.product2.id,
            'section_id': cls.brd_section2.id,
            'sale_price_unit': 20,
            'qty': 5,
        })
        cls.deliverable3 = cls.brd_model.create({
            'name': 'Test deliverable 3',
            'business_requirement_id': cls.business_requirement.id,
            'product_id': cls.product2.id,
            'sale_price_unit': 2,
            'qty': 3,
        })
        cls.wizard = cls.env['business.requirement.create.sale'].with_context(
            active_model=cls.br_model._name,
            active_id=cls.business_requirement.id,
        ).create({})


class TestBusinessRequirementSale(TestBusinessRequirementSaleBase):
    def test_no_deliverables_selected(self):
        with self.assertRaises(exceptions.UserError):
            self.wizard.button_create()

    def test_full_flow(self):
        self.assertEqual(
            self.wizard.business_requirement_id, self.business_requirement,
        )
        self.assertTrue(self.wizard.has_undefined_section)
        self.assertEqual(len(self.wizard.applicable_section_ids), 2)
        self.assertFalse(self.wizard.deliverable_ids)
        self.wizard.section_ids = self.wizard.applicable_section_ids
        self.wizard._onchange_section_ids()
        self.assertEqual(len(self.wizard.deliverable_ids), 2)
        self.wizard.undefined_section = True
        self.wizard._onchange_undefined_section()
        self.assertEqual(len(self.wizard.deliverable_ids), 3)
        self.assertTrue(self.wizard.has_undefined_section)
        action = self.wizard.button_create()
        # Sales order
        self.assertTrue(action['res_id'])
        order = self.env['sale.order'].browse(action['res_id'])
        self.assertEqual(order.partner_id, self.partner)
        self.assertEqual(len(order.order_line), 5)
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
        so_mapping = {
            # index: (deliverable id, name, display_type,
            #         section id, product_uom_qty, price_unit, product id)
            0: (self.deliverable3.id, 'Test deliverable 3', False,
                False, 1, 6, self.product2.id),
            1: (False, 'Test BRD section 2', 'line_section',
                self.brd_section2.id, 0, 0, False),
            2: (self.deliverable2.id, 'Test deliverable 2', False,
                False, 1, 100, self.product2.id),
            3: (False, 'Test BRD section 1', 'line_section',
                self.brd_section1.id, 0, 0, False),
            4: (self.deliverable1.id, 'Test deliverable 1', False,
                False, 1, 240, self.product1.id),
        }
        for index in so_mapping:
            line = order.order_line[index]
            self.assertEqual(
                line.business_requirement_deliverable_id.id,
                so_mapping[index][0],
            )
            self.assertEqual(line.name, so_mapping[index][1])
            self.assertEqual(line.display_type, so_mapping[index][2])
            self.assertEqual(
                line.br_deliverable_section_id.id, so_mapping[index][3],
            )
            self.assertAlmostEqual(line.product_uom_qty, so_mapping[index][4])
            self.assertAlmostEqual(line.price_unit, so_mapping[index][5])
            self.assertEqual(line.product_id.id, so_mapping[index][6])

    def test_flow_one_line_non_totaled(self):
        self.wizard.deliverable_ids = [(6, 0, self.deliverable1.ids)]
        self.wizard.totaled_method = 'standard'
        action = self.wizard.button_create()
        self.assertTrue(action['res_id'])
        order = self.env['sale.order'].browse(action['res_id'])
        self.assertEqual(len(order.order_line), 2)
        self.assertAlmostEqual(
            order.order_line.filtered('product_id').product_uom_qty, 3)
        self.assertAlmostEqual(
            order.order_line.filtered('product_id').price_unit, 80)

    def test_no_deliverables_in_br(self):
        br = self.br_model.create({
            'name': 'Test BR no deliverables',
            'description': 'Test BR',
            'partner_id': self.partner.id,
        })
        with self.assertRaises(exceptions.UserError):
            self.env['business.requirement.create.sale'].with_context(
                active_model=br._name, active_id=br.id,
            ).create({})
