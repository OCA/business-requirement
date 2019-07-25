# Copyright 2019 Tecnativa - Victor M.M. Torres
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestBusinessRequirementCrm(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.br_model = cls.env['business.requirement']
        cls.lead_model = cls.env['crm.lead']
        cls.lead = cls.lead_model.create({
            'name': 'Test lead',
            'description': 'Investigate and estimate',
        })
        cls.wizard = cls.env['crm.lead.create.requirement'].with_context(
            active_model=cls.lead_model._name,
            active_id=cls.lead.id,
        ).create({})

    def test_action_lead_to_business_requirement(self):
        self.wizard.action_lead_to_business_requirement()
        # default_get
        self.assertEqual(self.wizard.lead_id, self.lead)
        # new br created
        self.assertTrue(self.lead.business_requirement_ids)
        # count on lead of br linked
        self.assertEqual(self.lead.business_requirement_count, 1)
        # br data
        br = self.lead.business_requirement_ids
        self.assertEqual(br.description, 'Test lead')
        self.assertEqual(
            br.business_requirement, '<p>Investigate and estimate</p>',
        )
        self.assertEqual(br.user_id, self.env.user)
