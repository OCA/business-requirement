# © 2017-2019 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from openerp.exceptions import ValidationError
from odoo import _


@common.at_install(False)
@common.post_install(True)
class BusinessRequirementTestCase(common.TransactionCase):
    def setUp(self):
        super(BusinessRequirementTestCase, self).setUp()

        # Configure unit of measure.
        self.categ_wtime = self.ref('product.uom_categ_wtime')
        self.categ_kgm = self.ref('product.product_uom_categ_kgm')
        self.partner1 = self.ref('base.res_partner_1')
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

        self.br = self.env['business.requirement']

        vals = {
            'description': 'test',
        }
        # Product Created A, B, C, D
        self.ProductObj = self.env['product.product']
        self.productA = self.ProductObj.create(
            {'name': 'Product A', 'uom_id': self.uom_hours.id,
             'uom_po_id': self.uom_hours.id,
             'standard_price': 450})
        self.productB = self.ProductObj. \
            create({'name': 'Product B', 'uom_id': self.uom_hours.id,
                    'uom_po_id': self.uom_hours.id,
                    'standard_price': 550})

        vals1 = vals.copy()
        vals2 = vals.copy()
        self.brA = self.br.create(vals)
        self.brB = self.br.create(vals1)
        self.brC = self.br.create(vals2)

    def test_message_post(self):
        self.brA.with_context({
            'default_model': 'business.requirement',
            'default_res_id': self.brA.id
        }).message_post(
            body=_('Test Body'),
            message_type='notification',
            subtype='mt_notification',
            parent_id=False,
            attachments=None,
            content_subtype='html',
            **{}
        )

    def test_get_default_company(self):
        self.brA._get_default_company()
        self.env.user.company_id = False
        with self.assertRaises(ValidationError):
            self.brA._get_default_company()

    def test_br_name_search(self):
        br_vals = {
            'name': ' test',
            'description': 'test',
        }
        self.br.create(br_vals)

        brs = self.br.name_search(name='test')
        self.assertEqual(bool(brs), True)

    def test_create_name_equal_slash(self):
        name = self.env['ir.sequence'].next_by_code('business.requirement')
        br_vals = {
            'name': '/',
            'description': 'test',
        }
        len_seq = name[2:]
        seq = "BR" + str(int(len_seq) + 1).zfill(int(len(len_seq)))
        res = self.br.create(br_vals)
        self.assertEqual(seq, res.name)

    def test_br_read_group(self):
        self.env['business.requirement'].read_group(
            [],
            ['state'], ['state'])[0]
        self.env['business.requirement'].read_group(
            [],
            [], [])[0]
