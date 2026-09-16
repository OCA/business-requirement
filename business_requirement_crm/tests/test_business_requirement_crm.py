# Copyright 2019 Tecnativa - Victor M.M. Torres
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestBusinessRequirementCrm(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.br_model = cls.env["business.requirement"]
        cls.lead_model = cls.env["crm.lead"]
        cls.lead = cls.lead_model.create(
            {"name": "Test lead", "description": "Investigate and estimate"}
        )
        cls.wizard = (
            cls.env["crm.lead.create.requirement"]
            .with_context(active_model=cls.lead_model._name, active_id=cls.lead.id)
            .create({})
        )

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
        self.assertEqual(br.description, "Test lead")
        self.assertEqual(br.business_requirement, "<p>Investigate and estimate</p>")
        self.assertEqual(br.user_id, self.env.user)

    def test_default_get_without_active_id(self):
        """browse() on a missing active_id yields a truthy empty record"""
        defaults = (
            self.env["crm.lead.create.requirement"]
            .with_context(active_model=self.lead_model._name)
            .default_get(["lead_id", "description", "customer_history"])
        )
        self.assertFalse(defaults.get("lead_id"))
        self.assertFalse(defaults.get("description"))

    def test_chatter_messages_keep_their_link(self):
        """message_post escapes plain strings, so the links need Markup"""
        self.wizard.action_lead_to_business_requirement()
        requirement = self.lead.business_requirement_ids
        for record in (self.lead, requirement):
            body = (
                self.env["mail.message"]
                .search(
                    [("model", "=", record._name), ("res_id", "=", record.id)],
                    order="id desc",
                    limit=1,
                )
                .body
            )
            self.assertIn("<a ", body)
            self.assertNotIn("&lt;a", body)

    def test_open_requirements_of_one_lead(self):
        """A single lead pre-filters the requirement list by itself"""
        action = self.lead.open_requirements()
        self.assertEqual(action["res_model"], "business.requirement")
        self.assertEqual(action["context"]["search_default_lead_id"], self.lead.id)

    def test_open_requirements_of_several_leads(self):
        """Several leads are filtered by a domain instead of the context"""
        leads = self.lead + self.lead_model.create({"name": "Another lead"})
        action = leads.open_requirements()
        # A domain is a list of leaves, not a tuple wrapping one
        self.assertIsInstance(action["domain"], list)
        self.assertEqual(action["domain"], [("lead_id", "in", leads.ids)])
