# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common
from openerp.exceptions import Warning as UserError


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

        vals = {
            'description': ' test',
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
                                'user_id': self.user.id,
                            }),
                            (0, 0, {
                                'name': 'Resource Line1',
                                'product_id': self.productC.id,
                                'qty': 100,
                                'uom_id': self.uom_hours.id,
                                'resource_type': 'task',
                                'user_id': self.user.id,
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
        self.br = self.env['business.requirement'].create(vals)

    def test_get_cost_total(self):
        cost_total = self.br.total_revenue
        self.assertEqual(
            cost_total, 900.0 * 1 + 1100.0 * 1 + 1300.0 * 1 + 1500.0 * 1)

    def test_compute_get_price_total(self):
        for line in self.br.deliverable_lines:
            if line.name == 'deliverable line1':
                self.assertEqual(line.price_total, 900.0 * 1)
            elif line.name == 'deliverable line2':
                self.assertEqual(line.price_total, 1100.0 * 1)
            elif line.name == 'deliverable line3':
                self.assertEqual(line.price_total, 1300.0 * 1)
            elif line.name == 'deliverable line4':
                self.assertEqual(line.price_total, 1500.0 * 1)

    def test_resource_uom_change(self):
        for line in self.br.deliverable_lines:
            for resource in line.resource_ids:
                if resource and resource.resource_type == 'task':
                    try:
                        res = resource.write({'uom_id': self.uom_kg.id})
                    except:
                        res = False
                    self.assertEqual(res, False)
                    break

    def test_resource_product_id_change(self):
        resource = self.env['business.requirement.resource'].search([
            ('product_id', '=', self.productA.id)])[0]

        resource.write({'product_id': self.productB.id})
        resource.product_id_change()

        self.assertEqual(
            resource.name, self.productB.name)
        self.assertEqual(
            resource.product_id.id, self.productB.id)
        self.assertEqual(
            resource.uom_id.id, self.productB.uom_id.id)

    def test_compute_get_currency(self):
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        self.br._compute_get_currency()
        partner_id = self.br.partner_id
        currency_id = partner_id.property_product_pricelist.currency_id
        self.assertEqual(
            self.br.currency_id, currency_id)

    def test_deliverable_compute_get_currency(self):
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        partner_id = self.br.partner_id
        currency_id = partner_id.property_product_pricelist.currency_id
        for line in self.br.deliverable_lines:
            line._compute_get_currency()
            self.assertEqual(line.currency_id, currency_id)

    def test_resource_type_change(self):
        for line in self.br.deliverable_lines:
            for resource in line.resource_ids:
                if resource and resource.resource_type == 'task':
                    resource.write({'resource_type': 'procurement'})
                    resource.resource_type_change()
                    self.assertEqual(resource.user_id.id, False)

    def test_get_pricelist(self):
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        for line in self.br.deliverable_lines:
            price_list = line._get_pricelist()
            self.assertEqual(
                price_list.id,
                self.partner.property_product_pricelist.id)

    def test_product_id_change(self):
        for line in self.br.deliverable_lines:
            line.write({'product_id': self.productA.id})
            description = ''
            unit_price = 0
            product = self.productA

            if product:
                description = product.name_get()[0][1]
                unit_price = product.list_price

            if product.description_sale:
                description += '\n' + product.description_sale

            unit_price = line.product_id.list_price
            pricelist = line._get_pricelist()

            if pricelist:
                product = line.product_id.with_context(
                    lang=line.business_requirement_id.partner_id.lang,
                    partner=line.business_requirement_id.partner_id.id,
                    quantity=line.qty,
                    pricelist=pricelist.id,
                    uom=line.uom_id.id,
                )
                unit_price = product.price

            if pricelist:
                product = line.product_id.with_context(
                    lang=line.business_requirement_id.partner_id.lang,
                    partner=line.business_requirement_id.partner_id.id,
                    quantity=line.qty,
                    pricelist=pricelist.id,
                    uom=line.uom_id.id,
                )
                unit_price = product.price

            line.product_id_change()
            self.assertEqual(line.name, description)
            self.assertEqual(line.uom_id.id, self.productA.uom_id.id)
            self.assertEqual(line.unit_price, unit_price)

    def test_product_uom_change(self):
        self.uom_id = self.env['product.uom'].search([('id', '=', 2)])
        for line in self.br.deliverable_lines:
            line.write({'product_id': self.productA.id})
            line.product_id_change()
            line.write({'product_id': self.uom_id.id})
            self.unit_price = line.unit_price
            line.product_uom_change()
            self.assertTrue(line.unit_price > self.unit_price)

    def test_partner_id_change(self):
        self.partner = self.env['res.partner'].create({
            'name': 'Your company test',
            'email': 'your.company@your-company.com',
            'customer': True,
        })
        self.br.write({'partner_id': self.partner.id})
        try:
            self.br.partner_id_change()
        except UserError, e:
            self.assertEqual(type(e), UserError)
