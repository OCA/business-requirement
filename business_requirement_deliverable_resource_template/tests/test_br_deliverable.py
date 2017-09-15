# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class BusinessRequirementDeliverable(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementDeliverable, self).setUp()
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
        vals = {
            'description': ' test',
            'deliverable_lines': [
                (0, 0, {'name': 'deliverable line1', 'qty': 1.0,
                        'product_id': self.ProductS.id,
                        'sale_price_unit': 900, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line2', 'qty': 1.0,
                        'sale_price_unit': 1100, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line3', 'qty': 1.0,
                        'sale_price_unit': 1300, 'uom_id': 1}),
                (0, 0, {'name': 'deliverable line4', 'qty': 1.0,
                        'sale_price_unit': 1500, 'uom_id': 1,
                        }),
            ]
        }
        self.br = self.env['business.requirement'].create(vals)
        self.BRTemplate = self.env['business.requirement.resource.template']

    def test_product_id_change(self):
        for dl in self.br.deliverable_lines:
            dl.product_id_change()

    def test_prepare_resource_lines(self):
        self.BRT = self.BRTemplate.create({
            'name': 'BR Template',
            'product_template_id': self.ProductS.product_tmpl_id.id,
            'uom_id': self.uom_hours.id,
            'resource_type': 'task'
        })
        for dl in self.br.deliverable_lines:
            dl._prepare_resource_lines()
