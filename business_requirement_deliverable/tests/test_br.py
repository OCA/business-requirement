# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo.exceptions import UserError


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
                'uom_po_id': self.uom_hours.id})
        self.productB = self.ProductObj.create(
            {'name': 'Product B', 'uom_id': self.uom_hours.id,
                'uom_po_id': self.uom_hours.id})
        self.productC = self.ProductObj.create(
            {'name': 'Product C', 'uom_id': self.uom_days.id,
                'uom_po_id': self.uom_days.id})
        self.productD = self.ProductObj.create(
            {'name': 'Product D', 'uom_id': self.uom_kg.id,
                'uom_po_id': self.uom_kg.id})

        self.user = self.env['res.users'].sudo().create({
            'name': 'Your user test',
            'login': 'your.user@your-user.com'
        })
        self.currency_usd_id = self.env.ref("base.USD")
        self.currency_eur_id = self.env.ref("base.EUR")

        self.pricelist_id = self.env['product.pricelist'].create({
            'name': 'United States',
            'sequence': 10,
            'currency_id': self.currency_eur_id.id
        })
        self.partner1 = self.env.ref('base.res_partner_1')
        vals = {
            'description': ' test',
            'partner_id': self.partner1.id,
            'pricelist_id': self.pricelist_id.id
        }
        self.br = self.env['business.requirement'].create(vals)
        self.br.write({
            'deliverable_lines': [
                (0, 0, {'name': 'deliverable line1',
                        'user_case': 'mock case',
                        'proposed_solution': 'mock proposed_solution',
                        'qty': 1.0,
                        'sale_price_unit': 900, 'uom_id': 1,
                        'business_requirement_id': self.br.id,
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

    def test_commercial_fields(self):
        self.br.partner_id._commercial_fields()

    def test_get_cost_total(self):
        cost_total = self.br.total_revenue
        total_cost = 900.0 * 1 + 1100.0 * 1 + 1300.0 * 1 + 1500.0 * 1
        self.assertEqual(cost_total, total_cost)

    def test_compute_price_total(self):
        for line in self.br.deliverable_lines:
            if line.name == 'deliverable line1':
                self.assertEqual(line.price_total, 900.0 * 1)
            elif line.name == 'deliverable line2':
                self.assertEqual(line.price_total, 1100.0 * 1)
            elif line.name == 'deliverable line3':
                self.assertEqual(line.price_total, 1300.0 * 1)
            elif line.name == 'deliverable line4':
                self.assertEqual(line.price_total, 1500.0 * 1)

    def test_compute_business_requirement_dl_rl(self):
        self.br._compute_dl_count()

    def test_open_business_requirement_dl(self):
        self.br.open_deliverable_line()

    def test_compute_dl_total_revenue(self):
        for r in self.br:
            dl_total_revenue = sum(dl.price_total for dl in
                                   r.deliverable_lines)
        self.assertEqual(dl_total_revenue, r.dl_total_revenue)

    def test_compute_currency_id(self):
        self.br.partner_id = False
        self.br._compute_currency_id()
        if not self.br.partner_id:
            self.br.deliverable_lines[0]._compute_currency_id()
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        self.br._compute_currency_id()
        currency_id = self.pricelist_id.currency_id
        self.assertEqual(
            self.br.currency_id, currency_id)

    def test_deliverable_compute_currency_id(self):
        if not self.br.partner_id:
            self.br.deliverable_lines[0]._compute_currency_id()
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        currency_id = self.br.pricelist_id.currency_id
        for line in self.br.deliverable_lines:
            line._compute_currency_id()
            self.assertEqual(line.currency_id, currency_id)

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

            if line.business_requirement_id and \
                    line.business_requirement_id.pricelist_id:
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
            sale_price_unit = 0
            product = self.productA

            if product:
                description = product.name_get()[0][1]
                sale_price_unit = product.list_price

            if product.description_sale:
                description += '\n' + product.description_sale

            sale_price_unit = line.product_id.list_price

            line.business_requirement_id.onchange_partner_id()

            if line.business_requirement_id and \
                    line.business_requirement_id.pricelist_id:
                product = line.product_id.with_context(
                    lang=line.business_requirement_id.partner_id.lang,
                    partner=line.business_requirement_id.partner_id.id,
                    quantity=line.qty,
                    pricelist=line.business_requirement_id.pricelist_id.id,
                    uom=line.uom_id.id,
                )
                sale_price_unit = product.price

            line.product_id_change()
            self.assertEqual(line.uom_id.id, self.productA.uom_id.id)
            self.assertEqual(line.sale_price_unit, sale_price_unit)

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
            line.write({'uom_id': self.uom_days.id})
            self.sale_price_unit = line.sale_price_unit
            line.product_uom_change()
            product = self.productA.with_context(
                lang=self.br.partner_id.lang,
                partner=self.br.partner_id.id,
                quantity=line.qty,
                pricelist=line.business_requirement_id.pricelist_id.id,
                uom=line.uom_id.id,
            )
            self.assertEqual(line.sale_price_unit, product.price)

    def test_partner_id_change(self):
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        with self.assertRaises(UserError):
            self.br.partner_id_change()
