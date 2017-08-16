# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo.exceptions import ValidationError


class BusinessRequirementResourceTemplate(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementResourceTemplate, self).setUp()
        self.categ_wtime = self.env.ref('product.uom_categ_wtime')
        self.categ_kgm = self.env.ref('product.product_uom_categ_kgm')

        self.UomObj = self.env['product.uom']
        self.uom_hours = self.UomObj.create({
            'name': 'Test-Hours',
            'category_id': self.categ_wtime.id,
            'factor': 8,
            'uom_type': 'smaller'})
        self.uom_kg = self.UomObj.create({
            'name': 'Test-KG',
            'category_id': self.categ_kgm.id,
            'factor_inv': 1,
            'factor': 1,
            'uom_type': 'reference',
            'rounding': 0.000001})
        self.ProductS = self.env.ref('product.service_order_01')
        self.ProductObj = self.env['product.template']
        self.productA = self.ProductObj.create({
            'name': 'Product A',
            'resource_lines': [
                (0, 0, {
                    'name': 'Resource Line1',
                    'product_id': self.ProductS.id,
                    'qty': 100,
                    'uom_id': self.uom_hours.id,
                    'resource_type': 'task'
                })]})

    def test_product_id_change(self):
        for resource in self.productA.resource_lines:
            resource.product_id_change()
            description = self.ProductS.name_get()[0][1]
            self.assertEqual(resource.name, description)

    def test_resource_uom_change(self):
        for line in self.productA:
            for resource in line.resource_lines:
                if resource and resource.resource_type == 'task':
                    with self.assertRaises(ValidationError):
                        resource.write({'uom_id': self.uom_kg.id})
