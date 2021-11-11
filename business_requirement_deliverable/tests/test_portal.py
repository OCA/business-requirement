# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo.tests

from odoo.addons.business_requirement.tests.test_portal import (
    BusinessRequirementPortalBase,
)


@odoo.tests.tagged("post_install", "-at_install")
class BusinessRequirementDeliverablePortal(BusinessRequirementPortalBase):
    def setUp(self):
        super().setUp()
        self.brd = self.env["business.requirement.deliverable"].create(
            {
                "name": "test",
                "portal_published": True,
                "business_requirement_id": self.br.id,
            }
        )
        self.brd.message_subscribe(
            partner_ids=self.env.ref("base.demo_user0").partner_id.ids
        )

    def test_tour(self):
        self.start_tour(
            "/", "business_requirement_deliverable_portal_tour", login="portal"
        )
