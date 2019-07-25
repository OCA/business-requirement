# Copyright 2017-2019 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common
from odoo import _


class BusinessRequirementTestBase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # This is for reducing the diff coming from TransactionCase
        self = cls
        # Configure.
        self.BR = self.env['business.requirement']
        self.br = self.BR.create({
            'description': 'test',
        })


class BusinessRequirementTest(BusinessRequirementTestBase):

    def test_message_post(self):
        self.message = self.br.with_context({
            'default_model': 'business.requirement',
            'default_res_id': self.br.id,
        }).message_post(
            body=_('Test Body'),
            message_type='notification',
            subtype='mt_notification',
            **{}
        )
        self.assertEqual(
            self.message.subject, 'Re: {}-test'.format(self.br.name))

    def test_get_default_company(self):
        self.assertEqual(self.br._get_default_company(), 1)

    def test_br_name_search(self):
        br_vals = {
            'name': ' test',
            'description': 'test',
        }
        self.br.create(br_vals)
        self.assertTrue(self.br.name_search(name='test'))

    def test_create_name_sequence(self):
        name = self.env['ir.sequence'].next_by_code('business.requirement')
        br_vals = {
            'name': '/',
            'description': 'test',
        }
        len_seq = name[2:]
        seq = "BR" + str(int(len_seq) + 1).zfill(int(len(len_seq)))
        res = self.BR.create(br_vals)
        self.assertEqual(seq, res.name)

    def test_br_read_group(self):
        self.read_group = self.env['business.requirement'].read_group(
            [],
            ['state'], ['state'])[0]
        self.assertTrue(self.read_group['state'])
        self.assertTrue(self.read_group['state_count'])

    def test_get_portal_confirmation_action(self):
        self.portal_confirmation_action = \
            self.br.get_portal_confirmation_action()
        self.assertEqual(self.portal_confirmation_action, 'none')

    def test_compute_access_url(self):
        self.assertEqual(
            self.br.access_url ,
            '/my/business_requirement/{}'.format(self.br.id))

    def test_portal_publish_button(self):
        self.assertFalse(self.br.portal_published)
