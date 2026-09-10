# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo.tests


@odoo.tests.tagged("post_install", "-at_install")
class BusinessRequirementDeliverablePortal(odoo.tests.HttpCase):
    def setUp(self):
        super().setUp()
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
        self.br.message_subscribe(
            partner_ids=self.env.ref("base.demo_user0").partner_id.ids
        )

    def test_tour(self):
        self.start_tour(
            "/", "business_requirement_deliverable_portal_tour", login="portal"
        )
