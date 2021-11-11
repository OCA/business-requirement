# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import odoo.tests


class BusinessRequirementPortalBase(odoo.tests.HttpCase):
    def setUp(self):
        super().setUp()
        self.br = self.env["business.requirement"].create(
            {"description": "test", "portal_published": True}
        )
        self.br.message_subscribe(
            partner_ids=self.env.ref("base.demo_user0").partner_id.ids
        )


@odoo.tests.tagged("post_install", "-at_install")
class BusinessRequirementPortal(BusinessRequirementPortalBase):
    def setUp(self):
        super().setUp()

    def test_tour(self):
        self.start_tour("/", "business_requirement_portal_tour", login="portal")
