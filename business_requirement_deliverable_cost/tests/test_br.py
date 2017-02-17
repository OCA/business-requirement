# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


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

    def test_compute_sale_price_total(self):
        """ Checks if the _compute_sale_price_total works properly
        """
        resource = self.env['business.requirement.resource'].search([
            ('name', '=', 'Resource Line1')])
        self.assertEqual(
            resource.sale_price_total, 40000)

    def test_product_id_change(self):
        """ Checks if the product_id_change works properly
        """
        resource = self.env['business.requirement.resource'].search([
            ('name', '=', 'Resource Line1')])
        resource.product_id_change()
        # should be ammend

        unit_price = 0
        unit_price = resource.product_id.standard_price
        pricelist_id = resource._get_pricelist()
        # partner_id = resource._get_partner()
        sale_price_unit = resource.product_id.list_price
        if pricelist_id and resource.partner_id and resource.uom_id:
            product = resource.product_id.with_context(
                lang=resource.partner_id.lang,
                # partner=resource.partner_id.id,
                quantity=resource.qty,
                pricelist=pricelist_id.id,
                uom=resource.uom_id.id,
            )
            sale_price_unit = product.list_price
            unit_price = product.standard_price

        self.assertEqual(
            resource.unit_price, unit_price)
        self.assertEqual(
            resource.sale_price_unit, sale_price_unit)

    def test_compute_resource_task_total(self):
        """ Checks if the _compute_resource_task_total works properly
        """
        self.assertEqual(
            self.br.resource_task_total, 100000.0)

    def test_compute_resource_procurement_total(self):
        """ Checks if the _compute_resource_procurement_total works properly
        """
        self.assertEqual(
            self.br.resource_procurement_total, 50000.0)

    def test_compute_gross_profit(self):
        """ Checks if the _compute_gross_profit works properly
        """
        self.assertEqual(
            self.br.gross_profit, -145200.00)

    def test_compute_get_price_total(self):
        resource = self.env['business.requirement.resource'].search([
            ('name', '=', 'Resource Line1')])
        price_total = resource.unit_price * resource.qty
        resource._compute_get_price_total()
        self.assertEqual(
            resource.price_total, price_total)

    def test_product_uom_change(self):
        resource = self.env['business.requirement.resource'].search([
            ('name', '=', 'Resource Line1')])
        resource.product_uom_change()
        qty_uom = 0
        unit_price = resource.unit_price
        sale_price_unit = resource.product_id.list_price
        pricelist = resource._get_pricelist()
        # partner_id = resource._get_partner()
        product_uom = resource.env['product.uom']

        if resource.qty != 0:
            qty_uom = product_uom._compute_qty(
                resource.uom_id.id,
                resource.qty,
                resource.product_id.uom_id.id
            ) / resource.qty

        if pricelist:
            product = resource.product_id.with_context(
                lang=resource.partner_id.lang,
                partner=resource.partner_id.id,
                quantity=resource.qty,
                pricelist=pricelist.id,
                uom=resource.uom_id.id,
            )
            unit_price = product.standard_price
            sale_price_unit = product.list_price

        self.unit_price = unit_price * qty_uom
        self.sale_price_unit = sale_price_unit * qty_uom

        self.assertEqual(
            resource.unit_price, self.unit_price)
        self.assertEqual(
            resource.sale_price_unit, self.sale_price_unit)

    def test_action_button_update_estimation(self):
        deliverable = self.br.deliverable_lines[0]
        deliverable.action_button_update_estimation()
        if deliverable.resource_ids:
            for resource in deliverable.resource_ids:
                pricelist_id = resource._get_pricelist()
                sale_price_unit = resource.product_id.lst_price
                if pricelist_id and resource.partner_id and resource.uom_id:
                    product = resource.product_id.with_context(
                        lang=resource.partner_id.lang,
                        partner=resource.partner_id.id,
                        quantity=resource.qty,
                        pricelist=pricelist_id.id,
                        uom=resource.uom_id.id,
                    )
                    sale_price_unit = product.price

                self.assertEqual(
                    resource.sale_price_unit, sale_price_unit)
