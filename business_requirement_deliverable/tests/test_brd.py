# Copyright 2017-2019 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.addons.business_requirement.tests.test_br import \
    BusinessRequirementTestBase
from openerp.exceptions import UserError


class BusinessRequirementDeliverableTest(BusinessRequirementTestBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_a = cls.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        cls.br.write({
            'partner_id': cls.partner_a.id,
            'deliverable_lines': [
                (0, 0, {'name': 'deliverable line1',
                        'user_case': 'mock case',
                        'proposed_solution': 'mock proposed_solution',
                        'qty': 1.0,
                        'sale_price_unit': 900, 'uom_id': 1,
                        'business_requirement_id': cls.br.id,
                        }),
                (0, 0, {'name': 'deliverable line2',
                        'user_case': 'mock case',
                        'proposed_solution': 'mock proposed_solution',
                        'qty': 1.0,
                        'sale_price_unit': 1100, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line3',
                        'user_case': 'mock case',
                        'proposed_solution': 'mock proposed_solution',
                        'qty': 1.0,
                        'sale_price_unit': 1300, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line4',
                        'user_case': 'mock case',
                        'proposed_solution': 'mock proposed_solution',
                        'qty': 1.0,
                        'sale_price_unit': 1500, 'uom_id': 1,
                        }),
            ]})
        cls.uom_hour_id = cls.env.ref('uom.product_uom_hour').id
        cls.uom_day_id = cls.env.ref('uom.product_uom_day').id
        # Product Created A, B
        cls.ProductObj = cls.env['product.product']
        cls.productA = cls.ProductObj.create({
            'name': 'Product A',
            'uom_id': cls.uom_hour_id,
            'uom_po_id': cls.uom_hour_id,
            'lst_price': 500,
            'standard_price': 450})
        cls.productB = cls.ProductObj.create({
            'name': 'Product B',
            'uom_id': cls.uom_hour_id,
            'uom_po_id': cls.uom_hour_id,
            'lst_price': 600,
            'standard_price': 550})

    def test_commercial_fields(self):
        self.assertTrue(
            'property_product_estimation_pricelist' in (
                self.br.partner_id._commercial_fields())
        )

    def test_get_cost_total(self):
        self.assertEqual(self.br.total_revenue, 4800.0)

    def test_compute_price_total(self):
        for line in self.br.deliverable_lines:
            if line.name == 'deliverable line1':
                self.assertEqual(line.price_total, 900.0)
            elif line.name == 'deliverable line2':
                self.assertEqual(line.price_total, 1100.0)
            elif line.name == 'deliverable line3':
                self.assertEqual(line.price_total, 1300.0)
            elif line.name == 'deliverable line4':
                self.assertEqual(line.price_total, 1500.0)

    def test_compute_business_requirement_dl_rl(self):
        self.assertEqual(self.br.dl_count, 4)

    def test_open_business_requirement_dl(self):
        self.return_action = self.br.open_deliverable_line()
        self.assertTrue(self.return_action['type'], 'ir.actions.act_window')

    def test_compute_dl_total_revenue(self):
        self.dl_total_revenue = sum(
            dl.price_total for dl in self.br.deliverable_lines)
        self.assertEqual(self.dl_total_revenue, 4800.0)

    def test_compute_currency_id(self):
        if not self.br.pricelist_id:
            self.assertEqual(
                self.br.currency_id, self.env.user.company_id.currency_id)
        self.pricelist_id = self.env.ref(
            'business_requirement_deliverable.brpricelist0').id
        self.br.write({'pricelist_id': self.pricelist_id})
        self.assertEqual(
            self.br.currency_id.name, 'HKD')

    def test_deliverable_compute_currency_id(self):
        if not self.br.pricelist_id:
            for line in self.br.deliverable_lines:
                line._compute_currency_id()
                self.assertEqual(line.currency_id,
                                 self.env.user.company_id.currency_id)
        self.pricelist_id = self.env.ref(
            'business_requirement_deliverable.brpricelist0').id
        self.br.write({'pricelist_id': self.pricelist_id})
        for line in self.br.deliverable_lines:
            line._compute_currency_id()
            self.assertEqual(line.currency_id.name, 'HKD')

    def test_product_id_change(self):
        for line in self.br.deliverable_lines:
            line.write({'product_id': self.productA.id, 'name': ''})
            description = ''
            sale_price_unit = 0
            product = self.productA

            if product:
                description = product.name_get()[0][1]
                sale_price_unit = product.list_price

            if product.description_sale:
                description += '\n' + product.description_sale

            sale_price_unit = line.product_id.list_price
            line.business_requirement_id.onchange_partner_id()

            if line.business_requirement_id.pricelist_id:
                product = line.product_id.with_context(
                    lang=line.business_requirement_id.partner_id.lang,
                    partner=line.business_requirement_id.partner_id.id,
                    quantity=line.qty,
                    pricelist=line.business_requirement_id.pricelist_id.id,
                    uom=line.uom_id.id,
                )
                sale_price_unit = product.price
            line.product_id_change()
            self.assertEqual(line.name, description)
            self.assertEqual(line.uom_id.id, self.productA.uom_id.id)
            self.assertEqual(line.sale_price_unit, sale_price_unit)

    def test_product_id_change_with_pricelist(self):
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        for line in self.br.deliverable_lines:
            line.write({'product_id': self.productA.id})
            description = ''
            product = self.productA
            if product:
                description = product.name_get()[0][1]
            if product.description_sale:
                description += '\n' + product.description_sale
            line.business_requirement_id.onchange_partner_id()
            line.product_id_change()
            self.assertEqual(line.uom_id.id, self.productA.uom_id.id)
            self.assertEqual(line.sale_price_unit, 500.0)

    def test_product_id_change_description_sale(self):
        self.productA.write({
            'description_sale': 'Sales Description Product A'})
        for line in self.br.deliverable_lines:
            if not line.name:
                line.write({'product_id': self.productA.id})
                line.product_id_change()
                self.assertTrue(
                    self.productA.description_sale in line.name)

    def test_product_uom_change(self):
        for line in self.br.deliverable_lines:
            line.write({'product_id': self.productA.id})
            line.product_id_change()
            line.write({'uom_id': self.uom_day_id})
            self.sale_price_unit = line.sale_price_unit
            line.product_uom_change()
            self.assertEqual(line.sale_price_unit, 4000.0)

    def test_partner_id_change(self):
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        with self.assertRaises(UserError):
            self.br.partner_id_change()
