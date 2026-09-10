# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo.tests


@odoo.tests.tagged("post_install", "-at_install")
class BusinessRequirementPortal(odoo.tests.HttpCase):
    def setUp(self):
        super().setUp()
        self.br = self.env["business.requirement"].create(
            {"description": "test", "portal_published": True}
        )
        self.br.message_subscribe(
            partner_ids=self.env.ref("base.demo_user0").partner_id.ids
        )

    def test_tour(self):
        self.start_tour("/", "business_requirement_portal_tour", login="portal")

    def test_portal_assigned_to_shows_the_responsible_user(self):
        """The portal credits the responsible user, not the record owner"""
        owner = self.env["res.users"].create(
            {"name": "Owner Of The Record", "login": "br_portal_owner"}
        )
        responsible = self.env["res.users"].create(
            {"name": "Responsible For The Work", "login": "br_portal_responsible"}
        )
        stakeholder = self.env["res.partner"].create({"name": "Stakeholder Company"})
        br = self.env["business.requirement"].create(
            {
                "description": "who is assigned",
                "portal_published": True,
                "user_id": owner.id,
                "responsible_user_id": responsible.id,
                "partner_id": stakeholder.id,
            }
        )
        # The deliverable module extends this page with a field the public
        # user cannot read, so browse it as the portal user does
        self.authenticate("portal", "portal")
        page = self.url_open(
            f"/my/business_requirement/{br.id}"
            f"?access_token={br._portal_ensure_token()}"
        )
        self.assertEqual(page.status_code, 200)
        assigned, requested = page.text.split("Assigned to")[1].split("Requested by")
        self.assertIn(responsible.name, assigned)
        self.assertNotIn(owner.name, assigned)
        self.assertIn(stakeholder.name, requested)
