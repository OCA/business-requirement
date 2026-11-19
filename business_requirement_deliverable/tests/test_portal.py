# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo.tests
from odoo.tests.common import new_test_user


@odoo.tests.tagged("post_install", "-at_install")
class BusinessRequirementDeliverablePortal(odoo.tests.HttpCase):
    def setUp(self):
        super().setUp()
        self.portal_user = new_test_user(
            self.env, login="brd_portal_user", groups="base.group_portal"
        )
        self.br = self.env["business.requirement"].create(
            {"description": "test", "portal_published": True}
        )
        self.brd = self.env["business.requirement.deliverable"].create(
            {
                "name": "test",
                "portal_published": True,
                "business_requirement_id": self.br.id,
            }
        )
        # Subscribe the requirement, not the deliverable: the portal counter
        # filters on the requirement's followers, and message_subscribe()
        # propagates them down to its deliverable_lines (not the other way
        # around), which is what makes the /my/brd entry visible.
        self.br.message_subscribe(partner_ids=self.portal_user.partner_id.ids)

    def test_tour(self):
        self.start_tour(
            "/",
            "business_requirement_deliverable_portal_tour",
            login=self.portal_user.login,
        )

    def test_portal_search(self):
        other = self.env["business.requirement.deliverable"].create(
            {
                "name": "Another deliverable",
                "portal_published": True,
                "business_requirement_id": self.br.id,
            }
        )
        self.authenticate(self.portal_user.login, self.portal_user.login)
        for search_in in ("content", "all"):
            page = self.url_open(f"/my/brd?search=test&search_in={search_in}")
            self.assertEqual(page.status_code, 200)
            self.assertIn(f"/my/brd/{self.brd.id}?", page.text)
            self.assertNotIn(f"/my/brd/{other.id}?", page.text)
        # Without search both deliverables are listed
        page = self.url_open("/my/brd")
        self.assertIn(f"/my/brd/{self.brd.id}?", page.text)
        self.assertIn(f"/my/brd/{other.id}?", page.text)
